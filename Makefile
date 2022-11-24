VENV = venv
PYTHON ?= $(VENV)/bin/python3
PIP ?= $(VENV)/bin/pip

# ifdef $(USERNAME)
# 	echo Follow README guide or run make USERNAME=your_username
# else
# 	run: $(VENV)/bin/activate
# 	$(PYTHON) main.py $(USERNAME)
# endif


$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt


clean:
	rm -rf __pycache__
	rm -rf $(VENV)
