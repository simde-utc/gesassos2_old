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
cat > /etc/nginx/assos/${line}.conf <<EOF
location /${line}/ {
  proxy_pass      http://web.mde.utc;
}
EOF

cat > /etc/nginx/assos/${line}.conf-ssl <<EOF
location /${line}/ {
  proxy_pass      https://web.mde.utc;
}
EOF
done < '/root/assos.list'""")
	
	sudo('service nginx reload')








