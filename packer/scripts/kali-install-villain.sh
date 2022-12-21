#!/bin/bash
###########################
# kali-install-villain.sh #
##########################

echo "[->] kali-install-villain.sh"

echo "[*] Installing Villain."
cd
git clone https://github.com/t3l3machus/Villain
cd ./Villain
pip3 install -r requirements.txt
echo "[*] Done."
