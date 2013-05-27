from fabric.api import *

@task(default=True)
@roles('files')
def main():
  print("files.main")
  
def add_user(login):
  env.host_string = 'files.mde.utc'
  sudo('smbldap-useradd  -a -d /assos/%s -A1 %s' % (login, login))
  sudo('mkdir /assos/%s' % login)
  sudo('mkdir /sites/%s' % login)
  sudo('mkdir /sites/sessions/%s' % login)
  sudo('chown -R %s:"Domain Users" /assos/%s' % (login, login))
  sudo('chown -R %s:web /sites/%s' % (login, login))
  sudo('chown -R %s:web /sites/sessions/%s' % (login, login))
  sudo('chmod 0700 -R /assos/%s' % login)
  sudo('chmod 2750 -R /sites/%s' % login)
  sudo('chmod 2750 -R /sites/sessions/%s' % login)
  sudo("echo \"<?php\nheader('Location: http://assos.utc.fr/asso/%s');\n?>\" > /sites/%s/index.php" % (login, login))
  sudo('chown %s /sites/%s/index.php' % (login, login))
  sudo('ln -s /sites/%s /assos/%s/public_html' % (login, login))
