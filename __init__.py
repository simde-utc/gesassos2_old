from fabric.contrib.console import confirm

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
  files.add_user(login)
  mail.add_mail(login)
  mail.add_assotous(login)
  web.add_web(login)
  sql.add_sql(login)
  mail.send_passwords(login, president)

