#!/bin/bash

# Define the output file name
output_file="create_vlans.txt"

# Define the base network and subnet mask
base_network="10.0.0.0"
subnet_mask="255.255.255.240"

# Function to generate VLAN commands
generate_vlan_commands() {
  for vlan_id in {2..201}; do
    # Calculate the VLAN subnet
    subnet=$(printf "%d.%d.%d.%d" "$((vlan_id / 256 / 256 / 256 % 256))" "$((vlan_id / 256 / 256 % 256))" "$((vlan_id / 256 % 256))" "$((vlan_id % 256))")

    echo "vlan $vlan_id"
    echo "name VLAN_$vlan_id"
    echo "!"
    echo "interface Vlan$vlan_id"
    echo "ip address $subnet $subnet_mask"
    echo "no shutdown"
    echo "!"
  done
}

# Generate VLAN commands and write to the output file
generate_vlan_commands > "$output_file"

echo "VLAN commands have been written to $output_file."
