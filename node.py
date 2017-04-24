# coding=utf-8

from fabric.api import *
from contextlib import nested

@task(default=True)
@roles('node')
def main():
  print("node.main")

@task
@roles('node')
def add_user(login_asso):
  print("Création du site node de l'utilisateur")
  print("TODO")

@task
@roles('node')
def del_user(login_asso):
  print("Desactivation du site node de l'utilisateur")
  print("TODO")
