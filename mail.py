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
  db=MySQLdb.connect(user=env.config.mysql.username, passwd=env.config.mysql.password,db="mailman") #ajouter hostname
  c=db.cursor()
  print("ajout dans la bdd mailman")
  c.execute("INSERT INTO mailman_mysql (listname, address, hide, nomail, ack, not_metoo, digest, plain, password, lang, name, one_last_digest, user_options, delivery_status, topics_userinterest, delivery_status_timestamp, bi_cookie, bi_score, bi_noticesleft, bi_lastnotice, bi_date) VALUES (‘asso-tous’, ‘$login@assos.utc.fr’, 'N', 'N', 'Y', 'Y', 'N', 'N', %s, 'fr', '', 'N', '264', '0', NULL, '0000-00-00 00:00:00', NULL, '0', '0', '0000-00-00', '0000-00-00')" % mdp)
  c.close()
  db.close()

def howto_signup(president):
  print("envoi du mail au président pour lui dire d'aller signer la charte")
  to = president + "@etu.utc.fr"
  msg = """From: Simde <simde@assos.utc.fr>
To: <""" + to + """>
Subject: Signature de la charte

Le compte de votre asso a été précré, veuillez signer la charte en suivant la procédure suivante
http://assos.utc.fr/simde/wiki/signaturecharte

Une fois cela fait envoyé nous un mail pour que nous puissions valider et finir la création du compte

Bonne journée
"""
  send_email("simde@assos.utc.fr", to, msg)

def send_passwords(president, mdp1, mdp2):
  print('Envoi des passwords au président de l\'asso')
  to = president + "@etu.utc.fr"
  msg = """From: Simde <simde@assos.utc.fr>
To: <""" + to + """>
Subject: Passwords du nouveau compte asso

Le compte de votre asso a été créé.

Voici les mots de passe associés :
 - compte asso : """ + mdp1 + """
 - base de donnée sql : """ + mdp2 + """

Pour toute question n'hésitez pas à consulter le wiki du simde :
http://assos.utc.fr/simde/wiki/accueil

Bonne journée
"""
  send_email("simde@assos.utc.fr", to, msg)

def send_new_password_asso(president, mdp):
  print('Envoi du nouveau password asso au président de l\'asso')
  to = president + "@etu.utc.fr"
  msg = """From: Simde <simde@assos.utc.fr>
To: <""" + to + """>
Subject: Changement du password du compte asso

Le mot de passe du compte asso a été changé.

Voici le nouveau mot de passe : """ + mdp + """

Pour toute question n'hésitez pas à consulter le wiki du simde :
http://assos.utc.fr/simde/wiki/accueil

Bonne journée
"""
  send_email("simde@assos.utc.fr", to, msg)

def send_new_password_sql(president, mdp):
  print('Envoi du nouveau password sql au président de l\'asso')
  to = president + "@etu.utc.fr"
  msg = """From: Simde <simde@assos.utc.fr>
To: <""" + to + """>
Subject: Changement du password de la base de donnée

Le mot de passe de la base de donnée a été changé.

Voici le nouveau mot de passe : """ + mdp + """

Pour toute question n'hésitez pas à consulter le wiki du simde :
http://assos.utc.fr/simde/wiki/accueil

Bonne journée
"""
  send_email("simde@assos.utc.fr", to, msg)