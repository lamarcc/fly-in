NAME        = codexion
UV          = uv
PYTHON      = python3
RM          = rm -rf
SRCDIR      = src
MYPYFLAGS   = --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

SRCS        = $(SRCDIR)/main.py

install:
	$(UV) sync

run:
	$(UV) run $(SRCS)

debug:
	$(UV) run $(PYTHON) -m pdb $(SRCS)

lint:
	$(UV) run flake8 $(SRCDIR)
	$(UV) run mypy $(SRCDIR) $(MYPYFLAGS)

clean:
	find $(SRCDIR) -type d -name "__pycache__" -exec rm -rf {} +
	$(RM) .mypy_cache

.PHONY: install run debug lint lint-strict clean
