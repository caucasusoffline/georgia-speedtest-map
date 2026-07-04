import pandas as pd
import geopandas as gpd
from shapely import wkt
import requests
import os
from datetime import datetime

os.makedirs("data", exist_ok=True)

# საქართველოს მიახლოებითი კოორდინატები
MIN_LON, MIN_LAT, MAX_LON, MAX_LAT = 40.0, 41.0, 46.8, 43.6

def get_latest_ookla_url(network_type="mobile"):
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
                    print(f"✅ მოიძებნა უახლესი მონაცემები: {year} წლის კვარტალი {q_num} ({network_type})")
                    response.close()
                    return s3_url
            except requests.RequestException:
                continue
                
    raise Exception("ვერ მოიძებნა Ookla-ს მონაცემების ვალიდური ლინკი.")

def main():
    print("ვიწყებთ მონაცემების განახლების პროცესს...")
    url = get_latest_ookla_url(network_type="mobile")
    print(f"ლინკი: {url}")
    
    print("მიმდინარეობს გლობალური მონაცემების ჩამოტვირთვა... (შეიძლება 1-2 წუთი დასჭირდეს)")
    # 1. ვკითხულობთ სტანდარტულ Parquet ფაილს
    df = pd.read_parquet(url, storage_options={"anon": True})
    
    print("მონაცემების გაფილტვრა საქართველოს კოორდინატებით...")
    # 2. ვიყენებთ Regex-ს, რომ პირდაპირ ტექსტიდან 'POLYGON((x y...))' ამოვიღოთ კოორდინატები
    coords = df['tile'].str.extract(r'\(\(\s*([0-9.-]+)\s+([0-9.-]+)')
    df['lon'] = coords[0].astype(float)
    df['lat'] = coords[1].astype(float)
    
    # 3. ვფილტრავთ მხოლოდ საქართველოს 
    georgia_df = df[
        (df['lon'] >= MIN_LON) & (df['lon'] <= MAX_LON) &
        (df['lat'] >= MIN_LAT) & (df['lat'] <= MAX_LAT)
    ].copy()
    
    records_count = len(georgia_df)
    print(f"📊 ნაპოვნია {records_count} ლოკაცია საქართველოს ტერიტორიაზე.")
    
    if records_count > 0:
        print("გეომეტრიული ფიგურების გენერაცია...")
        # 4. გაფილტრულ (მცირე) მონაცემებზე ვქმნით ნამდვილ გეომეტრიას
        georgia_df['geometry'] = georgia_df['tile'].apply(wkt.loads)
        gdf = gpd.GeoDataFrame(georgia_df, geometry='geometry', crs="EPSG:4326")
        
        # სიჩქარეების კონვერტაცია Mbps-ში
        gdf['avg_d_kbps'] = gdf['avg_d_kbps'] / 1000 
        gdf['avg_u_kbps'] = gdf['avg_u_kbps'] / 1000 
        
        # ვტოვებთ მხოლოდ იმ სვეტებს, რაც რუკისთვის გვჭირდება (რათა ფაილი მსუბუქი იყოს)
        columns_to_keep = ['geometry', 'avg_d_kbps', 'avg_u_kbps', 'tests']
        gdf = gdf[columns_to_keep]
        
        output_file = "data/georgia_mobile.geojson"
        gdf.to_file(output_file, driver="GeoJSON")
        print(f"✅ ფაილი წარმატებით შეინახა: {output_file}")
    else:
        print("⚠️ საქართველოს ტერიტორიაზე მონაცემები ვერ მოიძებნა.")

if __name__ == "__main__":
    main()
