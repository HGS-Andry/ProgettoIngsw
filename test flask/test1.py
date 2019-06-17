from flask import *
from flask.templating import render_template
from psycopg2 import *
import psycopg2.extras

from model import Model

app = Flask(__name__)
app.model = Model()
name= "Qualcosa"


@app.route("/")
def index():
    alert = ""
    if request.args:
        alert = request.args['alert'] 
    listacose = app.model.getlistacose()
    return render_template('intro.html', titolo = name, alert = alert, lista = listacose)

@app.route("/inserttable")
def inserttable():
    return render_template('inserttable.html', titolo = name)

@app.route("/addrow", methods=['POST'])
def addttable():
    nome = request.form['nome']
    quant = request.form['quant']
    messaggio = app.model.insertcose(nome,quant)
    return redirect("/?alert=" + messaggio)

@app.teardown_appcontext
def __del__(error):
    print("| controller close")
    print(error)
    app.model.close()

if __name__ == '__main__':
    app.run(port=5000, debug=False)
