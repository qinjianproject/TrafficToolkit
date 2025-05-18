import os
import subprocess

import pandas as pd
import numpy
import shutil

cfm_path = '/home/fattysand/CICFlowMeter/bin'

tmp_pcap_root = '/home/fattysand/small.pcap'
csv_root = '/home/fattysand'

pcap_path_to_cfm = os.path.relpath(tmp_pcap_root, cfm_path)
csv_path_to_cfm = os.path.relpath(csv_root, cfm_path)
cmd = './cfm ' + pcap_path_to_cfm + ' ' + csv_path_to_cfm
subprocess.call(cmd, shell=True, cwd=cfm_path)