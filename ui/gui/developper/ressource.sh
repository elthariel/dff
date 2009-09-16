#!/bin/sh

rm gui_rc.py

lrelease i18n/*fr.ts -qm i18n/Dff_fr.qm
lrelease i18n/*en.ts -qm i18n/Dff_en.qm
pyrcc4 gui.qrc -o gui_rc.py
