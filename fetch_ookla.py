import geopandas as gpd
import requests
import os
from datetime import datetime

os.makedirs("data", exist_ok=True)
GEORGIA_BBOX = (40.0, 41.0, 46.8, 43.6)

def get_latest_ookla_url(network_type="mobile"):
    current_year = datetime.now().year
    
    quarters = [
        (4, "-10-01"),
        (3, "-07-01"),
        (2, "-04-01"),
        (1, "-01-01")
    ]
    
    # ვამოწმებთ ბოლო 5 წლის მონაცემებს
    for year in range(current_year, current_year - 5, -1):
        for q_num, date_suffix in quarters:
            date_str = f"{year}{date_suffix}"
            url = f"https://ookla-open-data.s3.amazonaws.com/shapefiles/performance/type={network_type}/year={year}/quarter={q_num}/{date_str}_performance_{network_type}_tiles.parquet"
            
            try:
                # HEAD-ის ნაცვლად ვიყენებთ GET-ს stream=True პარამეტრით
                response = requests.get(url, stream=True, timeout=10)
                if response.status_code == 200:
                    print(f"✅ მოიძებნა უახლესი მონაცემები: {year} წლის კვარტალი {q_num}")
                    response.close() # ვხურავთ კავშირს, რადგან შემოწმება გავიარეთ
                    return url
            except requests.RequestException:
                continue
                
    raise Exception("ვერ მოიძებნა Ookla-ს მონაცემების ვალიდური ლინკი.")

def main():
    print("ვიწყებთ მონაცემების განახლების პროცესს...")
    
    url = get_latest_ookla_url(network_type="mobile")
    print(f"ლინკი: {url}")
    
    print("მიმდინარეობს საქართველოს მონაცემების ამოჭრა... (ამას შეიძლება 1-2 წუთი დასჭირდეს)")
    gdf = gpd.read_parquet(url, bbox=GEORGIA_BBOX)
    
    records_count = len(gdf)
    print(f"📊 ნაპოვნია {records_count} ლოკაცია საქართველოს ტერიტორიაზე.")
    
    if records_count > 0:
        gdf['avg_d_kbps'] = gdf['avg_d_kbps'] / 1000 
        gdf['avg_u_kbps'] = gdf['avg_u_kbps'] / 1000 
        
        output_file = "data/georgia_mobile.geojson"
        gdf.to_file(output_file, driver="GeoJSON")
        print(f"✅ ფაილი წარმატებით შეინახა: {output_file}")
    else:
        print("⚠️ საქართველოს ტერიტორიაზე მონაცემები ვერ მოიძებნა.")

if __name__ == "__main__":
    main()
