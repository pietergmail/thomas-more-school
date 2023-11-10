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
with open("opensuse-vlan.txt", "w") as config_file:

    # Check if there are enough addresses in the parent subnet
    if num_subnets * subnet_size > parent_subnet.num_addresses:
        print("Error: Not enough addresses in the parent subnet to create 200 /28 subnets.")
    else:
        subnets = list(parent_subnet.subnets(new_prefix=subnet_prefix_length))

        for i, subnet in enumerate(subnets[:num_subnets]):
            outputfile = f"ifcfg-vlan{i+2}"
            vlan_network = str(subnet.network_address)
            vlan_ip = str(subnet.network_address + 2)

            config_file.write(f"echo IPADDR=\\'{vlan_ip}\\' >> {outputfile} \n")
            config_file.write(f"echo BOOTPROTO=\\'static\\' >> {outputfile} \n")
            config_file.write(f"echo STARTMODE=\\'hotplug\\' >> {outputfile} \n")
            config_file.write(f"echo NETMASK=\\'255.255.255.240\\' >> {outputfile} \n")
            config_file.write(f"echo ZONE=public >> {outputfile} \n")
            config_file.write(f"echo VLAN=\\'yes\\' >> {outputfile} \n")
            config_file.write(f"echo ETHERDEVICE=\\'eth0\\' >> {outputfile} \n")

print("Configuration file generated: opensuse-vlan.txt")
