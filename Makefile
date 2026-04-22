install:
	python3 -m venv virt_env
run:
	virt_env/bin/python3 fly_in.py
debug:
	python3 -m pdb fly_in.py
clean:
# 	rm -rf smth
lint:
	flake8 . and mypy . --warn-return-any \
	--warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs \
	--check-untyped-defs
