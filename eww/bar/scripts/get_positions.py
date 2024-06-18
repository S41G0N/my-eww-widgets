import subprocess
import argparse
from typing import List

WIDGET_HEIGHT = 100
WIDGET_Y_OFFSET = 10
CALENDAR_WIDTH = 300
BATTERY_WIDTH = 240
WIDGET_WIDTH_PERCENTAGE=60


def get_monitor_resolution() -> List[int]:
    # Define the shell command with properly escaped backslashes
    command = "hyprctl monitors | grep -oP '\\d+x\\d+(?=@)' | head -n 1"
    # Execute the command using subprocess.Popen
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()
    output = stdout.strip()

    x_res = int(output.split('x')[0])
    y_res = int(output.split('x')[-1])
    return [x_res, y_res]

def get_calendar_coordinates(monitor_resolution) -> None:
    monitor_width = monitor_resolution[0]
    calendar_x_coordinate = int(monitor_width/2 - CALENDAR_WIDTH/2)
    print(calendar_x_coordinate)

def get_battery_coordinates(monitor_resolution) -> None:
    monitor_width = monitor_resolution[0]
    percentage_to_pixels = monitor_width/100
    x_coordinate = (monitor_width - ((100-WIDGET_WIDTH_PERCENTAGE) / 2 * percentage_to_pixels) - BATTERY_WIDTH/2)
    print(x_coordinate)

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Extract resolution details.")
    parser.add_argument('--calendar_coordinates', action='store_true', help="get X/Y coordinates of calendar")
    parser.add_argument('--battery_coordinates', action='store_true', help="get X/Y coordinates of battery")
    args = parser.parse_args()

    monitor_resolution = get_monitor_resolution()

    if args.calendar_coordinates:
        get_calendar_coordinates(monitor_resolution)

    elif args.battery_coordinates:
        get_battery_coordinates(monitor_resolution)
    else:
        print("Please provide a valid flag: --calendar_coordinates or --battery_coordinates")

if __name__ == "__main__":
    main()
