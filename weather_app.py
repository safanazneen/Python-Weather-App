
import json
from urllib.request import urlopen, Request
from urllib.parse import urlencode
from urllib.error import URLError


def get_data(url, params):
    full_url = url + "?" + urlencode(params)
    request = Request(
        full_url,
        headers={"User-Agent": "PythonWeatherApp"}
    )

    with urlopen(request, timeout=15) as response:
        return json.loads(response.read().decode("utf-8"))


def main():
    print("=" * 30)
    print("      PYTHON WEATHER APP")
    print("=" * 30)

    city = input("Enter your city name: ").strip()

    if not city:
        print("Please enter a city name.")
        return

    try:
        location = get_data(
            "https://geocoding-api.open-meteo.com/v1/search",
            {"name": city, "count": 1, "language": "en"}
        )

        if not location.get("results"):
            print("City not found. Check the spelling.")
            return

        place = location["results"][0]

        weather = get_data(
            "https://api.open-meteo.com/v1/forecast",
            {
                "latitude": place["latitude"],
                "longitude": place["longitude"],
                "current": (
                    "temperature_2m,"
                    "relative_humidity_2m,"
                    "wind_speed_10m"
                ),
                "timezone": "auto"
            }
        )

        current = weather["current"]

        print("\n===== WEATHER REPORT =====")
        print("City:", place["name"])
        print("Country:", place.get("country", "Unknown"))
        print("Temperature:", current["temperature_2m"], "°C")
        print("Humidity:", current["relative_humidity_2m"], "%")
        print("Wind Speed:", current["wind_speed_10m"], "km/h")
        print("==========================")

    except (URLError, TimeoutError, OSError) as error:
        print("Could not connect to the weather service.")
        print("Check your internet connection.", error)

    except (KeyError, ValueError, TypeError):
        print("Could not process the weather data. Try again.")


if __name__ == "__main__":
    main()
