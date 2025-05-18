import os
import subprocess
import argparse
from tqdm import tqdm



def pcapfilter(input_path, output_path, filter_rule=""):
    """
    Filter pcap files using tshark command with the given filter rule
    
    Args:
        input_path (str): Path to input pcap file
        output_path (str): Path to save filtered pcap file
        filter_rule (str): Filter rule to apply (BPF syntax)
    """
    try:
        # Create output directory if it doesn't exist
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        pcap_list = [os.path.join(input_path, p) for p in os.listdir(input_path)]

        for pcap in pcap_list:
            # Build tshark command
            output_path_file = os.path.join(output_path, os.path.basename(pcap))
            cmd = [
                'tshark',
                '-r', pcap,          # Input file
                '-Y', filter_rule,         # Display filter
                '-w', output_path_file,         # Output file
                '-F', 'pcap'              # Output format
            ]
            # Run tshark command
            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            print(f"✅ {pcap} -> {output_path_file}")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error filtering {input_path}: {e.stderr.decode('utf-8')}")
    except Exception as e:
        print(f"❌ Unexpected error processing {input_path}: {str(e)}")





def main(input_path, output_path):
    if os.path.exists(input_path):
        output_path = os.path.join(output_path, os.path.basename(input_path))
        pcapfilter(input_path, output_path)
    else:
        print(f"⚠️  {input_path} does not exist.")


def main_folder(folder_input_path, folder_output_path):
    if os.path.exists(folder_input_path):
        folder_input_list = [os.path.join(folder_input_path,f) for f in os.listdir(folder_input_path)]
        folder_output_list = [os.path.join(folder_output_path,f) for f in os.listdir(folder_input_path)]
        for i in tqdm(range(len(folder_input_list))):
            pcapfilter(folder_input_list[i], folder_output_list[i])
    else:
        print(f"⚠️  {folder_input_path} does not exist.")
    
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Filter pcap files')
    parser.add_argument('--input_path', required=False, help='Input - Path to the folder containing pcap files', default=None, type=str)
    parser.add_argument('--output_path', required=False, help='Output - Path to the folder containing pcap files', default=None, type=str)
    parser.add_argument('--folder_input_path', required=False, help='Input - Path to the folder containing folder files', default=None, type=str)
    parser.add_argument('--folder_output_path', required=False, help='Output - Path to the folder containing folder files', default=None, type=str)
    parser.add_argument('--filter_rule', required=False, help='filter rules', default=None, type=str)
    
    args = parser.parse_args()

    if (args.input_path != None and args.output_path != None and args.filter_rule != None) and (args.folder_input_path == None and args.folder_output_path==None):
        main(args.input_path, args.output_path)
    elif (args.folder_input_path != None and args.folder_output_path != None and args.filter_rule != None) and (args.input_path == None and args.output_path == None):
        main_folder(args.folder_input_path, args.folder_output_path)
    else:
        print("Parameter input error")
    