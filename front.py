from fabric.api import *

@task(default=True)
@roles('front')
def main():
  print("front.main")
  
@task
@roles('front')
def add_front(login_asso):
  print("Ajout sql dans la base du front pour la redirection avec le reverse proxy")
  sudo('echo %s php >> /root/assos.list' % (login_asso))
  generate_vhost_front()

@task
@roles('front')
def del_front(login_asso):
  try:
    print("Suppression sql dans la base du front pour la redirection avec le reverse proxy")
    sudo("sed -i '/%s/d' /root/assos.list" % login_asso)
    generate_vhost_front()
  except:
    pass

# Pour chaque ligne de /root/assos.list
# generer un fichier de conf nginx php, python ou node
@task
@roles('front')
def generate_vhost_front():
	sudo("""while read -r line
do
ligne=`echo ${line}|grep "php"|awk -F " " '{print $1}'`

cat > /etc/nginx/assos/$ligne.conf <<EOF
location /$ligne/ {
  proxy_pass      http://10.10.10.107;
}
EOF

ligne=`echo ${line}|grep "python"|awk -F " " '{print $1}'`

cat > /etc/nginx/assos/$ligne.conf <<EOF
location /$ligne/ {
  proxy_pass      http://10.10.10.109;
}
EOF

ligne=`echo ${line}|grep "node"|awk -F " " '{print $1}'`

cat > /etc/nginx/assos/$ligne.conf <<EOF
location /$ligne/ {
  proxy_pass      http://10.10.10.108;
}
EOF

done < '/root/assos.list'""")
	
	sudo('service nginx reload')

@task
@roles('front')
def change_for_python(login_asso):
  print("Le site sera desormais en python")
  sudo('sed -i "s/%s php/%s python/g; s/%s node/%s python/g" /root/assos.list' % (login_asso, login_asso, login_asso, login_asso))
  generate_vhost_front()

@task
@roles('front')
def change_for_php(login_asso):
  print("Le site sera desormais en php")
  sudo('sed -i "s/%s python/%s php/g; s/%s node/%s php/g" /root/assos.list' % (login_asso, login_asso, login_asso, login_asso))
  generate_vhost_front()








