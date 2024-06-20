import subprocess
import argparse
import json
from typing import List

BATTERY_WIDTH = 240

def get_monitor_resolution() -> List[int]:
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
    monitor_resolution = get_monitor_resolution()
    x_coordinate = int(monitor_resolution[0] - (monitor_resolution[0] * 0.6 / 2) - BATTERY_WIDTH)
    return x_coordinate

def get_main_bar_width() -> int:
    monitor_resolution = get_monitor_resolution()
    bar_width = int(monitor_resolution[0] * 0.4)
    return bar_width
