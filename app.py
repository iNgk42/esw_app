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
        return redirect('/comptes/' + user_account["pers_email"] + "/" + user_account["pers_nom"])

@app.route("/comptes/<email>/<nom>")
def affichage_compte(email, nom):
    connection_button_state = "visually-hidden"
    home_button_state = ""
    user_account = load_user_account_from_db(email)
    return render_template('compte_utilisateur.html', state=connection_button_state,
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
    

# Exécution de l'application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
