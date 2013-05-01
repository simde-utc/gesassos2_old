from fabric.api import *

@task(default=True)
@roles('mail')
def main():
  print("mail.main")
