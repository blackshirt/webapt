##(c) 2013, blackshirtmuslim@yahoo.co.id

from flask import Flask, render_template, flash, request, url_for, redirect
app = Flask(__name__)
app.secret_key = 'some'
import gevent.monkey
gevent.monkey.patch_all()

from webapt import core


##test
##@app.route('/base')
#def base():
#	return render_template('base.html')
entry = core.get_all_section()

@app.route('/')
def index():
	core.open_database()
	return render_template('base.html', entry=entry)
	
@app.route('/view/<path:section>')
def view(section=None):
    with core.cache.actiongroup(): 	
    	all_pkgs = (core.cache[name] for name in core.cache.keys())
    	packages = [pkg for pkg in all_pkgs if pkg.section == section]
    return render_template('view.html', packages=packages, entry=entry)

@app.route('/paket/<path:name>')
def paket(name=None):
	cachepkg = core.cache[name]
	nama = cachepkg.shortname
	paket = cachepkg.candidate
	deskripsi = paket.description
	return render_template('paket.html', entry=entry, nama=nama, deskripsi=deskripsi)

@app.route('/list/<path:status>')
def list(status=None):
	status = status
	return render_template('list', status=status)

@app.route('/install/<path:paket>')
def install(paket=None):
	paketchanges = core.get_yang_berubah()
	with core.cache.actiongroup():
		for paket in paketchanges :
			paket.mark_install()
		return render_template('install.html', paket=paketchanges)

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
	return render_template('menu.html', entry=entry)

@app.route('/about')
def about():
	return render_template('about.html', entry=entry)

@app.route('/apply')
def apply():
	perubahan = core.get_yang_berubah()
	return render_template('apply.html', perubahan=perubahan, entry=entry)

PER_PAGE = 20

@app.route('/users/', defaults={'page': 1})
@app.route('/users/page/<int:page>')
def show_users(page):
    count = count_all_users()
    users = get_users_for_page(page, PER_PAGE, count)
    if not users and page != 1:
        abort(404)
    pagination = Pagination(page, PER_PAGE, count)
    return render_template('users.html',
        pagination=pagination,
        users=users
    )

if __name__ == '__main__':
	app.run(debug=True)

#if __name__ == '__main__':
#    import gevent.monkey
#    from gevent.wsgi import WSGIServer
#    from werkzeug.serving import run_with_reloader
#    from werkzeug.debug import DebuggedApplication
#    gevent.monkey.patch_all()
 
#    @run_with_reloader
#    def run_server():
#       http_server = WSGIServer(('', 5000), DebuggedApplication(app))
#        http_server.serve_forever()
 
#    run_server()
    