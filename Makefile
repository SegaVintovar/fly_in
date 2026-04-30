install:
	python3 -m venv virt_env
	virt_env/bin/pip install -r requirements.txt

# AI made these for me:
# Example map paths:
# maps/easy/01_linear_path.txt
# maps/easy/02_simple_fork.txt
# maps/easy/03_basic_capacity.txt
# maps/medium/01_dead_end_trap.txt
# maps/medium/02_circular_loop.txt
# maps/medium/03_priority_puzzle.txt
# maps/hard/01_maze_nightmare.txt
# maps/hard/02_capacity_hell.txt
# maps/hard/03_ultimate_challenge.txt
# maps/challenger/01_the_impossible_dream.txt
run:
	virt_env/bin/python3 main.py maps/easy/03_basic_capacity.txt
debug:
	python3 -m pdb fly_in.py
clean:
	rm -rf /__pycahce__
lint:
	flake8 . and mypy . --warn-return-any \
	--warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs \
	--check-untyped-defs
