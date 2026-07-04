import pandas as pd
import geopandas as gpd
from shapely import wkt
import requests
import os
import json
from datetime import datetime

os.makedirs("data", exist_ok=True)
MIN_LON, MIN_LAT, MAX_LON, MAX_LAT = 40.0, 41.0, 46.8, 43.6

def get_all_valid_urls(network_type):
    valid_urls = []
    current_year = datetime.now().year
    # Q1, Q2, Q3, Q4 თარიღები
    quarters = [(1, "-01-01"), (2, "-04-01"), (3, "-07-01"), (4, "-10-01")]
    
    # Ookla-ს მონაცემები 2019 წლიდან იწყება
    for year in range(2019, current_year + 1):
        for q_num, date_suffix in quarters:
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

def process_network(network_type):
    print(f"\n--- ვეძებთ {network_type.upper()} მონაცემებს 2019 წლიდან დღემდე ---")
    urls = get_all_valid_urls(network_type)
    print(f"სერვერზე ნაპოვნია {len(urls)} კვარტლის ბაზა.")
    
    for year, q_num, url in urls:
        output_file = f"data/georgia_{network_type}_{year}_Q{q_num}.geojson"
        
        # თუ ფაილი უკვე არსებობს, ვტოვებთ (რომ დრო დავზოგოთ)
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
                
                gdf['avg_d_mbps'] = gdf['avg_d_kbps'] / 1000 
                gdf['avg_u_mbps'] = gdf['avg_u_kbps'] / 1000 
                gdf['year'] = year
                gdf['quarter'] = f"Q{q_num}"
                
                cols = ['geometry', 'avg_d_mbps', 'avg_u_mbps', 'avg_lat_ms', 'tests', 'devices', 'year', 'quarter']
                gdf = gdf[cols]
                
                gdf.to_file(output_file, driver="GeoJSON")
                print(f"✅ შეინახა: {output_file} ({len(gdf)} ლოკაცია)")
            else:
                print(f"⚠️ {year} Q{q_num}-ში მონაცემები ცარიელია.")
        except Exception as e:
            print(f"❌ შეცდომა {year} Q{q_num}-ის დამუშავებისას: {e}")

def generate_metadata():
    # ვქმნით JSON ფაილს, სადაც ეწერება რა ფაილები გვაქვს ჩამოტვირთული
    files = os.listdir("data")
    mobile_files = sorted([f for f in files if f.startswith("georgia_mobile_") and f.endswith(".geojson")], reverse=True)
    fixed_files = sorted([f for f in files if f.startswith("georgia_fixed_") and f.endswith(".geojson")], reverse=True)
    
    with open("data/metadata.json", "w") as f:
        json.dump({"mobile": mobile_files, "fixed": fixed_files}, f)
    print("\n✅ მენეჯერის ფაილი (metadata.json) განახლდა.")

def main():
    process_network("mobile")
    process_network("fixed")
    generate_metadata()

if __name__ == "__main__":
    main()
