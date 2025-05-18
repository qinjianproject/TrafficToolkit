import os
import subprocess
from tqdm import tqdm
import argparse

splitcap_exe_path = "../tool/SplitCap.exe"


def splitpcap(folder_input_path, folder_output_path, os_type):
    pcap_list = [os.path.join(folder_input_path, p) for p in os.listdir(folder_input_path)]

    if os_type == "windows":
        for pcap in tqdm(pcap_list):
            folder_output_path = os.path.join(folder_output_path, os.path.basename(folder_input_path))
            if not os.path.exists(folder_output_path):
                os.makedirs(folder_output_path)
            # 定义命令和参数
            command = splitcap_exe_path
            args = [
                "-r", f"{pcap}",
                "-s", "session",
                "-o", f"{folder_output_path}"
            ]

            # 使用 subprocess.run 执行命令
            try:
                result = subprocess.run([command] + args, 
                                    check=True, 
                                    stdout=subprocess.PIPE, 
                                    stderr=subprocess.PIPE,
                                    text=True)
            except subprocess.CalledProcessError as e:
                print(f"❌ {pcap} split failed！error: {e.stderr}")
            except FileNotFoundError:
                print("⚠️  Could not find SplitCap.exe. Please ensure it is in your system PATH or provide the full path")
    elif os_type == "linux":
        for pcap in tqdm(pcap_list):
            if not os.path.exists(folder_output_path):
                os.makedirs(folder_output_path)
            # 定义命令和参数
            command = splitcap_exe_path
            args = [
                "-r", f"{pcap}",
                "-s", "session",
                "-o", f"{folder_output_path}"
            ]

            # 使用 subprocess.run 执行命令
            try:
                result = subprocess.run(["mono"] + [command] + args, 
                                    check=True, 
                                    stdout=subprocess.PIPE, 
                                    stderr=subprocess.PIPE,
                                    text=True)
            except subprocess.CalledProcessError as e:
                print(f"❌ {pcap} split failed！error: {e.stderr}")
            except FileNotFoundError:
                print("⚠️  Could not find SplitCap.exe. Please ensure it is in your system PATH or provide the full path")


def main(input_path, output_path, os_type):
    if os.path.exists(input_path):
        splitpcap(input_path, output_path, os_type)
    else:
        print(f"⚠️  {input_path} does not exist.")


def main_folder(folder_input_path, folder_output_path, os_type):
    if os.path.exists(folder_input_path):
        folder_input_list = [os.path.join(folder_input_path,f) for f in os.listdir(folder_input_path)]
        folder_output_list = [os.path.join(folder_output_path,f) for f in os.listdir(folder_input_path)]
        for i in tqdm(range(len(folder_input_list))):
            splitpcap(folder_input_list[i], folder_output_list[i], os_type)
    else:
        print(f"⚠️  {folder_input_path} does not exist.")
    
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Split pcap files')
    parser.add_argument('--input_path', required=False, help='Input - Path to the folder containing pcap files', default=None, type=str)
    parser.add_argument('--output_path', required=False, help='Output - Path to the folder containing pcap files', default=None, type=str)
    parser.add_argument('--folder_input_path', required=False, help='Input - Path to the folder containing folder files', default=None, type=str)
    parser.add_argument('--folder_output_path', required=False, help='Output - Path to the folder containing folder files', default=None, type=str)
    parser.add_argument('--os_type', required=False, help='Operating system', default=None, type=str)
    
    args = parser.parse_args()

    if (args.input_path != None and args.output_path != None and args.os_type != None) and (args.folder_input_path == None and args.folder_output_path==None):
        main(args.input_path, args.output_path, args.os_type)
    elif (args.folder_input_path != None and args.folder_output_path != None and args.os_type != None) and (args.input_path == None and args.output_path == None):
        main_folder(args.folder_input_path, args.folder_output_path, args.os_type)
    else:
        print("Parameter input error")
    
        
