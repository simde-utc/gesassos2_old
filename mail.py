from fabric.api import *
import MySQLdb
import gen_mdp
import send_email


@task(default=True)
@roles('mail')
def main():
  print("mail.main")

@task
@roles('mail')
def add_mail(login_asso):
  sudo('mkdir /mails/%s' % login_asso)
  sudo('chown -R %s:"Domain Users" /mails/%s' % (login_asso, login_asso))
  sudo('chmod 0700 -R /mails/%s' % login_asso)
  
@task
@roles('mail')
def add_assotous(login_asso):  
  print("connexion a la bdd mailman")
  mdp = gen_mdp.gen_mdp(8)
  db=MySQLdb.connect(host=env.config['mysql']['host'], user=env.config['mysql']['username'], passwd=env.config['mysql']['password'], db="mail")
  c=db.cursor() 
  print("ajout dans la bdd mailman")
  c.execute("INSERT INTO mailman_mysql (listname, address, hide, nomail, ack, not_metoo, digest, plain, password, lang, name, one_last_digest, user_options, delivery_status, topics_userinterest, delivery_status_timestamp, bi_cookie, bi_score, bi_noticesleft, bi_lastnotice, bi_date) VALUES ('asso-tous', '%s@assos.utc.fr', 'N', 'N', 'Y', 'Y', 'N', 'N', '%s', 'fr', '', 'N', '392', '0', NULL, '0000-00-00 00:00:00', NULL, '0', '0', '0000-00-00', '0000-00-00')" % (login_asso, mdp))
  db.commit()
  c.close()
  db.close()

@task
@roles('mail')
def del_mail(login_asso):
  try:
    sudo('rm -R /mails/%s' % login_asso)
  except:
    pass
  
@task
@roles('mail')
def del_mailings(login_asso):  
  try:
    db=MySQLdb.connect(host=env.config['mysql']['host'], user=env.config['mysql']['username'], passwd=env.config['mysql']['password'], db="mail")
    c=db.cursor() 
    print("suppression des mailings et redirections ainsi que de l'asso-tous")

    c.execute("DELETE FROM mailman_mysql WHERE listname='asso-tous' AND address='%s@assos.utc.fr'" % login_asso)
    c.execute("DELETE FROM mailman_mysql WHERE listname LIKE '%s%'" % login_asso)
    c.execute("DELETE FROM gesmail WHERE Asso='%s'" % login_asso)
    c.execute("DELETE FROM postfix_alias WHERE alias LIKE '%s%'" % login_asso)
    db.commit()
    c.close()
    db.close()
  except:
    pass

@task
@roles('mail')
def howto_signup(login_president):
  print("envoi du mail au president pour lui dire d'aller signer la charte")
  to = login_president + "@etu.utc.fr"
  msg = """From: SiMDE <simde@assos.utc.fr>
To: <""" + to + """>
Subject: Signature de la charte

Bonjour,

Pour poursuivre la creation de ton compte asso, merci de signer la charte informatique en suivant la procedure suivante :
http://assos.utc.fr/simde/wiki/signaturecharte

Une fois cela fait, elle doit etre validee par le BDE, il faut donc le contacter a cette adresse pour faire la demande :
bde@assos.utc.fr

Cordialement,
L'equipe du SiMDE
"""
  send_email.send_email("simde@assos.utc.fr", to, msg)

@task
@roles('mail')
def send_passwords(login_asso, login_president, mdp1, mdp2):
  print('Envoi des passwords au president de l\'asso')
  to = login_president + "@etu.utc.fr"
  msg = """From: SiMDE <simde@assos.utc.fr>
To: <""" + to + """>
Subject: Creation du compte asso

Bonjour,

Le compte de ton asso a ete cree avec le login """ + login_asso + """

Voici les mots de passe associes :
 - compte asso : """ + mdp1 + """
 - base de donnee MySQL : """ + mdp2 + """

Toutes les informations relatives a l'utilisation du compte sont disponibles sur notre wiki :
http://assos.utc.fr/simde

Cordialement,
L'equipe du SiMDE
"""
  send_email.send_email("simde@assos.utc.fr", to, msg)

@task
@roles('mail')
def send_new_password_asso(login_asso, login_president, mdp):
  print('Envoi du nouveau password asso au president de l\'asso')
  to = login_president + "@etu.utc.fr"
  msg = """From: SiMDE <simde@assos.utc.fr>
To: <""" + to + """>
Subject: Changement de mot de passe

Bonjour,

Le mot de passe du compte asso """ + login_asso + """ vient d'etre change.

Voici le nouveau mot de passe : """ + mdp + """

Toutes les informations relatives a l'utilisation du compte sont disponibles sur notre wiki :
http://assos.utc.fr/simde

Cordialement,
L'equipe du SiMDE
"""
  send_email.send_email("simde@assos.utc.fr", to, msg)

@task
@roles('mail')
def send_new_password_sql(login_asso, login_president, mdp):
  print('Envoi du nouveau password sql au president de l\'asso')
  to = login_president + "@etu.utc.fr"
  msg = """From: SiMDE <simde@assos.utc.fr>
To: <""" + to + """>
Subject: Changement de mot de passe MySQL

Bonjour,

Le mot de passe de la base de donnee de l'asso """ + login_asso + """ a ete change.

Voici le nouveau mot de passe : """ + mdp + """

Toutes les informations relatives a l'utilisation du compte sont disponibles sur notre wiki :
http://assos.utc.fr/simde

Cordialement,
L'equipe du SiMDE
"""
  send_email.send_email("simde@assos.utc.fr", to, msg)
