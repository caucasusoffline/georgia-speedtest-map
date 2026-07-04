#!/usr/bin/env python3
"""
Ookla Open Data -> Georgia internet speed extractor.

მოაქვს Ookla Speedtest ღია მონაცემები (mobile/fixed), ჭრის მათ საქართველოს
საზღვრებით და ინახავს GeoJSON ფაილებად კვარტლების მიხედვით.

Requirements:
    pip install pandas geopandas shapely pyarrow s3fs
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable

import geopandas as gpd
import pandas as pd
import s3fs
from shapely import wkt

# --------------------------------------------------------------------------- #
# კონფიგურაცია
# --------------------------------------------------------------------------- #

DATA_DIR = Path("data")
LOCAL_BND_FILE = Path("municipality.geojson")

# Georgia-ს დაახლოებითი bounding box (სწრაფი პირველადი გაფილტვრისთვის)
MIN_LON, MIN_LAT, MAX_LON, MAX_LAT = 40.0, 41.0, 46.8, 43.6

S3_BUCKET = "ookla-open-data"
S3_PREFIX = "parquet/performance"

QUARTER_START = {1: "01-01", 2: "04-01", 3: "07-01", 4: "10-01"}

REQUIRED_COLUMNS = [
    "tile",
    "avg_d_kbps",
    "avg_u_kbps",
    "avg_lat_ms",
    "tests",
    "devices",
]

OUTPUT_COLUMNS = [
    "geometry",
    "avg_d_mbps",
    "avg_u_mbps",
    "avg_lat_ms",
    "tests",
    "devices",
    "year",
    "quarter",
]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("ookla-georgia")

# ერთი გაზიარებული S3 filesystem handle (ანონიმური წვდომა, ხელახლა გამოსაყენებელი)
_S3 = s3fs.S3FileSystem(anon=True)


@dataclass(frozen=True)
class Period:
    year: int
    quarter: int

    @property
    def date_str(self) -> str:
        return f"{self.year}-{QUARTER_START[self.quarter]}"

    def s3_key(self, network_type: str) -> str:
        return (
            f"{S3_PREFIX}/type={network_type}/year={self.year}/"
            f"quarter={self.quarter}/{self.date_str}_performance_{network_type}_tiles.parquet"
        )

    def s3_url(self, network_type: str) -> str:
        return f"s3://{S3_BUCKET}/{self.s3_key(network_type)}"

    def output_path(self, network_type: str) -> Path:
        return DATA_DIR / f"georgia_{network_type}_{self.year}_Q{self.quarter}.geojson"


# --------------------------------------------------------------------------- #
# საზღვრების ჩატვირთვა
# --------------------------------------------------------------------------- #

def get_georgia_polygon() -> gpd.GeoDataFrame:
    """ტვირთავს და ასწორებს საქართველოს საზღვრების GeoJSON-ს."""
    log.info("ვტვირთავთ საქართველოს საზღვრებს (%s)...", LOCAL_BND_FILE)

    if not LOCAL_BND_FILE.exists():
        raise FileNotFoundError(
            f"ვერ ვიპოვე ფაილი: {LOCAL_BND_FILE}. გთხოვთ, ატვირთოთ რეპოზიტორიუმში."
        )

    try:
        gdf_boundary = gpd.read_file(LOCAL_BND_FILE)
    except Exception:
        # ზოგ გარემოში pyogrio-ს default ჩავარდნისას fiona-ზე fallback
        log.warning("ავტომატური engine-ით წაკითხვა ჩავარდა, ვცდით fiona-ს...")
        gdf_boundary = gpd.read_file(LOCAL_BND_FILE, engine="fiona")

    # გეომეტრიის გასწორება (invalid polygons)
    gdf_boundary["geometry"] = gdf_boundary["geometry"].make_valid()

    # CRS-ის დამუშავება: თუ საერთოდ არ არის მითითებული, ვვარაუდობთ EPSG:4326-ს;
    # თუ სხვა CRS-ია, გადავიყვანთ EPSG:4326-ში, რადგან Ookla tiles ამ სისტემაშია.
    if gdf_boundary.crs is None:
        log.warning("ფაილს არ აქვს განსაზღვრული CRS — ვვარაუდობთ EPSG:4326-ს.")
        gdf_boundary = gdf_boundary.set_crs("EPSG:4326")
    elif gdf_boundary.crs.to_epsg() != 4326:
        log.info("ვასწორებთ ფაილის კოორდინატთა სისტემას (CRS)...")
        gdf_boundary = gdf_boundary.to_crs("EPSG:4326")

    dissolved = gdf_boundary.dissolve()
    if dissolved.empty or dissolved.geometry.iloc[0].is_empty:
        raise ValueError("საზღვრის გეომეტრია ცარიელია dissolve-ის შემდეგ.")

    return dissolved


# --------------------------------------------------------------------------- #
# ხელმისაწვდომი პერიოდების პოვნა
# --------------------------------------------------------------------------- #

def get_target_periods(
    network_type: str, target_year: int | None, target_quarter: int | None
) -> list[Period]:
    """S3-ზე ამოწმებს, რომელი კვარტლის ფაილები რეალურად არსებობს."""
    candidates: list[Period]
    if target_year and target_quarter:
        candidates = [Period(target_year, target_quarter)]
    else:
        current_year = datetime.now().year
        candidates = [
            Period(year, q)
            for year in range(current_year, current_year - 2, -1)
            for q in (4, 3, 2, 1)
        ]

    valid: list[Period] = []
    for period in candidates:
        key = period.s3_key(network_type)
        try:
            if _S3.exists(f"{S3_BUCKET}/{key}"):
                valid.append(period)
        except Exception as exc:  # noqa: BLE001 - გვინდა ცალკეული შემოწმების გაგრძელება
            log.debug("S3 exists() შემოწმება ჩავარდა %s-სთვის: %s", key, exc)
            continue

    return valid


# --------------------------------------------------------------------------- #
# ერთი ფაილის დამუშავება
# --------------------------------------------------------------------------- #

def process_period(
    network_type: str, period: Period, georgia_boundary: gpd.GeoDataFrame
) -> None:
    output_file = period.output_path(network_type)

    if output_file.exists():
        log.info("✅ უკვე არსებობს: %s (გამოვტოვებთ)", output_file)
        return

    log.info("მიმდინარეობს ჩამოტვირთვა: %s Q%s...", period.year, period.quarter)

    try:
        # ვტვირთავთ მხოლოდ საჭირო სვეტებს — მკვეთრად ამცირებს მეხსიერების
        # მოხმარებას, რადგან parquet სვეტობრივია.
        df = pd.read_parquet(
            period.s3_url(network_type),
            columns=REQUIRED_COLUMNS,
            storage_options={"anon": True},
        )
    except Exception as exc:
        log.error("❌ ჩამოტვირთვის შეცდომა (%s Q%s): %s", period.year, period.quarter, exc)
        return

    try:
        coords = df["tile"].str.extract(r"\(\(\s*([0-9.\-]+)\s+([0-9.\-]+)")
        df["lon"] = pd.to_numeric(coords[0], errors="coerce")
        df["lat"] = pd.to_numeric(coords[1], errors="coerce")
        df = df.dropna(subset=["lon", "lat"])

        # პირველადი, იაფი ამოჭრა bounding box-ით
        bbox_df = df[
            df["lon"].between(MIN_LON, MAX_LON) & df["lat"].between(MIN_LAT, MAX_LAT)
        ].copy()

        if bbox_df.empty:
            log.warning("⚠️ %s Q%s ცარიელია bounding box-ში.", period.year, period.quarter)
            return

        log.info("  კვადრატში მოხვდა %d უჯრა.", len(bbox_df))

        bbox_df["geometry"] = bbox_df["tile"].apply(wkt.loads)
        gdf = gpd.GeoDataFrame(bbox_df, geometry="geometry", crs="EPSG:4326")

        log.info("  მიმდინარეობს ზუსტი საზღვრებით ამოჭრა...")
        gdf_clipped = gpd.clip(gdf, georgia_boundary)

        if gdf_clipped.empty:
            log.warning(
                "  ⚠️ საზღვრებში გადაკვეთა არ მოხდა (%s Q%s) — შესაძლოა CRS-ის პრობლემა.",
                period.year,
                period.quarter,
            )
            return

        gdf_clipped["avg_d_mbps"] = gdf_clipped["avg_d_kbps"] / 1000
        gdf_clipped["avg_u_mbps"] = gdf_clipped["avg_u_kbps"] / 1000
        gdf_clipped["year"] = period.year
        gdf_clipped["quarter"] = f"Q{period.quarter}"

        gdf_clipped = gdf_clipped[OUTPUT_COLUMNS]

        DATA_DIR.mkdir(exist_ok=True)
        gdf_clipped.to_file(output_file, driver="GeoJSON")
        log.info("✅ შეინახა: %s (%d ლოკაცია)", output_file, len(gdf_clipped))

    except Exception as exc:
        log.error(
            "❌ დამუშავების შეცდომა (%s Q%s): %s", period.year, period.quarter, exc, exc_info=True
        )


def process_network(
    network_type: str,
    georgia_boundary: gpd.GeoDataFrame,
    target_year: int | None,
    target_quarter: int | None,
) -> None:
    if target_year and target_quarter:
        log.info("--- ვამუშავებთ: %s Q%s (%s) ---", target_year, target_quarter, network_type.upper())
    else:
        log.info("--- ვეძებთ უახლეს მონაცემებს (%s) ---", network_type.upper())

    periods = get_target_periods(network_type, target_year, target_quarter)
    if not periods:
        log.warning("ვერცერთი მოქმედი პერიოდი ვერ მოიძებნა %s-სთვის.", network_type)
        return

    for period in periods:
        process_period(network_type, period, georgia_boundary)


# --------------------------------------------------------------------------- #
# Metadata
# --------------------------------------------------------------------------- #

def generate_metadata() -> None:
    if not DATA_DIR.exists():
        log.warning("data/ დირექტორია არ არსებობს — metadata არ შეიქმნება.")
        return

    files = sorted(p.name for p in DATA_DIR.iterdir() if p.suffix == ".geojson")
    mobile_files = sorted(
        (f for f in files if f.startswith("georgia_mobile_")), reverse=True
    )
    fixed_files = sorted(
        (f for f in files if f.startswith("georgia_fixed_")), reverse=True
    )

    metadata_path = DATA_DIR / "metadata.json"
    with metadata_path.open("w", encoding="utf-8") as f:
        json.dump(
            {
                "mobile": mobile_files,
                "fixed": fixed_files,
                "generated_at": datetime.utcnow().isoformat() + "Z",
            },
            f,
            ensure_ascii=False,
            indent=2,
        )
    log.info("✅ მენეჯერის ფაილი (%s) განახლდა.", metadata_path)


# --------------------------------------------------------------------------- #
# Entry point
# --------------------------------------------------------------------------- #

def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Ookla Open Data-დან საქართველოს ინტერნეტ სიჩქარის მონაცემების ამოღება."
    )
    parser.add_argument("--year", type=int, help="სამიზნე წელი (მაგ. 2025)")
    parser.add_argument(
        "--quarter", type=int, choices=[1, 2, 3, 4], help="სამიზნე კვარტალი (1-4)"
    )
    args = parser.parse_args(argv)

    if bool(args.year) != bool(args.quarter):
        parser.error("--year და --quarter ერთად უნდა იყოს მითითებული, ან საერთოდ არცერთი.")

    return args


def main() -> int:
    args = parse_args()
    DATA_DIR.mkdir(exist_ok=True)

    try:
        georgia_boundary = get_georgia_polygon()
    except Exception as exc:
        log.error("საზღვრების ჩატვირთვა ჩავარდა: %s", exc)
        return 1

    for network_type in ("mobile", "fixed"):
        process_network(network_type, georgia_boundary, args.year, args.quarter)

    generate_metadata()
    return 0


if __name__ == "__main__":
    sys.exit(main())
