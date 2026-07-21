"""Sync Garmin daily calorie burn totals to the Notion Daily Calories database."""

from __future__ import annotations

import logging
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from garminconnect import Garmin as GarminClient
from notion_client import Client as NotionClient

from garmin_to_notion.config import Settings
from garmin_to_notion.notion_helpers import fetch_all_pages, get_prop

logger = logging.getLogger(__name__)


def _get_existing_calorie_dates(
    notion: NotionClient, database_id: str
) -> set[str]:
    """Fetch all existing Daily Calories entries and return their date strings."""
    pages = fetch_all_pages(notion, database_id)
    dates: set[str] = set()
    for page in pages:
        date_str = get_prop(page["properties"], "Date", "date")
        if date_str:
            dates.add(date_str[:10])
    return dates


def _fetch_calorie_range(
    garmin: GarminClient,
    days_back: int,
    tz: ZoneInfo,
    existing_dates: set[str],
) -> list[dict]:
    """Fetch daily calorie stats for the last *days_back* days, skipping known dates.

    Garmin's stats endpoint is per-day only (no date-range call like steps has),
    so this walks backward one day at a time, same pattern as sleep.py.
    """
    today = datetime.now(tz=tz).date()
    results: list[dict] = []
    skipped = 0

    for i in range(days_back):
        d = today - timedelta(days=i)
        date_str = d.isoformat()
        if date_str in existing_dates:
            skipped += 1
            continue
        try:
            stats = garmin.get_stats(date_str)
        except Exception as e:
            logger.debug("No calorie stats for %s: %s", date_str, e)
            continue
        if not stats:
            continue
        stats["calendarDate"] = date_str
        results.append(stats)
        if (i + 1) % 100 == 0:
            logger.info(
                "Calories fetch progress: %d/%d days checked (%d skipped)",
                i + 1, days_back, skipped,
            )

    if skipped:
        logger.info("Skipped %d days already in Notion", skipped)
    return results


def _build_properties(stats: dict) -> dict | None:
    """Build Notion properties from a Garmin daily stats payload."""
    date_str = stats.get("calendarDate")
    if not date_str:
        return None

    total_kcal = stats.get("totalKilocalories") or 0
    active_kcal = stats.get("activeKilocalories") or 0
    bmr_kcal = stats.get("bmrKilocalories") or 0

    if not total_kcal and not active_kcal and not bmr_kcal:
        # No real data for this day (e.g. watch not worn) -- skip rather
        # than write a zeroed-out row.
        return None

    return {
        "Name": {"title": [{"text": {"content": f"{round(total_kcal):,} kcal"}}]},
        "Date": {"date": {"start": date_str}},
        "Total Calories": {"number": round(total_kcal)},
        "Active Calories": {"number": round(active_kcal)},
        "BMR Calories": {"number": round(bmr_kcal)},
    }


def sync_daily_calories(
    garmin: GarminClient,
    notion: NotionClient,
    settings: Settings,
) -> None:
    """Sync historical daily calorie burn totals to the Notion Daily Calories database."""
    if not settings.calories_db_id:
        logger.info("No calories database configured, skipping")
        return

    logger.info("Fetching existing calorie entries from Notion...")
    existing_dates = _get_existing_calorie_dates(notion, settings.calories_db_id)
    logger.info("Found %d existing calorie entries in Notion", len(existing_dates))

    stats_list = _fetch_calorie_range(
        garmin, settings.days_back, settings.timezone, existing_dates
    )
    logger.info("Fetched %d new calorie entries from Garmin", len(stats_list))

    created, errors = 0, 0
    for stats in stats_list:
        try:
            props = _build_properties(stats)
            if not props:
                continue
            notion.pages.create(
                parent={"database_id": settings.calories_db_id},
                properties=props,
            )
            created += 1
        except Exception as e:
            errors += 1
            logger.error(
                "Skipping calorie entry for %s due to error: %s",
                stats.get("calendarDate"), e, exc_info=True,
            )
            continue

    logger.info(
        "Daily calories sync complete: %d created, %d errors",
        created, errors,
    )
