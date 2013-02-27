##(c) 2013, blackshirtmuslim@yahoo.co.id

from flask import Flask, render_template, flash, request, url_for, redirect
app = Flask(__name__)
app.secret_key = 'some'
from webapt import core


##test
@app.route('/base')
def base():
	return render_template('base.html')

@app.route('/')
def index():
	return redirect(url_for('home'))

@app.route('/view/<path:section>')
def view(section=None):
	section = section
	return render_template('view.html', section=section)

@app.route('/paket/<path:name>')
def paket(name=None):
	cachepkg = core.cache[name]
	nama = cachepkg.shortname
	return render_template('paket.html', nama=nama)

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
def view_installed():
	pass

@app.route("/notinstalled")
def view_not_installed():
	pass

@app.route("/home")
def home():
	entry = core.get_all_section()
	return render_template('menu.html', entry=entry)


if __name__ == '__main__':
	app.run(debug=True)
