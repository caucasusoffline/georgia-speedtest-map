
import geopandas as gpd
import requests
import os
from datetime import datetime

# 1. ვქმნით data ფოლდერს, სადაც შენახული იქნება ჩვენი geojson ფაილი
os.makedirs("data", exist_ok=True)

# 2. საქართველოს მიახლოებითი კოორდინატები (Bounding Box)
# ფორმატი: (მინიმალური გრძედი/Lon, მინიმალური განედი/Lat, მაქსიმალური გრძედი, მაქსიმალური განედი)
GEORGIA_BBOX = (40.0, 41.0, 46.8, 43.6)

def get_latest_ookla_url(network_type="mobile"):
    """
    ეს ფუნქცია ავტომატურად პოულობს Ookla-ს ყველაზე ბოლო კვარტლის მონაცემების ლინკს.
    ის მიმდინარე წლიდან უკან მიყვება თარიღებს და ამოწმებს, რომელი ფაილია ატვირთული.
    """
    current_year = datetime.now().year
    
    # Ookla მონაცემებს ატვირთავს ამ თვეების პირველ რიცხვში
    quarters = [
        (4, "-10-01"), # Q4
        (3, "-07-01"), # Q3
        (2, "-04-01"), # Q2
        (1, "-01-01")  # Q1
    ]
    
    # ვამოწმებთ ბოლო 3 წლის მონაცემებს
    for year in range(current_year, current_year - 3, -1):
        for q_num, date_suffix in quarters:
            date_str = f"{year}{date_suffix}"
            url = f"https://ookla-open-data.s3.amazonaws.com/shapefiles/performance/type={network_type}/year={year}/quarter={q_num}/{date_str}_performance_{network_type}_tiles.parquet"
            
            # ვამოწმებთ ლინკს (მხოლოდ header-ს ვიწერთ, რომ დრო არ დაიკარგოს)
            try:
                response = requests.head(url)
                if response.status_code == 200:
                    print(f"✅ მოიძებნა უახლესი მონაცემები: {year} წლის კვარტალი {q_num}")
                    return url
            except requests.RequestException:
                continue
                
    raise Exception("ვერ მოიძებნა Ookla-ს მონაცემების ვალიდური ლინკი.")


def main():
    print("ვიწყებთ მონაცემების განახლების პროცესს...")
    
    # უახლესი Parquet ფაილის ლინკის მიღება
    url = get_latest_ookla_url(network_type="mobile")
    print(f"ლინკი: {url}")
    
    print("მიმდინარეობს საქართველოს მონაცემების ამოჭრა... (ამას შეიძლება 1-2 წუთი დასჭირდეს)")
    # geopandas პირდაპირ კითხულობს Parquet ფაილს ონლაინ და bbox-ის დახმარებით
    # იწერს მხოლოდ იმ ნაწილს, რომელიც საქართველოს ეკუთვნის.
    gdf = gpd.read_parquet(url, bbox=GEORGIA_BBOX)
    
    records_count = len(gdf)
    print(f"📊 ნაპოვნია {records_count} ლოკაცია საქართველოს ტერიტორიაზე.")
    
    if records_count > 0:
        # ვიზუალიზაციისთვის ფაილის წონის შესამცირებლად, შეგვიძლია ზედმეტი სვეტები წავშალოთ
        # ვტოვებთ მხოლოდ: გეომეტრიას, ჩამოტვირთვის და ატვირთვის სიჩქარეებს (Kbps -> Mbps), და ტესტების რაოდენობას
        gdf['avg_d_kbps'] = gdf['avg_d_kbps'] / 1000 # Mbps-ში გადაყვანა
        gdf['avg_u_kbps'] = gdf['avg_u_kbps'] / 1000 
        
        output_file = "data/georgia_mobile.geojson"
        
        # ვინახავთ მონაცემებს
        gdf.to_file(output_file, driver="GeoJSON")
        print(f"✅ ფაილი წარმატებით შეინახა: {output_file}")
    else:
        print("⚠️ საქართველოს ტერიტორიაზე მონაცემები ვერ მოიძებნა.")

if __name__ == "__main__":
    main()
