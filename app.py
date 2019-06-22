from flask import *
# from psycopg2 import *
from werkzeug.utils import secure_filename
import os

from model import Model

app = Flask(__name__)
app.model = Model()
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
app.secret_key = 'any random string'  #penso una stringa che debba essere creata random, non ho ben capito
app.path = os.path.dirname(os.path.realpath(__file__))
app.folder_copertine = app.path+'\static\copertine' #prendo la directory dove mettere le copertine
app.folder_generi = app.path+'\static\generi' #prendo la directory dove mettere le foto dei generi
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])

#################################
##  Main 
#################################
@app.route("/")
def main():
    # gestiamo il main, bisogna gestire se siamo registrati o meno
    #
    if 'usertype' not in session:
        setsession(0,None,None) # in caso di utente non loggato
    if session['usertype'] == 2: #in caso di admin
        return redirect("/dashboard")

    messaggio, result, listaGeneri = app.model.getGeneri()
    if result:
        return render_template('main.html',generi = listaGeneri)
    print(messaggio)

    

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
    checksession(2)
    isbn = request.form['isbn']
    titolo = request.form['titolo']
    datapub = request.form['datapub']
    prezzo = request.form['prezzo']
    punti = request.form['punti']
    descr = request.form['descr']
    posclas = request.form['posclas']
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
    
    # if user does not select file, browser also
    # submit a empty part without filename
    immagine=''
    if 'immagine' in request.files:
        file = request.files['immagine']
        if file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.folder_copertine, filename))
            immagine = filename

    messaggio, result, isbn = app.model.addLibro( isbn, titolo, datapub, prezzo, punti, descr, 11 , immagine , idedit, quant, idaut,idgenere) #la posizione in classifica sarà aggiornata dopo, viene settatta automatifcamente a 11
    if not result:
        flash(messaggio)
        return redirect(request.referrer)
    if posclas != '11':
        flash('Classifica aggiornata')
        #setta la posizione del libro in classifica
    flash('Libro aggiunto')
    return redirect("/insalterbook/"+isbn)

@app.route("/modlibro", methods=['POST'])
def modlibro():
    checksession(2)
    isbn = request.form['isbn']
    titolo = request.form['titolo']
    datapub = request.form['datapub']
    prezzo = request.form['prezzo']
    punti = request.form['punti']
    descr = request.form['descr']
    posclas = request.form['posclas']
    idedit = request.form['idedit']
    quant = request.form['quant']
    idaut = request.form['idaut']
    idgenere = request.form['idgenere']

    oldposclas = request.form['oldposclas']
    oldimmagine = request.form['oldimmagine']

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
    
    # if user does not select file, browser also
    # submit a empty part without filename
    immagine=oldimmagine
    if 'immagine' in request.files:
        file = request.files['immagine']
        if file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.folder_copertine, filename))
            immagine = filename

    # messaggio, result, isbn = app.model.modLibro( isbn, titolo, datapub, prezzo, punti, descr, immagine , idedit, quant, idaut,idgenere) #la posizione in classifica sarà aggiornata dopo, viene settatta automatifcamente a 11
    # if not result:
    #     flash(messaggio)
    #     return redirect(request.referrer)
    if posclas != oldposclas:
        flash('Classifica aggiornata')
        #setta la posizione del libro in classifica
    flash('Libro modificato')
    return redirect("/insalterbook/"+isbn)

#################################
##  visualizza / inserisci / modifica generi 
#################################
@app.route("/gestgeneri")
def gestgeneri():
    checksession(2)
    messaggio, result, listaGeneri = app.model.getGeneri()
    if result:
        return render_template('gestgeneri.html', generi = listaGeneri)
    flash(messaggio)
    return('/dashboard')

######    Aggiungi genere
@app.route("/addgenere")
def addgenere():
    checksession(2)
    return render_template('addgenere.html')

@app.route("/execaddgenere", methods=['POST'])
def execaddgenere():
    checksession(2)
    nome = request.form['nome']
    immagine=''
    if 'immagine' in request.files:
        file = request.files['immagine']
        if file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.folder_generi, filename))
            immagine = filename
    messaggio, result, idgenere = app.model.addGenere(nome,immagine)
    if result:
        flash('Genere %s aggiunto con id %s'%(nome, idgenere))
        return redirect('/modgenere/'+idgenere)
    flash(messaggio)
    return redirect(request.referrer)

######    modifica genere

@app.route("/modgenere/<idgenere>")
def modgenere(idgenere):
    checksession(2)
    messaggio, result, genere = app.model.getGenere(idgenere)
    if result:
        return render_template('modgenere.html', genere = genere, libri = [] )
    #TODO aggiungere lista libri del genere
    flash(messaggio)
    return redirect(request.referrer)

@app.route("/execmodgenere", methods=['POST'])
def execmodgenere():
    checksession(2)
    idgenere = request.form['idgenere']
    nome = request.form['nome']
    immagine=request.form['immagine']
    if 'immagine' in request.files:
        file = request.files['immagine']
        if file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.folder_generi, filename))
            immagine = filename
    messaggio, result = app.model.modGenere(idgenere, nome,immagine)
    if result:
        flash('Genere modificato')
        return redirect('/modgenere/'+idgenere)
    flash(messaggio)
    return redirect(request.referrer)

    
#################################
##  Carrello 
#################################
# @app.route("/carrello")
# def carrello():
#     # gestiamo il carrello
#     return render_template('carrello.html')

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

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    app.run(port=5000, debug=False)