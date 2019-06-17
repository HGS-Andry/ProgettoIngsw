from flask import *
from flask.templating import render_template
from psycopg2 import *
import psycopg2.extras

from model import Model

app = Flask(__name__)
app.secret_key = 'any random string'  #penso una stringa che debba essere creata random, non ho ben capito 
app.model = Model()
app.name= "Qualcosa" #collego la variabile name all'oggetto app
#session['usrtype']=0 #0 per utente, 1 per utente registrato, 2 per admin

# per la session: https://www.tutorialspoint.com/flask/flask_sessions.htm


@app.route("/")
def index():
    usrtype = 0 #questo usertype è locale alla funzione
    alert = ""
    if request.args: #se c'è un argomento in modo get
        alert = request.args['alert'] 
    listacose = app.model.getlistacose()
    if 'usrtype' in session: #controllo se nella sessione c'è l'elemento
        if session['usrtype'] == 1:
            username =  session['username'] #leggo dalla sessione
            app.name = username
            usrtype = 1
    return render_template('intro.html', titolo = app.name, alert = alert, lista = listacose, usrtype = usrtype) 

@app.route("/inserttable")
def inserttable():
    return render_template('inserttable.html', titolo = app.name)

@app.route("/addrow", methods=['POST'])
def addttable():
    nome = request.form['nome']
    quant = request.form['quant']
    messaggio = app.model.insertcose(nome,quant)
    return redirect("/?alert=" + messaggio)

@app.route("/delete", methods=['GET'])
def delete():
    id = request.args['id']
    messaggio = app.model.delete(id)
    return redirect("/?alert=" + messaggio)

@app.route("/login")
def login():
    return render_template('login.html', titolo = app.name)

@app.route("/exec-login", methods=['POST'])
def execlogin():
    username = request.form['username'] # qui sarebbe da controllare nel database se esiste
    password = request.form['password'] # si potrebbe fare un redirect alla pagina /login che ha un alert in get come nell'index
    # messaggio = app.model.insertcose(nome,quant)
    # return redirect("/?alert=" + messaggio)
    session['usrtype'] = 1 #setto la variabile di sessione
    session['username'] = username #setto la variabile di sessione (in questo caso viene anche creata)
    return redirect("/")


@app.route("/logout")
def logout():
    session['usrtype'] = 0 #setto la variabile di sessione
    session.pop('username', None) #elimino la variabile di sessione
    app.name = 'Qualcosa' #riresetto la variabile collegata all'oggetto app
    return redirect("/")

@app.teardown_appcontext
def test(error):
    print("** "+str(error)) # ho provato a fare una funzione per capire quando viene chiamata. Ho notato che viene sempre chiamata e restituisce non come errore, 
    if error:               # si potrebbe fare che se c'è un errore allora si chioude, altrimenti si continua. MA con debug true non funziona lo stesso 
        print("| controller close")  #non so se possa portare ad errori, magari meglio commentarlo
        app.model.close()

def __del__():
    print("| controller close")
    app.model.close()

if __name__ == '__main__':
    app.run(port=5000, debug=False)
