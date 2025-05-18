import os
import subprocess
import argparse

def pcapng2pcap(folder_path, output_folder_path):
    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        if filename.endswith(".pcap"): # 有的pcapng文件也是以pcap文件结尾的
            # 获取文件的完整路径
            input_file = os.path.join(folder_path, filename)
            output_file_folder = os.path.join(output_folder_path, os.path.basename(folder_path))

            if not os.path.exists(output_file_folder):
                os.makedirs(output_file_folder)

            output_file = os.path.join(output_file_folder, filename)
            
            # 构造tshark命令
            command = ["tshark", "-F", "pcap", "-r", input_file, "-w", output_file]
            
            try:
                # 执行命令
                subprocess.run(command, check=True)
                print(f"✅ sucess: {input_file} -> {output_file}")
            except subprocess.CalledProcessError as e:
                print(f"❌ failed: {e}")
        elif filename.endswith(".pcapng"):
            # 获取文件的完整路径
            input_file = os.path.join(folder_path, filename)
            output_file_folder = os.path.join(output_folder_path, os.path.basename(folder_path))

            if not os.path.exists(output_file_folder):
                os.makedirs(output_file_folder)

            output_file = os.path.join(output_file_folder, filename.replace(".pcapng", ".pcap"))
            
            # 构造tshark命令
            command = ["tshark", "-F", "pcap", "-r", input_file, "-w", output_file]
            
            try:
                # 执行命令
                subprocess.run(command, check=True)
                print(f"✅ sucess: {input_file} -> {output_file}")
            except subprocess.CalledProcessError as e:
                print(f"❌ failed: {e}")

def main(path, output_path):
    if os.path.exists(path):
        pcapng2pcap(path, output_path)
        print("finished")
    else:
        print(f"⚠️  {path} does not exist.")


def main_folder(folder_path, output_folder_path):
    if os.path.exists(folder_path):
        folder_path_list = [os.path.join(folder_path, f) for f in os.listdir(folder_path)]
        for folder in folder_path_list:
            pcapng2pcap(folder, output_folder_path)
        print("finished")
    else:
        print(f"⚠️  {folder_path} does not exist.")
    
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Pcapng -> Pcap')
    parser.add_argument('--input_path', required=False, help='Input - Path to the folder containing pcap files', default=None, type=str)
    parser.add_argument('--output_path', required=False, help='Output - Path to the folder containing pcap files', default=None, type=str)
    parser.add_argument('--folder_input_path', required=False, help='Input - Path to the folder containing folder files', default=None, type=str)
    parser.add_argument('--folder_output_path', required=False, help='Output - Path to the folder containing folder files', default=None, type=str)
    
    args = parser.parse_args()

    if (args.input_path != None and args.output_path != None) and (args.folder_input_path == None and args.folder_output_path==None):
        main(args.input_path, args.output_path)
    elif (args.folder_input_path != None and args.folder_output_path != None) and (args.input_path == None and args.output_path == None):
        main_folder(args.folder_input_path, args.folder_output_path)
    else:
        print("Parameter input error")