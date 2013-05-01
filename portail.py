from fabric.api import *

@task(default=True)
@roles('portail')
def main():
  print("portail.main")
