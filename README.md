# vk-xkcd

Downloads a random comic from https://xkcd.com and publishes to the group vk.com.

## Installing

1) Clone project
```bash
git clone https://github.com/shadowsking/vk-xkcd.git
cd vk-xkcd
```
2) Create virtual environments
```bash
python -m venv venv
source venv/scripts/activate
```
3) Install requirements
```bash
pip install -r requirements.txt
```
4) Create new '.env' file from '.env.example' and fill in environment variables
   - GROUP_ID
   - VK_API_TOKEN

## Running
```bash
python main.py
```
