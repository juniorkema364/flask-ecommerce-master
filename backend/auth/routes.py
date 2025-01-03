
import bcrypt
from flask import Blueprint, jsonify, request, session
from backend  import db , bcrypt
from backend .auth.models import User
from flask_login import login_user, logout_user 


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
                return jsonify({"erreur " : "Utlisateur non existant"}), 401
            
        except Exception as e : 
            db.session.rollback()
            return jsonify({'error ': str (e)}) , 500
        
       
@auth.route('/api/auth/signup' , methods =['POST'])
def signup() : 
    if request.method == "POST" : 
        try : 
            data = request.json

            field = [name , email , password]

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
            return jsonify({"message" : "User has been created"}) , 201
        
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


        
            