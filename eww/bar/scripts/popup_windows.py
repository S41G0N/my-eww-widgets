import subprocess
import argparse
import os
from typing import List
import json

def read_config(file_path):
    config = {}
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            # Ignore empty lines and comments
            if not line or line.startswith("#"):
                continue
            # Split the line into key and value
            key, value = line.split("=", 1)
            config[key.strip()] = value.strip()
    return config


eww = "eww -c ~/.config/eww/bar"
CONFIG = read_config(os.path.expanduser("~/.config/eww/bar/bar.conf"))
BATTERY_WIDTH = int(CONFIG.get("BATTERY_WIDGET_WIDTH_PX", 400))


def get_scaled_resolution() -> List[int]:
    monitor_info = "hyprctl monitors -j | jq '.[0] | {width, height, scale}'"
    # Execute the command using subprocess.Popen
    process = subprocess.Popen(
        monitor_info,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    stdout, stderr = process.communicate()
    output = stdout.strip()
    results = json.loads(output)
    monitor_scale = results["scale"]
    x_res = results["width"] / monitor_scale
    y_res = results["height"] / monitor_scale
    return [x_res, y_res]


def get_battery_coordinates() -> int:
    monitor_resolution = get_scaled_resolution()
    x_coordinate = int(
        monitor_resolution[0] - (monitor_resolution[0] * 0.6 / 2) - BATTERY_WIDTH
    )
    return x_coordinate


def get_main_bar_width() -> int:
    monitor_resolution = get_scaled_resolution()
    bar_width_percentage = int(CONFIG.get("BAR_WIDTH", 50)) / 100
    bar_width = int(monitor_resolution[0] * bar_width_percentage)
    return bar_width


open_widgets = {
    "calendar": f"{eww} update day='`scripts/time_info --day`' && {eww} update month='`scripts/time_info --month`' && {eww} update year='`scripts/time_info --year`' && {eww} open calendar",
    "powerManager": f"{eww} open powerManager --arg x_cor={get_battery_coordinates()} --arg width={BATTERY_WIDTH}",
    "mainbar": f"{eww} open mainbar --screen 0 --arg width={get_main_bar_width()}",
}


def toggle_window(window: str) -> None:
    close_window = f"{eww} close {window}"
    open_window = open_widgets[window]
    try:
        process = subprocess.run(
            close_window,
            shell=True,
            check=True,
        )
    except subprocess.CalledProcessError:
        process = subprocess.run(
            open_window,
            shell=True,
            check=True,
        )


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Open a specific bar using a use flag")
    parser.add_argument(
        "--mainbar",
        action="store_true",
        help="toggle main bar",
    )
    parser.add_argument(
        "--calendar",
        action="store_true",
        help="toggle calendar",
    )
    parser.add_argument(
        "--powerManager",
        action="store_true",
        help="toggle calendar",
    )
    args = parser.parse_args()

    if args.mainbar:
        toggle_window("mainbar")

    elif args.calendar:
        toggle_window("calendar")

    elif args.powerManager:
        toggle_window("powerManager")

    else:
        print("Please provide a valid flag: --mainbar, --calendar, --powerManager")


if __name__ == "__main__":
    main()
