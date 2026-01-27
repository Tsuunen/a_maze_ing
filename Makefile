MAIN=a_maze_ing.py
MYPY_FLAGS=--warn-return-any --warn-unused-ignores \
		   --ignore-missing-imports --disallow-untyped-defs \
		   --check-untyped-defs
FILES=$(MAIN) srcs/

run:
	@python3 $(MAIN) config.txt

debug:
	@python3 -m pdb $(MAIN)

install:
	pip install -r requirement.txt

clean:
	rm -rf __pycache__ .mypy_cache

lint:
	@flake8 $(FILES)
	mypy srcs $(MYPY_FLAGS)
	mypy $(MAIN) $(MYPY_FLAGS)

lint-strict:
	@flake8 $(FILES)
	@mypy srcs $(MYPY_FLAGS) --strict
	@mypy $(MAIN) $(MYPY_FLAGS) --strict
