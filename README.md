# Weltzerstörungsknopf
Was der Weltzerstörungskopf ist und eine genaue Dokumentation des Systems findet man [hier](https://github.com/artandtechspace/Weltzerstoerungsknopf-Dokumentation).

# Entwicklungsumgebung aufsetzen
Die Hauptsoftware wurde in Python3.9 entwickelt, daher wird empfohlen eine entsprechende IDE zu installieren. Wir haben dafür [PyCharm Community](https://www.jetbrains.com/pycharm/) genommen, da es aktuelle und entsprechende Funktionen biete und Quelloffen ist. Aber jede andere Entwicklungsumgebung geht selbstverständlich auch.

## Python-Packete
Aufgrund dessen, dass der Pi über GPIO pins verfügt, welche zum ansprechen der Neopixel und anderer Hardware gebraucht wird, müssen auf dem Pi zusätzliche Packete zu den Grundpacketen installiert werden.

Leider kann der Code daher auf deinem Entwicklungsrechner ohne GPIO-Pins lediglich nur entwickelt und in einzelstücken getestet werden.
In künftigen Versionen könnte man diese Probleme durch Development-Packete lösen, welche zum Beispiel ein Interface für die GPIO-Pins mitliefern. Aktuell ist dies allerdings nicht geplant.

Um die Software korrekt auf dem Pi zu installieren sind außerdem noch einige andere Schritte nötig, welche im [Dokumentation-Repository](https://github.com/artandtechspace/Weltzerstoerungsknopf-Documentation) erklärt werden. Daher muss für die Installation der Packete in der Entwicklungsumgebung ledigtlich die

```bash
pip install -r requirements-on-dev.txt
```

genutzt werden.

## Kurzübersicht über die Software
Die Startdatei des Projektes heißt `main.py` im root-Ordner und kann als Python-Module mittels
```bash
python -m main
```
gestartet werden. Für die IDE muss diese Datei auch als Start-Pfad eingetragen werden.

Folgend ist eine kurzübersicht über wichtige Ordner und Dateien des Projekte. Ordner/Dateien, welche nicht erwähnt werden gehören zur Software und sind trotzdem essenziel:
```
Weltzerstoerungsknopf-Software/
  ├─ core/                   - Hier sind die Zustände des Welti und deren Ablauf definiert
  ├─ logs/                   - Enthält alle Logs
  ├─ peripherals/            - Definiert alle Hardware-Schnittstellen, welche vom Program genutzt werden
  |    └─ tests/             - Definiert Tests, welche über das Webtool ausgeführt werden können
  ├─ rsc/                    - Enthält alle Ressourcen, wie
  |    ├─ config.json           - die Konfigdatei...
  |    ├─ webpage/              - das Webtool...
  |    └─ images/               - bilder für den Drucker...
  ├─ utils/
  ├─ webserver/              - REST-Api-Schnittstellen und außlieferung des Web-Config-Tools
  ├─ requirements-on-dev.txt - Python-Packages für die Entwicklungsumgebung
  ├─ requirements-on-pi.txt  - Python-Packages für den Pi selber
  └─ main.py                 - Einstiegspunkt der Software

```

## Hosting des Web-Config-Tools

Auch wenn das Web-Config-Tool selber unabhängig von der Haupt-Software ist, wird trotzdem immer ein Build von diesem mit der Hauptsoftware ausgeliefert um schnellen Zugriff auf die Konfiguration von außerhalb zu erhalten.

Dieser Build liegt unter rsc/webpage/Weltzerstoerungsknopf-Configinterface/, wobei Weltzerstoerungsknopf-Configinterface als Git-Sub-Module eingebunden ist.

Hierfür enthält das Weltzerstoerungsknopf-Configinterface-Repository einen extra Branch, welcher außschließlich einen Build der aktuellen Version des Webtools enthält.

Um diesen Ordner zu initialisieren, bitte folgende Befehle ausführen:

```bash
git submodule init
git submodule update
```
