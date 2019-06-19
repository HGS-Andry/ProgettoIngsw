from flask import *
from psycopg2 import *

app = Flask(__name__)

@app.route("/")
def main():
    # gestiamo il main, bisogna gestire se siamo registrati o meno
    # 
    return render_template('main.html')

if __name__ == '__main__':
    app.run(port=5000, debug=False)