
VERSION = 1.2.4
BUILD = 1
PREFIX = /usr
INSTALL = /usr/bin/install
PROGRAM = medidas
MAKEPKG = /sbin/makepkg

clean:
	@echo "Clean..."
	@find . -name *~ | xargs rm -f

build_forms:
	@echo "Libraries..."
	pyuic4 -o forms/Ui_calc.py forms/calc.ui
	pyuic4 -o forms/Ui_altitude_dialog.py forms/altitude_dialog.ui
	@sed -i 's/utf\-8/iso\-8859\-1/' forms/Ui_calc.py
	@sed -i 's|images|/usr/lib/medidas/images|' forms/Ui_calc.py
	@sed -i 's/utf\-8/iso\-8859\-1/' forms/Ui_altitude_dialog.py
	@sed -i 's|images|/usr/lib/medidas/images|' forms/Ui_altitude_dialog.py

install_programs:
	$(INSTALL) -D --mode=0755 src/mcalc $(DESTDIR)/$(PREFIX)/bin/mcalc
	@sed -i '/^##>/,/^##</ d; s/^#sys/sys/' $(DESTDIR)/$(PREFIX)/bin/mcalc

install_libs:
	$(INSTALL) -D --mode=0644 libs/medidas.py $(DESTDIR)/$(PREFIX)/lib/$(PROGRAM)/medidas.py

install_uis:
	$(INSTALL) -D --mode=0644 forms/Ui_calc.py $(DESTDIR)/$(PREFIX)/lib/$(PROGRAM)/Ui_calc.py
	$(INSTALL) -D --mode=0644 forms/Ui_altitude_dialog.py $(DESTDIR)/$(PREFIX)/lib/$(PROGRAM)/Ui_altitude_dialog.py

install_desktop:
	$(INSTALL) -D --mode=0644 docs/mcalc.desktop $(DESTDIR)/$(PREFIX)/share/applications/mcalc.desktop
	$(INSTALL) -D --mode=0644 forms/images/calculator.png $(DESTDIR)/$(PREFIX)/lib/$(PROGRAM)/images/calculator.png
	$(INSTALL) -D --mode=0644 forms/images/arrow-up.png $(DESTDIR)/$(PREFIX)/lib/$(PROGRAM)/images/arrow-up.png
	$(INSTALL) -D --mode=0644 forms/images/arrow-down.png $(DESTDIR)/$(PREFIX)/lib/$(PROGRAM)/images/arrow-down.png
	$(INSTALL) -D --mode=0644 forms/images/arrow-left.png $(DESTDIR)/$(PREFIX)/lib/$(PROGRAM)/images/arrow-left.png
	$(INSTALL) -D --mode=0644 forms/images/arrow-right.png $(DESTDIR)/$(PREFIX)/lib/$(PROGRAM)/images/arrow-right.png

install: clean
	@echo "Install..."
	make build_forms install_libs install_programs install_uis install_desktop

uninstall:
	@echo "Uninstall..."
	@rm $(DESTDIR)/$(PREFIX)/bin/mcalc
	@rm -rf $(DESTDIR)/$(PREFIX)/lib/$(PROGRAM)
	@rm $(DESTDIR)/$(PREFIX)/share/applications/mcalc.desktop

package:
	@echo "Remember to run this option as root!"
	@rm -rf /tmp/package-$(PROGRAM)
	@mkdir -p /tmp/package-$(PROGRAM)
	@make DESTDIR=/tmp/package-$(PROGRAM) install
	@cd /tmp/package-$(PROGRAM) && $(MAKEPKG) -c y -l y /tmp/$(PROGRAM)-$(VERSION)-noarch-$(BUILD).tgz && cd - && rm -rf /tmp/package-$(PROGRAM)

windows:
	@echo "Remember to run this option as root!"
	@rm -rf /tmp/$(PROGRAM)
	@mkdir -p /tmp/$(PROGRAM)
	@make DESTDIR=/tmp/$(PROGRAM) install
	@sed -i 's|/usr/lib/%s|c:/medidas/usr/lib/%s|' /tmp/$(PROGRAM)/usr/bin/mcalc
	@sed -i '/^ *set_procname(__program_name__)/ d' /tmp/$(PROGRAM)/usr/bin/mcalc
	@sed -i 's|/usr/lib/medidas/images/calculator.png|c:/medidas/usr/lib/medidas/images/calculator.png|' /tmp/$(PROGRAM)/usr/lib/medidas/Ui_calc.py
	@sed -i 's|/usr/lib/medidas/images/arrow-left.png|c:/medidas/usr/lib/medidas/images/arrow-left.png|' /tmp/$(PROGRAM)/usr/lib/medidas/Ui_calc.py
	@sed -i 's|/usr/lib/medidas/images/arrow-up.png|c:/medidas/usr/lib/medidas/images/arrow-up.png|' /tmp/$(PROGRAM)/usr/lib/medidas/Ui_calc.py
	@sed -i 's|/usr/lib/medidas/images/arrow-down.png|c:/medidas/usr/lib/medidas/images/arrow-down.png|' /tmp/$(PROGRAM)/usr/lib/medidas/Ui_calc.py
	@sed -i 's|/usr/lib/medidas/images/arrow-right.png|c:/medidas/usr/lib/medidas/images/arrow-right.png|' /tmp/$(PROGRAM)/usr/lib/medidas/Ui_calc.py
	@echo "c:\Python26\python c:\medidas\usr\bin\mcalc" >> /tmp/$(PROGRAM)/mcal.bat
	@todos /tmp/$(PROGRAM)/usr/bin/mcalc
	@todos /tmp/$(PROGRAM)/usr/lib/medidas.py
	@todos /tmp/$(PROGRAM)/usr/lib/medidas/Ui_calc.py
	@cd /tmp && zip -r $(PROGRAM)-$(VERSION)-windows-$(BUILD).zip $(PROGRAM)

