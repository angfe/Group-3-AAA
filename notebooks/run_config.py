from pathlib import Path
from dataclasses import dataclass

# --------------------------------------------------
# Set the run mode below to "sample" or "full"
RUN_MODE = "full" # "sample" or "full"

# Set App Token for Chicago Data (see more details in Notebooks "00_01_data_loader.ipynb")
APP_TOKEN = "kujE0csvYM9mpKDXjIfDzHGAg"
# --------------------------------------------------
# Start and end date of taxi and weather data
START_DATE = "2024-01-01T00:00:00"
END_DATE = "2026-05-01T00:00:00"
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"

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
    silver_taxi_trips: Path
    silver_weatherdata: Path
    silver_census_tracts: Path
    silver_community_areas: Path
    silver_hexagon: Path
    silver_boundary: Path
    
    # Gold
    gold_taxi_trips: Path
    gold_weatherdata: Path
    gold_hourly_demand_census_tracts: Path
    gold_hourly_demand_community_areas: Path
    gold_hourly_demand_hexagon: Path
    
    # Train Test Split
    train: Path
    val: Path
    test: Path


PATHS_BY_MODE = {
    "sample": DataPaths(
        # Raw
        raw_taxi_trips=DATA_DIR / "sample" / "taxi_sample.csv",
        raw_weatherdata=DATA_DIR / "sample" / "weatherdata.csv",
        raw_census_tracts=DATA_DIR / "sample" / "Census_Tracts.csv",
        raw_community_areas=DATA_DIR / "sample" / "Community_Areas.csv",
        
        # Bronze
        bronze_taxi_trips=DATA_DIR / "sample" / "bronze_taxi_sample.parquet",
        bronze_weatherdata=DATA_DIR / "sample" / "bronze_weatherdata.parquet",
        bronze_census_tracts=DATA_DIR / "sample" / "bronze_Census_Tracts.parquet",
        bronze_community_areas=DATA_DIR / "sample" / "bronze_Community_Areas.parquet",
        bronze_osm_geo=DATA_DIR / "sample" / "bronze_osm_chicago_pois.geoparquet",
        bronze_osm=DATA_DIR / "sample" / "bronze_osm_chicago_pois.parquet",
        
        # Silver
        silver_taxi_trips=DATA_DIR / "sample" / "silver_taxi_sample.parquet",
        silver_weatherdata=DATA_DIR / "sample" / "silver_weatherdata.parquet",
        silver_census_tracts=DATA_DIR / "sample" / "silver_census_tracts.geoparquet",
        silver_community_areas=DATA_DIR / "sample" / "silver_community_areas.geoparquet",
        silver_hexagon=DATA_DIR / "sample" / "silver_dim_h3_chicago_7.parquet",
        silver_boundary=DATA_DIR / "sample" / "silver_chicago_boundary_from_census_tracts_H3_RESOLUTION.parquet",
        
        # Gold
        gold_taxi_trips=DATA_DIR / "sample" / "gold_taxi_sample.parquet",
        gold_weatherdata=DATA_DIR / "sample" / "gold_weather.parquet",
        gold_hourly_demand_census_tracts=DATA_DIR / "sample" / "gold_hourly_demand_census_tracts.parquet",
        gold_hourly_demand_community_areas=DATA_DIR / "sample" / "gold_hourly_demand_community_areas.parquet",
        gold_hourly_demand_hexagon=DATA_DIR / "sample" / "gold_hourly_demand_hexagon.parquet",
        
        # Train Test Split
        train=DATA_DIR / "sample" / "train.parquet",
        val=DATA_DIR / "sample" / "val.parquet",
        test=DATA_DIR / "sample" / "test.parquet",
          
    ),

    "full": DataPaths(
        # Raw
        raw_taxi_trips=DATA_DIR / "raw_data" / "taxi.csv",
        raw_weatherdata=DATA_DIR / "raw_data" / "weatherdata.csv",
        raw_census_tracts=DATA_DIR / "raw_data" / "Census_Tracts.csv",
        raw_community_areas=DATA_DIR / "raw_data" / "Community_Areas.csv",
        
        # Bronze
        bronze_taxi_trips=DATA_DIR / "processed_data" / "bronze_taxi_sample.parquet",
        bronze_weatherdata=DATA_DIR / "processed_data" / "bronze_weatherdata.parquet",
        bronze_census_tracts=DATA_DIR / "processed_data" / "bronze_Census_Tracts.parquet",
        bronze_community_areas=DATA_DIR / "processed_data" / "bronze_Community_Areas.parquet",
        bronze_osm_geo=DATA_DIR / "processed_data" / "bronze_osm_chicago_pois.geoparquet",
        bronze_osm=DATA_DIR / "processed_data" / "bronze_osm_chicago_pois.parquet",
        
        # Silver
        silver_taxi_trips=DATA_DIR / "processed_data" / "silver_taxi.parquet",
        silver_weatherdata=DATA_DIR / "processed_data" / "silver_weatherdata.parquet",
        silver_census_tracts=DATA_DIR / "processed_data" / "silver_census_tracts.geoparquet",
        silver_community_areas=DATA_DIR / "processed_data" / "silver_community_areas.geoparquet",
        silver_hexagon=DATA_DIR / "processed_data" / "silver_dim_h3_chicago_8.parquet",
        silver_boundary=DATA_DIR / "processed_data" / "silver_chicago_boundary_from_census_tracts_H3_RESOLUTION.parquet",
        
        # Gold
        gold_taxi_trips=DATA_DIR / "processed_data" / "gold_taxi.parquet",
        gold_weatherdata=DATA_DIR / "processed_data" / "gold_weather.parquet",
        gold_hourly_demand_census_tracts=DATA_DIR / "processed_data" / "gold_hourly_demand_census_tracts.parquet",
        gold_hourly_demand_community_areas=DATA_DIR / "processed_data" / "gold_hourly_demand_community_areas.parquet",
        gold_hourly_demand_hexagon=DATA_DIR / "processed_data" / "gold_hourly_demand_hexagon.parquet",
        
        # Train Test Split
        train=DATA_DIR / "train_test_data" / "train.parquet",
        val=DATA_DIR / "train_test_data" / "val.parquet",
        test=DATA_DIR / "train_test_data" / "test.parquet",
    
    ),
}


def get_paths() -> DataPaths:
    if RUN_MODE not in PATHS_BY_MODE:
        raise ValueError(
            f"Unknown RUN_MODE '{RUN_MODE}'. Use one of: {list(PATHS_BY_MODE.keys())}"
        )

    return PATHS_BY_MODE[RUN_MODE]

PATHS = get_paths()