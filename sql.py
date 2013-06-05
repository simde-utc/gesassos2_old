from fabric.api import *
import random
import string
import MySQLdb

@task(default=True)
@roles('sql')
def main():
  print("sql.main") 
  
def gen_mdp(length):
	print("le generateur")
	# 26 lettres majuscules + 26 lettres minuscules + 10 chiffres [0..9] = 62
	letters = string.printable[:62]
	password = ''
	for ununsed_count in range(length):
		password += letters[random.randint(0, len(letters) - 1)]
	return password

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