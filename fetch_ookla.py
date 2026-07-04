import pandas as pd
import geopandas as gpd
from shapely import wkt
import requests
import os
import json
import argparse
from datetime import datetime

os.makedirs("data", exist_ok=True)
MIN_LON, MIN_LAT, MAX_LON, MAX_LAT = 40.0, 41.0, 46.8, 43.6
GEORGIA_BND_URL = "https://caucasusoffline.com/test1000/js/municipality-shapes-converted.geojson"

def get_georgia_polygon():
    print("ვტვირთავთ საქართველოს საზღვრებს...")
    gdf_boundary = gpd.read_file(GEORGIA_BND_URL)
    return gdf_boundary.dissolve()

def get_target_urls(network_type, target_year=None, target_quarter=None):
    valid_urls = []
    current_year = datetime.now().year
    quarters_map = {1: "-01-01", 2: "-04-01", 3: "-07-01", 4: "-10-01"}
    
    # ლოგიკა: თუ მითითებულია წელი და კვარტალი, ვტვირთავთ მხოლოდ მას
    if target_year and target_quarter:
        years = [target_year]
        quarters = [target_quarter]
    else:
        # ავტომატური რეჟიმი: ვამოწმებთ მხოლოდ ბოლო 2 წელს (დროის დასაზოგად)
        years = range(current_year, current_year - 2, -1)
        quarters = [4, 3, 2, 1]

    for year in years:
        for q_num in quarters:
            date_suffix = quarters_map[q_num]
            date_str = f"{year}{date_suffix}"
            check_url = f"https://ookla-open-data.s3.amazonaws.com/parquet/performance/type={network_type}/year={year}/quarter={q_num}/{date_str}_performance_{network_type}_tiles.parquet"
            s3_url = f"s3://ookla-open-data/parquet/performance/type={network_type}/year={year}/quarter={q_num}/{date_str}_performance_{network_type}_tiles.parquet"
            
            try:
                response = requests.get(check_url, stream=True, timeout=5)
                if response.status_code == 200:
                    valid_urls.append((year, q_num, s3_url))
                response.close()
            except:
                continue
                
    return valid_urls

def process_network(network_type, georgia_boundary, target_year=None, target_quarter=None):
    if target_year and target_quarter:
         print(f"\n--- ვამუშავებთ: {target_year} Q{target_quarter} ({network_type.upper()}) ---")
    else:
         print(f"\n--- ვეძებთ უახლეს მონაცემებს ({network_type.upper()}) ---")
         
    urls = get_target_urls(network_type, target_year, target_quarter)
    
    for year, q_num, url in urls:
        output_file = f"data/georgia_{network_type}_{year}_Q{q_num}.geojson"
        
        if os.path.exists(output_file):
            print(f"✅ უკვე არსებობს: {output_file} (გამოვტოვებთ)")
            continue

        print(f"მიმდინარეობს ჩამოტვირთვა: {year} წლის Q{q_num}...")
        try:
            df = pd.read_parquet(url, storage_options={"anon": True})
            coords = df['tile'].str.extract(r'\(\(\s*([0-9.-]+)\s+([0-9.-]+)')
            df['lon'] = coords[0].astype(float)
            df['lat'] = coords[1].astype(float)
            
            georgia_df = df[
                (df['lon'] >= MIN_LON) & (df['lon'] <= MAX_LON) &
                (df['lat'] >= MIN_LAT) & (df['lat'] <= MAX_LAT)
            ].copy()
            
            if len(georgia_df) > 0:
                georgia_df['geometry'] = georgia_df['tile'].apply(wkt.loads)
                gdf = gpd.GeoDataFrame(georgia_df, geometry='geometry', crs="EPSG:4326")
                
                print("  მიმდინარეობს ზუსტი საზღვრებით ამოჭრა...")
                gdf_clipped = gpd.clip(gdf, georgia_boundary)
                
                if len(gdf_clipped) == 0:
                     continue

                gdf_clipped['avg_d_mbps'] = gdf_clipped['avg_d_kbps'] / 1000 
                gdf_clipped['avg_u_mbps'] = gdf_clipped['avg_u_kbps'] / 1000 
                gdf_clipped['year'] = year
                gdf_clipped['quarter'] = f"Q{q_num}"
                
                cols = ['geometry', 'avg_d_mbps', 'avg_u_mbps', 'avg_lat_ms', 'tests', 'devices', 'year', 'quarter']
                gdf_clipped = gdf_clipped[cols]
                
                gdf_clipped.to_file(output_file, driver="GeoJSON")
                print(f"✅ შეინახა: {output_file}")
            else:
                print(f"⚠️ {year} Q{q_num} ცარიელია.")
        except Exception as e:
            print(f"❌ შეცდომა: {e}")

def generate_metadata():
    files = os.listdir("data")
    mobile_files = sorted([f for f in files if f.startswith("georgia_mobile_") and f.endswith(".geojson")], reverse=True)
    fixed_files = sorted([f for f in files if f.startswith("georgia_fixed_") and f.endswith(".geojson")], reverse=True)
    
    with open("data/metadata.json", "w") as f:
        json.dump({"mobile": mobile_files, "fixed": fixed_files}, f)
    print("\n✅ მენეჯერის ფაილი (metadata.json) განახლდა.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", type=int, help="წელი")
    parser.add_argument("--quarter", type=int, help="კვარტალი")
    args = parser.parse_args()

    georgia_boundary = get_georgia_polygon()
    
    process_network("mobile", georgia_boundary, args.year, args.quarter)
    process_network("fixed", georgia_boundary, args.year, args.quarter)
    
    generate_metadata()

if __name__ == "__main__":
    main()
