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
    checksession(2)
    return render_template('dashboard.html')

#################################
##  inserisci / modifica libro 
#################################
@app.route('/insalterbook/', defaults={'isbn': ''})
@app.route("/insalterbook/<isbn>")
def insalterbook(isbn):
    # gestiamo la form del login
    # libro = {'isbn':'', 'titolo':'', 'datapub':'', 'prezzo':'', 'punti':'', 'descr':'', 'posclas':'', 'dataaggclas':'', 'immagine':'', 'idedit':'', 'quant':''}
    checksession(2)
    libro={}

    #Carica gli autori
    messaggio, result, listaAutori = app.model.getAutori()
    if not result:
        flash(messaggio)

    # carica le case editrici
    messaggio, result, listaEdit = app.model.getEdit()
    if not result:
        flash(messaggio)

    #carica i generi
    messaggio, result, listaGeneri = app.model.getGeneri()
    if not result:
        flash(messaggio)

    # se è stato inserito un libro si visualizza la pagina di modifica del alibro, altrimenti quella di inserimento
    if isbn:
        messaggio, result, libro = app.model.getLibro(isbn) #gestisco la modifica del libro ottengo una lista con i dati
        if not result:
            flash(messaggio)
    return render_template('insalterbook.html',libro=libro, autori=listaAutori, caseed=listaEdit, generi = listaGeneri)

@app.route("/addlibro" , methods=['POST'])
def addlibro():
    isbn = request.form['isbn']
    titolo = request.form['titolo']
    datapub = request.form['datapub']
    prezzo = request.form['prezzo']
    punti = request.form['punti']
    descr = request.form['descr']
    posclas = request.form['posclas']
    immagine = request.form['immagine']
    idedit = request.form['idedit']
    quant = request.form['quant']
    idaut = request.form['idaut']
    idgenere = request.form['idgenere']

    if not idaut.isdigit():
        messaggio, result, idaut = app.model.addAutore(idaut)
        if not result:
            flash(messaggio)
            return redirect(request.referrer)

    if not idedit.isdigit():
        messaggio, result, idedit = app.model.addEdit(idedit)
        if not result:
            flash(messaggio)
            return redirect(request.referrer)

    messaggio, result, isbn = app.model.addLibro( isbn, titolo, datapub, prezzo, punti, descr, posclas, immagine , idedit, quant, idaut,idgenere)
    if not result:
        flash(messaggio)
        return redirect(request.referrer)
    return redirect("/insalterbook/"+isbn)

@app.route("/modlibro", methods=['POST'])
def modlibro():
    # gestiamo la form del login
    return render_template('insalterbook.html')

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

def checksession(usrtype):
    '''Controlla se l'utene appartiene ad uno dei tipi (0,1,2) inseriti in usrtype.Abort a 403 se non è tra quelli inseriti.  Accetta anche array di più valori. '''
    if session['usertype'] != usrtype:
        abort(403)

if __name__ == '__main__':
    app.run(port=5000, debug=False)