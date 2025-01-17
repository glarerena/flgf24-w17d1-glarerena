import pandas as pd
import requests
from sklearn.neighbors import KNeighborsRegressor
from datetime import datetime, timedelta, UTC

class WeatherPredictor:
    def __init__(self, api_key):
        self.api_key = api_key
        self.model = KNeighborsRegressor(n_neighbors=2)  # 7 day rolling average 
        
    def fetch_data(self, city):
        """Fetch last 7 days of weather data"""
        records = []
        today = datetime.now(UTC)
        
        # Get last 7 days
        for i in range(7, 0, -1):
            date = today - timedelta(days=i)
            date_str = date.strftime('%Y-%m-%d')
            
            response = requests.get(
                "http://api.weatherapi.com/v1/history.json",
                params={
                    'key': self.api_key,
                    'q': city,
                    'dt': date_str
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                temp = data['forecast']['forecastday'][0]['day']['avgtemp_c']
                records.append({'date': date_str, 'temp': temp})
                print(f"✓ {date_str}: {temp}°C")
            
            # Simple delay between API calls
            from time import sleep
            sleep(1) # 1 second between each api call
            
        return pd.DataFrame(records)
    
    def predict_tomorrow(self, df):
        """Use 3-day rolling average to predict tomorrow"""
        if len(df) < 3:
            return None
            
        df['rolling_avg'] = df['temp'].rolling(3).mean()
        latest_avg = df['rolling_avg'].iloc[-1]
        latest_temp = df['temp'].iloc[-1]
        
        # Simple weighted average between last temp and rolling average
        prediction = (latest_temp * 0.7) + (latest_avg * 0.3)
        return round(prediction, 1)

def main():
    API_KEY = "c513808fb9f94271b05233618251401"
    CITY = "Danville, VA"
    
    predictor = WeatherPredictor(API_KEY)
    
    print("Fetching last 7 days of weather data...")
    df = predictor.fetch_data(CITY)
    
    if not df.empty:
        prediction = predictor.predict_tomorrow(df)
        print(f"\nCurrent temperature: {df['temp'].iloc[-1]}°C")
        print(f"3-day average: {df['temp'].rolling(3).mean().iloc[-1]:.1f}°C")
        print(f"Prediction for tomorrow: {prediction}°C")

if __name__ == "__main__":
    main()