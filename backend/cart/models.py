
from backend  import db 
   
class CartItems(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, default=1)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    product = db.relationship('Product', backref='cart_items')
    
    def to_json(self) : 
        return({
            "id" :self.id , 
            "quantity": self.quantity , 
            "product_id" : self.product_id ,
            "user_id" : self.user_id
        })
        