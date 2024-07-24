#!/usr/bin/env python3
import subprocess, argparse, os, json
from typing import Dict, List

def read_config(file_path: str) -> Dict:
    config = {}
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith("#"):
                key, value = line.split("=", 1)
                config[key.strip()] = value.strip()
    return config

CONFIG = read_config(os.path.expanduser("~/.config/eww/bar/bar.conf"))
RUN_EWW = f"eww -c {CONFIG.get('CONFIG_FILE_LOCATION')}"
WIDGET_DEFAULT_WIDTH = 400
BATTERY_WIDGET_WIDTH = int(CONFIG.get("BATTERY_WIDGET_WIDTH_PX", WIDGET_DEFAULT_WIDTH))
NETWORK_WIDGET_WIDTH = int(CONFIG.get("NETWORK_WIDGET_WIDTH_PX", WIDGET_DEFAULT_WIDTH))
BAR_WIDTH_PERCENTAGE = int(CONFIG.get("BAR_WIDTH", 100))

def get_scaled_resolution(executed_command: str) -> List[int]:
    output = subprocess.check_output(executed_command, shell=True, text=True)
    results = json.loads(output)
    monitor_scale = results["scale"]
    return [results["width"] / monitor_scale, results["height"] / monitor_scale]

def get_battery_coordinates() -> int:
    x_res = get_scaled_resolution("hyprctl monitors -j | jq '.[0] | {width, height, scale}'")[0]
    return int(x_res - (x_res * (100 - BAR_WIDTH_PERCENTAGE) / 200) - BATTERY_WIDGET_WIDTH)

def get_main_bar_width() -> int:
    x_res = get_scaled_resolution("hyprctl monitors -j | jq '.[0] | {width, height, scale}'")[0]
    return int(x_res * int(CONFIG.get("BAR_WIDTH", 50)) / 100)

open_widgets = {
    "mainbar": f"{RUN_EWW} open mainbar --screen 0 --arg width={get_main_bar_width()}",
    "calendar": f"{RUN_EWW} open calendar",
    "powerManager": f"{RUN_EWW} open powerManager --arg x_cor={get_battery_coordinates()} --arg width={BATTERY_WIDGET_WIDTH}",
    "networkManager": f"{RUN_EWW} open networkManager --arg x_cor={get_battery_coordinates()} --arg width={NETWORK_WIDGET_WIDTH}",
    "monitorManager": f"{RUN_EWW} open monitorManager --arg x_cor={get_battery_coordinates()} --arg width={NETWORK_WIDGET_WIDTH}",
}

def toggle_window(window: str) -> None:
    try:
        subprocess.run(f"{RUN_EWW} close {window}", shell=True, check=True)
    except subprocess.CalledProcessError:
        subprocess.run(open_widgets[window], shell=True, check=True)

def main():
    parser = argparse.ArgumentParser(description="Open a specific bar using a use flag")
    window_list = ["mainbar", "calendar", "powerManager", "networkManager", "monitorManager"]
    for widget in window_list:
        parser.add_argument(f"--{widget}", action="store_true", help=f"toggle {widget}")
    args = parser.parse_args()
    
    for widget in window_list:
        if getattr(args, widget):
            toggle_window(widget)
            break
    else:
        print("Please provide a valid flag: --mainbar, --calendar, --powerManager, or --networkManager")

if __name__ == "__main__":
    main()
