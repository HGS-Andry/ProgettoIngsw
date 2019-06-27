from flask import *
# from flask import session
# from psycopg2 import *
from werkzeug.utils import secure_filename
from datetime import date
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
    # session.clear()
    if 'usertype' not in session:
        setsession(0,None,None) # in caso di utente non loggato
    if 'carrello' not in session:
        session['carrello']={} #Il carrello per un non loggato è un dizionario con isbn:quantitá per ogni libro
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
            messaggio, result, session['idord'] = app.model.getCarrello(librocard)
            if not result:
                flash(messaggio)
                return redirect("/logout")
            #TODO copiare carrello in session su quello vecchio?
            session['carrello']={} # resetto il carrello
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
    session.pop('idord', None) # cancello l'id del carrello
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
##  visualizza profilo
#################################
@app.route("/profilo/<int:librocard>")
def profilo(librocard):
    if session['usertype'] ==0:
        abort(403)
    if session['usertype'] ==1 and session['userid']!=librocard:
        abort(403)
    messaggio, result, utente = app.model.getUtente(librocard)
    if not result:
        flash(messaggio)
        return redirect(request.referrer)
    
    # messaggio, result, ordini = app.model.getOrdiniUtente(librocard)
    # if not result:
    #     flash(messaggio)
    #     return redirect(request.referrer)
    return render_template('profilo.html', utente=utente, ordini = [])

#################################
##  visualizza risultati ricerca libro 
#################################
@app.route("/search", methods=['GET'])
def search():
    #TODO controllo input
    string = request.args['string']
    messaggio, result, listaLibri = app.model.searchBooks(string)
    if result:
        return render_template('listalibri.html', libri=listaLibri, search=string, genere = None) #TODO fare metodo per ricevere i libri
    else:
        flash(messaggio)
        return redirect(request.referrer)

#################################
##  visualizza lista per genere 
#################################
@app.route("/genere/<idgenere>")
def genere(idgenere):
    #TODO controllo input
    messaggio, result, genere = app.model.getGenere(idgenere)
    if not result:
        flash(messaggio)
        return redirect(request.referrer)
    listaLibri=[]
    #messaggio, result, listaLibri = app.model.getLibriPerGenere(idgenere) #TODO fare metodo per ricevere i libri
    if result:
        return render_template('listalibri.html', libri=listaLibri, genere = genere)
    else:
        flash(messaggio)
        return redirect(request.referrer)
#################################
##  visualizza dettagli libro 
#################################
@app.route("/libro/<isbn>")
def vislibro(isbn):
    messaggio, result, libro = app.model.getLibro(isbn) #gestisco la modifica del libro ottengo una lista con i dati
    if not result:
        flash(messaggio)
        abort(404)
    if session['usertype'] == 0:
        quantcarr = session['carrello'].get(isbn)
        if not quantcarr:
            quantcarr = 0
    elif session['usertype'] == 1:
        messaggio, result, dettRelLibOrd = app.model.isInCart(session['idord'],isbn)
        if result:
            quantcarr = dettRelLibOrd['rel_quant']
        else:
            quantcarr = 0
    else:
        quantcarr = 0
    settclassifica = (date.today()-libro['dataaggclas']).days/7
    return render_template('vislibro.html',libro=libro, settclassifica = int(settclassifica),quantcarr=int(quantcarr))

#################################
##  Dashboard 
#################################
@app.route("/dashboard")
def dashboard():
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

    messaggio, result, isbn = app.model.addLibro( isbn, titolo, datapub, prezzo, punti, descr, posclas , immagine , idedit, quant, idaut,idgenere) #la posizione in classifica sarà aggiornata dopo, viene settatta automatifcamente a 11
    if not result:
        flash(messaggio)
        return redirect(request.referrer)
    # if posclas != '11':
    #     flash('Classifica aggiornata')
    #     #setta la posizione del libro in classifica
    flash('Libro aggiunto')
    return redirect("/libro/"+isbn)

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
    if immagine == 'None':
        immagine=''
    messaggio, result = app.model.modLibro(isbn, titolo, datapub, prezzo, punti, descr, immagine, idedit, quant, idaut, idgenere) #la posizione in classifica sarà aggiornata dopo, viene settatta automatifcamente a 11
    if not result:
        flash(messaggio)
        return redirect(request.referrer)
    if posclas != oldposclas:
        messaggio, result = app.model.aggiornaClassifica(isbn, posclas)
        flash(messaggio)
    flash('Libro modificato')
    return redirect("/libro/"+isbn)


