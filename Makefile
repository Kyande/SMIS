all: clean dist

clean:
	python setup.py clean --all
	rm -rf dist build

build:
	python setup.py build

dist:
	python setup.py build sdist

.PHONY: clean build dist all
