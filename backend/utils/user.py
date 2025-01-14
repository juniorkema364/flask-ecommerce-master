from flask import Blueprint , send_from_directory
import os

 

main = Blueprint('main' , __name__)




frontend_folder = os.path.join(os.getcwd(),"..","frontend")
dist_folder = os.path.join(frontend_folder,"dist")

 


@main.route("/",defaults={"filename":""})
@main.route("/<path:filename>") 
def index(filename):
  if not filename:
    filename = "index.html"
  return send_from_directory(dist_folder,filename)





 