-- Load eww configuration from user's home directory
local RUN_EWW = "eww -c " .. os.getenv("HOME") .. "/.config/eww/dock"

local function close_dock()
	return os.execute(RUN_EWW .. " close dock")
end

local function open_dock(height)
	return os.execute(RUN_EWW .. " open dock --arg height=" .. height)
end

local function mainbar_is_active()
	local command = "eww -c " .. os.getenv("HOME") .. "/.config/eww/bar active-windows"
	local handle = io.popen(command)
	local result = ""

	if handle ~= nil then
		result = handle:read("*a")
		handle:close()
	end

	return result:find("mainbar") ~= nil
end

local failed = 0

-- Attempt to close the dock, and if it fails, open it
if close_dock() ~= failed then
	if mainbar_is_active() then
		open_dock(1330)
	else
		open_dock(1280)
	end
end
