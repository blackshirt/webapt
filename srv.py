##(c) 2013, blackshirtmuslim@yahoo.co.id

import gevent.monkey
gevent.monkey.patch_all()
from flask import Flask, render_template, flash, request, url_for, redirect, Response
app = Flask(__name__)
app.secret_key = 'some'

import os
from webapt import core, pagination, mythread


entry = core.get_all_section()

def url_for_other_page(page):
	args = request.view_args.copy()
	args['page'] = page
	return url_for(request.endpoint, **args)
app.jinja_env.globals['url_for_other_page'] = url_for_other_page

@app.context_processor
def inject_entry(): 
	return {'entry': entry}

@app.route('/')
def index():
	core.open_database()
	return render_template('base.html')
	
#@app.route('/view/<path:section>')
#def view(section=None):
#    with core.cache.actiongroup(): 	
#    	all_pkgs = (core.cache[name] for name in core.cache.keys())
#    	packages = (pkg for pkg in all_pkgs if pkg.section == section)
#    return render_template('view.html', packages=packages)

PER_PAGE = 17

def get_paket_for_page(section, PER_PAGE, page=1):
	paketnya = core.slicepaket(section, PER_PAGE)
	return sorted(paketnya[page - 1])

@app.route('/view/<path:section>/', defaults={'page': 1})
@app.route('/view/<path:section>/<int:page>')
def show_paket(section=None, page=1):
    count = core.count_paket_dari_section(section)
    paket = get_paket_for_page(section, PER_PAGE, page)
    if not paket and page != 1:
        abort(404)
    paginasi = pagination.Pagination(page, PER_PAGE, count)
    return render_template('view.html', paginasi=paginasi, paket=paket)

@app.route('/paket/<path:name>')
def paket(name=None):
	cachepkg = core.cache[name]
	paket = cachepkg.candidate 
	informasi = dict(Nama = cachepkg.shortname, 
		         Description = paket.description,
		         Essential = cachepkg.essential)
	return render_template('paket.html', informasi=informasi)

@app.route('/list/<path:status>')
def list(status=None):
	status = status
	return render_template('list', status=status)

@app.route('/install/<path:paket>')
def install(paket=None):
	pkg = core.cache[paket]
	if(pkg.is_installed is False):
		pkg.mark_install()
	if(pkg.is_installed and pkg.is_upgradable):
		pkg.mark_upgrade()
	paketchanges = core.get_yang_berubah()
	return render_template('install.html', paketchanges=paketchanges)


@app.route('/download')
def download():
	pass

@app.route("/update")
def update():
	#flash('Please wait for update')
	#cache_updated = cache.update()
	#if cache_updated == True:
	#	return "cache updated", 200
	#else:
	#	return "cache update failed", 500
	#pass
	#'''	apt progress menyediakan opsi output ke file with open('file', 'r') as myfile: codeflow: read_date = myfile.read() file.close() or whatever '''
	#with open('temp/acqoutput', 'rwb', 1) as myfile:
	#	core.update_database()
	#	rows = myfile.readline()
	#	myfile.flush()
	#myfile.close()	
	#return render_template('update.html', rows=rows)
	(rh, wh) = os.pipe()
	rows = os.fdopen(rh, 'r')
	w = os.fdopen(wh, 'w')

	mythread(w).start()
	return render_template('update.html', rows=rows)


@app.route("/commit")
def commit():
	status = False
	with core.cache.actiongroup():
		for paket in core.get_yang_berubah():
			status = paket.commit(core.apt.progress.base.AcquireProgress(), core.apt.progress.base.OpProgress())
		if status == True:
			flash("sukses in install")
			return render_template('resultinstall.html', status=status)
		
@app.route('/search', methods=['GET', 'POST'])
def search():
#from python people in the channel
#data = {}
#keyword = 'apache'
#output = {}
#for key, value in dict.items():
#	if keyword in key or keyword in value:
#		out.update({key: value})
#len(out) ==> untuk menghitung jumlah dict
#print out ==> menampilkan dict yagn memenuhi		
	searchtext = None
	found = []
	if request.method == 'POST':
		searchtext = request.form.get('search_text', 'Not deffined')
		print "searchtext is : %r" % (searchtext)
		found = [ paket	for paket in core.allpkg if searchtext in paket]
	return render_template('result.html', found=found)

@app.route("/upgradable")
def view_upgradabale():
	pass

@app.route("/newpackages")
def new_packages():
	pass

@app.route("/installed")
def view_installed():
	pass

@app.route("/statistic")
def statistic():
	data = dict(jml=core.get_jumlah_pkg(), all=core.jml_pkg_all_installed(), upgradable=core.jml_pkg_upgradable(), installed=core.jml_pkg_installed())
	return render_template("statistic.html", data=data)

@app.route("/notinstalled")
def view_not_installed():
	pass

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/apply')
def apply():
	perubahan = core.get_yang_berubah()
	return render_template('apply.html', perubahan=perubahan)



if __name__ == '__main__':
	app.run(debug=True)
#
#if __name__ == '__main__':
#    import gevent.monkey
#    from gevent.wsgi import WSGIServer
#   from werkzeug.serving import run_with_reloader
#    from werkzeug.debug import DebuggedApplication
#    gevent.monkey.patch_all()

#    @run_with_reloader
#    def run_server():

#       http_server = WSGIServer(('', 5000), DebuggedApplication(app))
#       http_server.serve_forever()
 
#    run_server()
    

