import apt

cache = apt.Cache()
cache.open()

allpkg = cache.keys()

def get_jumlah_pkg():
	return len(allpkg)

def get_all_pkgname():
	print "\n".join(sorted(allpkg))

def count_all_installed_pkg():
	all_installed = []
	for pkg in allpkg:
		selected_pkg = cache[pkg]

		if selected_pkg.is_installed:
			all_installed.append(pkg)

	return len(all_installed)

def count_upgradable_pkg():
	upgradable = []
	for pkg in allpkg:
		upgradable_pkg = cache[pkg]

		if upgradable_pkg.is_upgradable:
			upgradable.append(pkg)

	return len(upgradable)

def count_installed_pkg():
	installed = count_all_installed_pkg()
	upgradable = count_upgradable_pkg()
	return (installed - upgradable)

def get_section(pkg):
	if pkg in allpkg:
		pkg = cache[pkg]	
		return pkg.section
	else:
		return pkg.installed.section

def get_component(self, pkg):
	pkg = cache[pkg]
	componen = pkg.installed.origins[0].component
	return componen
