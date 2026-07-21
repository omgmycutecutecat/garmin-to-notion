"""Sync Garmin activities to the Notion Activities database."""

from __future__ import annotations

import logging
from datetime import datetime, timedelta

from garminconnect import Garmin as GarminClient
from notion_client import Client as NotionClient

from garmin_to_notion.config import Settings
from garmin_to_notion.formatters import (
    format_activity_type,
    format_duration,
    format_effect_rich,
    format_pace,
    format_training_effect,
    gmt_to_local,
)
from garmin_to_notion.mappings import ACTIVITY_EMOJIS, classify_modality

logger = logging.getLogger(__name__)

# Garmin's activity list endpoint silently caps how many rows it returns per
# single request (observed to be well under whatever "limit" you pass in).
# We page through it in fixed-size batches instead of trusting one big call.
BATCH_SIZE = 100


def _build_properties(activity: dict, settings: Settings) -> dict:
    """Build the Notion properties payload from a Garmin activity."""
    activity_name = activity.get("activityName", "Unnamed Activity")
    activity_type, activity_subtype = format_activity_type(
        activity.get("activityType", {}).get("typeKey", "Unknown"),
        activity_name,
    )
    modality = classify_modality(activity_type, activity_subtype, activity_name)

    local_date = gmt_to_local(activity.get("startTimeGMT"), settings.timezone)
    duration_seconds = activity.get("duration", 0) or 0
    end_time = local_date + timedelta(seconds=duration_seconds)
    day_of_week = local_date.strftime("%A")

    return {
        "Date": {"date": {"start": local_date.isoformat()}},
        "Start Time": {"date": {"start": local_date.isoformat()}},
        "End Time": {"date": {"start": end_time.isoformat()}},
        "Modality": {"select": {"name": modality}},
        "Name": {"title": [{"text": {"content": activity_name}}]},
        "Distance (km)": {"number": round(activity.get("distance", 0) / 1000, 2)},
        "Duration": {
            "rich_text": [
                {"text": {"content": format_duration(activity.get("duration", 0))}}
            ]
        },
        "Calories": {"number": round(activity.get("calories", 0))},
        "Avg Pace": {
            "rich_text": [
                {"text": {"content": format_pace(activity.get("averageSpeed", 0))}}
            ]
        },
        "Avg HR": {"number": round(activity.get("averageHR", 0) or 0)},
        "Max HR": {"number": round(activity.get("maxHR", 0) or 0)},
        "Avg Power": {"number": round(activity.get("avgPower", 0) or 0, 1)},
        "Training Effect": {
            "rich_text": [
                {
                    "text": {
                        "content": format_training_effect(
                            activity.get("trainingEffectLabel", "Unknown")
                        )
                    }
                }
            ]
        },
        "Aerobic Effect": {
            "rich_text": [
                {
                    "text": {
                        "content": format_effect_rich(
                            activity.get("aerobicTrainingEffect", 0) or 0,
                            activity.get("aerobicTrainingEffectMessage", "Unknown"),
                        )
                    }
                }
            ]
        },
        "Anaerobic Effect": {
            "rich_text": [
                {
                    "text": {
                        "content": format_effect_rich(
                            activity.get("anaerobicTrainingEffect", 0) or 0,
                            activity.get("anaerobicTrainingEffectMessage", "Unknown"),
                        )
                    }
                }
            ]
        },
        "Steps": {"number": activity.get("steps", 0) or 0},
        "Garmin ID": {"number": activity.get("activityId")},
        "Day of Week": {"select": {"name": day_of_week}},
    }


def _get_icon_emoji(activity: dict) -> str:
    """Get the emoji icon for an activity based on its type."""
    activity_name = activity.get("activityName", "")
    _, activity_subtype = format_activity_type(
        activity.get("activityType", {}).get("typeKey", "Unknown"),
        activity_name,
    )
    return ACTIVITY_EMOJIS.get(activity_subtype, ACTIVITY_EMOJIS["Other"])


def _activity_exists(
    notion: NotionClient,
    database_id: str,
    garmin_id: int | None,
    activity_date: datetime,
    modality: str,
    activity_name: str,
) -> dict | None:
    """Check if an activity already exists in the Notion database.

    Primary lookup: by Garmin ID (unique). Fallback: date + modality + name.
    """
    if garmin_id:
        query = notion.databases.query(
            database_id=database_id,
            filter={"property": "Garmin ID", "number": {"equals": garmin_id}},
        )
        if query["results"]:
            return query["results"][0]

    # Fallback for legacy entries without Garmin ID
    lookup_min = activity_date - timedelta(minutes=5)
    lookup_max = activity_date + timedelta(minutes=5)

    query = notion.databases.query(
        database_id=database_id,
        filter={
            "and": [
                {"property": "Date", "date": {"on_or_after": lookup_min.isoformat()}},
                {"property": "Date", "date": {"on_or_before": lookup_max.isoformat()}},
                {"property": "Modality", "select": {"equals": modality}},
                {"property": "Name", "title": {"equals": activity_name}},
            ]
        },
    )
    results = query["results"]
    return results[0] if results else None


