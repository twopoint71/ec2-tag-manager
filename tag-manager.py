import subprocess
import json

# Global variable to store the selected instance ID
selected_instance_id = None

def load_instance_tags():
    global selected_instance_id
    selected_instance_id = input("Enter Instance Name or Instance ID: ")
    command = f"aws ec2 describe-tags --filters \"Name=resource-id,Values={selected_instance_id}\""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result.stdout)

def list_tags():
    if not selected_instance_id:
        print("No instance selected. Please load an instance first.")
        return

    command = f"aws ec2 describe-tags --filters \"Name=resource-id,Values={selected_instance_id}\""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    try:
        tags = json.loads(result.stdout)['Tags']
        for idx, tag in enumerate(tags):
            print(f"{idx + 1}. {tag['Key']}: {tag['Value']}")
    except (KeyError, json.JSONDecodeError):
        print("Error parsing tags data. Please ensure the instance ID is correct and try again.")

def create_tag():
    if not selected_instance_id:
        print("No instance selected. Please load an instance first.")
        return

    key = input("Enter Tag Key: ")
    value = input("Enter Tag Value: ")
    command = f"aws ec2 create-tags --resources {selected_instance_id} --tags Key={key},Value={value}"
    subprocess.run(command, shell=True)

def update_tag():
    if not selected_instance_id:
        print("No instance selected. Please load an instance first.")
        return

    list_tags()
    tag_id = int(input("Enter the ID of the Tag to Update: ")) - 1
    value = input("Enter New Tag Value: ")

    command = f"aws ec2 describe-tags --filters \"Name=resource-id,Values={selected_instance_id}\""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    tags = json.loads(result.stdout)['Tags']
    key = tags[tag_id]['Key']

    command = f"aws ec2 create-tags --resources {selected_instance_id} --tags Key={key},Value={value}"
    subprocess.run(command, shell=True)

def delete_tag():
    if not selected_instance_id:
        print("No instance selected. Please load an instance first.")
        return

    list_tags()
    tag_id = int(input("Enter the ID of the Tag to Delete: ")) - 1

    command = f"aws ec2 describe-tags --filters \"Name=resource-id,Values={selected_instance_id}\""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    tags = json.loads(result.stdout)['Tags']
    key = tags[tag_id]['Key']

    command = f"aws ec2 delete-tags --resources {selected_instance_id} --tags Key={key}"
    subprocess.run(command, shell=True)

def main():
    while True:
        print("\nMenu:")
        print("1. Load EC2 Instance Tags")
        print("2. List Tags")
        print("3. Create a Tag")
        print("4. Update a Tag")
        print("5. Delete a Tag")
        print("6. Quit")

        choice = input("Enter your choice: ")

        if choice == '1':
            load_instance_tags()
        elif choice == '2':
            list_tags()
        elif choice == '3':
            create_tag()
        elif choice == '4':
            update_tag()
        elif choice == '5':
            delete_tag()
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
