from fabric.api import *

@task(default=True)
@roles('sql')
def main():
  print("sql.main")

def add_sql(login, password):
  print("generation mot de passse et appel de la procedure")