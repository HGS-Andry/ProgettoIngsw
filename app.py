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
    if session['usertype'] == 2:
        return redirect("/dashboard")
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
        messaggio, result,  idAdmin , nome  = app.model.loginadmin(account, password)
        if result:
            setsession(2,idAdmin, nome)
            return redirect("/")
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
@app.route("/dashboard")
def dashboard():
    # gestiamo la form del login
    return render_template('dashboard.html')

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

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html')

@app.errorhandler(403)
def page_Forbidden(e):
    # note that we set the 403 status explicitly
    return render_template('403.html')

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