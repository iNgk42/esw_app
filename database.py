# python code to connect app to database
import datetime
from sqlalchemy import create_engine, URL, text

connection_url = URL.create(
    "mysql+pymysql",
    username="root",
    password="mysql_root_password",
    host="localhost",
    port=3306,
    database="esw_db",
)

engine = create_engine(connection_url)

# get user's informations and save them to database after verify that new email was not already used
def edit_user_account(user_edits, id): 
    with engine.connect() as connection:
        
        verif_query = text("SELECT * FROM personnel WHERE pers_email=:new_user_mail AND pers_id=:user_id").\
                        bindparams(new_user_mail=user_edits["email"], user_id=id)

        verif_result = connection.execute(verif_query)

        if len(verif_result.all()) == 1: # user didn't change his email
            query = text("UPDATE personnel " \
                                        "SET pers_nom = :nom," \
                                            "pers_prenom = :prenom," \
                                            "pers_sexe = :sexe," \
                                            "pers_email = :email," \
                                            "pers_telephone = :telephone," \
                                            "pers_poste = :poste," \
                                            "pers_descriptionposte = :descriptionposte," \
                                            "pers_mdp = :mdp" \
                                        " WHERE pers_id = :id" \
                                        ).\
                    bindparams( nom=user_edits["nom"],
                                prenom=user_edits["prenom"],
                                sexe=user_edits["sexe"],
                                email=user_edits["email"],
                                telephone=user_edits["telephone"],
                                poste=user_edits["poste"],
                                descriptionposte=user_edits["description_poste"],
                                mdp=user_edits["mot_de_passe"],
                                id=id
                            )

            connection.execute(query)
            connection.commit()
            return "success"
        elif len(verif_result.all()) == 0: # user changed his email
            # verify that the new user's email is unique in database before updating user account infos
            # verification
            unique_mail_verif_query = text("SELECT * FROM personnel WHERE pers_email=:new_user_mail").\
                        bindparams(new_user_mail=user_edits["email"])
            unique_mail_verif_result = connection.execute(unique_mail_verif_query)
            if unique_mail_verif_result.all() == []:
                # updating
                query = text("UPDATE personnel " \
                                        "SET pers_nom = :nom," \
                                            "pers_prenom = :prenom," \
                                            "pers_sexe = :sexe," \
                                            "pers_email = :email," \
                                            "pers_telephone = :telephone," \
                                            "pers_poste = :poste," \
                                            "pers_descriptionposte = :descriptionposte," \
                                            "pers_mdp = :mdp" \
                                        " WHERE pers_id = :id" \
                                        ).\
                    bindparams( nom=user_edits["nom"],
                                prenom=user_edits["prenom"],
                                sexe=user_edits["sexe"],
                                email=user_edits["email"],
                                telephone=user_edits["telephone"],
                                poste=user_edits["poste"],
                                descriptionposte=user_edits["description_poste"],
                                mdp=user_edits["mot_de_passe"],
                                id=id
                            )

                connection.execute(query)
                connection.commit()
                return "success"
            else:
                return "failed"
        else:
            return "failed"
        
#get user's edits and update user account in database 
def add_user_to_db(new_user): 
    with engine.connect() as connection:
        
        verif_query = text("SELECT * FROM personnel WHERE pers_email=:new_user_mail").\
                        bindparams(new_user_mail=new_user["email"])

        verif_result = connection.execute(verif_query)

        if verif_result.all() == []:
            submitted_date = datetime.date.today()
            query = text("INSERT INTO personnel (" \
                                            "pers_nom, " \
                                            "pers_prenom, " \
                                            "pers_sexe, " \
                                            "pers_email, " \
                                            "pers_telephone, " \
                                            "pers_poste, " \
                                            "pers_descriptionposte, " \
                                            "pers_mdp, " \
                                            "pers_datecreation" \
                                        ") " \
                                        "VALUES (" \
                                            ":nom, " \
                                            ":prenom, " \
                                            ":sexe, " \
                                            ":email, " \
                                            ":telephone, " \
                                            ":poste, " \
                                            ":descriptionposte, " \
                                            ":mdp, " \
                                            ":datecreation" \
                                        ")").\
                    bindparams( nom=new_user["nom"],
                                prenom=new_user["prenom"],
                                sexe=new_user["sexe"],
                                email=new_user["email"],
                                telephone=new_user["telephone"],
                                poste=new_user["poste"],
                                descriptionposte=new_user["description_poste"],
                                mdp=new_user["mot_de_passe"],
                                datecreation=submitted_date
                            )

            connection.execute(query)
            connection.commit()
            return "success"
        else:
            return "failed"


# get all users's infos from database 
def load_users_infos_from_db():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT * FROM personnel"))
        users_infos = []
        for row in result.all():
            users_infos.append(dict(row))
    return users_infos

# get user's credentials and verify it in database
def login(user_credentials):
    with engine.connect() as connection:
        
        verif_query = text("SELECT * FROM personnel WHERE pers_email=:user_email AND pers_mdp=:user_mdp").\
                        bindparams(user_email=user_credentials["email"], user_mdp=user_credentials["mot_de_passe"])

        verif_result = connection.execute(verif_query).mappings().all() # mappings() converti les sql alchemy row en dictionnaire

        if verif_result == []:
            return "Not Found"
        else:
            #user_name = verif_result[0]["pers_nom"]
            #return "success", user_name
            user_account = verif_result[0]
            return user_account

# get id of a user's account and load his infos and return it
def load_user_account_from_db(id):
    with engine.connect() as connection:
        
        load_query = text("SELECT * FROM personnel WHERE pers_id=:user_id").\
                        bindparams(user_id=id)

        load_result = connection.execute(load_query).mappings().all()

        return load_result[0]