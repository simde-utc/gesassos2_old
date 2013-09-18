from fabric.api import *

@task(default=True)
@roles('portail')
def main():
  print("portail.main")
  
def add_portail(login):
  print("Ajout sql dans la base du portail")
  sudo('echo %s >> /root/assos.list' % (login)) // a revoir si un seul fichier sur le serveur, créer un autre .py ?
  //sudo('/root/generate_vhost.sh')





