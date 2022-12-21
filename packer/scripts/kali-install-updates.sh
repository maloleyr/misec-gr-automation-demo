#!/bin/bash
###############################
# kali-install-updates.sh #
###############################

echo "[->] kali-install-updates.sh"

echo "[*] Installing available updates."
apt-get update -y
apt-get upgrade -y
echo "[*] Done."
