from fabric.api import *
import MySQLdb
import gen_mdp

@task(default=True)
@roles('sql')
def main():
  print("sql.main") 

def add_sql(login, mdp2):
  print("connexion au compte gesassos et creation du nouveau User")
  db=MySQLdb.connect(host=env.config.mysql.host, user=env.config.mysql.username, passwd=env.config.mysql.password)
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
  c.execute("SELECT pole.id, asso.name FROM pole INNER JOIN asso ON asso.id = pole.asso_id")
  num_pole = input("Entrez le numero du pole de l'asso à creer : ")
  name = raw_input("Entrez le nom de l'asso pour le portail : ")
  c.execute("INSERT INTO asso (name, login, pole_id, active, created_at, updated_at) values (%s, %s, %d, 1, NOW(), NOW())" % (name, login, num_pole)) #necessaire le created at ? remplit automatiquement par sql a la creation de l'entree ?
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

