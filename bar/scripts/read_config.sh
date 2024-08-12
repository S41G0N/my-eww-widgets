#!/bin/bash

# Function to read a variable from the config file
read_config_var() {
    local var_name="$1"
    local config_file="bar.conf"
    
    if [ ! -f "$config_file" ]; then
        echo "Error: Config file '$config_file' not found." >&2
        exit 1
    fi

    local value
    value=$(grep "^$var_name=" "$config_file" | cut -d'=' -f2)
    
    if [ -z "$value" ]; then
        echo "Error: Variable '$var_name' not found in $config_file." >&2
        exit 1
    fi
    
    echo "$value"
}

# Check if a variable name was provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 VARIABLE_NAME" >&2
    exit 1
fi

# Read and output the requested variable
read_config_var "$1"
