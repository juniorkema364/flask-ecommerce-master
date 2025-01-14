from backend import create_app


app = create_app()

if '__main__' == __name__ : 
    app.run("0.0.0.0" , debug=True  )