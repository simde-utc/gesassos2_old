from fabric.api import *

@task(default=True)
@roles('files')
def main():
  print("files.main")
