from __future__ import print_function
from flask import *
from flaskext.mysql import MySQL
import sys
from testepyserial import *

control = ControladorSensores()
dbm = ControladorBanco("localhost", "root", "", "sensor")


app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def index():
	return render_template("index.html")
    
@app.route('/getLeituras', methods = ['GET', 'POST'])
def getLeituras():
	return jsonify(dbm.getLeituras())

@app.route('/getUltimaLeitura', methods = ['GET', 'POST'])
def getUltimaLeitura():
	return jsonify(dbm.getUltimaLeitura())
