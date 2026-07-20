"""All mapping constants for activity types, icons, and modalities."""

# ---------------------------------------------------------------------------
# Activity Emojis (used by Activities sync)
# Maps activity subtype/type to native Notion emoji icons
# ---------------------------------------------------------------------------
ACTIVITY_EMOJIS: dict[str, str] = {
    # Running
    "Running": "\U0001f3c3",
    "Treadmill Running": "\U0001f3c3",
    "Street Running": "\U0001f3c3",
    "Indoor Running": "\U0001f3c3",
    "Trail Running": "\U0001f3d4\ufe0f",
    "Track Running": "\U0001f3c3",
    "Ultra Running": "\U0001f3c3",
    # Cycling
    "Cycling": "\U0001f6b4",
    "Indoor Cycling": "\U0001f6b4",
    "Mountain Biking": "\U0001f6b5",
    "Gravel Cycling": "\U0001f6b4",
    "E Biking": "\U0001f6b4",
    "Cyclocross": "\U0001f6b4",
    "Virtual Ride": "\U0001f6b4",
    # Swimming
    "Swimming": "\U0001f3ca",
    "Lap Swimming": "\U0001f3ca",
    "Open Water Swimming": "\U0001f30a",
    # Walking
    "Walking": "\U0001f6b6",
    "Hiking": "\U0001f97e",
    "Speed Walking": "\U0001f6b6",
    "Casual Walking": "\U0001f6b6",
    "Stair Climbing": "\U0001f6b6",
    # Strength & Fitness
    "Strength Training": "\U0001f3cb\ufe0f",
    "Barre": "\U0001f3cb\ufe0f",
    "Functional Training": "\U0001f3cb\ufe0f",
    "Crossfit": "\U0001f3cb\ufe0f",
    "HIIT": "\U0001f525",
    "Cardio": "\U0001f4aa",
    "Indoor Cardio": "\U0001f4aa",
    "Elliptical": "\U0001f3c3",
    "Jump Rope": "\u23ed\ufe0f",
    # Yoga & Mindfulness
    "Yoga": "\U0001f9d8",
    "Pilates": "\U0001f9d8",
    "Stretching": "\U0001f938",
    "Meditation": "\U0001f9d8",
    "Breathwork": "\U0001fac1",
    # Rowing
    "Rowing": "\U0001f6a3",
    "Indoor Rowing": "\U0001f6a3",
    # Racquet Sports
    "Tennis": "\U0001f3be",
    "Padel": "\U0001f3be",
    "Badminton": "\U0001f3f8",
    "Pickleball": "\U0001f3d3",
    "Squash": "\U0001f3be",
    "Table Tennis": "\U0001f3d3",
    # Team Sports
    "Soccer": "\u26bd",
    "Basketball": "\U0001f3c0",
    "Volleyball": "\U0001f3d0",
    "Football": "\U0001f3c8",
    "Rugby": "\U0001f3c9",
    "Hockey": "\U0001f3d2",
    # Combat
    "Mixed Martial Arts": "\U0001f94b",
    "Boxing": "\U0001f94a",
    "Kickboxing": "\U0001f94a",
    # Winter Sports
    "Skiing": "\u26f7\ufe0f",
    "Resort Skiing Snowboarding": "\u26f7\ufe0f",
    "Snowboarding": "\U0001f3c2",
    "Cross Country Skiing": "\u26f7\ufe0f",
    "Snowshoeing": "\U0001f97e",
    "Ice Skating": "\u26f8\ufe0f",
    # Water Sports
    "Kayaking": "\U0001f6f6",
    "Stand Up Paddleboarding": "\U0001f3c4",
    "Surfing": "\U0001f3c4",
    # Climbing
    "Rock Climbing": "\U0001f9d7",
    "Bouldering": "\U0001f9d7",
    "Indoor Climbing": "\U0001f9d7",
    "Mountaineering": "\U0001f9d7",
    # Other
    "Golf": "\u26f3",
    "Skateboarding": "\U0001f6f9",
    "Dance": "\U0001f483",
    "Horseback Riding": "\U0001f3c7",
    "Multi Sport": "\U0001f3c5",
    "Triathlon": "\U0001f3c5",
    "Other": "\U0001f3c5",
}

