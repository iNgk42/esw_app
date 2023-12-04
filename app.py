from flask import Flask, render_template, request, jsonify, redirect
from database import * #load_users_infos_from_db, add_user_to_db

# Créer une instance d'application web flask
app = Flask(__name__)

# Les décorateurs ci-dessous spécifient 
# les fonctions à exécuter pour une url donnée
@app.route("/")
def accueil():
    connection_button_state = ""
    home_button_state = "visually-hidden"
    return render_template('accueil.html', state=connection_button_state,
                                           home_button_state=home_button_state)

@app.route("/connexion")
def connexion():
    connection_button_state = "visually-hidden"
    home_button_state = ""
    return render_template('connexion.html', state=connection_button_state,
                                             home_button_state=home_button_state)
                                        
@app.route("/connexion/verification", methods=['post'])
def verification_connexion():
    connection_button_state = "visually-hidden"
    home_button_state = ""
    user_credentials = request.form
    user_account = login(user_credentials)
    if user_account == "Not Found":
        return render_template('connexion_failed.html', state=connection_button_state,
                                                        home_button_state=home_button_state)
    else:
        return redirect('/comptes/' + str(user_account["pers_id"]) + "/" + user_account["pers_nom"])

@app.route("/comptes/<id>/<nom>")
def affichage_compte(id, nom):
    connection_button_state = "visually-hidden"
    home_button_state = ""
    user_account = load_user_account_from_db(id)
    return render_template('compte_utilisateur.html', state=connection_button_state,
                                               home_button_state=home_button_state,
                                               user_account=user_account)

@app.route("/comptes/<id>/<nom>/gerer-mon-compte")
def gerer_compte(id, nom):
    connection_button_state = "visually-hidden"
    home_button_state = ""
    user_account = load_user_account_from_db(id)
    return render_template('gerer_mon_compte.html', state=connection_button_state,
                                               home_button_state=home_button_state,
                                               user_account=user_account)

@app.route("/inscription")
def inscription():
    connection_button_state = "visually-hidden"
    home_button_state = ""
    return render_template('inscription.html', state=connection_button_state,
                                               home_button_state=home_button_state)

@app.route("/inscription/comptes/nouveau", methods=['post'])
def confirmation_inscription():
    connection_button_state = "visually-hidden"
    home_button_state = ""
    new_user = request.form
    verif = add_user_to_db(new_user)
    return render_template('inscription_validee.html', state=connection_button_state,
                                                    home_button_state=home_button_state,
                                                    new_user=new_user,
                                                    verif=verif)

@app.route("/comptes/<id>/<nom>/gerer-mon-compte/modifier", methods=['post'])
def confirmation_modification_compte(id, nom):
    connection_button_state = "visually-hidden"
    home_button_state = ""
    user_edits = request.form
    verif = edit_user_account(user_edits, id)
    return render_template('validation_modification.html', state=connection_button_state,
                                                    home_button_state=home_button_state,
                                                    user_edits=user_edits,
                                                    verif=verif,
                                                    id=id)

# Exécution de l'application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
