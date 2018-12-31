!/bin/bash
# Must be run as user with sudo permission
set -v
set -e
USERNAME=sftp-$1
NEW_USER=$1
echo "Creating new user $1"
# New user does not need a password
# No login with password is available
sudo adduser --disabled-password --gecos ""  $USERNAME
# Create and set permissions on needed directories
sudo mkdir -p /var/sftp/$NEW_USER/uploads
sudo chown root:root /var/sftp
sudo chown root:root /var/sftp/$NEW_USER
sudo chown $USERNAME:$USERNAME /var/sftp/$NEW_USER/uploads
sudo chmod 755 /var/sftp
sudo chmod 755 /var/sftp/$NEW_USEER
# Lock down user sssh options to only sftp
sudo tee -a  /etc/ssh/sshd_config << EOF
# Sftp user only $USERNAME
Match User $USERNAME
ForceCommand internal-sftp
PasswordAuthentication yes
ChrootDirectory /var/sftp/$NEW_USER
PermitTunnel no
AllowAgentForwarding no
AllowTcpForwarding no
X11Forwarding no
EOF
# Restart the ssh daemon:
sudo systemctl restart sshd

SFTP_KEYFILE=sftp_$NEW_USER
# Set up user keys
# Rename private key to make it more obvious
# Set up access with public key
sudo su - $USERNAME <<EOF
mkdir .ssh
cd .ssh
ssh-keygen -t rsa -N "" -f $SFTP_KEYFILE
mv $SFTP_KEYFILE $SFTP_KEYFILE.key
cat $SFTP_KEYFILE.pub >> authorized_keys
EOF
echo "Done!"

