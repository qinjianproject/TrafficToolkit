import subprocess
import json
import os
import shutil
import argparse


# Read file and get corresponding information
def get_protolist(file_path):
    proto_list = {}
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines() 
    except FileNotFoundError:
        print(f"{file_path} does not exist.")
    
    for line in lines:
        line = line.strip()
        line = line.replace("|", '')
        if line:
            parts = line.split()  # Split by space
            protocol_name = parts[0]  # Protocol name
            is_encrypted = parts[1]  # Whether encrypted
            usage_category = " ".join(parts[2:])  # Usage category
            proto_list[protocol_name] = {
                "is_encrypted": is_encrypted,
                "usage_category": usage_category
            }
    return proto_list


# Return encryption status based on nDPI identified protocol information
def get_isencrypted(proto_list, protocol):
    if protocol in proto_list:
        return proto_list[protocol]['is_encrypted']
    else:
        return ""

# Return usage category based on nDPI identified protocol information
def get_usage_category(proto_list, protocol):
    if protocol in proto_list:
        return proto_list[protocol]['usage_category']
    else:
        return ""


# Get protocol information from pcap file containing single session
def get_session_protocol(pcap_file):
    # Call nDPI to analyze file and write results to temporary file
    command = [
        "ndpiReader",
        "-i", pcap_file,
        "-j", "tmp.json"
    ]
    output = subprocess.run(command, capture_output=True, text=True)
    try:
        with open('tmp.json', 'r') as file:
            data = json.load(file)
        os.remove("tmp.json")
    except Exception as e:
        print(f"❌ Error parsing: {e}")

    # Extract protocol field
    detected_protos = data.get("detected.protos", [])
    if detected_protos:
        # If multiple, extract first protocol name, default to Unknown
        protocol_name = detected_protos[0].get("name", "Unknown") 
        if protocol_name == "Unknown":
            print(f"⚠️  {pcap_file}: No protocol information detected")
        return protocol_name
    else:
        print(f"⚠️  {pcap_file}: No protocol information detected")
        return ""


def main(input_path, en_output_path, plain_output_path):
    proto_list = get_protolist("../files/proto.md")
    protocol_result = []
    en_result_dict = {}
    plain_result_dict = {}
    for filename in os.listdir(input_path):
        protocol = get_session_protocol(os.path.join(input_path, filename))
        is_encrypted = get_isencrypted(proto_list, protocol) # Check if encrypted
        if is_encrypted == "Yes":
            source_file_path = os.path.join(input_path, filename)
            destination_folder_path = os.path.join(en_output_path, os.path.basename(input_path))
            if not os.path.exists(destination_folder_path):
                os.makedirs(destination_folder_path)
            destination_file_path = os.path.join(destination_folder_path, filename)
            if not os.path.exists(destination_file_path):
                shutil.copy(source_file_path, destination_file_path)
                en_result_dict[destination_file_path] = protocol
        elif is_encrypted == "No":
            source_file_path = os.path.join(input_path, filename)
            destination_folder_path = os.path.join(plain_output_path, os.path.basename(input_path))
            if not os.path.exists(destination_folder_path):
                os.makedirs(destination_folder_path)
            destination_file_path = os.path.join(destination_folder_path, filename)
            if not os.path.exists(destination_file_path):
                shutil.copy(source_file_path, destination_file_path)
                plain_result_dict[destination_file_path] = protocol
        else:
            protocol_result.append(protocol)
    print(f"⚠️  Here are some protocols not included in the proto.md file but can be parsed: {set(protocol_result)}.  Please manually verify whether these protocols are encrypted and supplement them into the proto.md file.  Then, rerun the process to continue classifying the previously unclassified files.")
    # Save en_result_dict to a JSON file in en_output_path
    en_dict_path = os.path.join(en_output_path, "encrypted_protocols.json")
    with open(en_dict_path, 'w') as f:
        json.dump(en_result_dict, f, indent=4)
    print(f"✅ {en_dict_path} stores all the protocol types of encrypted pcap files that can be parsed.")

    plain_dict_path = os.path.join(plain_output_path, "plaintext_protocols.json")
    with open(plain_dict_path, 'w') as f:
        json.dump(plain_result_dict, f, indent=4)
    print(f"✅ {plain_dict_path} stores all the protocol types of plaintext pcap files that can be parsed.")





