# 🛠️ PCAP处理工具包
中文README | [English README](README.md)

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey)


这是一个全面的PCAP网络流量文件处理工具包，包含格式转换、分割会话、过滤以及加密与明文流量分类等功能。

## 🌟 功能
- **📁 PCAPNG转PCAP**: 将新版PCAPNG文件转换为传统PCAP格式
- **🧹 流量过滤​​**: 使用Wireshark风格规则批量过滤PCAP文件
- **✂️ PCAP分割**: 将大型PCAP文件分割为独立会话
- **📊 流量采样​**: 提取前K个最长会话进行分析
- **🔐 流量区分**: 区分加密与明文会话 & 识别协议

## 🚀 安装
Linux用户:

```bash
sudo apt install mono-runtime libndpi-bin
```


## 💻 使用

### 1. 🔄 PCAPNG转PCAP
```bash
# 单文件夹处理
python Pcapng2Pcap.py --input_path ../dataset/dataset_raw/Tor-nonTor/audio_streaming --output_path ../dataset/dataset_pcap/Tor-nonTor
```
```bash
# 递归文件夹处理
python Pcapng2Pcap.py --folder_input_path ../dataset/dataset_raw/Tor-nonTor --folder_output_path ../dataset/dataset_pcap/Tor-nonTor
```
### 2. 🧹 流量过滤
```bash
# 单文件夹处理(过滤TCP流量)
python PcapFilter.py --input_path ../dataset/dataset_pcap/Tor-nonTor/browsing --output_path ../dataset/dataset_filter/Tor-nonTor --filter_rule tcp
```
```bash
# 递归文件夹处理
python PcapFilter.py --folder_input_path ../dataset/dataset_pcap/Tor-nonTor --folder_output_path ../dataset/dataset_filter/Tor-nonTor --filter_rule tcp
```
### 3. ✂️ PCAP分割
Windows:
```bash
# 单文件夹处理
python PcapSplit.py --input_path ../dataset/dataset_filter/Tor-nonTor/audio_streaming --output_path ../dataset/dataset_split/Tor-nonTor --os_type windows
```
```bash
# 递归文件夹处理
python PcapSplit.py --folder_input_path ../dataset/dataset_filter/Tor-nonTor --folder_output_path ../dataset/dataset_split/Tor-nonTor --os_type windows
```
Linux:
```bash
# 单文件夹处理
python PcapSplit.py --input_path ../dataset/dataset_filter/Tor-nonTor/audio_streaming --output_path ../dataset/dataset_split/Tor-nonTor --os_type linux
```
```bash
# 递归文件夹处理
python PcapSplit.py --folder_input_path ../dataset/dataset_filter/Tor-nonTor --folder_output_path ../dataset/dataset_split/Tor-nonTor --os_type linux
```
### 4. 📊 会话采样(前MAX_NUM个最长会话)
```bash
# 单文件夹处理
python PcapGetDemo.py --input_path ../dataset/dataset_split/Tor-nonTor/browsing --output_path ../dataset/dataset_demo/Tor-nonTor --MAX_NUM 100
```
```bash
# 递归文件夹处理
python PcapGetDemo.py --folder_input_path ../dataset/dataset_split/Tor-nonTor --folder_output_path ../dataset/dataset_demo/Tor-nonTor --MAX_NUM 100
```
### 5. 🔍 流量区分
区分明文与加密会话 & 提取协议信息

Windows用户需要先执行以下命令:

> 1. 安装并启动WSL, 如果是Windows家庭版，需要先运行命令: 
>
>    `wsl --set-default-version 1`
>
>    `wsl --install`
>
>    `wsl -d ubuntu`
>
> 2. 更换镜像源: 
>
>    参考: https://blog.csdn.net/MacWx/article/details/137689898
>
> 3. 安装ndpi: 
>
>    `sudo apt install libndpi-bin`


使用:
```bash
# 单文件夹处理
python PcapDistinct.py --input_path ../dataset/dataset_demo/Tor-nonTor/browsing --en_output_path ../dataset/pcap_distinct/Tor-nonTor/encrypted --plain_output_path ../dataset/pcap_distinct/Tor-nonTor/plaintext
```
```bash
# 递归文件夹处理
python PcapDistinct.py --folder_input_path ../dataset/dataset_demo/Tor-nonTor --en_folder_output_path ../dataset/pcap_distinct/Tor-nonTor/encrypted --plain_folder_output_path ../dataset/pcap_distinct/Tor-nonTor/plaintext
```


### ✅ 推荐处理流程
1. PCAPNG转PCAP:

  ```bash
  python Pcapng2Pcap.py --folder_input_path ../dataset/dataset_raw/Tor-nonTor --folder_output_path ../dataset/dataset_pcap/Tor-nonTor
  ```

2. 过滤PCAP:

  ```bash
  python PcapFilter.py --folder_input_path ../dataset/dataset_pcap/Tor-nonTor --folder_output_path ../dataset/dataset_filter/Tor-nonTor --filter_rule tcp
  ```

3. 分割PCAP文件:

  ```bash
  python PcapSplit.py --folder_input_path ../dataset/dataset_filter/Tor-nonTor --folder_output_path ../dataset/dataset_split/Tor-nonTor --os_type linux
  ```

4. 采样最长会话:

  ```bash
  python PcapGetDemo.py --folder_input_path ../dataset/dataset_split/Tor-nonTor --folder_output_path ../dataset/dataset_demo/Tor-nonTor --MAX_NUM 100
  ```

5. 区分流量类型:

  ```bash
  python PcapDistinct.py --folder_input_path ../dataset/dataset_demo/Tor-nonTor --en_folder_output_path ../dataset/pcap_distinct/Tor-nonTor/encrypted --plain_folder_output_path ../dataset/pcap_distinct/Tor-nonTor/plaintext
  ```

## 😀持续更新

之后会更新一些PCAP文件的特征提取方面的内容，助力深度学习模型开发。敬请期待....

## 📜 许可证

本项目采用MIT许可证 - 详见LICENSE文件。



