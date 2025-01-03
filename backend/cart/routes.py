

from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from backend  import db
from backend .auth.models import User
from backend .cart.models import CartItems
from backend .products.models import Product


cart = Blueprint('cart', __name__)


@cart.route('/api/cart', methods=['GET'])
@login_required
def get_cart_products():
    if request.method == 'GET':
        try:
            if not current_user.is_authenticated:
                return jsonify({"message": "Unauthorized access"}), 401
            
            cart_items = CartItems.query.filter_by(user_id=current_user.id).all()

            if not cart_items:
                return jsonify({"message": "Votre panier est vide"}), 404
  
            cart_products = []
            for item in cart_items:
                product = Product.query.get(item.product_id)
                
                if product:
                    cart_products.append({
                        "id": product.id,
                        "name": product.name,
                        "price": product.price,
                        "quantity": item.quantity
                    })

            return jsonify(cart_products), 200

        except Exception as e:
            db.session.rollback()
            print("Error in get_cart_products controller", str(e))
            return jsonify({"message": "Server error", "error": str(e)}), 500
 
@cart.route('/api/cart/add', methods = ['POST'])
@login_required 
def addToCart():
    if request.method == "POST" :
        try : 
            data = request.json

            user_id = current_user
            product_id = data.get('product_id')
            quantity = data.get('quantity' , 1)

            product = Product.query.get(product_id)
        
            if not product : 
                return jsonify({"message" : "Le produit n'est pas disponoble"}) , 404 
            
            panier = CartItems.query.filter_by(product_id = product_id).first()

            if panier : 
                CartItems.quantity += 1
            else :  
                new_panier = CartItems(
                    user = user_id , 
                    product_id = product_id , 
                    quantity = quantity
                )

                db.session.add(new_panier)
                db.session.commit()

            print("Nouvel element ajouté au panier")
            return jsonify({"message" : "Nouvelle element ajouté au panier"})

        except Exception as e :
            db.session.rollback()
            print("Error in get_cart_products controller", str(e))
            return jsonify({"message": "Server error", "error": str(e)}), 500
            

@cart.route('/api/cart/<int:product_id>' , methods = ['DELETE'])
@login_required
def removeAllFormCart(product_id) : 

    if request.method == 'DELETE' : 
        try :
            user = current_user
            products = CartItems.query.filter_by(product_id = product_id , user_id = user.id).first()
            if products  :
                db.session.delete(products)
                db.session.commit()
                print('Element supprimé avec succes')
                return jsonify({"message" : "Elmement supprimé avec succes"})
            else : 
                print('Votre panier est vide')
                return jsonify({"message" : "Votre panier est vide"})
            
        except Exception as e : 
            db.session.rollback()
            print("Error in get_cart_products controller", str(e))
            return jsonify({"message": "Server error", "error": str(e)}), 500
        
@cart.route('/api/cart/update/<int:product_id>', methods=['PUT'])
@login_required
def update_quantity(product_id):
    if request.method == 'PUT' :
        if current_user.is_authenticated :
            try:
                data = request.json
                quantity = data.get('quantity')
                
                if quantity is None:
                    return jsonify({"message": "La quantité est recomandé"}), 400
                
                cart_item = CartItems.query.filter_by(user_id=current_user.id, product_id=product_id).first()

                if not cart_item:
                    return jsonify({"message": "Votre panier est vide"}), 404

                if quantity == 0:
                        
                    db.session.delete(cart_item)
                    db.session.commit()
                    return jsonify({"message": "Item removed from cart", "cart": get_cart_products()}), 200

                
                cart_item.quantity = quantity
                db.session.commit()

                return jsonify({"message": "Quantity updated successfully", "cart": get_cart_products()}), 200

            except Exception as e:
                db.session.rollback()
                print("Error in update_quantity controller:", str(e))
                return jsonify({"message": "Server error", "error": str(e)}), 500

        else : 
            return jsonify({
                "message" : "Veillez vous connectez avant d'acceder à cette page"
            })
        
        