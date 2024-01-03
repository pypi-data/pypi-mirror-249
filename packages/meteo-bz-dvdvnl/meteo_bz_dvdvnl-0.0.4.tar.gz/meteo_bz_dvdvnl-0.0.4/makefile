clean:
	rm -rf dist/*

build:
	$(MAKE) clean
	python3 -m build

publish:
	python3 -m twine upload dist/*
	
publish-test:
	python3 -m twine upload --repository testpypi dist/*


