##(c) 2013, blackshirtmuslim@yahoo.co.id
#

import gevent.monkey
gevent.monkey.patch_all()

import apt, subprocess

from flask import Flask, render_template, flash, request, url_for, redirect, Response
app = Flask(__name__)
app.secret_key = 'some'

import os
from webapt import core, pagination


PER_PAGE = 17
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

@app.route('/open')
def open():
    out = subprocess.check_output('python webapt/open.py'.split())
    return render_template('update.html', out=out)

@app.route('/update')
def update():
    out = subprocess.check_output('python webapt/update.py'.split())
    return render_template('update.html', out=out)

@app.route("/commit")
def commit():
    for paket in core.get_yang_berubah():
        out = subprocess.check_output('python webapt/commit.py'.split())
    return render_template('resultinstall.html', out=out)
		
@app.route('/search', methods=['GET', 'POST'])
def search():
	searchtext = None
	found = []
	if request.method == 'POST':
		searchtext = request.form.get('search_text', 'Not deffined')
		print "searchtext is : %r" % (searchtext)
		found = [ paket	for paket in core.allpkg if searchtext in paket]
	return render_template('result.html', found=found)

@app.route("/statistic")
def statistic():
	data = dict(jml=core.get_jumlah_pkg(), all=core.jml_pkg_all_installed(), upgradable=core.jml_pkg_upgradable(), installed=core.jml_pkg_installed())
	#data = core.statistik()
	return render_template("statistic.html", data=data)

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/apply')
def apply():
	perubahan = core.get_yang_berubah()
	return render_template('apply.html', perubahan=perubahan)


#
if __name__ == '__main__':
	app.run(debug=True)
#
#if __name__ == '__main__':
#	import gevent.monkey
#	from gevent.wsgi import WSGIServer
#	from werkzeug.serving import run_with_reloader
#	from werkzeug.debug import DebuggedApplication
#	gevent.monkey.patch_all()

#	@run_with_reloader
#	def run_server():

#		http_server = WSGIServer(('', 5000), DebuggedApplication(app))
#		http_server.serve_forever()
 
#	run_server()
    

