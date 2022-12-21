#!/bin/bash
###############################
# kali-configure-usergroup.sh #
###############################

echo "[->] kali-configure-usergroup.sh"

echo "[*] Adding kali to the vboxsf group."
usermod -a -G vboxsf kali

echo "[*] Done."
