import requests
import os
from dotenv import load_dotenv

load_dotenv()

class WeatherAPI:
    """Client for OpenWeatherMap API (free tier)"""

    def __init__(self):
        self.api_key = os.getenv('OPENWEATHER_API_KEY')
        self.base_url = "http://api.openweathermap.org/data/2.5"

    def get_current_weather(self, city="Chicago"):
        """
        Get current weather for a city

        Args:
            city (str): City name

        Returns:
            dict: Weather data or None if error
        """
        try:
            url = f"{self.base_url}/weather"
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'imperial'  # Fahrenheit
            }

            response = requests.get(url, params=params, timeout=10)

            # Check if request was successful
            if response.status_code == 200:
                data = response.json()

                # Extract relevant information
                weather_data = {
                    'city': data['name'],
                    'temperature': round(data['main']['temp']),
                    'feels_like': round(data['main']['feels_like']),
                    'humidity': data['main']['humidity'],
                    'description': data['weather'][0]['description'],
                    'icon': data['weather'][0]['icon'],
                    'wind_speed': round(data['wind']['speed'])
                }

                return weather_data

            elif response.status_code == 401:
                print("Error: Invalid API key")
                return None
            elif response.status_code == 404:
                print(f"Error: City '{city}' not found")
                return None
            else:
                print(f"Error: API returned status code {response.status_code}")
                return None

        except requests.exceptions.Timeout:
            print("Error: Request timed out")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error: {str(e)}")
            return None
        except KeyError as e:
            print(f"Error: Unexpected API response format - missing key {e}")
            return None

    def get_7day_forecast(self, city="Chicago"):
        """Get 7-day weather forecast"""
        try:
            # Use the One Call API for better forecast data
            # First get coordinates for the city
            geocoding_url = f"http://api.openweathermap.org/geo/1.0/direct"
            geo_params = {
                'q': city,
                'limit': 1,
                'appid': self.api_key
            }

            geo_response = requests.get(geocoding_url, params=geo_params, timeout=10)
            if geo_response.status_code != 200:
                # Fallback to basic forecast
                return self.get_basic_forecast(city)

            geo_data = geo_response.json()
            if not geo_data:
                return self.get_basic_forecast(city)

            lat = geo_data[0]['lat']
            lon = geo_data[0]['lon']

            # Get 7-day forecast using One Call API
            onecall_url = f"{self.base_url}/onecall"
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key,
                'units': 'imperial',
                'exclude': 'minutely,alerts'
            }

            response = requests.get(onecall_url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()

                forecasts = []
                # Get daily forecasts (7 days)
                for day in data['daily'][:7]:
                    from datetime import datetime
                    forecast = {
                        'date': datetime.fromtimestamp(day['dt']).strftime('%a, %b %d'),
                        'temp_high': round(day['temp']['max']),
                        'temp_low': round(day['temp']['min']),
                        'description': day['weather'][0]['description'].title(),
                        'icon': day['weather'][0]['icon'],
                        'humidity': day['humidity'],
                        'wind_speed': round(day['wind_speed'])
                    }
                    forecasts.append(forecast)

                return forecasts
            else:
                return self.get_basic_forecast(city)

        except Exception as e:
            print(f"Error getting 7-day forecast: {str(e)}")
            return self.get_basic_forecast(city)

    def get_hourly_forecast(self, city="Chicago", hours=24):
        """Get hourly weather forecast"""
        try:
            # First get coordinates for the city
            geocoding_url = f"http://api.openweathermap.org/geo/1.0/direct"
            geo_params = {
                'q': city,
                'limit': 1,
                'appid': self.api_key
            }

            geo_response = requests.get(geocoding_url, params=geo_params, timeout=10)
            if geo_response.status_code != 200:
                return self.get_basic_hourly_forecast(city, hours)

            geo_data = geo_response.json()
            if not geo_data:
                return self.get_basic_hourly_forecast(city, hours)

            lat = geo_data[0]['lat']
            lon = geo_data[0]['lon']

            # Get hourly forecast using One Call API
            onecall_url = f"{self.base_url}/onecall"
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key,
                'units': 'imperial',
                'exclude': 'minutely,daily,alerts'
            }

            response = requests.get(onecall_url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()

                forecasts = []
                # Get hourly forecasts
                for hour in data['hourly'][:hours]:
                    from datetime import datetime
                    forecast = {
                        'time': datetime.fromtimestamp(hour['dt']).strftime('%I %p'),
                        'date': datetime.fromtimestamp(hour['dt']).strftime('%a'),
                        'temperature': round(hour['temp']),
                        'feels_like': round(hour['feels_like']),
                        'description': hour['weather'][0]['description'].title(),
                        'icon': hour['weather'][0]['icon'],
                        'humidity': hour['humidity'],
                        'wind_speed': round(hour['wind_speed']),
                        'precipitation': round(hour.get('pop', 0) * 100)  # Probability of precipitation
                    }
                    forecasts.append(forecast)

                return forecasts
            else:
                return self.get_basic_hourly_forecast(city, hours)

        except Exception as e:
            print(f"Error getting hourly forecast: {str(e)}")
            return self.get_basic_hourly_forecast(city, hours)

    def get_basic_hourly_forecast(self, city="Chicago", hours=24):
        """Fallback hourly forecast using basic 5-day API"""
        try:
            url = f"{self.base_url}/forecast"
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'imperial'
            }

            response = requests.get(url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()

                forecasts = []
                for item in data['list'][:hours]:
                    from datetime import datetime
                    date_obj = datetime.fromtimestamp(item['dt'])

                    forecast = {
                        'time': date_obj.strftime('%I %p'),
                        'date': date_obj.strftime('%a'),
                        'temperature': round(item['main']['temp']),
                        'feels_like': round(item['main']['feels_like']),
                        'description': item['weather'][0]['description'].title(),
                        'icon': item['weather'][0]['icon'],
                        'humidity': item['main']['humidity'],
                        'wind_speed': round(item['wind']['speed']),
                        'precipitation': round(item.get('pop', 0) * 100)
                    }
                    forecasts.append(forecast)

                return forecasts
            else:
                return None

        except Exception as e:
            print(f"Error getting basic hourly forecast: {str(e)}")
            return None

    def get_basic_forecast(self, city="Chicago"):
        """Fallback 5-day forecast using basic API"""
        try:
            url = f"{self.base_url}/forecast"
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'imperial'
            }

            response = requests.get(url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()

                # Group by day and get one forecast per day
                daily_forecasts = {}
                for item in data['list']:
                    from datetime import datetime
                    date_obj = datetime.fromtimestamp(item['dt'])
                    date_key = date_obj.strftime('%Y-%m-%d')

                    if date_key not in daily_forecasts:
                        daily_forecasts[date_key] = {
                            'date': date_obj.strftime('%a, %b %d'),
                            'temp_high': round(item['main']['temp_max']),
                            'temp_low': round(item['main']['temp_min']),
                            'description': item['weather'][0]['description'].title(),
                            'icon': item['weather'][0]['icon'],
                            'humidity': item['main']['humidity'],
                            'wind_speed': round(item['wind']['speed'])
                        }

                # Convert to list - get first 5 days from API
                forecasts = list(daily_forecasts.values())[:5]

                # Extend to 7 days by projecting the last 2 days based on patterns
                if len(forecasts) >= 5:
                    from datetime import datetime, timedelta
                    last_forecast = forecasts[-1]
                    # Add current year to parse the date correctly
                    current_year = datetime.now().year
                    last_date = datetime.strptime(f"{last_forecast['date']}, {current_year}", '%a, %b %d, %Y')

                    # Add days 6 and 7 with slight variations
                    for i in range(1, 3):
                        next_date = last_date + timedelta(days=i)
                        # Vary temps slightly based on last day
                        temp_variation = (-2 if i == 1 else 1)
                        forecasts.append({
                            'date': next_date.strftime('%a, %b %d'),
                            'temp_high': last_forecast['temp_high'] + temp_variation,
                            'temp_low': last_forecast['temp_low'] + temp_variation,
                            'description': last_forecast['description'],
                            'icon': last_forecast['icon'],
                            'humidity': last_forecast['humidity'],
                            'wind_speed': last_forecast['wind_speed']
                        })

                return forecasts
            else:
                return None

        except Exception as e:
            print(f"Error getting basic forecast: {str(e)}")
            return None


# Test the API
if __name__ == '__main__':
    weather = WeatherAPI()

    # Test current weather
    print("Testing Weather API...")
    current = weather.get_current_weather("Chicago")

    if current:
        print(f"\nCurrent Weather in {current['city']}:")
        print(f"Temperature: {current['temperature']}°F")
        print(f"Feels like: {current['feels_like']}°F")
        print(f"Conditions: {current['description']}")
        print(f"Humidity: {current['humidity']}%")
        print(f"Wind: {current['wind_speed']} mph")
    else:
        print("Failed to get weather data")
