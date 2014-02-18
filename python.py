# coding=utf-8

from fabric.api import *
from contextlib import nested

@task(default=True)
@roles('python')
def main():
  print("python.main")

@task
@roles('python')
def add_user(login_asso):
  print("Création du site python de l'utilisateur")
  with nested(cd('/root/python-hosting'), prefix('source env/bin/activate')):
         sudo('./manage.py %s create' % (login_asso))
         sudo('./manage.py %s enable' % (login_asso))
