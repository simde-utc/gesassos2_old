from fabric.api import *

@task(default=True)
@roles('portail')
def main():
  print("portail.main")
  
@task
@roles('portail')
def add_portail(login_asso):
  print("Ajout sql dans la base du portail pour la redirection avec le reverse proxy")
  sudo('echo %s >> /root/assos.list' % (login_asso))
  generate_vhost_portail()

@task
@roles('portail')
def del_portail(login_asso):
  print("Suppression sql dans la base du portail pour la redirection avec le reverse proxy")
  sudo("sed '/%s/d' /root/assos.list" % login_asso)
  generate_vhost_portail()

@task
@roles('portail')
def generate_vhost_portail():
	sudo("""while read -r line
do
ligne=`echo ${line}|grep -v "python"|grep -v "nodejs"|awk -F " " '{print $1}'`

cat > /etc/nginx/assos/$ligne.conf <<EOF
location /$ligne/ {
  proxy_pass      http://web.mde.utc;
}
EOF

cat > /etc/nginx/assos/$ligne.conf-ssl <<EOF
location /$ligne/ {
  proxy_pass      https://web.mde.utc;
}
EOF


ligne=`echo ${line}|grep "python"|awk -F " " '{print $1}'`

cat > /etc/nginx/assos/$ligne.conf <<EOF
location /$ligne/ {
  proxy_pass      http://python.mde.utc;
}
EOF

cat > /etc/nginx/assos/$ligne.conf-ssl <<EOF
location /$ligne/ {
  proxy_pass      http://python.mde.utc;
}
EOF


ligne=`echo ${line}|grep "nodejs"|awk -F " " '{print $1}'`

cat > /etc/nginx/assos/$ligne.conf <<EOF
location /$ligne/ {
  proxy_pass      http://nodejs.mde.utc;
}
EOF

cat > /etc/nginx/assos/$ligne.conf-ssl <<EOF
location /$ligne/ {
  proxy_pass      http://nodejs.mde.utc;
}
EOF

done < '/root/assos.list'""")
	
	sudo('service nginx reload')

@task
@roles('portail')
def change_for_python(login_asso):
  print("Le site sera desormais en python")
  sudo('sed -i "s/%s nodejs/%s/" /root/assos.list' % (login_asso, login_asso)) # if currently Nodejs
  sudo('sed -i "s/%s/%s python/" /root/assos.list' % (login_asso, login_asso))
  generate_vhost_portail()

@task
@roles('portail')
def change_for_php(login_asso):
  print("Le site sera desormais en php")
  sudo('sed -i "s/%s python/%s/" /root/assos.list' % (login_asso, login_asso))
  sudo('sed -i "s/%s nodejs/%s/" /root/assos.list' % (login_asso, login_asso))
  generate_vhost_portail()

@task
@roles('portail')
def change_for_nodejs(login_asso):
  print("Le site sera desormais en nodejs")
  sudo('sed -i "s/%s python/%s/" /root/assos.list' % (login_asso, login_asso)) # if currently Python
  sudo('sed -i "s/%s/%s nodejs/" /root/assos.list' % (login_asso, login_asso))
  generate_vhost_portail()








