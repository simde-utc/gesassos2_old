from fabric.api import *

@task(default=True)
@roles('php')
def main():
  print("php.main")

@task
@roles('php')
def add_php(login_asso):
  print("Ajout des fichiers de conf apache")
  # sudo('sed "s/LOGIN/%s/g" /root/modele.suphp > /etc/apache2/custom/%s.suphp' % (login_asso,login_asso))
  sudo('echo "%s php7" >> /root/assos.list' % (login_asso))
  generate_vhost_web()

@task
@roles('php')
def del_php(login_asso):
    print("Suppression des fichiers de conf apache")
    try:
      sudo('rm /etc/apache2/custom/%s.suphp' % login_asso)
    except:
      pass
    try:
      sudo('rm /etc/apache2/custom/%s' % login_asso)
    except:
      pass
    try:
      sudo('rm /etc/apache2/custom/%s.directory' % login_asso)
    except:
      pass
    try:
      sudo('rm /etc/php5/fpm/pool.d/%s.conf' % login_asso)
    except:
      pass
    try:
      sudo('rm /etc/php/7.0/fpm/pool.d/%s.conf' % login_asso)
    except:
      pass
    try:
      sudo('rm /etc/apache2/sites-available/%s' % login_asso)
    except:
      pass  
    try:
      sudo('rm /etc/apache2/sites-enabled/%s' % login_asso)
    except:
      pass      
    try:
      sudo('rm /etc/php5/fpm/pool.d/custom/%s.conf' % login_asso)
    except:
      pass
    try:
      sudo('rm /etc/php/7.0/fpm/pool.d/custom/%s.conf' % login_asso)
    except:
      pass
    try:
      sudo("sed -i '/%s php/d' /root/assos.list" % login_asso)
    except:
      pass
    try:
      generate_vhost_web()
    except:
      pass

@task
@roles('php')
def generate_vhost_web():
  # Pool php-fpm	
  sudo("""while read -r line
do
#Config PHP5
ligne=`echo ${line}|grep "php5"|awk -F " " '{print $1}'`

cat > /etc/php5/fpm/pool.d/$ligne.conf <<EOF
[$ligne]
user = $ligne
group = nogroup
listen = /var/run/php5-fpm-$ligne.sock
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

# Config apache PHP5

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
touch /etc/php5/fpm/pool.d/custom/$ligne.conf 
touch /etc/apache2/custom/$ligne.directory 
touch /etc/apache2/custom/$ligne 
  

# Creation du dossier pour les sessions

mkdir -p /sites/sessions/$ligne 
chown $ligne.web /sites/sessions/$ligne
chmod 2750 /sites/sessions/$ligne 


# Activation de l'alias

a2ensite $ligne

# Config PHP7
ligne=`echo ${line}|grep "php7"|awk -F " " '{print $1}'`

cat > /etc/php/7.0/fpm/pool.d/$ligne.conf <<EOF
[$ligne]
user = $ligne
group = nogroup
listen = /var/run/php7-fpm-$ligne.sock
listen.owner = www-data
listen.group = www-data
pm = ondemand
pm.max_children = 5
pm.process_idle_timeout = 10s
chroot=
chdir = /
php_value[session.save_path] = /sites/sessions/$ligne
php_value[session.cookie_path] = /$ligne
include=/etc/php/7.0/fpm/pool.d/custom/$ligne.conf
EOF

# Config apache PHP7 

cat > /etc/apache2/sites-available/$ligne <<EOF
Include /etc/apache2/custom/$ligne
Alias /$ligne /sites/$ligne
Alias /php7-$ligne.fastcgi /var/lib/apache2/fastcgi/php7-$ligne.fastcgi
FastCGIExternalServer /var/lib/apache2/fastcgi/php7-$ligne.fastcgi -socket /var/run/php7-fpm-$ligne.sock -idle-timeout 60
Action php-script-$ligne /php7-$ligne.fastcgi
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
touch /etc/php/7.0/fpm/pool.d/custom/$ligne.conf 
touch /etc/apache2/custom/$ligne.directory 
touch /etc/apache2/custom/$ligne 
  

# Creation du dossier pour les sessions

mkdir -p /sites/sessions/$ligne 
chown $ligne.web /sites/sessions/$ligne
chmod 2750 /sites/sessions/$ligne 


# Activation de l'alias

a2ensite $ligne

done < '/root/assos.list'""")

	# reload php-fpm
  sudo("service php5-fpm reload")
  sudo("service php7.0-fpm reload")
  # reload apache2
  sudo("service apache2 reload")

@task
@roles('php')
def change_for_python(login_asso):
  sudo('sed -i "s/%s php5/%s python/g; s/%s php7/%s python/g" /root/assos.list' % (login_asso, login_asso))
  generate_vhost_web()

@task
@roles('php')
def change_for_php(login_asso, php_version):
  if php_version == 7:
    sudo('sed -i "s/%s python/%s php7/g; s/%s php5/%s php7/g" /root/assos.list' % (login_asso, login_asso, login_asso, login_asso))
  elif php_version == 5:
    sudo('sed -i "s/%s python/%s php5/g; s/%s php7/%s php5/g" /root/assos.list' % (login_asso, login_asso, login_asso, login_asso))   
  else:
    print "Wrong PHP version"
  generate_vhost_web()





