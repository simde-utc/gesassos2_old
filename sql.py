# coding=utf-8

from fabric.api import *
import MySQLdb
import gen_mdp
from datetime import datetime

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
  get_poles()
  num_pole = input("Entrez le numero du pole de l'asso a creer : ")
  nom_asso = raw_input("Entrez le nom de l'asso pour le portail : ")
  c.execute("INSERT INTO asso (name, login, pole_id, active, created_at, updated_at) values ('%s', '%s', '%d', 1, NOW(), NOW())" % (nom_asso, login_asso, num_pole))
  db.commit()
  c.close()
  db.close()

@task
@roles('sql')
def get_poles():
  db=MySQLdb.connect(host=env.config['mysql']['host'], user=env.config['mysql']['username'], passwd=env.config['mysql']['password'], db="portail")
  c=db.cursor()
  c.execute("SELECT pole.id, asso.name FROM pole INNER JOIN asso ON asso.id = pole.asso_id")
  for pole in c:
    print('{0} correspond au pole {1}'.format(pole[0], pole[1]))
  c.close()
  db.close()

@task
@roles('sql')
def del_sql(login_asso):
  try:
    print("Pensez à supprimer à la main le user mysql")
    db=MySQLdb.connect(host=env.config['mysql']['host'], user=login_asso, passwd=mdp)
    c=db.cursor()
    c.execute("DROP DATABASE %s " % login_asso)
    c.close()
    db.close()

@task
@roles('sql')
def del_from_portal(login_asso):
  try:
    print("Désactivation de l'asso en mettant son pole a vide, si vous avez besoin de vraiment le supprimer, il faut le faire à la main dans le backend")
    db=MySQLdb.connect(host=env.config['mysql']['host'], user=env.config['mysql']['username'], passwd=env.config['mysql']['password'], db="portail")
    c=db.cursor()
    c.execute("UPDATE asso SET pole_id=NULL WHERE login='%s'" % login_asso)
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
  c.execute("SELECT date, confirmation, login FROM charte_info WHERE asso_name = '%s' ORDER BY id DESC" % (login_asso))
  # print(c.fetchall()) 
  lastPresident = c.fetchone()
  if not lastPresident:
    abort("Cette asso n'existe pas...")

  lP_date = lastPresident[0]
  lP_confirmation = lastPresident[1]
  lP_login = lastPresident[2]

  now = datetime.now()
  login_president = ""
  if (lP_confirmation == 1): # si confirmé
    if (2 <= now.month <= 9) and (2 <= lP_date.month <= 9) and (lP_date.year == now.year): # si on est au printemp et la déclaration du prez aussi
      login_president = lP_login
    else: # si on est à l'automne dans la même année (on vérifie)
      if  ((9 <= now.month <= 12) and (9 <= lP_date.month <= 12) and (lP_date.year == now.year)) or\
        ((1 <= now.month <= 2) and (1 <= lP_date.month <= 2) and (lP_date.year == now.year)) or\
	((1 <= now.month <= 2) and (9 <= lP_date.month <= 12) and (lP_date.year == now.year-1)):
        login_president = lP_login

  if login_president:
    print('{0} est président(e) depuis le {1}/{2}/{3}'.format( login_president, lP_date.day, lP_date.month, lP_date.year))
  else:
    print('Pas de président confirmé ce semestre, on annule tout...')
    print(lastPresident)
    print(c.fetchall())
    abort("")

  c.close()
  db.close()
  return login_president

