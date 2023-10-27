import ipaddress

# Define the parent subnet (10.0.0.0/8)
parent_subnet = ipaddress.IPv4Network('10.0.0.0/8')

# Calculate the subnet prefix length (/28)
subnet_prefix_length = 28

# Calculate the number of subnets to create
num_subnets = 200

# Calculate the size of each subnet
subnet_size = 2 ** (32 - subnet_prefix_length)

# Open a file for writing the configuration
with open("dhcp_config.txt", "w") as config_file:
    # Write the initial configuration
    config_file.write("configure terminal\n")


    # Check if there are enough addresses in the parent subnet
    if num_subnets * subnet_size > parent_subnet.num_addresses:
        print("Error: Not enough addresses in the parent subnet to create 200 /28 subnets.")
    else:
        subnets = list(parent_subnet.subnets(new_prefix=subnet_prefix_length))

        for i, subnet in enumerate(subnets[:num_subnets]):
            vlan_name = f"VLAN{i+2}"
            vlan_network = str(subnet.network_address)
            vlan_default = str(subnet.network_address + 2)
            vlan_ip_start = str(subnet.network_address + 3)
            vlan_ip_end = str(subnet.network_address + 14)

            config_file.write(f"echo subnet={vlan_network} netmask = 255.255.255.240 '{{' >> /etc/dhcpd.conf \n")
            config_file.write(f"echo \"    range dynamic-bootp {vlan_ip_start} {vlan_ip_end};\" >> /etc/dhcpd.conf\n")
            config_file.write(f"echo \"    option routers {vlan_default};\" >> /etc/dhcpd.conf\n")
            config_file.write("echo } >> /etc/dhcpd.conf\n")


print("Configuration file generated: dhcp_config.txt")
