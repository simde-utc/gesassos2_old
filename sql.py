from fabric.api import *
import MySQLdb
import gen_mdp

@task(default=True)
@roles('sql')
def main():
  print("sql.main") 

def add_sql(login, mdp2):
  print("connexion au compte gesassos et creation du nouveau User")
  db=MySQLdb.connect(host=env.config.mysql.host, user=env.config.mysql.username, passwd=env.config.mysql.password,db="")
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
  print("Ajout a la base du portail")
  db=MySQLdb.connect(host=env.config.mysql.host, user=env.config.mysql.username, passwd=env.config.mysql.password,db="portail")
  c=db.cursor()
  print("ajout dans la bdd du portail")
  c.execute("INSERT INTO asso (login, active) values (%s, 1)" % (login)) #necessaire le created at ? remplit automatiquement par sql a la creation de l'entree ?
  c.close()
  db.close()

def change_passwd(login, mdp):
  print("Changement du mot de passe de la bdd de l'asso")
  db=MySQLdb.connect(host=env.config.mysql.host, user=env.config.mysql.username, passwd=env.config.mysql.password,db="") #ajouter db
  c=db.cursor()
  print("changement du password sql de l'asso")
  c.execute("CALL changePassword(%s, %s)" % (login, mdp))
  c.close()
  db.close()

