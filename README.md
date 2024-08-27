# my-eww-widgets
A collection of custom widgets in [eww](https://github.com/elkowar/eww). Feel free to use them and modify them according to your wishes.

## Widgets
### BAR
A custom bar which provides simple workspace manager, displays time and provides the ability to set display brightness, speakers and microphone volume and input sensitivity.
It also tracks many more things such as disk space, memory usage and battery.

![Main Bar](img/demo_bar.gif)
### DOCK
A custom dock which displays the most commonly used apps, buttons are clickable and will launch the selected applications.

## Project Prerequisites & Setup
These are the prerequisites used by the essential scripts, make sure to install them to make the widgets work properly:
- **Hyprland**: A tiling window manager this widget was designed for
- **Hyprlang**: Hyprlang should be included by default when Hyprland is installed
- **eww**: The ElKowar's Wacky Widgets.
- **jq**: A lightweight and flexible command-line JSON processor
- **socat**: Multipurpose relay (SOcket CAT).
- **pipewire**: A server and user space API to handle multimedia pipelines.
- **wireplumber**: A modular session and policy manager for PipeWire.
- **system76-power**: A system76 power management tool
- **lua**: The Lua programming language
- **luajson**: A JSON parser/encoder for Lua
- **lua-cjson**: A fast JSON encoding/parsing module for Lua
- **luasocket**: Network support for the Lua language

Ensure you have these tools installed on your system to proceed with the setup and usage of this project.
## Installation Instructions
1. Clone this repository:
   ```sh
   git clone https://github.com/S41G0N/my-eww-widgets.git
   cd my-eww-widgets
   ```
2. Install the required dependencies. The exact commands depend on your Linux distribution
3. Copy the widget files to your eww configuration directory using the following script:
   ```sh
   ./install_widgets
   ```
4. Update your Hyprland configuration to start eww with these widgets. Add the following to your Hyprland config file:
   ```sh
   exec-once = ~/.config/eww/bar/scripts/toggle_mainbar
   ```
5. Restart Hyprland or log out and log back in to apply the changes.

