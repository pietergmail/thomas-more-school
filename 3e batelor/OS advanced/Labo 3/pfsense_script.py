# Open a file for writing the configuration
with open("pfsense_vlans.txt", "w") as config_file:
    # Write the initial configuration
    config_file.write(f"1\n")
    config_file.write(f"y\n")
    for i in range(0, 200):
        config_file.write("vmx1\n")
        config_file.write(f"{i+2}\n")

    config_file.write("\n")

print("Configuration file generated: pfsense_vlans.txt")