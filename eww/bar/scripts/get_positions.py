import subprocess
import argparse
import json
from typing import List

WIDGET_HEIGHT = 100
WIDGET_Y_OFFSET = 10
CALENDAR_WIDTH = 300
BATTERY_WIDTH = 240
WIDGET_WIDTH_PERCENTAGE=60


def get_monitor_resolution() -> List[int]:
    monitor_info = "hyprctl monitors -j | jq '.[0] | {width, height, scale}'"
    # Execute the command using subprocess.Popen
    process = subprocess.Popen(monitor_info, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()
    output = stdout.strip()
    results = json.loads(output)
    monitor_scale = results["scale"]
    x_res = results["width"] / monitor_scale
    y_res = results["height"] / monitor_scale
    return [x_res, y_res, results["width"]]

def get_calendar_coordinates() -> None:
    monitor_resolution = get_monitor_resolution()
    monitor_width = monitor_resolution[0]
    calendar_x_coordinate = int(monitor_width/2 - CALENDAR_WIDTH/2)
    print(calendar_x_coordinate)

def get_battery_coordinates() -> None:
    monitor_resolution = get_monitor_resolution()
    x_coordinate = (monitor_resolution[0] - (monitor_resolution[0] * 0.6/2) - BATTERY_WIDTH)
    print(x_coordinate)

def get_main_bar_width() -> None:
    monitor_resolution = get_monitor_resolution()
    bar_width = int(monitor_resolution[0] * 0.4)
    print(bar_width)

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Extract resolution details.")
    parser.add_argument('--calendar_coordinates', action='store_true', help="get X/Y coordinates of calendar")
    parser.add_argument('--battery_coordinates', action='store_true', help="get X/Y coordinates of battery")
    parser.add_argument('--main_bar_width', action='store_true', help="get the width of the main bar in pixels")
    args = parser.parse_args()

    if args.calendar_coordinates:
        get_calendar_coordinates()

    elif args.battery_coordinates:
        get_battery_coordinates()

    elif args.main_bar_width:
        get_main_bar_width()

    else:
        print("Please provide a valid flag: --calendar_coordinates or --battery_coordinates")

if __name__ == "__main__":
    main()
