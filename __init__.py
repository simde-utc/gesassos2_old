from fabric.contrib.console import confirm
from fabric.operations import prompt, sudo
from fabric.api import *
from fabric.state import env

import files, web, portail, mail, sql
import config

env.use_ssh_config = True
env.roledefs = {
  'portail': ['portail.mde.utc'],
  'web': ['web.mde.utc'],
  'files': ['files.mde.utc'],
  'mail': ['mail.mde.utc'],
  'sql': ['sql.mde.utc'],
}

@task(default=True)
@runs_once
def main():
  print("Run 'fab list' to see all commands")

@task
@runs_once
def precreate_asso(login, president):
  sql.add_to_portal(login)
  mail.howto_signup(president)

@task
@runs_once
def create_asso(login, president):
  confirm("Did the president signup the charter ?",False)
  confirm("Are you sure the asso does not exist already ?", False)
  mdp1 = gen_mdp(8)
  mdp2 = gen_mdp(8)
  files.add_user(login, mdp1)
  mail.add_mail(login)
  mail.add_assotous(login)
  web.add_web(login)
  portail.add_portail(login)
  sql.add_sql(login, mdp2)
  mail.send_passwords(login, president, mdp1, mdp2)
  
@task
@runs_once
def change_password_asso(login, president):
  confirm("Did the president signup the charter ?",False)
  mdp = gen_mdp(8)
  files.change_passwd(login, mdp)
  mail.send_new_password_asso(login, president, mdp)

@task
@runs_once
def change_password_mysql(login, president):
  confirm("Did the president signup the charter ?",False)
  mdp = gen_mdp(8)
  sql.change_passwd(login, mdp)
  mail.send_new_password_sql(login, president, mdp)


@task
@runs_once
def install_modif_generate_vhost():
  put('generate_vhost_web.sh', '/root/generate_vhost_web.sh', True)
  put('generate_vhost_portail.sh', '/root/generate_vhost_portail.sh', True)

