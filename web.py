from fabric.api import *

@task(default=True)
@roles('web')
def main():
  print("web.main")
