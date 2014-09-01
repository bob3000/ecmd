all: ecmd.egg-info man/ecmd.1.gz

install: all
	python3 setup.py install

ecmd.egg-info:
	python3 setup.py egg_info

test: all
	python3 setup.py test

coverage: clean
	coverage3 run --source=. setup.py test
	coverage3 html
	coverage3 report

man/ecmd.1.gz:
	gzip -kf man/ecmd.1

pep8:
	pep8 .

clean:
	python3 setup.py clean
	rm -rf ecmd.egg-info ecmd-?.?.?
	rm -rf .coverage htmlcov/
	rm -rf man/ecmd.1.gz
	rm -rf test_config
	rm -rf build
	rm -rf dist
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete
