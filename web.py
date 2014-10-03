from fabric.api import *

@task(default=True)
@roles('web')
def main():
  print("web.main")

@task
@roles('web')
def add_web(login_asso):
  print("Ajout des fichiers de conf apache")
  sudo('sed "s/LOGIN/%s/g" /root/modele.suphp > /etc/apache2/custom/%s.suphp' % (login_asso,login_asso))
  sudo('echo %s >> /root/assos.list' % (login_asso))
  generate_vhost_web()

@task
@roles('web')
def generate_vhost_web():
	# Pool php-fpm	
	sudo("""while read -r line
do
ligne=`echo ${line}|awk -F " " '{print $1}'`

cat > /etc/php5/fpm/pool.d/$ligne.conf <<EOF
[$ligne]
user = $ligne
group = nogroup
listen = /var/run/php-fpm-$ligne.sock
listen.owner = www-data
listen.group = www-data
pm = ondemand
pm.max_children = 5
pm.process_idle_timeout = 10s
chroot=
chdir = /
php_value[session.save_path] = /sites/sessions/$ligne
php_value[session.cookie_path] = /$ligne
include=/etc/php5/fpm/pool.d/custom/$ligne.conf
EOF


# Config apache	

cat > /etc/apache2/sites-available/$ligne <<EOF
Include /etc/apache2/custom/$ligne
Alias /$ligne /sites/$ligne
Alias /php5-$ligne.fastcgi /var/lib/apache2/fastcgi/php5-$ligne.fastcgi
FastCGIExternalServer /var/lib/apache2/fastcgi/php5-$ligne.fastcgi -socket /var/run/php-fpm-$ligne.sock -idle-timeout 60
Action php-script-$ligne /php5-$ligne.fastcgi
<Directory /sites/$ligne>
  AddHandler php-script-$ligne .php
  Options FollowSymLinks
  AllowOverride All
  Order allow,deny
  Allow from all
  Include /etc/apache2/custom/$ligne.directory
</Directory>
EOF


# Creation des fichiers de config custom

touch /etc/apache2/custom/$ligne.directory 
touch /etc/apache2/custom/$ligne 
touch /etc/php5/fpm/pool.d/custom/$ligne.conf 
	

# Creation du dossier pour les sessions

mkdir -p /sites/sessions/$ligne 
chown $ligne.web /sites/sessions/$ligne 
chmod 2750 /sites/sessions/$ligne 


# Activation de l'alias

a2ensite $ligne
done < '/root/assos.list'""")
	
	# reload php-fpm
	sudo("service php5-fpm reload")
	
	# reload apache2
	sudo("service apache2 reload")

@task
@roles('web')
def change_for_python(login_asso):
  sudo('sed -i "s/%s/%s python/" /root/assos.list' % (login_asso, login_asso))

@task
@roles('web')
def change_for_php(login_asso):
  sudo('sed -i "s/%s python/%s/" /root/assos.list' % (login_asso, login_asso))





