from flask import *
# from psycopg2 import *

from model import Model

app = Flask(__name__)
app.model = Model()
app.secret_key = 'any random string'  #penso una stringa che debba essere creata random, non ho ben capito 

#################################
##  Main 
#################################
@app.route("/")
def main():
    # gestiamo il main, bisogna gestire se siamo registrati o meno
    #
    if 'usertype' not in session:
        session['usertype'] = 0 # in caso di utente non loggato
    return render_template('main.html')

#################################
##  Login - Logout - registrazione
#################################
@app.route("/login")
def login():
    # gestiamo la form del login
    return render_template('login.html')

@app.route("/execlogin", methods=['POST'])
def execlogin():
    # gestiamo il login, con la scelta se utenti o amministratori
    #if 'usertype' in [session]:
    session['usertype'] = 1 # in caso di utente registrato
    return redirect("/")

@app.route("/logout")
def execlogout():
    # gestiamo il logout
    session['usertype'] = 0 # in caso di utente registrato
    return redirect("/")

@app.route("/registrati")
def registrati():
    # gestiamo la form della registrazione
    return render_template('registrazione.html')

@app.route("/execregist", methods=['POST'])
def execregist():
    '''gestiamo la registrazione'''
    #if 'usertype' in [session]:
    #session['usertype'] = 1 # Una volta registrato fa direttamente il login?
    nome = request.form['nome']
    cognome = request.form['cognome']
    email = request.form['email']
    password = request.form['psw']
    if nome != '' and cognome != '' and email != '' and password != '': 
        result, messaggio  = app.model.registrazione(nome, cognome, email, password)
        if result:
            return redirect("/")  
    else:
        flash("Dati mancanti")
    flash(messaggio)
    return redirect("/registrati")

#################################
##  Dashboard 
#################################

#################################
##  Carrello 
#################################
@app.route("/carrello")
def carrello():
    # gestiamo il carrello
    return render_template('carrello.html')

#################################
##  Ordini 
#################################
@app.route("/getordine")
def getordine():
    # gestiamo il carrello
    return render_template('carrello.html')

if __name__ == '__main__':
    app.run(port=5000, debug=False)