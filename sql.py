from fabric.api import *
import random
import string

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
  sudo("mysql -u gesassos -p %s --execute='CONNECT gesassos'" % (password))
  sudo("mysql -u gesassos -p %s --execute='CALL createUser('%s','%s');' " % (password, login, mdp))
  sudo("mysql -u %s -p %s --execute='CREATE DATABASE %s;' " % (login, mdp, login))