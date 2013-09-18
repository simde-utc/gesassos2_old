from fabric.api import *

@task(default=True)
@roles('portail')
def main():
  print("portail.main")
  
def add_portail(login):
  print("Ajout sql dans la base du portail pour la redirection avec le reverse proxy")
  sudo('echo %s >> /root/assos.list' % (login))
  sudo('/root/generate_vhost_portail.sh')





