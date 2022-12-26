# Install the OpenSSH Server
Add-WindowsCapability -Online -Name "OpenSSH.Server~~~~0.0.1.0"
# Start the sshd service
Start-Service sshd

# OPTIONAL but recommended:
Set-Service -Name sshd -StartupType 'Automatic'
