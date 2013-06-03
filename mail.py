from fabric.api import *

@task(default=True)
@roles('mail')
def main():
  print("mail.main")
  
def gen_mdp(length):
	print("le generateur")
	# 26 lettres majuscules + 26 lettres minuscules + 10 chiffres [0..9] = 62
	letters = string.printable[:62]
	password = ''
	for ununsed_count in range(length):
		password += letters[random.randint(0, len(letters) - 1)]
	return password

def add_mail(login):
  sudo('mkdir /mails/%s' % login)
  sudo('chown -R %s:"Domain Users" /mails/%s' % (login, login))
  sudo('chmod 0700 -R /mails/%s' % login)
  
def add_assotous(login):  
  print("connexion a la bdd mailman")
  sudo("mysql -u gesassos -p %s --execute='CONNECT gesassos'" % (password))
  print("ajout dans la bdd mailman")
  mdp = gen_mdp(8)
  sudo("mysql -u gesassos -p %s --execute='INSERT INTO mailman_mysql (listname, address, hide, nomail, ack, not_metoo, digest, plain, password, lang, name, one_last_digest, user_options, delivery_status, topics_userinterest, delivery_status_timestamp, bi_cookie, bi_score, bi_noticesleft, bi_lastnotice, bi_date) VALUES (‘asso-tous’, ‘$login@assos.utc.fr’, 'N', 'N', 'Y', 'Y', 'N', 'N', %s, 'fr', '', 'N', '264', '0', NULL, '0000-00-00 00:00:00', NULL, '0', '0', '0000-00-00', '0000-00-00')'" % (password, mdp))