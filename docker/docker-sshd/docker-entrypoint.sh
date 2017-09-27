#!/bin/ash

set -e

ssh-keygen -A
mkdir /var/run/sshd
{
	echo "PubkeyAuthentication yes"
	echo "PasswordAuthentication no"
	echo "PermitRootLogin no"
	echo "AllowTcpForwarding yes"
} >> /etc/ssh/sshd_config

user=${SSH_USER:-ssh-user}

adduser -D "$user"
echo "$user:*" | chpasswd -e
mkdir "/home/$user/.ssh"
touch "/home/$user/.ssh/authorized_keys"
chmod 0600 "/home/$user/.ssh/authorized_keys"
if [ -n "$AUTHORIZED_KEYS" ]; then
	echo "${AUTHORIZED_KEYS}" >> "/home/$user/.ssh/authorized_keys"
fi
chown -R "$user" "/home/$user/.ssh"

echo "Ready to ssh in with user $user using authorized_keys:"
cat "/home/$user/.ssh/authorized_keys"

exec "$@"