def main_folder(folder_input_path, en_folder_output_path, plain_folder_output_path):
    proto_list = get_protolist("../files/proto.md")
    protocol_result = []
    for folder in os.listdir(folder_input_path):
        en_result_dict = {}
        plain_result_dict = {}
        folder_path = os.path.join(folder_input_path, folder)
        for filename in os.listdir(folder_path):
            protocol = get_session_protocol(os.path.join(folder_path, filename))
            is_encrypted = get_isencrypted(proto_list, protocol) # Check if encrypted
            if is_encrypted == "Yes":
                source_file_path = os.path.join(folder_path, filename)
                destination_folder_path = os.path.join(en_folder_output_path, folder)
                if not os.path.exists(destination_folder_path):
                    os.makedirs(destination_folder_path)
                destination_file_path = os.path.join(destination_folder_path, filename)
                if not os.path.exists(destination_file_path):
                    shutil.copy(source_file_path, destination_file_path)
                    en_result_dict[destination_file_path] = protocol
            elif is_encrypted == "No":
                source_file_path = os.path.join(folder_path, filename)
                destination_folder_path = os.path.join(plain_folder_output_path,folder)
                if not os.path.exists(destination_folder_path):
                    os.makedirs(destination_folder_path)
                destination_file_path = os.path.join(destination_folder_path, filename)
                if not os.path.exists(destination_file_path):
                    shutil.copy(source_file_path, destination_file_path)
                    plain_result_dict[destination_file_path] = protocol
            else:
                protocol_result.append(protocol)
        
        en_dict_path = os.path.join(en_folder_output_path, f"{folder}_encrypted_protocols.json")
        with open(en_dict_path, 'w') as f:
            json.dump(en_result_dict, f, indent=4)
        print(f"✅ {en_dict_path} stores all the protocol types of encrypted pcap files that can be parsed.")

        plain_dict_path = os.path.join(plain_folder_output_path, f"{folder}_plaintext_protocols.json")
        with open(plain_dict_path, 'w') as f:
            json.dump(plain_result_dict, f, indent=4)
        print(f"✅ {plain_dict_path} stores all the protocol types of plaintext pcap files that can be parsed.")

    print(f"⚠️  Here are some protocols not included in the proto.md file but can be parsed: {set(protocol_result)}.  Please manually verify whether these protocols are encrypted and supplement them into the proto.md file.  Then, rerun the process to continue classifying the previously unclassified files.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Distinguish whether pcap files are encrypted or plaintext.')
    parser.add_argument('--input_path', required=False, help='Input - Path to the folder containing pcap files', default=None, type=str)
    parser.add_argument('--en_output_path', required=False, help='Output - Path to the encrypted output folder containing pcap files', default=None, type=str)
    parser.add_argument('--plain_output_path', required=False, help='Output - Path to the plaintext output folder containing pcap files', default=None, type=str)
    parser.add_argument('--folder_input_path', required=False, help='Path to the folder containing folder files', default=None, type=str)
    parser.add_argument('--en_folder_output_path', required=False, help='Path to the encrypted output folder containing folder files', default=None, type=str)
    parser.add_argument('--plain_folder_output_path', required=False, help='Path to the plaintext output folder containing folder files', default=None, type=str)
    
    args = parser.parse_args()

    if (args.input_path != None and args.en_output_path != None and args.plain_output_path != None) and (args.folder_input_path == None and args.en_folder_output_path == None and args.plain_folder_output_path == None):
        main(args.input_path, args.en_output_path, args.plain_output_path)
    elif (args.folder_input_path != None and args.en_folder_output_path != None and args.plain_folder_output_path != None) and (args.input_path == None and args.en_output_path == None and args.plain_output_path == None):
        main_folder(args.folder_input_path, args.en_folder_output_path, args.plain_folder_output_path)
    else:
        print("Parameter input error")
                 
