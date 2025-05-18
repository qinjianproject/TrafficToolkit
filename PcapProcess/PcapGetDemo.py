import os
import shutil
import argparse

def sort_and_trim_files(folder_path, folder_output_path, MAX):
    # 获取文件夹中的所有文件
    files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    # 按照文件大小从大到小排序
    files.sort(key=lambda x: os.path.getsize(x), reverse=True)
    
    # 如果文件数量超过MAX，则执行删除任务
    if len(files) > MAX:
        for file in files[:MAX]:
            dest_path = os.path.join(folder_output_path, os.path.basename(file))
            shutil.copy(file, dest_path)
        print(f"✅ {os.path.basename(folder_path)} finished: {len(os.listdir(folder_output_path))}")
    else:
        print(f"😀 {os.path.basename(folder_path)} No files to delete. Total files: {len(os.listdir(folder_path))}")


def main(input_path, output_path, MAX_NUM):
    if os.path.exists(input_path):
        output_path = os.path.join(output_path, os.path.basename(input_path))
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        sort_and_trim_files(input_path, output_path, MAX_NUM)
    else:
        print(f"⚠️  {input_path} does not exist.")


def main_folder(folder_input_path, folder_output_path, MAX_NUM):
    if os.path.exists(folder_input_path):
        folder_input_list = [os.path.join(folder_input_path, f) for f in os.listdir(folder_input_path)]
        folder_output_list = [os.path.join(folder_output_path, f) for f in os.listdir(folder_input_path)]

        for i in range(len(folder_input_list)):
            if not os.path.exists(folder_output_list[i]):
                os.makedirs(folder_output_list[i])
            sort_and_trim_files(folder_input_list[i], folder_output_list[i], MAX_NUM)
    else:
        print(f"⚠️  {folder_input_path} does not exist.")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get demo dataset.')
    parser.add_argument('--input_path', required=False, help='Input - Path to the folder containing pcap files', default=None, type=str)
    parser.add_argument('--output_path', required=False, help='Output - Path to the folder containing pcap files', default=None, type=str)
    parser.add_argument('--folder_input_path', required=False, help='Input - Path to the folder containing folder files', default=None, type=str)
    parser.add_argument('--folder_output_path', required=False, help='Output - Path to the folder containing folder files', default=None, type=str)
    parser.add_argument('--MAX_NUM', required=False, help='Output - Path to the folder containing pcap files', default=1000, type=int)
    

    args = parser.parse_args()

    if (args.input_path != None and args.output_path != None) and (args.folder_input_path == None and args.folder_output_path==None):
        main(args.input_path, args.output_path, args.MAX_NUM)
    elif (args.folder_input_path != None and args.folder_output_path != None) and (args.input_path == None and args.output_path == None):
        main_folder(args.folder_input_path, args.folder_output_path, args.MAX_NUM)
    else:
        print("Parameter input error")


    