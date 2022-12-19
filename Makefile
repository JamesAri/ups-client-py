VENV = venv
PYTHON ?= $(VENV)/bin/python3.10
PIP ?= $(VENV)/bin/pip
CMD = build

# ifeq ($(CMD),run)
# ifndef USERNAME
# $(error USERNAME is not set. Usage: make CMD=run USERNAME=<your_username>)
# endif
# run: $(VENV)/bin/activate
# 	$(PYTHON) main.py $(USERNAME)
# endif

$(VENV)/bin/activate: requirements.txt
	python3.10 -m venv $(VENV)
	$(PIP) install -r requirements.txt

clean:
	rm -rf __pycache__
	rm -rf $(VENV)
