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
        setsession(0,None,None) # in caso di utente non loggato
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
    # Prendo i parametri dalla form in post
    account = request.form['account']
    password = request.form['psw']

    #controllo se è una mail per cerfcare tra gli utenti registrati
    if '@' in account:
        messaggio, result,  librocard, nome  = app.model.login(account, password)
        if result: #se va tutto bene
            setsession(1,librocard, nome) #setto la sessione ad utente registrato
            return redirect("/")  # ritorno alla home
    else:
        #TODO gestire l'amministratore
        messaggio = 'Sei un amministratore ora!'
        setsession(2,1,'Amministratore')
        #TODO redirect dashboard
    # in caso di errore
    flash(messaggio)
    return redirect("/login") #ritorno alla registrazione


@app.route("/logout")
def execlogout():
    # gestiamo il logout
    setsession(0,None,None) # in caso di utente registrato
    return redirect("/")

@app.route("/registrati")
def registrati():
    # gestiamo la form della registrazione
    return render_template('registrazione.html')

@app.route("/execregist", methods=['POST'])
def execregist():
    '''gestiamo la registrazione ed effettuiamo il login'''
    # Prendo i parametri dalla form in post
    nome = request.form['nome']
    cognome = request.form['cognome']
    email = request.form['email']
    password = request.form['psw']

    messaggio, result,  librocard  = app.model.registrazione(nome, cognome, email, password)
    if result: #se va tutto bene
        setsession(1,librocard, nome) #setto la sessione ad utente registrato
        return redirect("/")  # ritorno alla home
    # in caso di errore
    flash(messaggio)
    return redirect("/registrati") #ritorno alla registrazione

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

#################################
##  Funzioni varie 
#################################
def setsession(usrtype, userid, username):
    '''Ímposta la session, usertype (0 non registrato, 1 utente registrato, 2 admin), id e nome.'''
    session['usertype'] = usrtype
    session['userid'] = userid
    session['username'] = username 


if __name__ == '__main__':
    app.run(port=5000, debug=False)