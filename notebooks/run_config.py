from dataclasses import dataclass
from pathlib import Path

# --------------------------------------------------
# Set the run mode below to "sample" or "full"
RUN_MODE = "full"

# Gold datasets generated on every run.
GOLD_TIME_UNITS = ("1h", "2h", "4h")

# Set App Token for Chicago Data (see notebook 00_01_data_loader.ipynb)
APP_TOKEN = "***"

# Start and end date of taxi and weather data
START_DATE = "2024-01-01T00:00:00"
END_DATE = "2026-05-01T00:00:00"

# Predictive-model period used by the train/validation/test split in full mode
# The start is inclusive and the end is exclusive.
MODEL_START_DATE = "2025-01-01T00:00:00"
MODEL_END_DATE = "2026-05-01T00:00:00"

# Contiguous, complete taxi-data window used in sample mode. The end is exclusive.
# The max row is a guard against unexpectedly large API responses
# reaching it fails validation because that would leave the last sample day incomplete.
SAMPLE_START_DATE = "2026-04-13T00:00:00"
SAMPLE_END_DATE = "2026-04-27T00:00:00"
SAMPLE_MAX_TRIPS = 400_000
SAMPLE_MIN_COMPLETE_DAYS = 12



# Set H3_Resolution
H3_RESOLUTION = 7
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
MODE_DIR = DATA_DIR / RUN_MODE
RAW_DIR = MODE_DIR / "raw_data"
PROCESSED_DIR = MODE_DIR / "processed_data"
TRAIN_TEST_DIR = MODE_DIR / "train_test_data"
MODELS_DIR = PROJECT_ROOT / "models" / RUN_MODE

# The existing sample files use a taxi-specific suffix and H3 resolution 7.
TAXI_SUFFIX = "_sample" if RUN_MODE == "sample" else ""


@dataclass(frozen=True)
class DataPaths:
    # Raw
    raw_taxi_trips: Path
    raw_weatherdata: Path
    raw_census_tracts: Path
    raw_community_areas: Path

    # Bronze
    bronze_taxi_trips: Path
    bronze_weatherdata: Path
    bronze_census_tracts: Path
    bronze_community_areas: Path
    bronze_osm_geo: Path
    bronze_osm: Path

    # Silver
    silver_taxi_community_areas_unfiltered: Path
    silver_taxi_community_areas: Path
    silver_taxi_census_tracts: Path
    silver_taxi_hexagon: Path
    silver_weatherdata: Path
    silver_census_tracts: Path
    silver_community_areas: Path
    silver_hexagon: Path
    silver_boundary: Path

    # Gold
    gold_taxi_trips: Path
    gold_weatherdata: Path
    gold_1h_demand_census_tracts: Path
    gold_1h_demand_community_areas: Path
    gold_1h_demand_community_area_unfiltered: Path
    gold_1h_demand_hexagon: Path
    gold_2h_demand_census_tracts: Path
    gold_2h_demand_community_areas: Path
    gold_2h_demand_community_area_unfiltered: Path
    gold_2h_demand_hexagon: Path
    gold_4h_demand_census_tracts: Path
    gold_4h_demand_community_areas: Path
    gold_4h_demand_community_area_unfiltered: Path
    gold_4h_demand_hexagon: Path

    # Train/validation/test outputs
    train_test_dir: Path


