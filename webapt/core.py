import apt_pkg
import apt

apt_pkg.init()
cachepkg = apt_pkg.Cache()
cache = apt.Cache()
cache.open()

allpkg = cache.keys()
allfromaptpkg = cachepkg.packages

def get_jumlah_pkg():
	return len(allpkg)

def get_all_pkgname():
	print "\n".join(sorted(allpkg))

def jml_pkg_all_installed():
	all_installed = []
	for pkg in allpkg:
		selected_pkg = cache[pkg]

		if selected_pkg.is_installed:
			all_installed.append(pkg)

	return len(all_installed)

def jml_pkg_upgradable():
	upgradable = []
	for pkg in allpkg:
		upgradable_pkg = cache[pkg]

		if upgradable_pkg.is_upgradable:
			upgradable.append(pkg)

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
	
	
def get_section(pkg):
	if pkg in allpkg:
		pkg = cache[pkg]	
		return pkg.section
	else:
		return pkg.installed.section

def get_component(pkg):
	pkg = cache[pkg]
	componen = pkg.installed.origins[0].component
	return componen
