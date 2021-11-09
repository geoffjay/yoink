reqi = requirements.in requirements-dev.in
reqo = $(reqi:.in=.txt)

all: serve

serve:
	@python main.py

%.txt: %.in $(REQ)
	@pip-compile --output-file=$@ $<

requirements: $(reqo)
