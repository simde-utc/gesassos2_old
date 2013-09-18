from fabric.api import *

@task(default=True)
@roles('web')
def main():
  print("web.main")

def add_web(login):
  print("Ajout des fichiers de conf apache")
  sudo('sed "s/LOGIN/%s/g" /root/modele.suphp > /etc/apache2/custom/%s.suphp' % (login,login))
  sudo('echo %s >> /root/assos.list' % (login))
  #sudo('/root/generate_vhost.sh')


  
def activer_web(login):
  print("a2ensite et reload")