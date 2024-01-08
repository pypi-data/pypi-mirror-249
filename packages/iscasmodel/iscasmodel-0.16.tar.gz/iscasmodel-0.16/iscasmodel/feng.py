from datetime import datetime, timedelta


def calculate_hexagram_with_hour(year, month, day, hour):
    """
    A method to map a date and hour to one of the 64 hexagrams.
    We sum the year, month, day, and hour, and then use modulo 64 to map it to a hexagram.
    Hexagrams are numbered from 1 to 64, so we add 1 after modulo operation.
    """
    return (year + month + day + hour) % 64 + 1

def find_feng_hours(year):
    """
    Find all hours in the given year when the hexagram is Feng (Hexagram 55).
    Feng (Abundance) is hexagram number 55 in I Ching.
    """
    feng_hours = []
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31)
    day_delta = timedelta(days=1)

    while start_date <= end_date:
        for hour in range(24):  # Check each hour of the day
            hexagram = calculate_hexagram_with_hour(start_date.year, start_date.month, start_date.day, hour)
            if hexagram == 55:  # Feng hexagram
                feng_hours.append(start_date.strftime("%Y-%m-%d") + f" {hour}:00")
        start_date += day_delta

    return feng_hours

# Calculate Feng hexagram hours for the year 2024
feng_hours_2024 = find_feng_hours(2024)
print(feng_hours_2024)
feng_hours_2024[:10]  # Display the first 10 hours as a sample

