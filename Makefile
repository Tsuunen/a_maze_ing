MAIN=a_maze_ing.py
MYPY_FLAGS=--warn-return-any --warn-unused-ignores \
		   --ignore-missing-imports --disallow-untyped-defs \
		   --check-untyped-defs

run:
	@python3 $(MAIN)

debug:
	@python3 -m pdb $(MAIN)

install:
	@echo "Nothing to install"

clean:
	rm -rf __pycache__ .mypy_cache

lint:
	flake8 .
	mypy . $(MYPY_FLAGS)

lint-strict:
	flake8 .
	mypy . --strict
