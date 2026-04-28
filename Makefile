install:
	python3 -m venv virt_env
	virt_env/bin/pip install -r requirements.txt
run:
	virt_env/bin/python3 main.py maps/easy/01_linear_path.txt
debug:
	python3 -m pdb fly_in.py
clean:
	rm -rf /__pycahce__
lint:
	flake8 . and mypy . --warn-return-any \
	--warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs \
	--check-untyped-defs
