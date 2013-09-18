from fabric.api import *
import MySQLdb
import gen_mdp.py

@task(default=True)
@roles('sql')
def main():
  print("sql.main") 

def add_sql(login, mdp2):
  print("connexion a la bdd gesassos")
  db=MySQLdb.connect(user=env.config.mysql.username, passwd=env.config.mysql.password,db="") # hostname et db à completer
  c=db.cursor()
  c.execute("CALL createUser('%s','%s')" % (login, mdp2))
  c.close()
  db.close()
  db=MySQLdb.connect(user=login, passwd=mdp2)
  c=db.cursor()
  c.execute("CREATE DATABASE %s " % login)
  c.close()
  db.close()

def add_to_portal(login):
  print("Ajout à la base du portail")
  db=MySQLdb.connect(user=env.config.mysql.username, passwd=env.config.mysql.password,db="portail") #ajouter hostname
  c=db.cursor()
  print("ajout dans la bdd du portail")
  c.execute("INSERT INTO asso (login, active) values (%s, 1)" % (login)) #nécessaire le created at ? remplit automatiquement par sql à la creation de l'entrée ?
  c.close()
  db.close()

def change_passwd(login, mdp):
  print("Changement du mot de passe de la bdd de l'asso")

