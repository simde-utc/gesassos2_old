from fabric.api import *

@task(default=True)
@roles('portail')
def main():
  print("portail.main")
  
def add_portail(login):
  print("Ajout sql dans la base du portail pour la redirection avec le reverse proxy")
  sudo('echo %s >> /root/assos.list' % (login))
  sudo('/root/generate_vhost_portail.sh')
  #generate_vhost_portail()

def generate_vhost_portail():
	sudo("while read -r line do cat > /etc/nginx/assos/${line}.conf <<EOF location /${line}/ {  #more_set_input_headers 'Host: ${line}.\$http_host';  #rewrite      ^/${line}/(.*)$  /\$1  break;  proxy_pass      http://web.mde.utc; } EOF done < '/root/assos.list'")
	sudo('service nginx reload')








