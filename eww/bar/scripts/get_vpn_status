#!/usr/bin/env lua

local function execute_command(cmd)
	local handle = io.popen(cmd)
	local result = handle:read("*a")
	handle:close()
	return result
end

local function check_openvpn()
	local result = execute_command("pgrep -a openvpn")
	return result ~= ""
end

local function check_wireguard()
	local result = execute_command("ip -br link show type wireguard")
	return result ~= ""
end

local function main()
	local openvpn_connected = check_openvpn()
	local wireguard_connected = check_wireguard()

	if openvpn_connected then
		print("OpenVPN")
	elseif wireguard_connected then
		print("WireGuard")
	else
		print("No VPN")
	end

	return openvpn_connected or wireguard_connected
end

main()
