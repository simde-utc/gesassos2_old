from fabric.api import *

@task(default=True)
@roles('web')
def main():
  print("web.main")

def add_web(login):
  print("Ajout des fichiers de conf apache")
  
def activer_web(login):
  print("a2ensite et reload")