
import bcrypt
from flask import Blueprint, jsonify, request, session
from flask_migrate import current
from backend  import db , bcrypt
from backend .auth.models import Resources, Role, User
from flask_login import current_user, login_required, login_user, logout_user , current_user
 

auth = Blueprint('auth' , __name__)

@auth.route('/api/auth/login' , methods = ['POST'])
def login() : 
    if request.method == "POST" : 
        try : 
            data = request.json 
            email = data.get('email')
            user = User.query.filter_by(email = email ).first()
            if user : 
                if not bcrypt.check_password_hash(user.password, data.get('password')): 
                    return jsonify({'erreur ':  "Désolé , mais le mot de passe est invalid"}) , 400
                    
                else : 
                    login_user(user)
                    print('Connexion etablie')
                    return jsonify({"Message" : "Connexion établie"}) , 201
            else :
                print('utlisateur non exisitant')
                return jsonify({"erreur " : "Utlisateur non existant"}), 404
            
        except Exception as e : 
            db.session.rollback()
            return jsonify({'error ': str (e)}) , 500
        
       
@auth.route('/api/auth/signup' , methods =['POST'])
def signup() : 
    if request.method == "POST" : 
        try : 
            data = request.json

            field = ["name" , "email" , "password"]

            for champ in field : 
                if champ not in data : 
                    return jsonify({"message" : "Veuillez a remplir tout les champs"}) , 400 

            name = data.get('name')
            email = data.get('email')
            password = data.get('password')
            password_hash = bcrypt.generate_password_hash(password).decode('UTF-8')

          
            personne = User.query.filter_by(email = email ).first()
            if personne   : 
                print('Désole, cette utlisateur existe deja')
                return jsonify({
                    "erreur " : "Désolé, cette utilisateur existe deja"
                }) , 400 


            user = User(
                name = name , 
                email = email , 
                password = password_hash 
            )
   
            db.session.add(user)
            db.session.commit()

            print('User has benn created')
            return jsonify({"message" : "utlisateur a bien été crée"}) , 201
        
        except Exception as e : 
            db.session.rollback()
            print('Erreur serveur :  ' , str(e))
            return jsonify({'Erreur ' : str(e)}) ,500 
        
        
        
@auth.route('/api/auth/logout' ,methods =['POST'])
def logout(): 
    try : 
        logout_user()
        session.clear() 
        print('Utilisateur déconnecté avec succes')
        return jsonify({'message' :"Déconnecté avec succès"}) , 200 
 
    except Exception as e : 
        
        db.session.rollback()
        print('erreur : ' ,  str(e))
        return jsonify({"message" : str(e)})


@auth.route('/api/auth/profile' , methods= ['GET' , 'POST'])
@login_required
def getProfile() :
    if request.method == "GET" : 
        try : 
            user_data = current_user.to_json()
            if user_data  : 
                return jsonify(user_data)

            return jsonify({"message" : "user non trouvé"}) , 404
        except Exception as e: 
            db.session.rollback()
            print('Erreur serveur '  , str(e))
            return jsonify({
                'Erreur server' : str(e) 
            })     



@auth.route('/api/auth/admin' , methods = ['POST'])
def install_config() : 
    if request.method == "POST" : 
        data = request.json 

       
        admin_name  = data.get('admin_name')
        admin_email = data.get('admin_email')
        admin_password = data.get('admin_password')

        try : 

            hashed_password = bcrypt.generate_password_hash(admin_password).decode('utf-8')
            session['admin_name'] = admin_name
            session['admin_email'] = admin_email
            session['admin_password'] = hashed_password

            empty_setup()
            db.session.commit()

            print('Nouvel admin installé ')
            return jsonify({"message" : "Nouvelle utilisateur installé"}) , 201 
            
        except Exception as e: 
            db.session.rollback()
            print('Erreur serveur : ' , str (e))
            return jsonify({
                "Erreur serveur"  : str (e)
            }) , 500
        

    
def empty_setup():
    # create system roles & resources
    role = Role(name='admin')
    
    role.resources.append(
        Resources(
            name='staff',
            can_view=True,
            can_edit=False,
            can_create=False,
            can_delete=False
        )
    )

    role.resources.append(
        Resources(
            name='leads',
            can_view=True,
            can_edit=False,
            can_create=True,
            can_delete=False
        )
    )

    role.resources.append(
        Resources(
            name='accounts',
            can_view=True,
            can_edit=False,
            can_create=True,
            can_delete=False
        )
    )

    role.resources.append(
        Resources(
            name='contacts',
            can_view=True,
            can_edit=True,
            can_create=True,
            can_delete=False
        )
    )

    role.resources.append(
        Resources(
            name='deals',
            can_view=True,
            can_edit=False,
            can_create=True,
            can_delete=False
        )
    )

    user = User(name =session['admin_name'],
                email=session['admin_email'],
                password=session['admin_password'],
                is_admin=True,
                is_first_login=True,
                is_user_active=True
                )
    


    db.session.add(role)
    db.session.add(user)


            

        
@auth.route('/api/refresh-token' , methods=['POST'])
def refreshToken() : 
    if request.method == "POST" : 
        try :
            pass 
        except Exception as e : 
            print('Erreur console : ' ,str(e))
            return jsonify({'Erreur'  : str(e)}) , 500
      

        
