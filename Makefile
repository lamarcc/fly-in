NAME        = codexion
UV          = uv
PYTHON      = python3
FLAKE       = flake8
RM          = rm -rf
SRCDIR      = src
MYPYFLAGS   = --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

SRCS        = $(SRCDIR)/main.py

install:
	$(UV) sync

run:
	$(UV) run $(SRCS)

clean:
	$(RM) $(OBJDIR)

lint:
	$(FLAKE) $(SRCDIR)/ && $(PYTHON) -m mypy $(SRCDIR)/ $(MYPYFLAGS)

debug:
	$(PYTHON) -m pdb $(SRCS)

.PHONY: install run clean lint debug
