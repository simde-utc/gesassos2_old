# coding=utf-8

from fabric.api import *
import gen_mdp

@task(default=True)
@roles('files')
def main():
  print("files.main")

@task  
@roles('files')
def add_user(login_asso, mdp):
  env.host_string = 'files.mde.utc'
  sudo('smbldap-useradd -a -d /assos/%s -A1 %s' % (login_asso, login_asso))  
  sudo('echo -ne "%s\n%s\n" | smbpasswd -s %s' % (mdp, mdp, login_asso))
  sudo('mkdir -p /assos/%s' % login_asso)
  sudo('mkdir -p /sites/%s' % login_asso)
  sudo('mkdir -p /sites/sessions/%s' % login_asso)
  sudo('chown -R %s:"Domain Users" /assos/%s' % (login_asso, login_asso))
  sudo('chown -R %s:web /sites/%s' % (login_asso, login_asso))
  sudo('chown -R %s:web /sites/sessions/%s' % (login_asso, login_asso))
  sudo('chmod 0700 -R /assos/%s' % login_asso)
  sudo('chmod 2750 -R /sites/%s' % login_asso)
  sudo('chmod 2750 -R /sites/sessions/%s' % login_asso)
  sudo("echo \"<?php\nheader('Location: http://assos.utc.fr/asso/%s');\n?>\" > /sites/%s/index.php" % (login_asso, login_asso))
  sudo('chown %s:web /sites/%s/index.php' % (login_asso, login_asso))
  sudo('chmod 0640 /sites/%s/index.php' % login_asso)
  sudo('ln -s /sites/%s /assos/%s/public_html' % (login_asso, login_asso))

@task  
@roles('files')
def del_user(login_asso):
  env.host_string = 'files.mde.utc'
  sudo('smbldap-userdel %s' % login_asso)
  sudo('rm -R /assos/%s' % login_asso)
  sudo('rm -R /sites/%s' % login_asso)
  sudo('rm -R /sites/sessions/%s' % login_asso)

@task  
@roles('files')
def change_passwd(login_asso, mdp):
  print("Le mdp va être changé")
  sudo('echo -ne "%s\n%s\n" | smbpasswd -s %s' % (mdp, mdp, login_asso))
