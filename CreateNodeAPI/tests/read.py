import json

# Path to the JSON file
path = r"C:\Users\liewg\Desktop\tebiki at created 27-06-2024\treeview-git\EnterpriseTreeView\CreateNodeAPI\tests\test_lambda_result.json"

# Read and process the JSON file
with open(path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Extract the display_data array
display_data = data['body']['display_data']

# Print the display_data array
# print(json.dumps(display_data, ensure_ascii=False, indent=4))

# Optionally, iterate through the display_data array and print each item
for item in display_data:
    print(f"Key: {item['key']}, Name: {item['name']}, Parent: {item.get('parent', 'N/A')}")