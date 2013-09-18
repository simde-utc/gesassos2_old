from fabric.api import *

@task(default=True)
@roles('portail')
def main():
  print("portail.main")
  
def add_portail(login):
  print("Ajout sql dans la base du portail")
  sudo('echo %s >> /root/assos.list' % (login)) // a revoir si un seul fichier sur le serveur, créer un autre .py ?
  //sudo('/root/generate_vhost.sh')

while (read -r line): // lecture de fichier à faire
  sudo('cat > /etc/nginx/assos/${line}.conf <<EOF')
  sudo('location /${line}/ { proxy_pass      http://web.mde.utc; } EOF')
  #more_set_input_headers 'Host: ${line}.\$http_host';
  #rewrite      ^/${line}/(.*)$  /\$1  break;
  sudo('done < "/root/assos.list"')  
  sudo('service nginx reload')




  while read -r line
do
cat > /etc/nginx/assos/${line}.conf <<EOF
location /${line}/ {
  #more_set_input_headers 'Host: ${line}.\$http_host';
  #rewrite      ^/${line}/(.*)$  /\$1  break;
  proxy_pass      http://web.mde.utc;
}
EOF
done < "/root/assos.list"
service nginx reload



