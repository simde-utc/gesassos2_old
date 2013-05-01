from fabric.api import *

@task(default=True)
@roles('sql')
def main():
  print("sql.main")
