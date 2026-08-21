import json
import sys
import pandas as pd

# Function to create a DataFrame from a list of records
def create_dataframe(data_list, columns):
    return pd.DataFrame([{col: item.get(col, '-') for col in columns} for item in data_list])

def convert_json_to_tables(json_file, output_file=None):
    with open(json_file, 'r') as file:
        data = json.load(file)

    # Extract chassis inventory
    chassis_inventory = data.get("inventory", {}).get("chassis", [])
    chassis_columns = [
        "id", "name", "type", "manufacturer", "model", 
        "serial", "sku", "health_status", "operation_status"
    ]
    chassis_df = create_dataframe(chassis_inventory, chassis_columns)

    # Extract fan inventory
    fan_inventory = data.get("inventory", {}).get("fan", [])
    fan_columns = [
        "id", "name", "location", "health_status", 
        "operation_status", "reading", "reading_unit"
    ]
    fan_df = create_dataframe(fan_inventory, fan_columns)

    # Extract firmware inventory
    firmware_inventory = data.get("inventory", {}).get("firmware", [])
    firmware_columns = [
        "id", "name", "location", "version", 
        "health_status", "operation_status", "updateable"
    ]
    firmware_df = create_dataframe(firmware_inventory, firmware_columns)

    # Extract memory inventory
    memory_inventory = data.get("inventory", {}).get("memory", [])
    memory_columns = [
        "id", "name", "type", "base_type", "channel", "slot", 
        "socket", "size", "speed", 
        "health_status", "operation_status", "part_number", 
        "serial", "system_ids"
    ]
    memory_df = create_dataframe(memory_inventory, memory_columns)

    # Extract network adapter inventory
    network_adapter_inventory = data.get("inventory", {}).get("network_adapter", [])
    network_adapter_columns = [
        "id", "name", "firmware", "health_status", 
        "operation_status", "model", "manufacturer", 
        "part_number", "num_ports", "serial"
    ]
    network_adapter_df = create_dataframe(network_adapter_inventory, network_adapter_columns)

    # Extract network port inventory
    network_port_inventory = data.get("inventory", {}).get("network_port", [])
    network_port_columns = [
        "id", "adapter_id", "port_name", "current_speed", 
        "full_duplex", "link_status", "health_status", 
        "operation_status"
    ]
    network_port_df = create_dataframe(network_port_inventory, network_port_columns)

    # Extract power supply inventory
    power_supply_inventory = data.get("inventory", {}).get("power_supply", [])
    power_supply_columns = [
        "id", "name", "bay", "capacity", 
        "health_status", "operation_status", "model", 
        "serial", "firmware", "vendor"
    ]
    power_supply_df = create_dataframe(power_supply_inventory, power_supply_columns)

    # Extract physical drive inventory
    physical_drive_inventory = data.get("inventory", {}).get("physical_drive", [])
    physical_drive_columns = [
        "id", #"name", 
        "model", "serial", 
        "bay", "health_status", 
        "operation_status", 
	"interface_type", 
        "firmware", "size_in_byte", "type", "temperature",
        "power_on_hours",
        "predicted_media_life_left_percent"
    ]
    physical_drive_df = create_dataframe(physical_drive_inventory, physical_drive_columns)
    GB = (1024 ** 3)
    physical_drive_df['size_in_gigabytes'] = (physical_drive_df['size_in_byte'] / (1000 ** 3))
    physical_drive_df['size_in_gigabytes'] = physical_drive_df['size_in_gigabytes'].round(3)
    physical_drive_df.drop(columns='size_in_byte', inplace=True)
    # Remove the column you want to move
    size_col = physical_drive_df.pop('size_in_gigabytes')
    # Insert it at the desired position (0 for first position)
    physical_drive_df.insert(3, 'size_in_gigabytes', size_col)

    # Extract processor inventory
    processor_inventory = data.get("inventory", {}).get("processor", [])
    processor_columns = [
        "id", #"name", 
        "health_status", 
        "operation_status", "manufacturer", "model", 
        "current_speed", #"max_speed", 
        "cores", 
        "threads", "architecture", "socket"
    ]
    processor_df = create_dataframe(processor_inventory, processor_columns)

    # Extract storage controller inventory
    storage_controller_inventory = data.get("inventory", {}).get("storage_controller", [])
    storage_controller_columns = [
        "id", "name", "manufacturer", "model", 
        "health_status", "operation_status", 
        "firmware", "serial", "location", 
        "backup_power_present", "physical_drive_ids"
    ]
    storage_controller_df = create_dataframe(storage_controller_inventory, storage_controller_columns)

    # Extract storage enclosure inventory
    storage_enclosure_inventory = data.get("inventory", {}).get("storage_enclosure", [])
    storage_enclosure_columns = [
        "id", "name", "manufacturer", "model", 
        "firmware", "health_status", "operation_status", 
        "serial", "location", "num_bays"
    ]
    storage_enclosure_df = create_dataframe(storage_enclosure_inventory, storage_enclosure_columns)

    # Extract system information
    system_inventory = data.get("inventory", {}).get("system", [])
    system_columns = [
        "id", "name", "manufacturer", "model", 
        "health_status", "operation_status", "bios_version", 
        "cpu_num", "mem_size", "host_name", 
        "power_state", "serial"
    ]
    system_df = create_dataframe(system_inventory, system_columns)

    # Print the DataFrames
    print("Chassis Inventory:\n", chassis_df.to_string(index=False))
    print("\n\nFan Inventory:\n", fan_df.to_string(index=False))
    print("\n\nFirmware Inventory:\n", firmware_df.to_string(index=False))
    print("\n\nMemory Inventory:\n", memory_df.to_string(index=False))
    print("\n\nNetwork Adapter Inventory:\n", network_adapter_df.to_string(index=False))
    print("\n\nNetwork Port Inventory:\n", network_port_df.to_string(index=False))
    print("\n\nPower Supply Inventory:\n", power_supply_df.to_string(index=False))
    print("\n\nPhysical_drive Inventory:\n", physical_drive_df.to_string(index=False))
    print("\n\nProcessor Inventory:\n", processor_df.to_string(index=False))
    print("\n\nStorage_controller Inventory:\n", storage_controller_df.to_string(index=False))
    print("\n\nSystem Inventory:\n", system_df.to_string(index=False))

def main():
    # Check if the script received the required arguments
    if len(sys.argv) != 2:
        # Prompt user for input
        json_file_path = input("Please provide the path to the JSON file: ")
    else:
        # Retrieve the arguments
        json_file_path = sys.argv[1]

    convert_json_to_tables(json_file_path)

if __name__ == "__main__":
    main()