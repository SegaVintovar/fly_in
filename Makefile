install:
	python3 -m venv virt_env
	virt_env/bin/pip install -r requirements.txt

# AI made these for me:
# Example map paths:
# maps/easy/01_linear_path.txt	i do not finish with the last drone
# maps/easy/02_simple_fork.txt	works 5 steps
# maps/easy/03_basic_capacity.txt	works 4 steps
# maps/medium/01_dead_end_trap.txt	works -8 steps, stoped working with 10d
# maps/medium/02_circular_loop.txt	doesn work, prints spaces
# maps/medium/03_priority_puzzle.txt	works, 7 steps
# maps/hard/01_maze_nightmare.txt		crash after first move
# maps/hard/02_capacity_hell.txt		almost all drones arrived, but some got stuck, some times it is succeceded
# maps/hard/03_ultimate_challenge.txt	does 2 moves and then breaks
# maps/challenger/01_the_impossible_dream.txt
run:
	virt_env/bin/python3 main.py maps/medium/03_priority_puzzle.txt
debug:
	python3 -m pdb fly_in.py
clean:
	rm -rf /__pycahce__
lint:
	flake8 . and mypy . --warn-return-any \
	--warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs \
	--check-untyped-defs
