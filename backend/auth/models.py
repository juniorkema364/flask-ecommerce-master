from flask_login import UserMixin
from backend  import db , login_manager
from backend.cart.models import CartItems


@login_manager.user_loader 
def load_user(id) :
    return User.query.get(int(id))

class User(db.Model , UserMixin): 
    id = db.Column(db.Integer  , primary_key = True  , autoincrement = True ) 
    name = db.Column(db.String(200) , nullable = False)
    email = db.Column(db.String(255) , unique = True  , nullable = False )
    password = db.Column(db.Integer, nullable = False)
    role_id = db.Column(db.Integer ,  db.ForeignKey('role.id' ,ondelete = "SET NULL") ,nullable= True)
    is_admin  = db.Column(db.Boolean , nullable = False , default = False)
    is_first_login = db.Column(db.Boolean , nullable = False, default = True)
    is_user_active = db.Column(db.Boolean , nullable = False ,  default = False)

    cartItems = db.relationship('CartItems', backref='user', lazy=True)


 

    def to_json(self) : 
        return({
            "id": self.id , 
            "name" : self.name , 
            "email" : self.email , 
            'password' : self.password ,
            "role_id" : self.role_id , 
            "is_admin" : self.is_admin , 
        })
 

role_resources = db.Table(
    'role_resources' , 
    db.Column('role_id' , db.Integer , db.ForeignKey('role.id')) , 
    db.Column('resources_id' , db.Integer , db.ForeignKey('resources.id'))
)


 


    

class Role(db.Model):
    id = db.Column(db.Integer , primary_key = True , autoincrement = True)
    name = db.Column(db.String(20) , unique = True , nullable = False )


    user = db.relationship('User' , uselist = False , backref = 'role' , lazy = True)
    resources = db.relationship('Resources' , secondary =role_resources , backref = db.backref('resources' , lazy ='dynamic'))


    def set_permission(self , resources):
        for i in range(len(resources)):
            self.resources[i].can_view = resources[i].can_view.data
            self.resources[i].can_create = resources[i].can_create.data
            self.resources[i].can_edit = resources[i].can_edit.data
            self.resources[i].can_delete = resources[i].can_delete.data


class Resources(db.Model):
    id = db.Column(db.Integer , autoincrement = True , primary_key = True)
    name = db.Column(db.String(20) , nullable = False )
    can_view = db.Column(db.Boolean , nullable = False )
    can_edit = db.Column(db.Boolean , nullable = False )
    can_create = db.Column(db.Boolean , nullable = False )
    can_delete = db.Column(db.Boolean , nullable = False )
    