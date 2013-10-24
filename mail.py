from fabric.api import *
import MySQLdb
import gen_mdp
import send_email


@task(default=True)
@roles('mail')
def main():
  print("mail.main")


def add_mail(login):
  sudo('mkdir /mails/%s' % login)
  sudo('chown -R %s:"Domain Users" /mails/%s' % (login, login))
  sudo('chmod 0700 -R /mails/%s' % login)
  
def add_assotous(login):  
  print("connexion a la bdd mailman")
  mdp = gen_mdp(8)
  db=MySQLdb.connect(host=env.config.mysql.host, user=env.config.mysql.username, passwd=env.config.mysql.password,db="mailman")
  c=db.cursor()
  print("ajout dans la bdd mailman")
  c.execute("INSERT INTO mailman_mysql (listname, address, hide, nomail, ack, not_metoo, digest, plain, password, lang, name, one_last_digest, user_options, delivery_status, topics_userinterest, delivery_status_timestamp, bi_cookie, bi_score, bi_noticesleft, bi_lastnotice, bi_date) VALUES ('asso-tous', '$login@assos.utc.fr', 'N', 'N', 'Y', 'Y', 'N', 'N', %s, 'fr', '', 'N', '264', '0', NULL, '0000-00-00 00:00:00', NULL, '0', '0', '0000-00-00', '0000-00-00')" % mdp)
  c.close()
  db.close()

def howto_signup(president):
  print("envoi du mail au president pour lui dire d'aller signer la charte")
  to = president + "@etu.utc.fr"
  msg = """From: Simde <simde@assos.utc.fr>
To: <""" + to + """>
Subject: Signature de la charte

Le compte de votre asso a ete precre, veuillez signer la charte en suivant la procedure suivante
http://assos.utc.fr/simde/wiki/signaturecharte

Une fois cela fait envoye nous un mail pour que nous puissions valider et finir la creation du compte

Bonne journee
"""
  send_email.send_email("simde@assos.utc.fr", to, msg)

def send_passwords(president, mdp1, mdp2):
  print('Envoi des passwords au president de l\'asso')
  to = president + "@etu.utc.fr"
  msg = """From: Simde <simde@assos.utc.fr>
To: <""" + to + """>
Subject: Passwords du nouveau compte asso

Le compte de votre asso a ete cree.

Voici les mots de passe associes :
 - compte asso : """ + mdp1 + """
 - base de donnee sql : """ + mdp2 + """

Pour toute question n'hesitez pas a consulter le wiki du simde :
http://assos.utc.fr/simde/wiki/accueil

Bonne journee
"""
  send_email.send_email("simde@assos.utc.fr", to, msg)

def send_new_password_asso(president, mdp):
  print('Envoi du nouveau password asso au president de l\'asso')
  to = president + "@etu.utc.fr"
  msg = """From: Simde <simde@assos.utc.fr>
To: <""" + to + """>
Subject: Changement du password du compte asso

Le mot de passe du compte asso a ete change.

Voici le nouveau mot de passe : """ + mdp + """

Pour toute question n'hesitez pas a consulter le wiki du simde :
http://assos.utc.fr/simde/wiki/accueil

Bonne journee
"""
  send_email.send_email("simde@assos.utc.fr", to, msg)

def send_new_password_sql(president, mdp):
  print('Envoi du nouveau password sql au president de l\'asso')
  to = president + "@etu.utc.fr"
  msg = """From: Simde <simde@assos.utc.fr>
To: <""" + to + """>
Subject: Changement du password de la base de donnee

Le mot de passe de la base de donnee a ete change.

Voici le nouveau mot de passe : """ + mdp + """

Pour toute question n'hesitez pas a consulter le wiki du simde :
http://assos.utc.fr/simde/wiki/accueil

Bonne journee
"""
  send_email.send_email("simde@assos.utc.fr", to, msg)