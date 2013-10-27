#!/bin/bash
while read -r line
do

# Pool php-fpm
cat > /etc/php5/fpm/pool.d/${line}.conf <<EOF
[${line}]
user = ${line}
group = web
listen = /var/run/php-fpm-${line}.sock
pm = ondemand
pm.max_children = 5
pm.process_idle_timeout = 10s
chroot=
chdir = /
php_value[session.save_path] = /sites/sessions/${line}
php_value[disable_functions] = shell_exec
php_value[session.cookie_path] = /${line}
include=/etc/php5/fpm/pool.d/custom/${line}.conf
EOF

# Config apache
cat > /etc/apache2/sites-available/${line} <<EOF
Include /etc/apache2/custom/${line}
Alias /${line} /sites/${line}
Alias /php5-${line}.fastcgi /var/lib/apache2/fastcgi/php5-${line}.fastcgi
FastCGIExternalServer /var/lib/apache2/fastcgi/php5-${line}.fastcgi -socket /var/run/php-fpm-${line}.sock -idle-timeout 60
Action php-script-${line} /php5-${line}.fastcgi
<Directory /sites/${line}>
  AddHandler php-script-${line} .php
  Options FollowSymLinks
  AllowOverride All
  Order allow,deny
  Allow from all
  Include /etc/apache2/custom/${line}.directory
</Directory>
EOF

# Creation des fichiers de config custom
touch /etc/apache2/custom/${line}.directory
touch /etc/apache2/custom/${line}
touch /etc/php5/fpm/pool.d/custom/${line}.conf

# On retire la config disable_functions s'il y en a un dans le custom
if [ $( grep disable_functions /etc/php5/fpm/pool.d/custom/${line}.conf | grep -v "^#" | wc -l ) != 0 ]
then
sed -i '/disable_functions/d' /etc/php5/fpm/pool.d/${line}.conf
fi

# Creation du dossier pour les sessions
mkdir -p /sites/sessions/${line}
chown ${line}.web /sites/sessions/${line}
chmod 2750 /sites/sessions/${line}

# Activation de l'alias
a2ensite ${line}

done < "/root/assos.list"

# reload php-fpm
service php5-fpm reload

# reload apache2
service apache2 reload
