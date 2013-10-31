from fabric.api import *

@task(default=True)
@roles('web')
def main():
  print("web.main")

def add_web(login_asso):
  print("Ajout des fichiers de conf apache")
  sudo('sed "s/LOGIN/%s/g" /root/modele.suphp > /etc/apache2/custom/%s.suphp' % (login_asso,login_asso))
  sudo('echo %s >> /root/assos.list' % (login_asso))
  sudo('/root/generate_vhost_web.sh')
  #generate_vhost_web()

def generate_vhost_web():
	# Pool php-fpm
	sudo("while read -r line do cat > /etc/php5/fpm/pool.d/${line}.conf <<EOF [${line}] user = ${line} group = web listen = /var/run/php-fpm-${line}.sock pm = ondemand pm.max_children = 5 pm.process_idle_timeout = 10s chroot= chdir = / php_value[session.save_path] = /sites/sessions/${line} php_value[session.cookie_path] = /${line} include=/etc/php5/fpm/pool.d/custom/${line}.conf EOF done < '/root/assos.list'")
	
	# Config apache
	sudo("while read -r line do cat > /etc/apache2/sites-available/${line} <<EOF Include /etc/apache2/custom/${line} Alias /${line} /sites/${line} Alias /php5-${line}.fastcgi /var/lib/apache2/fastcgi/php5-${line}.fastcgi FastCGIExternalServer /var/lib/apache2/fastcgi/php5-${line}.fastcgi -socket /var/run/php-fpm-${line}.sock -idle-timeout 60 Action php-script-${line} /php5-${line}.fastcgi <Directory /sites/${line}> AddHandler php-script-${line} .php Options FollowSymLinks AllowOverride All Order allow,deny Allow from all Include /etc/apache2/custom/${line}.directory </Directory> EOF done < '/root/assos.list'")
	
	# Creation des fichiers de config custom
	sudo("while read -r line do touch /etc/apache2/custom/${line}.directory done < '/root/assos.list'")
	sudo("while read -r line do touch /etc/apache2/custom/${line} done < '/root/assos.list'")
	sudo("while read -r line do touch /etc/php5/fpm/pool.d/custom/${line}.conf done < '/root/assos.list'")
	
	# Creation du dossier pour les sessions
	sudo("while read -r line do mkdir -p /sites/sessions/${line} done < '/root/assos.list'")
	sudo("while read -r line do chown ${line}.web /sites/sessions/${line} done < '/root/assos.list'")
	sudo("while read -r line do chmod 2750 /sites/sessions/${line} done < '/root/assos.list'")
	
	# Activation de l'alias
	sudo("while read -r line do a2ensite ${line} done < '/root/assos.list'")
	
	# reload php-fpm
	sudo("service php5-fpm reload")
	
	# reload apache2
	sudo("service apache2 reload")





