#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

set -e

echo -e "${CYAN}���������� FunPayVertex${NC}"
echo -e "${MAGENTA}By NightStranger & Lemarty${NC}\n"

echo -e "${GREEN}���������� �������...${NC}"
sudo apt update -y && sudo apt upgrade -y

echo -e "${GREEN}��������� ��������� ������...${NC}"
sudo apt install -y language-pack-ru

echo -e "${GREEN}�������� �������...${NC}"
if ! locale -a | grep -q 'ru_RU.utf8'; then
    echo -e "${GREEN}���������� �������...${NC}"
    sudo update-locale LANG=ru_RU.utf8

    echo -e "${RED}������ ��� �� �����������. ����������, ������������� �������� � ��������� ������� ������� �������.${NC}"
    exit 1
fi

echo -e "${GREEN}��������� software-properties-common...${NC}"
sudo apt install -y software-properties-common

echo -e "${GREEN}���������� ����������� deadsnakes/ppa...${NC}"
sudo add-apt-repository -y ppa:deadsnakes/ppa

echo -e "${GREEN}������� � �������� ����������...${NC}"
cd ~

echo -e "${GREEN}��������� Python 3.11 � ������������...${NC}"
sudo apt install -y python3.11 python3.11-dev python3.11-gdbm python3.11-venv
wget https://bootstrap.pypa.io/get-pip.py -nc
sudo python3.11 get-pip.py

rm -rf get-pip.py

echo -e "${GREEN}��������� git...${NC}"
sudo apt install -y git

sudo rm -rf FunPayVertex

echo -e "${GREEN}������������ ����������� FunPayVertex...${NC}"
git clone https://github.com/NightStrang6r/FunPayVertex

echo -e "${GREEN}������� � ���������� �������...${NC}"
cd FunPayVertex

echo -e "${GREEN}��������� ������������ ����...${NC}"
sudo python3.11 setup.py

echo -e "${GREEN}������ ���������� ��������� ��������� ���������${NC}"
echo -e "${GREEN}����{NC}"

echo -e "${GREEN}��, ������ ������� ���� ��� ������� �������${NC}"

echo -e "${GREEN}��������� curl...${NC}"
sudo apt-get install -y curl

echo -e "${GREEN}�������� NodeJS...${NC}"
curl -sL https://deb.nodesource.com/setup_16.x | sudo bash -

echo -e "${GREEN}��������� NodeJS...${NC}"
sudo apt -y install nodejs

echo -e "${GREEN}��������� pm2...${NC}"
sudo npm install -g pm2

pm2 start main.py --interpreter=python3.11 --name=FunPayVertex
pm2 save
pm2 startup

echo -e "\n${CYAN}��������� FunPayVertex ���������!${NC}"
echo -e "${CYAN}��� ��������� ����� ����������� �������: pm2 logs FunPayVertex${NC}"

pm2 logs FunPayVertex

pm2 stop all
echo -e "${GREEN}������� �������{NC}"