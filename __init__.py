from fabric.api import *
from fabric.colors import red, green

import old
import files, web, portail, mail, sql

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


