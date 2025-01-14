from backend  import db 
from flask import Blueprint, json, jsonify, request
from backend.config import Config
from backend .products.models import Product
from redis import Redis



products = Blueprint('products' , __name__)

redis_client = Redis.from_url(Config.REDIS_URL)

@products.route('/api/products' , methods = ['GET' , 'POST'])
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
        
    elif request.method == "POST" : 
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

                print('Element supprimé avec succes')
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


@products.route('/api/products/<int:id>' , methods = ['PATCH'])
def tooglefeaturedPorduct(id): 
    if request.method == "PATCH" : 
        try : 
            product = Product.query.filter_by(id = id).first()
            if product :

                Product.isfeatured != Product.isfeatured 
                db.session.commit()
                updateFeaturedProductsCache()
                return jsonify()
            else : 
                print('Produit non trouvé ... ')
                return jsonify({'Erreur' : "Produit Non trouvé"}) ,404 
        except Exception as e : 
           print('Erreur console  : ' ,str(e))
           return jsonify({"message" : str(e)}) , 500 
    else : 
        return jsonify({"Erreur" : "Vous etes pas sur la bonne méthode"})
        

@products.route('/api/products/category/<string:category>' , methods = ['GET'])
def getProductsByCategory(category):
    if request.method == 'GET' : 
        try : 
            products = Product.query.filter(Product.category == category).order_by(Product.name).all()

            products_json = [product.to_json() for product in products]
           
            if products_json :
                print(products_json) 
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
      

@products.route('/api/products/featured' ,methods = ['GET'])
def getFeaturedProduct() : 
    if request.method == 'GET' :
        try : 
            cached_products = redis_client.get('featured_products')

            if cached_products:
                return jsonify({
                    "message" : "Produits récupéres depuis le cache" , 
                    "products": json.loads(cached_products)
                }), 200
            
            featured_products = Product.query.filter_by(isfeatured = True).all()

            if not featured_products: 
                return jsonify({
                    'error' : "Aucun produit en vedette trouvé"
                })  , 404
            
            products_data = [product.to_json() for product in featured_products]

            redis_client.set('featured_products' , json.dumps(products_data))

            return jsonify({
                'message' : "Produits récu"
            }) , 200
        
        except Exception as e :
            db.session.rollback()
            print('Erreur console  : '  ,str(e))
            return jsonify({"Erreur console " : str (e)}) , 500 



def updateFeaturedProductsCache() : 
    try : 
        featuredProduct = Product.query.filter_by(isfeatured = True).all()

        produit = [products.to_json() for products in featuredProduct]

        redis_client.set('featured_products' , json.dumps(produit))
        return jsonify({
                'message' : "Produits récu"
            }) , 200
        
    except Exception as e : 
        print('Erreur console :' , str(e))
        return jsonify({
            'Erreur' : str(e)
        }) , 500 


@products.route('/api/recommendations' , methods = ['GET'])
def getRecommendedProducts() :
    if request.method == "GET" : 
        try : 
            products = Product.query.filter_by(id = 1 , name = 1 ,description = 1 , image = 1  , price = 1).first()
            print(products)
            return jsonify(products)
        
        except Exception as e  : 
            print('Erreur console  : ' , str(e)) 
            return jsonify({
                'message' : str(e)
            }) ,500
    else : 
        print('Erreur au niveau de la méthode  ')
        return jsonify({
            'Erreur' : 'Erreur au niveau de la console'
        }) 