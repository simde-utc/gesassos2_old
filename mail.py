from fabric.api import *

@task(default=True)
@roles('mail')
def main():
  print("mail.main")

def add_mail(login):
  print("creation dossiers")
  
def add_assotous(login):
  print("ajout dans la bdd mailman")