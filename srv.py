##(c) 2013, blackshirtmuslim@yahoo.co.id

from flask import Flask, render_template, flash, request, url_for
app = Flask(__name__)
app.secret_key = 'some'
from webapt.core import cache


##test
@app.route('/base')
def base():
	return render_template('base.html')

@app.route('/view/<path:paket>')
def view(paket=None):
	paket = paket
	return render_template('view', paket=paket)

@app.route('/list/<path:status>')
def list(status=None):
	status = status
	return render_template('list', status=status)

@app.route('/install/<path:paket>')
def install(paket=None):
	with cache.actiongroup():
    	for paket in my_selected_packages:
        paket.mark_install()
	paket.commit()
	return render_template('install', paket=paket)

@app.route("/update")
def update():
	flash('Please wait for update')
	cache_updated = cache.update()
	if cache_updated == True:
		return "cache updated", 200
	else:
		return "cache update failed", 500
	
@app.route("/commit")
def commit():
	with cache.actiongroup():
    	for paket in my_selected_packages:
        paket.mark_install()
	paket.commit(apt.progress.base.AcquireProgress(), apt.progress.base.OpProgress())

@app.route("/upgradable")
def view_upgradabale():
	pass

@app.route("/newpackages")
def new_packages():
	pass

@app.route("/installed")
def view_installed()
	pass

@app.route("/notinstalled")
def view_not_installed()
	pass



if __name__ == '__main__':
	app.run(debug=True)