# 🛠️ TrafficToolkit

[中文README](README_zh.md) | English README

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey)

A comprehensive toolkit for processing PCAP network traffic files, including format conversion, splitting, filtering, and classification of encrypted vs plaintext traffic.

## 🌟 Function

- **📁 PCAPNG to PCAP Conversion**: Convert newer PCAPNG files to traditional PCAP format
- **🧹 Traffic Filtering**: Filter PCAPs using Wireshark-style rules
- **✂️ PCAP Splitting**: Split large PCAP files into individual sessions
- **📊 Traffic Sampling**: Extract top K longest sessions for analysis
- **🔐 Traffic Distinguish**: Distinguish between encrypted and plaintext sessions & Identify protocols


## 🚀 Installation
For Linux users:
```bash
sudo apt install mono-runtime libndpi-bin
```

## 💻 Usage
### 1. 🔄 PCAPNG to PCAP Conversion
```bash
# Single folder
python Pcapng2Pcap.py --input_path ../dataset/dataset_raw/Tor-nonTor/audio_streaming --output_path ../dataset/dataset_pcap/Tor-nonTor
```
```bash
# Recursive folder processing
python Pcapng2Pcap.py --folder_input_path ../dataset/dataset_raw/Tor-nonTor --folder_output_path ../dataset/dataset_pcap/Tor-nonTor
```


### 2. 🧹 Traffic Filtering
```bash
# Single folder (filter TCP traffic)
python PcapFilter.py --input_path ../dataset/dataset_pcap/Tor-nonTor/browsing --output_path ../dataset/dataset_filter/Tor-nonTor --filter_rule tcp
```
```bash
# Recursive folder processing
python PcapFilter.py --folder_input_path ../dataset/dataset_pcap/Tor-nonTor --folder_output_path ../dataset/dataset_filter/Tor-nonTor --filter_rule tcp
```


### 3. ✂️ PCAP Splitting
Windows:
```bash
# Single folder
python PcapSplit.py --input_path ../dataset/dataset_filter/Tor-nonTor/audio_streaming --output_path ../dataset/dataset_split/Tor-nonTor --os_type windows
```
```bash
# Recursive folder processing
python PcapSplit.py --folder_input_path ../dataset/dataset_filter/Tor-nonTor --folder_output_path ../dataset/dataset_split/Tor-nonTor --os_type windows
```

Linux:
```bash
# Single folder
python PcapSplit.py --input_path ../dataset/dataset_filter/Tor-nonTor/audio_streaming --output_path ../dataset/dataset_split/Tor-nonTor --os_type linux
```
```bash
# Recursive folder processing
python PcapSplit.py --folder_input_path ../dataset/dataset_filter/Tor-nonTor --folder_output_path ../dataset/dataset_split/Tor-nonTor --os_type linux
```


### 4. 📊 Session Sampling (Top [MAX_NUM] Longest Sessions)
```bash
# Single folder
python PcapGetDemo.py --input_path ../dataset/dataset_split/Tor-nonTor/browsing --output_path ../dataset/dataset_demo/Tor-nonTor --MAX_NUM 100
```
```bash
# Recursive folder processing
python PcapGetDemo.py --folder_input_path ../dataset/dataset_split/Tor-nonTor --folder_output_path ../dataset/dataset_demo/Tor-nonTor --MAX_NUM 100
```


### 5. 🔍 Traffic Distinguish
Distinguish between plaintext and encrypted sessions & extract the protocol

If it's Windows, you need to run the following command first:

> 1. Install and start WSL:
>    If it's Windows Home Edition, you need to first run the command: 
>
>    `wsl --set-default-version 1`
>
>    `wsl --install`
>
>    `wsl -d ubuntu`
>
> 2. Replace the image:
>
>    https://blog.csdn.net/MacWx/article/details/137689898
>
> 3. install ndpi:
>
>    `sudo apt install libndpi-bin`

Usage:

```bash
# Single folder
python PcapDistinct.py --input_path ../dataset/dataset_demo/Tor-nonTor/browsing --en_output_path ../dataset/pcap_distinct/Tor-nonTor/encrypted --plain_output_path ../dataset/pcap_distinct/Tor-nonTor/plaintext
```
```bash
# Recursive folder processing
python PcapDistinct.py --folder_input_path ../dataset/dataset_demo/Tor-nonTor --en_folder_output_path ../dataset/pcap_distinct/Tor-nonTor/encrypted --plain_folder_output_path ../dataset/pcap_distinct/Tor-nonTor/plaintext
```


### ✅ Suggested Processing Pipeline
1. Convert PCAPNG to PCAP:

   ```bash
   python Pcapng2Pcap.py --folder_input_path ../dataset/dataset_raw/Tor-nonTor --folder_output_path ../dataset/dataset_pcap/Tor-nonTor
   ```

2. Filter PCAP:

   ```bash
   python PcapFilter.py --folder_input_path ../dataset/dataset_pcap/Tor-nonTor --folder_output_path ../dataset/dataset_filter/Tor-nonTor --filter_rule tcp
   ```
3. Split PCAP files:

   ```bash
   python PcapSplit.py --folder_input_path ../dataset/dataset_filter/Tor-nonTor --folder_output_path ../dataset/dataset_split/Tor-nonTor --os_type linux
   ```
4. Sample longest sessions:

   ```bash
   python PcapGetDemo.py --folder_input_path ../dataset/dataset_split/Tor-nonTor --folder_output_path ../dataset/dataset_demo/Tor-nonTor --MAX_NUM 100
   ```

5. Distinguish traffic:

   ```bash
   python PcapDistinct.py --folder_input_path ../dataset/dataset_demo/Tor-nonTor --en_folder_output_path ../dataset/pcap_distinct/Tor-nonTor/encrypted --plain_folder_output_path ../dataset/pcap_distinct/Tor-nonTor/plaintext
   ```

## 😀*Continuous updates*

*Coming soon: Updates on PCAP file feature extraction to support deep learning model development. Stay tuned..*

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.
