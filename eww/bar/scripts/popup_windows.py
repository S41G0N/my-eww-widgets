import subprocess
import argparse
from get_positions import get_main_bar_width, get_battery_coordinates

eww = "eww -c ~/.config/eww/bar"

open_widgets = {
    "calendar": f"{eww} update day='`scripts/time_info --day`' && {eww} update month='`scripts/time_info --month`' && {eww} update year='`scripts/time_info --year`' && {eww} open calendar",
    "powerManager": f"{eww} open powerManager --arg x_cor={get_battery_coordinates()}",
    "mainbar": f"{eww} open mainbar --screen 0 --arg width={get_main_bar_width()}",
}


def toggle_window(window) -> None:
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