PATHS = DataPaths(
    # Raw
    raw_taxi_trips=(
        RAW_DIR / "taxi_sample.parquet"
        if RUN_MODE == "sample"
        else RAW_DIR / "taxi.csv"
    ),
    raw_weatherdata=RAW_DIR / "weatherdata.csv",
    raw_census_tracts=RAW_DIR / "Census_Tracts.csv",
    raw_community_areas=RAW_DIR / "Community_Areas.csv",

    # Bronze
    bronze_taxi_trips=PROCESSED_DIR / f"bronze_taxi{TAXI_SUFFIX}.parquet",
    bronze_weatherdata=PROCESSED_DIR / "bronze_weatherdata.parquet",
    bronze_census_tracts=PROCESSED_DIR / "bronze_Census_Tracts.parquet",
    bronze_community_areas=PROCESSED_DIR / "bronze_Community_Areas.parquet",
    bronze_osm_geo=PROCESSED_DIR / "bronze_osm_chicago_pois.geoparquet",
    bronze_osm=PROCESSED_DIR / "bronze_osm_chicago_pois.parquet",

    # Silver
    silver_taxi_community_areas_unfiltered=(
        PROCESSED_DIR / f"silver_taxi_community_areas_UNFILTERED{TAXI_SUFFIX}.parquet"
    ),
    silver_taxi_community_areas=(
        PROCESSED_DIR / f"silver_taxi_community_areas{TAXI_SUFFIX}.parquet"
    ),
    silver_taxi_census_tracts=(
        PROCESSED_DIR / f"silver_taxi_census_tracts{TAXI_SUFFIX}.parquet"
    ),
    silver_taxi_hexagon=(
        PROCESSED_DIR
        / f"silver_taxi_hexagon_{H3_RESOLUTION}{TAXI_SUFFIX}.parquet"
    ),
    silver_weatherdata=PROCESSED_DIR / "silver_weatherdata.parquet",
    silver_census_tracts=PROCESSED_DIR / "silver_census_tracts.geoparquet",
    silver_community_areas=PROCESSED_DIR / "silver_community_areas.geoparquet",
    silver_hexagon=PROCESSED_DIR / f"silver_dim_h3_chicago_{H3_RESOLUTION}.parquet",
    silver_boundary=(
        PROCESSED_DIR
        / f"silver_chicago_boundary_from_census_tracts_{H3_RESOLUTION}.parquet"
    ),

    # Gold
    gold_taxi_trips=PROCESSED_DIR / f"gold_taxi{TAXI_SUFFIX}.parquet",
    gold_weatherdata=PROCESSED_DIR / "gold_weather.parquet",
    gold_1h_demand_census_tracts=PROCESSED_DIR / "GOLD_1H_DEMAND_CENSUS_TRACTS.parquet",
    gold_1h_demand_community_areas=PROCESSED_DIR / "GOLD_1H_DEMAND_COMMUNITY_AREAS.parquet",
    gold_1h_demand_community_area_unfiltered=(
        PROCESSED_DIR / "GOLD_1H_DEMAND_COMMUNITY_AREAS_UNFILTERED.parquet"
    ),
    gold_1h_demand_hexagon=PROCESSED_DIR / f"GOLD_1H_DEMAND_HEXAGON_{H3_RESOLUTION}.parquet",

    gold_2h_demand_census_tracts=PROCESSED_DIR / "GOLD_2H_DEMAND_CENSUS_TRACTS.parquet",
    gold_2h_demand_community_areas=PROCESSED_DIR / "GOLD_2H_DEMAND_COMMUNITY_AREAS.parquet",
    gold_2h_demand_community_area_unfiltered=(
        PROCESSED_DIR / "GOLD_2H_DEMAND_COMMUNITY_AREAS_UNFILTERED.parquet"
    ),
    gold_2h_demand_hexagon=PROCESSED_DIR / f"GOLD_2H_DEMAND_HEXAGON_{H3_RESOLUTION}.parquet",
    
    gold_4h_demand_census_tracts=PROCESSED_DIR / "GOLD_4H_DEMAND_CENSUS_TRACTS.parquet",
    gold_4h_demand_community_areas=PROCESSED_DIR / "GOLD_4H_DEMAND_COMMUNITY_AREAS.parquet",
    gold_4h_demand_community_area_unfiltered=(
        PROCESSED_DIR / "GOLD_4H_DEMAND_COMMUNITY_AREAS_UNFILTERED.parquet"
    ),
    gold_4h_demand_hexagon=PROCESSED_DIR / f"GOLD_4H_DEMAND_HEXAGON_{H3_RESOLUTION}.parquet",

    # Train/validation/test outputs
    train_test_dir=TRAIN_TEST_DIR,
)


def demand_split_paths(spatial_unit: str, time_unit: str) -> dict[str, Path]:
    """Return the train/validation/test paths produced for one gold dataset."""
    spatial_suffixes = {
        "hexagon": "hexagon",
        "census_tracts": "census_tracts",
        "community_areas": "community_areas",
    }
    if spatial_unit not in spatial_suffixes:
        raise ValueError(f"Unsupported spatial unit: {spatial_unit}")
    if time_unit not in GOLD_TIME_UNITS:
        raise ValueError(
            f"Unsupported time unit: {time_unit}; expected one of {GOLD_TIME_UNITS}"
        )

    gold_attribute = (
        f"gold_{time_unit}_demand_{spatial_suffixes[spatial_unit]}"
    )
    gold_path = getattr(PATHS, gold_attribute)
    return {
        split: PATHS.train_test_dir / f"{gold_path.stem}_{split.upper()}.parquet"
        for split in ("train", "val", "test")
    }
