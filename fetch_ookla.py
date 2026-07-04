import pandas as pd
import geopandas as gpd
from shapely import wkt
import requests
import os
from datetime import datetime

os.makedirs("data", exist_ok=True)
MIN_LON, MIN_LAT, MAX_LON, MAX_LAT = 40.0, 41.0, 46.8, 43.6

def get_latest_ookla_url(network_type):
    current_year = datetime.now().year
    quarters = [(4, "-10-01"), (3, "-07-01"), (2, "-04-01"), (1, "-01-01")]
    
    for year in range(current_year, current_year - 5, -1):
        for q_num, date_suffix in quarters:
            date_str = f"{year}{date_suffix}"
            check_url = f"https://ookla-open-data.s3.amazonaws.com/parquet/performance/type={network_type}/year={year}/quarter={q_num}/{date_str}_performance_{network_type}_tiles.parquet"
            s3_url = f"s3://ookla-open-data/parquet/performance/type={network_type}/year={year}/quarter={q_num}/{date_str}_performance_{network_type}_tiles.parquet"
            
            try:
                response = requests.get(check_url, stream=True, timeout=10)
                if response.status_code == 200:
                    response.close()
                    return s3_url
            except requests.RequestException:
                continue
    raise Exception(f"ვერ მოიძებნა {network_type} მონაცემები.")

def process_network(network_type):
    print(f"\n--- ვიწყებთ {network_type.upper()} მონაცემების დამუშავებას ---")
    url = get_latest_ookla_url(network_type)
    
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
        
        # სიჩქარეების კონვერტაცია Mbps-ში
        gdf['avg_d_mbps'] = gdf['avg_d_kbps'] / 1000 
        gdf['avg_u_mbps'] = gdf['avg_u_kbps'] / 1000 
        
        # ვინახავთ ყველა მნიშვნელოვან პარამეტრს
        cols = ['geometry', 'avg_d_mbps', 'avg_u_mbps', 'avg_lat_ms', 'tests', 'devices']
        gdf = gdf[cols]
        
        output_file = f"data/georgia_{network_type}.geojson"
        gdf.to_file(output_file, driver="GeoJSON")
        print(f"✅ შეინახა: {output_file} ({len(gdf)} ლოკაცია)")
    else:
        print(f"⚠️ {network_type} მონაცემები ვერ მოიძებნა.")

def main():
    # რიგრიგობით უშვებს ორივეს
    process_network("mobile")
    process_network("fixed")

if __name__ == "__main__":
    main()
