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
def generate_vhost_portail():
	sudo("""while read -r line
do
ligne=`echo ${line}|grep -v "python"|awk -F " " '{print $1}'`

cat > /etc/nginx/assos/$ligne.conf <<EOF
location /${line}/ {
  proxy_pass      http://web.mde.utc;
}
EOF

cat > /etc/nginx/assos/$ligne.conf-ssl <<EOF
location /${line}/ {
  proxy_pass      https://web.mde.utc;
}
EOF


ligne=`echo ${line}|grep "python"|awk -F " " '{print $1}'`

cat > /etc/nginx/assos/$ligne.conf <<EOF
location /${line}/ {
  proxy_pass      http://python.mde.utc;
}
EOF

done < '/root/assos.list'""")
	
	sudo('service nginx reload')

@task
@roles('portail')
def change_for_python(login_asso):
  print("Le site sera desormais en python")
  sudo('sed -i "s/%s/%s python/" /root/assos.list' % (login_asso, login_asso))

@task
@roles('portail')
def change_for_php(login_asso):
  print("Le site sera desormais en php")
  sudo('sed -i "s/%s python/%s/" /root/assos.list' % (login_asso, login_asso))








