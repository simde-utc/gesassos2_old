import ldap
from fabric.operations import prompt, sudo
from fabric.api import *
from fabric.state import env

env.shell = '/bin/bash -c'

def hello():
  print("Yop")

def connect_ldap():
  return ldap.initialize('ldap://ldap.mde.utc')

def search_asso(login='*'):
  con = connect_ldap()
  res = con.search_s('ou=Users,dc=assos,dc=utc,dc=fr',ldap.SCOPE_SUBTREE,'(cn=%s)' % login,['cn','mail']) 
  return map(get_login, res)

def get_login(cn):
  return cn[1]['cn'][0]

@task()
def new_asso():
  newlogin = prompt('Login de l\'asso a ajouter ?', validate=r'^[a-z]+$')
  if search_asso(newlogin) <> []:
    abort('L\'asso existe deja.')
  add_user(newlogin)
  #add_portail
  #add_web
  #add_sql
  #add_mail
  #add_assotous
  #change_pass
  #mail

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

def add_portail(login):
  print("Ajout sql dans la base du portail")

def add_web(login):
  print("Ajout des fichiers de conf apache")

def activer_web(login):
  print("a2ensite et reload")

def add_sql(login, password):
  print("generation mot de passse et appel de la procedure")

def add_mail(login):
  print("creation dossiers")

def add_assotous(login):
  print("ajout dans la bdd mailman")

def change_pass(login, password):
  print("changer mdp avec smbpasswd")

def mail(login):
  print("mail des mots de passe au president")

def gen_password(length):
  return "aaaa"
