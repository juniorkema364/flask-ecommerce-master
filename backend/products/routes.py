from backend  import db 
from flask import Blueprint, jsonify, request
from backend .products.models import Product



products = Blueprint('products' , __name__)

@products.route('/api/products' , methods = ['GET'])
def getAllproducts() : 
    if request.method =="GET" : 
        try : 
            products = Product.query.all()
            print(products)
            produit = [produit.to_json() for produit in products]
            if produit :
                print(produit)
                return jsonify(produit)
            else: 
                print('Il y pas de produit  disponible')
                return jsonify({'Ereur' : 'Pas de produit disponible'}) , 404
        
        except Exception as e :
            db.session.rollback()
            print('Erreur serveur : ' , str(e))
            return jsonify({'Erreur' : str(e)}) , 500
        

 

@products.route('/api/products/add' , methods = ['POST'])
def createProduct() : 
    if request.method == "POST" : 
        try :
            data = request.json 

            name = data.get('name')
            description = data.get('description')
            price = data.get('price')
            image = data.get('image')
            category = data.get('category')

            products = Product(
                name = name , 
                description = description , 
                price = price  ,
                image = image , 
                category= category 
            )

            db.session.add(products)
            db.session.commit()

            print('Nouveau produit ajouté')
            return jsonify({'Message' : "Nouveau produit ajouté"}) , 201

        except Exception as e :
            db.session.rollback()
            print('Erreur serveur : ' ,  str(e))
            return jsonify({
                "message" : "Il y a une erreur" ,
                "Erreur  serveur " : str(e)
            }) , 500 
    

@products.route('/api/products/<int:id>' , methods=['DELETE'])
def DeleteProduct(id) : 
    if request.method == "DELETE" : 
        try : 
            products = Product.query.filter_by(id = id).first()
            
            if products  : 
                db.session.delete(products)
                db.session.commit()

                print('Element supprim" avec succes')
                return jsonify({'message' : "Element supprimé avec succes"})
            else : 
                print('Le produit existe pas')
                return jsonify({'message' : "Le produit n'existe pas "}) , 400 
        except Exception as e :
            db.session.rollback()
            print('Erreur serveur : ' ,  str(e))
            return jsonify({
                "message" : "Il y a une erreur" ,
                "Erreur  serveur " : str(e)
            }) , 500       
        
@products.route('/api/products/category/<string:category>' , methods = ['GET'])
def getProductsByCategory(category):
    if request.method == 'GET' : 
        try : 
            products = Product.query.filter(Product.category == category).order_by(Product.name).all()

            products_json = [product.to_json() for product in products]
            if products_json : 
                return jsonify(products_json), 200
            else :
                print('Produit non disponible')
                return jsonify({"message" : "produit non trouvé"}) , 404
        
        except Exception as e :
            db.session.rollback()
            print('Erreur serveur : ' ,  str(e))
            return jsonify({
                "message" : "Il y a une erreur" ,
                "Erreur  serveur " : str(e)
            }) , 500   
        