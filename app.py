# -*- coding: utf-8 -*-
# more modules this https://pypi.python.org/pypi/
import os, sys
# add paths for local modules
base_dir = os.path.dirname(os.path.abspath(__file__))
lib_flask = os.path.abspath(os.path.join(base_dir + '/modules/flask/'))
sys.path.append(lib_flask)
lib_werkzeug = os.path.abspath(os.path.join(base_dir + '/modules/Werkzeug/'))
sys.path.append(lib_werkzeug)
lib_jinja2 = os.path.abspath(os.path.join(base_dir + '/modules/Jinja2/'))
sys.path.append(lib_jinja2)
lib_markupsafe = os.path.abspath(os.path.join(base_dir + '/modules/markupsafe/'))
sys.path.append(lib_markupsafe)
lib_itsdangerous = os.path.abspath(os.path.join(base_dir + '/modules/itsdangerous/'))
sys.path.append(lib_itsdangerous)
# flask module
from flask import Flask, request, redirect, url_for, render_template, send_from_directory, jsonify
#app = Flask(__name__, static_url_path='')
app = Flask(__name__)
# bind to libreoffice module
from app_rununo import * #unoConnect, unoOpen, unoSave, replaceText
# parse data module
from app_parse_data import * 

# config
#file     = "myfile.odt"
#new_file = "new_myfile.odt"

# coonect to libreoffice
#desktop = unoConnect(host, port)

# Flask ON
app.url_map.strict_slashes = False   # Mixing /a/ and /a
#app.config["JSON_SORT_KEYS"] = False # No sort json items
#app.config['JSON_AS_ASCII'] = False  # Not use ASCII

@app.route("/")
#@app.route('/<name>')
def hello(name = None):
    return render_template('hello.html', name=name)

@app.route('/post', methods=['GET','POST'])
#@app.route('/post/<error>', methods=['GET','POST'])
def toReport(error = None):
    if request.method == 'POST':
        # parse data
        try:
            dataMap = request.data.decode('cp1251') # decode from cp1251
            #print("!!!!!!!!!!!!!!!!!!cp1251"+dataMap)
            #return dataMap
            return parseData(request.mimetype, dataMap)
        except Exception:
            dataMap = request.data.decode('utf-8') # decode from utf-8
            #print("!!!!!!!!!!!!!!!!utf-8"+dataMap)
            #return dataMap
            return parseData(request.mimetype, dataMap)
    else:
        return render_template('post.html', error=error)
        
if __name__ == "__main__":
    app.run(debug = True, host='0.0.0.0', port=8081) # debug - auto reload