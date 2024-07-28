local function getPowerConsumption()
	local handle = io.popen("upower -i $(upower -e | grep BAT) | grep 'energy-rate' | awk '{print $2}'")
	local result = handle:read("*a")
	handle:close()

	-- Remove any trailing whitespace or newline characters
	result = result:gsub("%s+", "")

	-- Convert the result to a number
    local power = math.floor(tonumber(result) + 0.5)

	if power then
		return power
	else
		return nil, "Failed to get power consumption"
	end
end

local power = getPowerConsumption()
if power then
	print(power)
else
	print("Error: Unable to retrieve power consumption")
end
