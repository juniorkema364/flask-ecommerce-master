from backend  import  db

class Product(db.Model) :
    id = db.Column(db.Integer, primary_key = True,  nullable = False , autoincrement = True)
    name = db.Column(db.String(255) , nullable = False  )
    description = db.Column(db.String(255) , nullable= False)
    price = db.Column(db.Integer , nullable = False)
    image = db.Column(db.String(255), nullable = False)
    category = db.Column(db.String(255) , nullable = False )
    isfeatured = db.Column(db.String(255), default = False )
     


  


    def to_json(self) : 
        return ({
            "id" : self.id , 
            "name" :self.id , 
            "description" : self.description , 
            "price" :self.price ,
            "image" :self.image , 
            "category" : self.category , 
            "isfeatured" : self.isfeatured
        })
