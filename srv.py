##(c) 2013, blackshirtmuslim@yahoo.co.id

from flask import Flask, render_template
app = Flask(__name__)


@app.route('/view/<path:paket>')
def view(paket=None):
	paket = paket
	return render_template('view', paket=paket)

@app.route('/list/<path:status>'):
def list(status=None):
	status = status
	return render_template('list', status=status)

@app.route('/install/<path:paket>'):
def install(paket=None):
	paket = paket
	return render_template('install', paket=paket)

@app.route('/update')
def update():
	return update()



if __name__ == '__main__'
	app.run(debug=True)