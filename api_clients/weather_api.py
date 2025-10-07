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

    def get_5day_forecast(self, city="Chicago"):
        """Get 5-day forecast"""
        try:
            url = f"{self.base_url}/forecast"
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'imperial',
                'cnt': 5  # Number of timestamps
            }

            response = requests.get(url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()

                # Extract daily forecasts
                forecasts = []
                for item in data['list']:
                    forecast = {
                        'date': item['dt_txt'],
                        'temp': round(item['main']['temp']),
                        'description': item['weather'][0]['description']
                    }
                    forecasts.append(forecast)

                return forecasts
            else:
                return None

        except Exception as e:
            print(f"Error getting forecast: {str(e)}")
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
