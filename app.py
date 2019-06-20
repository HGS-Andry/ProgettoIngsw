from flask import *
# from psycopg2 import *

app = Flask(__name__)
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
def exec_login():
    # gestiamo il login, con la scelta se utenti o amministratori
    #if 'usertype' in [session]:
    session['usertype'] = 1 # in caso di utente registrato
    return redirect("/")

@app.route("/logout")
def exec_logout():
    # gestiamo il logout
    session['usertype'] = 0 # in caso di utente registrato
    return redirect("/")

@app.route("/registrati")
def registrati():
    # gestiamo la form della registrazione
    return render_template('registrazione.html')

@app.route("/execregist", methods=['POST'])
def exec_regist():
    # gestiamo la registrazione
    #if 'usertype' in [session]:
    #session['usertype'] = 1 # Una volta registrato fa direttamente il login?
    return redirect("/")  

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