release:
	bumpversion --current-version `cat VERSION` --no-commit --allow-dirty patch VERSION
	python setup.py clean --all
	python setup.py sdist upload
	python setup.py bdist_wheel --universal upload

autotest:
	find . -name '*.py' | entr py.test