# ---------------------------------------------------------------------------
# Workouts: Garmin Activity Type / Subactivity Type -> Modality
# Subactivity (more specific) is checked first, then Activity Type
# ---------------------------------------------------------------------------
MODALITY_MAP: dict[str, str] = {
    # Subactivity Type mappings (checked first)
    "Treadmill Running": "Running",
    "Street Running": "Running",
    "Indoor Running": "Running",
    "Trail Running": "Running",
    "Track Running": "Running",
    "Ultra Running": "Running",
    "Indoor Cycling": "Indoor Cycling",
    "Virtual Ride": "Indoor Cycling",
    "Mountain Biking": "Outdoor Cycling",
    "Gravel Cycling": "Outdoor Cycling",
    "E Biking": "Outdoor Cycling",
    "Cyclocross": "Outdoor Cycling",
    "Casual Walking": "Walking",
    "Speed Walking": "Walking",
    "Stair Climbing": "Walking",
    "Strength Training": "Strength Training",
    "Strength": "Strength Training",
    "Functional Training": "Strength Training",
    "Barre": "Strength Training",
    "Pilates": "Pilates",
    "Yoga": "Yoga",
    "Lap Swimming": "Swimming",
    "Open Water Swimming": "Swimming",
    # FIXED: Mixed Martial Arts now stays as its own Modality instead of
    # being folded into BJJ.
    "Mixed Martial Arts": "Mixed Martial Arts",
    "Hiit": "HIIT",
    "Crossfit": "Crossfit",
    # Racquet sports
    "Tennis": "Racquet Sports",
    "Padel": "Racquet Sports",
    "Badminton": "Racquet Sports",
    "Pickleball": "Racquet Sports",
    "Squash": "Racquet Sports",
    "Table Tennis": "Racquet Sports",
    # Team sports
    "Soccer": "Team Sports",
    "Basketball": "Team Sports",
    "Volleyball": "Team Sports",
    "Football": "Team Sports",
    "Rugby": "Team Sports",
    "Hockey": "Team Sports",
    # Combat
    "Boxing": "Combat Sports",
    "Kickboxing": "Combat Sports",
    # Winter
    "Skiing": "Winter Sports",
    "Resort Skiing Snowboarding": "Winter Sports",
    "Snowboarding": "Winter Sports",
    "Cross Country Skiing": "Winter Sports",
    "Snowshoeing": "Winter Sports",
    "Ice Skating": "Winter Sports",
    # Water
    # FIXED: SUP and Surfing now stay as their own Modality instead of
    # being folded into the generic "Water Sports" bucket. Kayaking still
    # rolls up into Water Sports as before.
    "Kayaking": "Water Sports",
    "Stand Up Paddleboarding": "SUP",
    "Surfing": "Surf",
    # Climbing
    "Rock Climbing": "Climbing",
    "Bouldering": "Climbing",
    "Indoor Climbing": "Climbing",
    "Mountaineering": "Climbing",
    # Other
    "Golf": "Golf",
    "Dance": "Dance",
    "Multi Sport": "Multi Sport",
    "Triathlon": "Multi Sport",
    # Activity Type mappings (fallback)
    "Running": "Running",
    "Cycling": "Outdoor Cycling",
    "BJJ": "BJJ",
    "Mixed Martial Arts": "Mixed Martial Arts",
    "SUP": "SUP",
    "Surf": "Surf",
    "HIIT": "HIIT",
    "Swimming": "Swimming",
    "Walking": "Walking",
    "Yoga/Pilates": "Yoga",
    "Racquet Sports": "Racquet Sports",
    "Team Sports": "Team Sports",
    "Combat Sports": "Combat Sports",
    "Winter Sports": "Winter Sports",
    "Water Sports": "Water Sports",
    "Climbing": "Climbing",
    "Multi Sport": "Multi Sport",
}

# ---------------------------------------------------------------------------
# Workouts: Aerobic Effect -> Intensity
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
# Workouts: Activity Name overrides (for custom Garmin activities)
# ---------------------------------------------------------------------------
NAME_OVERRIDE_MAP: dict[str, str] = {
    "Sauna": "Sauna",
}

# ---------------------------------------------------------------------------
# Workouts: Modalities where Easy intensity doesn't apply -> minimum
# ---------------------------------------------------------------------------
INTENSITY_FLOOR: dict[str, str] = {
    "HIIT": "Moderate",
    "BJJ": "Moderate",
    "Mixed Martial Arts": "Moderate",
}

# ---------------------------------------------------------------------------
# Workouts: Skip these activity types (not real workouts)
# ---------------------------------------------------------------------------
SKIP_TYPES: set[str] = {"Breathwork", "Relaxation", "Meditation"}
