release:
	python setup.py clean --all
	python setup.py sdist upload
	python setup.py bdist_wheel --universal upload

autotest:
	find . -name '*.py' | entr py.test
