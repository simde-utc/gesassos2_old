# coding=utf-8

from fabric.api import *
import MySQLdb
import gen_mdp

@task(default=True)
@roles('sql')
def main():
  print("sql.main") 

def add_sql(login, mdp2):
  print("connexion au compte gesassos et creation du nouveau User")
  db=MySQLdb.connect(host=env.config['mysql']['host'], user=env.config['mysql']['username'], passwd=env.config['mysql']['password'])
  c=db.cursor()
  #c.execute("CALL createUser('%s','%s')" % (login, mdp2))
  c.execute("DELIMITER $$ CREATE PROCEDURE `createUser`(in varLogin char(16), in varPassword char(64) ) SQL SECURITY DEFINER BEGIN  # Ajout du user INSERT INTO mysql.user (Host, User, Password) VALUES('%.mde.utc', %s, PASSWORD(%s)); INSERT INTO mysql.db (Host, Db , User , Select_priv , Insert_priv , Update_priv , Delete_priv , Create_priv , Drop_priv , Grant_priv , References_priv , Index_priv , Alter_priv , Create_tmp_table_priv , Lock_tables_priv , Create_view_priv , Show_view_priv , Create_routine_priv , Alter_routine_priv , Execute_priv , Event_priv , Trigger_priv ) VALUES ('%.mde.utc', %s, %s ,'Y','Y','Y','Y','Y','Y','N','Y','Y','Y','Y','Y','Y','Y','Y','Y','Y','Y','Y'); FLUSH PRIVILEGES; END$$ DELIMITER ;" % (login, mdp2, login, mdp2))
  c.close()
  db.close()
  db=MySQLdb.connect(host=env.config.mysql.host, user=login, passwd=mdp2)
  c=db.cursor()
  c.execute("CREATE DATABASE %s " % login)
  c.close()
  db.close()

def add_to_portal(login):
  print("Ajout a la base du portail")
  db=MySQLdb.connect(host=env.config['mysql']['host'], user=env.config['mysql']['username'], passwd=env.config['mysql']['password'], db="portail")
  c=db.cursor()
  print("ajout dans la bdd du portail")
  c.execute("SELECT pole.id, asso.name FROM pole INNER JOIN asso ON asso.id = pole.asso_id")
  print(c.fetchall())
  num_pole = input("Entrez le numero du pole de l'asso a creer : ")
  nom_asso = raw_input("Entrez le nom de l'asso pour le portail : ")
  c.execute("INSERT INTO asso (name, login, pole_id, active, created_at, updated_at) values ('%s', '%s', '%d', 1, NOW(), NOW())" % (nom_asso, login, num_pole))
  c.close()
  db.close()

def change_passwd(login, mdp):
  print("Changement du mot de passe de la bdd de l'asso")
  db=MySQLdb.connect(host=env.config['mysql']['host'], user=env.config['mysql']['username'], passwd=env.config['mysql']['password'])
  c=db.cursor()
  print("changement du password sql de l'asso")
  #c.execute("CALL changePassword(%s, %s)" % (login, mdp))
  c.execute("DELIMITER $$ CREATE PROCEDURE `changePassword`(in varLogin char(16), in varPassword char(64) ) SQL SECURITY DEFINER BEGIN UPDATE mysql.user SET Password = PASSWORD(%s) WHERE Host LIKE '%.mde.utc' AND User LIKE %s; FLUSH PRIVILEGES; END$$ DELIMITER ;" % (mdp, login))
  c.close()
  db.close()

