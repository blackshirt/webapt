import apt_pkg
import apt
import itertools


#apt_pkg.init()
#cachepkg = apt_pkg.Cache()

#operationoutput = open('temp/opoutput','w')
#acquireoutput = open('temp/acqoutput', 'w')
opprogress = apt.progress.text.OpProgress()
#acqprogress = apt.progress.text.AcquireProgress()

cache = apt.Cache()

allpkg = cache.keys()
#allfromaptpkg = cachepkg.packages

def database_init():
	return cache

def open_database():
	return cache.open()

def update_database():
	cache.update(acqprogress)

	
def get_jumlah_pkg():
	return len(allpkg)

def get_all_pkgname():
	print "\n".join(sorted(allpkg))

def jml_pkg_all_installed():
	#all_installed = []
	with cache.actiongroup():
		all_installed = [cache[pkg] for pkg in allpkg if cache[pkg].is_installed]
	#	for pkg in allpkg:
	#		selected_pkg = cache[pkg]

	#		if selected_pkg.is_installed:
	#			all_installed.append(pkg)

	return len(all_installed)

def jml_pkg_upgradable():
	#upgradable = []
	with cache.actiongroup():
		upgradable = [pkg for pkg in allpkg if cache[pkg].is_upgradable]
	#for pkg in allpkg:
	#	upgradable_pkg = cache[pkg]

	#	if upgradable_pkg.is_upgradable:
	#		upgradable.append(pkg)

	return len(upgradable)

def jml_pkg_installed():
	installed = jml_pkg_all_installed()
	upgradable = jml_pkg_upgradable()
	return (installed - upgradable)

def jml_pkg_virtual():
	virtual = []
	for pkg in allfromaptpkg:
		if(pkg.has_provides and not pkg.has_versions):
			virtual.append(pkg)
	return len(virtual)
	
	
def get_section_for(pkg):
	if pkg in allpkg:
		pkg = cache[pkg]	
		return pkg.section
	else:
		return pkg.installed.section

def get_component_for(pkg):
	pkg = cache[pkg]
	componen = pkg.installed.origins[0].component
	return componen

def get_all_section():
	with cache.actiongroup():
		cachepkt = (cache[x] for x in allpkg)
		newlist = (pkg.section for pkg in cachepkt if pkg.installed)
	return sorted(set(newlist))

def get_description(paket):
	pkg = cache[paket]
	if pkg.candidate:
		return pkg.candidate.description

def build_dict():
	data = {}
	with cache.actiongroup():
		for nama in allpkg:
			descr = get_description(nama)
			data.update({nama: descr})
	return data
	
def get_all_component():
	pass

def get_yang_berubah():
	return cache.get_changes()

def count_paket_dari_section(section):
	with cache.actiongroup():
		all_pkgs = (cache[name] for name in allpkg)
   		packages = [pkg for pkg in all_pkgs if pkg.section == section]
   	return len(packages)

def paginate(iterable, page_size):
    while True:
        i1, i2 = itertools.tee(iterable)
        iterable, page = (itertools.islice(i1, page_size, None),
                list(itertools.islice(i2, page_size)))
        if len(page) == 0:
            break
        yield page

def slicepaket(section=None, size=16):
	with cache.actiongroup():
		paketnya = (cache[pkg] for pkg in allpkg if cache[pkg].section == section)
		#all_pkgs=(cache[name] for name in allpkg)
		#paketnya = (pkg for pkg in all_pkgs if pkg.section == section)
		slicelist = list(paginate(paketnya, size))
	return slicelist