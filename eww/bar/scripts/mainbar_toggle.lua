#!/usr/bin/env lua

local json = require("cjson") -- You might need to install luajson

local function read_config(file_path)
	local config = {}
	local file = io.open(file_path, "r")

	if not file then
		return nil, "Failed to open file"
	end

	for line in file:lines() do
		-- Remove leading/trailing whitespace
		line = line:match("^%s*(.-)%s*$")

		-- Check if line is not empty and doesn't start with #
		if line ~= "" and line:sub(1, 1) ~= "#" then
			local key, value = line:match("([^=]+)=(.+)")
			if key and value then
				-- Remove leading/trailing whitespace from key and value
				key = key:match("^%s*(.-)%s*$")
				value = value:match("^%s*(.-)%s*$")
				config[key] = value
			end
		end
	end

	file:close()
	return config
end

-- Load eww configuration from user's home directory
local HOME_DIRECTORY = os.getenv("HOME")
local RUN_EWW = "eww -c " .. HOME_DIRECTORY .. "/.config/eww/bar"
local CONFIG_FILE = read_config(HOME_DIRECTORY .. "/.config/eww/bar/bar.conf")


local function get_scaled_resolution(executed_command)
	local handle = io.popen(executed_command)
	local output = handle:read("*a")
	handle:close()

	local results = json.decode(output)
	local monitor_scale = results.scale
	return { results.width / monitor_scale, results.height / monitor_scale }
end

local function get_main_bar_width()
	local x_res = get_scaled_resolution("hyprctl monitors -j | jq '.[0] | {width, height, scale}'")[1]
	return math.floor(x_res * (tonumber(CONFIG_FILE["BAR_WIDTH"]) or 50) / 100)
end

local function close_window()
	return os.execute(RUN_EWW .. " close mainbar")
end

local function open_window(width)
	return os.execute(RUN_EWW .. " open mainbar --arg width=" .. width)
end

local failed = 0

-- Attempt to close the dock, and if it fails, open it
if close_window() ~= failed then
    local mainbar_width = get_main_bar_width()
	open_window(mainbar_width)
end
