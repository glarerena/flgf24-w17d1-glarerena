import pandas as pd
import requests
from datetime import datetime, timedelta, UTC
import time

def collect_historical_data(api_key, city="Danville, VA", months=6):
    """Collect historical weather data and save to CSV"""
    records = []
    end_date = datetime.now(UTC)
    start_date = end_date - timedelta(days=30 * months)
    current_date = start_date

    print(f"Collecting {months} months of weather data for {city}...")
    
    while current_date <= end_date:
        date_str = current_date.strftime('%Y-%m-%d')
        
        try:
            response = requests.get(
                "http://api.weatherapi.com/v1/history.json",
                params={
                    'key': api_key,
                    'q': city,
                    'dt': date_str
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                day_data = data['forecast']['forecastday'][0]['day']
                
                records.append({
                    'date': date_str,
                    'temp_c': day_data['avgtemp_c'],
                    'temp_f': day_data['avgtemp_f'],
                    'max_temp_f': day_data['maxtemp_f'],
                    'min_temp_f': day_data['mintemp_f'],
                    'humidity': day_data['avghumidity'],
                    'rain_mm': day_data['totalprecip_mm'],
                    'rain_in': day_data['totalprecip_in']
                })
            else:
                print(f"Error on {date_str}: {response.text}")
                
            # Respect API rate limits
            time.sleep(1)
            
        except Exception as e:
            print(f"Error on {date_str}: {str(e)}")
        
        current_date += timedelta(days=1)
    
    # Save to CSV
    df = pd.DataFrame(records)
    filename = f"danville_weather_{datetime.now().strftime('%Y%m%d')}.csv"
    df.to_csv(filename, index=False)
    print(f"Data collection complete! Saved {len(records)} days of data to {filename}")
    
    return df

def main():
    API_KEY = "c513808fb9f94271b05233618251401"
    df = collect_historical_data(API_KEY)
    
    # Display concise statistics
    print("\nSummary of Collected Data:")
    print(f"- Date Range: {df['date'].min()} to {df['date'].max()}")
    print(f"- Average Temperature: {df['temp_f'].mean():.1f}°F")
    print(f"- Max Temperature: {df['max_temp_f'].max():.1f}°F")
    print(f"- Min Temperature: {df['min_temp_f'].min():.1f}°F")
    print(f"- Average Humidity: {df['humidity'].mean():.1f}%")
    print(f"- Average Rainfall: {df['rain_in'].mean():.2f} inches")

if __name__ == "__main__":
    main()