def _activity_needs_update(
    existing: dict, new_activity: dict, settings: Settings
) -> bool:
    """Compare an existing Notion page with new Garmin data to detect changes."""
    props = existing["properties"]

    try:
        existing_date = props["Date"]["date"]["start"]
        new_date = gmt_to_local(
            new_activity.get("startTimeGMT"), settings.timezone
        ).isoformat()
        date_changed = existing_date != new_date

        distance_changed = (
            props["Distance (km)"]["number"]
            != round(new_activity.get("distance", 0) / 1000, 2)
        )
        calories_changed = (
            props["Calories"]["number"] != round(new_activity.get("calories", 0))
        )
        pace_changed = (
            props["Avg Pace"]["rich_text"][0]["text"]["content"]
            != format_pace(new_activity.get("averageSpeed", 0))
        )
        hr_changed = (
            props["Avg HR"]["number"] != round(new_activity.get("averageHR", 0) or 0)
            or props["Max HR"]["number"]
            != round(new_activity.get("maxHR", 0) or 0)
        )
        return (
            date_changed or distance_changed or calories_changed
            or pace_changed or hr_changed
        )
    except (KeyError, TypeError, IndexError):
        return True


def _fetch_recent_activities(garmin: GarminClient, settings: Settings) -> list[dict]:
    """Page through Garmin's activity list until we pass the days-back cutoff
    or hit the overall fetch_limit, instead of trusting a single large
    get_activities() call (which silently truncates to far fewer results
    than requested).
    """
    days_back = settings.days_back or 45
    cutoff = datetime.now() - timedelta(days=days_back)
    fetch_limit = settings.fetch_limit

    activities: list[dict] = []
    start = 0

    while True:
        batch = garmin.get_activities(start, BATCH_SIZE)
        if not batch:
            break

        activities.extend(batch)
        logger.info(
            "Fetched batch at offset %d (%d activities, %d total so far)",
            start, len(batch), len(activities),
        )

        # Walk backward from the end of the batch to find a record with a
        # usable timestamp -- one bad/missing startTimeGMT should not abort
        # the entire fetch.
        reached_cutoff = False
        for record in reversed(batch):
            raw_ts = record.get("startTimeGMT")
            if not raw_ts:
                continue
            try:
                oldest_in_batch = gmt_to_local(raw_ts, settings.timezone)
            except (ValueError, TypeError) as e:
                logger.warning("Skipping activity with unparseable timestamp %r: %s", raw_ts, e)
                continue
            reached_cutoff = oldest_in_batch.replace(tzinfo=None) < cutoff
            break
        else:
            logger.warning(
                "No activity in this batch had a usable timestamp; "
                "continuing pagination without a cutoff check for this batch."
            )

        got_full_batch = len(batch) == BATCH_SIZE
        under_fetch_limit = not fetch_limit or len(activities) < fetch_limit

        if reached_cutoff or not got_full_batch or not under_fetch_limit:
            break
        start += BATCH_SIZE

    if fetch_limit:
        activities = activities[:fetch_limit]

    return activities


def sync_activities(
    garmin: GarminClient,
    notion: NotionClient,
    settings: Settings,
) -> None:
    """Sync all Garmin activities to the Notion Activities database."""
    activities = _fetch_recent_activities(garmin, settings)
    logger.info("Fetched %d activities from Garmin (paginated)", len(activities))

    created, updated, skipped, errors = 0, 0, 0, 0

    for activity in activities:
        try:
            activity_name = activity.get("activityName", "Unnamed Activity")
            activity_type, activity_subtype = format_activity_type(
                activity.get("activityType", {}).get("typeKey", "Unknown"),
                activity_name,
            )
            modality = classify_modality(activity_type, activity_subtype, activity_name)
            activity_date = gmt_to_local(activity.get("startTimeGMT"), settings.timezone)
            garmin_id = activity.get("activityId")

            existing = _activity_exists(
                notion, settings.activities_db_id,
                garmin_id, activity_date, modality, activity_name,
            )

            if existing:
                if _activity_needs_update(existing, activity, settings):
                    props = _build_properties(activity, settings)
                    emoji = _get_icon_emoji(activity)
                    notion.pages.update(
                        page_id=existing["id"],
                        properties=props,
                        icon={"emoji": emoji},
                    )
                    updated += 1
                else:
                    skipped += 1
            else:
                props = _build_properties(activity, settings)
                emoji = _get_icon_emoji(activity)
                notion.pages.create(
                    parent={"database_id": settings.activities_db_id},
                    properties=props,
                    icon={"emoji": emoji},
                )
                created += 1
        except Exception as e:
            errors += 1
            logger.error(
                "Skipping activity %r (id=%s) due to error: %s",
                activity.get("activityName", "Unnamed Activity"),
                activity.get("activityId"),
                e,
                exc_info=True,
            )
            continue

    logger.info(
        "Activities sync complete: %d created, %d updated, %d unchanged, %d errors",
        created, updated, skipped, errors,
    )
