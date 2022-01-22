# Makefile at /
ZIP = zip
DIR_NAME = "Font Replacement for Insignia"
PKG_NAME = Font_Replacement_for_Insignia.zip

.PHONY: package clean

package: clean
	cp -r mod $(DIR_NAME)
	$(ZIP) -r $(PKG_NAME) $(DIR_NAME)
	rm -fr $(DIR_NAME)

clean:
	rm -fr $(PKG_NAME) $(DIR_NAME)
