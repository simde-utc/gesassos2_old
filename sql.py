from fabric.api import *
import MySQLdb
import gen_mdp.py

@task(default=True)
@roles('sql')
def main():
  print("sql.main") 

def add_sql(login, password):
  print("generation mot de passse et appel de la procedure")
  mdp = gen_mdp(8)
  print("connexion a la bdd gesassos")
  db=MySQLdb.connect(user="gesassos", passwd="",db="gesassos")
  c=db.cursor()
  c.execute("CALL createUser('%s','%s')" % (login, mdp))
  c.close()
  db.close()
  db=MySQLdb.connect(user=login, passwd=mdp)
  c=db.cursor()
  c.execute("CREATE DATABASE %s " % login)
  c.close()
  db.close()