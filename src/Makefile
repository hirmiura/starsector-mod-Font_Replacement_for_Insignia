# Makefile at /src
BMFONT = bmfont64.exe
PYTHON = python3
FNTNAME = NSJM
FNTS = $(FNTNAME)15aa.fnt $(FNTNAME)21aa.fnt $(FNTNAME)25aa.fnt
DST = ../mod/graphics/fonts/

.PHONY: all bmfc fnt install clean clean-fnt clean-bmfc clean-install
.SUFFIXES: .fnt .bmfc

all: bmfc fnt

.bmfc.fnt:
	$(BMFONT) -c $< -o $@

bmfc: bmfcgen.json
	$(PYTHON) bmfcgen.py

fnt: bmfc $(FNTS)

install:
	mv $(FNTNAME)15aa.fnt $(DST)insignia15LTaa.fnt
	mv $(FNTNAME)21aa.fnt $(DST)insignia21LTaa.fnt
	mv $(FNTNAME)25aa.fnt $(DST)insignia25LTaa.fnt
	mv *.png $(DST)

clean: clean-fnt clean-bmfc

clean-fnt:
	rm -f *.fnt *.png

clean-bmfc:
	rm -f *.bmfc

clean-install:
	rm -f $(DST)*fnt $(DST)*.png
