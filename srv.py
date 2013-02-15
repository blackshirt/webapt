##(c) 2013, blackshirtmuslim@yahoo.co.id


@app.route('/view/<path:paket>')
def view(paket):
	paket = paket
	return render_template('view', paket=paket)

@app.route('/list/<path:status>'):
def list(status):
	status = status
	return render_template('list', status=status)

@app.route('/install/<path:paket>'):
def install(paket):
	paket = paket
	return render_template('install', paket=paket)

@app.route('/update')
def update():
	return update()


