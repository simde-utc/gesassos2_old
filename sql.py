# coding=utf-8

from fabric.api import *
import MySQLdb
import gen_mdp

@task(default=True)
@roles('sql')
def main():
  print("sql.main") 

@task
@roles('sql')
def add_sql(login_asso, mdp):
  print("connexion au compte gesassos et creation du nouveau User")
  db=MySQLdb.connect(host=env.config['mysql']['host'], user=env.config['mysql']['username'], passwd=env.config['mysql']['password'], db='gesassos')
  c=db.cursor()
  c.execute("CALL createUser('%s','%s')" % (login_asso, mdp))
  c.close()
  db.close()
  db=MySQLdb.connect(host=env.config['mysql']['host'], user=login_asso, passwd=mdp)
  c=db.cursor()
  c.execute("CREATE DATABASE %s " % login_asso)
  c.close()
  db.close()

@task
@roles('sql')
def add_to_portal(login_asso):
  print("Ajout a la base du portail")
  db=MySQLdb.connect(host=env.config['mysql']['host'], user=env.config['mysql']['username'], passwd=env.config['mysql']['password'], db="portail")
  c=db.cursor()
  print("ajout dans la bdd du portail")
  c.execute("SELECT pole.id, asso.name FROM pole INNER JOIN asso ON asso.id = pole.asso_id")
  print(c.fetchall())
  num_pole = input("Entrez le numero du pole de l'asso a creer : ")
  nom_asso = raw_input("Entrez le nom de l'asso pour le portail : ")
  c.execute("INSERT INTO asso (name, login, pole_id, active, created_at, updated_at) values ('%s', '%s', '%d', 1, NOW(), NOW())" % (nom_asso, login_asso, num_pole))
  db.commit()
  c.close()
  db.close()

@task
@roles('sql')
def change_passwd(login_asso, mdp):
  print("changement du password sql de l'asso")
  db=MySQLdb.connect(host=env.config['mysql']['host'], user=env.config['mysql']['username'], passwd=env.config['mysql']['password'], db='gesassos')
  c=db.cursor()
  c.execute("CALL changePassword('%s', '%s')" % (login_asso, mdp))
  c.close()
  db.close()

@task
@roles('sql')
def get_asso_president(login_asso):
  print("Affichage du président de l'asso")
  db=MySQLdb.connect(host=env.config['mysql']['host'], user=env.config['mysql']['username'], passwd=env.config['mysql']['password'], db="portail")
  c=db.cursor()
  c.execute("SELECT date, confirmation, login, asso_name FROM charte_info WHERE asso_name = '%s' ORDER BY id DESC" % (login_asso))
  print(c.fetchall())  
  login_president = raw_input("Entrez le nom du président actuel de l'asso : ")
  c.close()
  db.close()
  return login_president

