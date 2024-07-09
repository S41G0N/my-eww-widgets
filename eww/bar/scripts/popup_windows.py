#!/usr/bin/env python3

import subprocess
import argparse
import os
from typing import Dict, List
import json

#Reads config file
def read_config(file_path: str) -> Dict:
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


CONFIG = read_config(os.path.expanduser("~/.config/eww/bar/bar.conf"))
RUN_EWW = f"eww -c {CONFIG.get("CONFIG_FILE_LOCATION")}"
WIDGET_DEFAULT_WIDTH = 400;
BATTERY_WIDGET_WIDTH = int(CONFIG.get("BATTERY_WIDGET_WIDTH_PX", WIDGET_DEFAULT_WIDTH))
NETWORK_WIDGET_WIDTH = int(CONFIG.get("NETWORK_WIDGET_WIDTH_PX", WIDGET_DEFAULT_WIDTH))
BAR_WIDTH_PERCENTAGE = int(CONFIG.get("BAR_WIDTH", 100))

#Return scaled resolution based on current screen information
def get_scaled_resolution(executed_comamand: str) -> List[int]:
    process = subprocess.Popen(executed_comamand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()
    output = stdout.strip()
    results = json.loads(output)
    monitor_scale = results["scale"]
    x_res = results["width"] / monitor_scale
    y_res = results["height"] / monitor_scale
    return [x_res, y_res]


def get_battery_coordinates() -> int:
    monitor_resolution = get_scaled_resolution("hyprctl monitors -j | jq '.[0] | {width, height, scale}'")
    x_coordinate = int(monitor_resolution[0] - (monitor_resolution[0] * (100 - BAR_WIDTH_PERCENTAGE) / 200) - BATTERY_WIDGET_WIDTH)
    return x_coordinate


def get_main_bar_width() -> int:
    monitor_resolution = get_scaled_resolution("hyprctl monitors -j | jq '.[0] | {width, height, scale}'")
    bar_width_percentage = int(CONFIG.get("BAR_WIDTH", 50)) / 100
    bar_width = int(monitor_resolution[0] * bar_width_percentage)
    return bar_width


open_widgets = {
    "mainbar": f"{RUN_EWW} open mainbar --screen 0 --arg width={get_main_bar_width()}",
    "calendar": f"{RUN_EWW} open calendar",
    "powerManager": f"{RUN_EWW} open powerManager --arg x_cor={get_battery_coordinates()} --arg width={BATTERY_WIDGET_WIDTH}",
    "networkManager": f"{RUN_EWW} open networkManager --arg x_cor={get_battery_coordinates()} --arg width={NETWORK_WIDGET_WIDTH}",
}


def toggle_window(window: str) -> None:
    try:
        subprocess.run(f"{RUN_EWW} close {window}", shell=True, check=True)

    except subprocess.CalledProcessError:
        subprocess.run(open_widgets[window], shell=True, check=True)


#Toggle windows based on parsed flags
def main():
    parser = argparse.ArgumentParser(description="Open a specific bar using a use flag")
    window_list = ["mainbar", "calendar", "powerManager", "networkManager"]

    for widget in window_list:
        parser.add_argument(f"--{widget}", action="store_true", help=f"toggle {widget}")
    args = parser.parse_args()

    for widget in window_list:
        if getattr(args, widget):
            toggle_window(widget)
            break
    else:
        print("Please provide a valid flag: --mainbar, --calendar, --powerManager etc..")

if __name__ == "__main__":
    main()
