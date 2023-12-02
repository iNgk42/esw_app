# python code to connect app to database
import datetime
from sqlalchemy import create_engine, URL, text

connection_url = URL.create(
    "mysql+pymysql",
    username="root",
    password="mysql_root_password",
    host="esw_db",
    port=3306,
    database="esw_db",
)

engine = create_engine(connection_url)

# get users's informations and save them to database
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


# get users's infos from database 
def load_users_infos_from_db():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT * FROM personnel"))
        users_infos = []
        for row in result.all():
            users_infos.append(dict(row))
    return users_infos


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

def load_user_account_from_db(email):
    with engine.connect() as connection:
        
        load_query = text("SELECT * FROM personnel WHERE pers_email=:user_email").\
                        bindparams(user_email=email)

        load_result = connection.execute(load_query).mappings().all()

        return load_result[0]