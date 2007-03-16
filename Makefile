# python setup.py --help bdist_rpm
#
# Mandriva policy is here:
# http://wiki.mandriva.com/en/Policies/Python

all:
	@echo 'supported target are:'
	@echo 'rpm (create a rpm)'
	@echo 'src (create a source package)'
	@echo 'install (install on your machine)'

install:
	python setup.py install

src:
	python setup.py sdist

rpm:
	python setup.py bdist_rpm \
	       	--requires python-imaging,pygtk \
		--packager bsergean@gmail.com