@app.route("/modclass", methods=['POST'])
def modclass():
    checksession(2)
    isbn = request.form['isbn']
    posclas = request.form['posclas']
    oldposclas = request.form['oldposclas']
    if posclas != oldposclas:
        messaggio, result = app.model.aggiornaClassifica(isbn, posclas)
        flash(messaggio)
    return redirect(request.referrer)

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
    nomegenere = request.form['nomegenere']
    immaginegenere=''
    if 'immaginegenere' in request.files:
        file = request.files['immaginegenere']
        if file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.folder_generi, filename))
            immaginegenere = filename
    messaggio, result, idgenere = app.model.addGenere(nomegenere,immaginegenere)
    if result:
        flash('Genere %s aggiunto con id %s'%(nomegenere, idgenere))
        return redirect('/modgenere/'+str(idgenere))
    flash(messaggio)
    return redirect(request.referrer)

######    modifica genere

@app.route("/modgenere/<idgenere>")
def modgenere(idgenere):
    checksession(2)

    messaggio, result, genere = app.model.getGenere(idgenere)
    if not result:
        flash(messaggio)
        return redirect(request.referrer)
    
    libri = []
    messaggio, result, libri = app.model.getClassificaPerGenere(idgenere)
    if not result:
        flash(messaggio)
        return redirect(request.referrer)
    return render_template('modgenere.html', genere = genere, libri = libri )
    #TODO aggiungere lista libri del genere


@app.route("/execmodgenere", methods=['POST'])
def execmodgenere():
    checksession(2)
    idgenere = request.form['idgenere']
    nomegenere = request.form['nomegenere']
    immaginegenere=request.form['immaginegenere']
    if 'immaginegenere' in request.files:
        file = request.files['immaginegenere']
        if file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.folder_generi, filename))
            immaginegenere = filename
    messaggio, result = app.model.modGenere(idgenere, nomegenere,immaginegenere)
    if result:
        flash('Genere modificato')
        return redirect('/modgenere/'+idgenere)
    flash(messaggio)
    return redirect(request.referrer)

    
#################################
##  Carrello 
#################################
@app.route("/carrello")
def carrello():
    if session['usertype'] ==2:
        abort(403)
    if session['usertype'] ==0:
        listalibri = list(session['carrello'].keys()) # prendo le chiavi (cioè l'isbn) e le trasformo in una lista
        messaggio, result, libri = app.model.getLibri(listalibri)
    else:
        messaggio, result, libri = app.model.getLibriInOrd(session['idord'])
        if not result:
            flash(messaggio)
            libri = []
    return render_template('carrello.html', libri= libri)

#################################
##  aggiungi al carrello
#################################
@app.route("/addtocart", methods=['POST'])
def addtocart():
    isbn = request.form['isbn']
    quant = request.form['quant']

    if session['usertype'] == 0:
        carrello = session['carrello']
        carrello[isbn] = quant
        session['carrello'] = carrello
    elif session['usertype'] == 1:
        #TODO carrello registrato
        idord = session['idord'] 
        messaggio, result = app.model.addCart(idord, isbn, quant)
        if not result:
            flash(messaggio)
    return redirect(request.referrer)

#################################
##  rimuovi dal carrello 
#################################
@app.route("/remlibcar/<isbn>")
def remlibcar(isbn):
    if session['usertype'] == 0:
        carrello = session['carrello']
        carrello.pop(isbn, None)
        session['carrello'] = carrello
    elif session['usertype'] == 1:
        messaggio, result = app.model.remLibOrd(session['idord'],isbn)
        if not result:
            flash(messaggio)
    else:
        abort(403)
    return redirect(request.referrer)

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