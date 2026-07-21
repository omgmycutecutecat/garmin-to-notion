"""Mapping constants for activity icons and intensity classification.

Modality/sport-type classification has been removed entirely -- it caused
more mismatches (SUP/MMA/etc. falling into "Other") than it was worth.
Activities and Workouts now use raw Garmin activity names directly.
"""

# ---------------------------------------------------------------------------
# Activity Emojis (used by Activities sync) -- keyed by Garmin's formatted
# activity subtype text. Purely cosmetic (the page icon), unrelated to any
# grouping/classification.
# ---------------------------------------------------------------------------
ACTIVITY_EMOJIS: dict[str, str] = {
    "Running": "\U0001f3c3",
    "Treadmill Running": "\U0001f3c3",
    "Street Running": "\U0001f3c3",
    "Indoor Running": "\U0001f3c3",
    "Trail Running": "\U0001f3d4\ufe0f",
    "Track Running": "\U0001f3c3",
    "Ultra Running": "\U0001f3c3",
    "Cycling": "\U0001f6b4",
    "Indoor Cycling": "\U0001f6b4",
    "Mountain Biking": "\U0001f6b5",
    "Gravel Cycling": "\U0001f6b4",
    "E Biking": "\U0001f6b4",
    "Cyclocross": "\U0001f6b4",
    "Virtual Ride": "\U0001f6b4",
    "Swimming": "\U0001f3ca",
    "Lap Swimming": "\U0001f3ca",
    "Open Water Swimming": "\U0001f30a",
    "Walking": "\U0001f6b6",
    "Hiking": "\U0001f97e",
    "Speed Walking": "\U0001f6b6",
    "Casual Walking": "\U0001f6b6",
    "Stair Climbing": "\U0001f6b6",
    "Strength Training": "\U0001f3cb\ufe0f",
    "Barre": "\U0001f3cb\ufe0f",
    "Functional Training": "\U0001f3cb\ufe0f",
    "Crossfit": "\U0001f3cb\ufe0f",
    "HIIT": "\U0001f525",
    "Cardio": "\U0001f4aa",
    "Indoor Cardio": "\U0001f4aa",
    "Elliptical": "\U0001f3c3",
    "Jump Rope": "\u23ed\ufe0f",
    "Yoga": "\U0001f9d8",
    "Pilates": "\U0001f9d8",
    "Stretching": "\U0001f938",
    "Meditation": "\U0001f9d8",
    "Breathwork": "\U0001fac1",
    "Rowing": "\U0001f6a3",
    "Indoor Rowing": "\U0001f6a3",
    "Tennis": "\U0001f3be",
    "Padel": "\U0001f3be",
    "Badminton": "\U0001f3f8",
    "Pickleball": "\U0001f3d3",
    "Squash": "\U0001f3be",
    "Table Tennis": "\U0001f3d3",
    "Soccer": "\u26bd",
    "Basketball": "\U0001f3c0",
    "Volleyball": "\U0001f3d0",
    "Football": "\U0001f3c8",
    "Rugby": "\U0001f3c9",
    "Hockey": "\U0001f3d2",
    "Mixed Martial Arts": "\U0001f94b",
    "Boxing": "\U0001f94a",
    "Kickboxing": "\U0001f94a",
    "Skiing": "\u26f7\ufe0f",
    "Resort Skiing Snowboarding": "\u26f7\ufe0f",
    "Snowboarding": "\U0001f3c2",
    "Cross Country Skiing": "\u26f7\ufe0f",
    "Snowshoeing": "\U0001f97e",
    "Ice Skating": "\u26f8\ufe0f",
    "Kayaking": "\U0001f6f6",
    "Stand Up Paddleboarding": "\U0001f3c4",
    "Surfing": "\U0001f3c4",
    "Rock Climbing": "\U0001f9d7",
    "Bouldering": "\U0001f9d7",
    "Indoor Climbing": "\U0001f9d7",
    "Mountaineering": "\U0001f9d7",
    "Golf": "\u26f3",
    "Skateboarding": "\U0001f6f9",
    "Dance": "\U0001f483",
    "Horseback Riding": "\U0001f3c7",
    "Multi Sport": "\U0001f3c5",
    "Triathlon": "\U0001f3c5",
    "Other": "\U0001f3c5",
}

# ---------------------------------------------------------------------------
# Aerobic Effect text -> Intensity. This is the only "classification" left --
# derived purely from Garmin's own training-effect message, nothing custom.
# ---------------------------------------------------------------------------
INTENSITY_MAP: dict[str, str] = {
    "Overreaching": "Maximum",
    "Highly Impacting": "Hard",
    "Impacting": "Moderate",
    "Improving": "Moderate",
    "Maintaining": "Moderate",
    "Some Benefit": "Easy",
    "Recovery": "Easy",
    "No Benefit": "Easy",
    "Unknown": "Moderate",
}

# ---------------------------------------------------------------------------
# Workouts: skip these if the raw activity NAME contains any of these words
# (case-insensitive). Replaces the old modality-based skip check.
# ---------------------------------------------------------------------------
SKIP_NAME_KEYWORDS: set[str] = {"meditation", "breathwork", "relaxation"}
