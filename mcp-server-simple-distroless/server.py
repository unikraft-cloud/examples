"""Simple Custom Weather MCP Server using FastMCP."""

from datetime import datetime
import random
import pytz
from fastmcp import FastMCP

# Simulated weather data
WEATHER_DATA = {
    'London': {'temp_range': (10, 20), 'conditions': ['Rainy', 'Cloudy', 'Partly cloudy']},
    'New York': {'temp_range': (15, 25), 'conditions': ['Sunny', 'Cloudy', 'Clear']},
    'Tokyo': {'temp_range': (18, 28), 'conditions': ['Humid', 'Partly cloudy', 'Clear']},
    'Paris': {'temp_range': (12, 22), 'conditions': ['Cloudy', 'Rainy', 'Partly cloudy']},
    'Berlin': {'temp_range': (8, 18), 'conditions': ['Cloudy', 'Rainy', 'Clear']},
}

mcp = FastMCP("Simple Weather MCP Server")


@mcp.tool()
def get_weather(city: str) -> str:
    """Get current weather for a city.

    Args:
        city: Name of the city

    Returns:
        Weather information including temperature, conditions, and humidity
    """
    # Get city data or use default
    city_data = WEATHER_DATA.get(city, {
        'temp_range': (15, 25),
        'conditions': ['Partly cloudy', 'Clear', 'Cloudy']
    })

    # Generate random weather
    temp = random.randint(*city_data['temp_range'])
    conditions = random.choice(city_data['conditions'])
    humidity = random.randint(40, 80)

    result = f"""Weather for {city}:
Temperature: {temp}°C
Conditions: {conditions}
Humidity: {humidity}%
Timestamp: {datetime.utcnow().isoformat()}"""

    return result


@mcp.tool()
def get_time(timezone: str) -> str:
    """Get current time in a timezone.

    Args:
        timezone: IANA timezone (e.g., America/New_York, Europe/London)

    Returns:
        Current time, date, day, and UTC offset for the specified timezone
    """
    try:
        tz = pytz.timezone(timezone)
        current_time = datetime.now(tz)

        result = f"""Time in {timezone}:
Time: {current_time.strftime('%H:%M:%S')}
Date: {current_time.strftime('%Y-%m-%d')}
Day: {current_time.strftime('%A')}
UTC Offset: {current_time.strftime('%z')}"""

        return result
    except pytz.exceptions.UnknownTimeZoneError:
        return f"Error: Unknown timezone {timezone}"


@mcp.tool()
def calculate(operation: str, a: float, b: float) -> str:
    """Perform a simple calculation.

    Args:
        operation: Mathematical operation (add, subtract, multiply, divide)
        a: First operand
        b: Second operand

    Returns:
        Result of the calculation
    """
    if operation == 'add':
        result = a + b
    elif operation == 'subtract':
        result = a - b
    elif operation == 'multiply':
        result = a * b
    elif operation == 'divide':
        if b == 0:
            return "Error: Division by zero"
        result = a / b
    else:
        return f"Error: Unknown operation {operation}"

    return f"{a} {operation} {b} = {result}"


if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8080, path="/mcp")
