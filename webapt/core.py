import apt

cache = apt.Cache()
cache.open()

allpkg = cache.keys()

def get_jumlah_pkg():
	return len(allpkg)

def get_all_pkgname():
	print "\n".join(sorted(allpkg))

def count_installed_pkg():
	installed = []
	for pkg in allpkg:
		selected_pkg = cache[pkg]

		if selected_pkg.is_installed:
			installed.append(pkg)

	return len(installed)

def count_upgradable_pkg()
	
