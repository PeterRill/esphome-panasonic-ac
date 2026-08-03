# Makerfabs ESP32-S3 Parallel TFT 4.3 V1.3: ESPHome-Test

Die Testkonfiguration `config/makerfabs-tft-v13-test.yaml` prueft:

- das 800 x 480 RGB565-Display,
- die Hintergrundbeleuchtung auf GPIO2,
- den GT911-Touchcontroller auf GPIO17/GPIO18,
- die Touch-Ausrichtung und Koordinaten,
- eine minimale LVGL-Oberflaeche.

Die Pinbelegung und Timings stammen aus den Arduino-GFX-Beispielen des
Makerfabs-Branches V1.3. Die Konfiguration ist fuer ESPHome 2026.7.3 erstellt.

## Lokale Umgebung

Die vorhandene virtuelle Umgebung dieses Repositories kann direkt verwendet
werden. Fuer ein separates Projekt kann dieselbe Struktur angelegt werden:

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install "esphome==2026.7.3"
```

Konfiguration pruefen und Firmware bauen:

```powershell
python -m esphome config .\config\makerfabs-tft-v13-test.yaml
python -m esphome compile .\config\makerfabs-tft-v13-test.yaml
```

## Erstes Flashen und Logausgabe

Zum ersten Flashen den mit dem CP2104 verbundenen USB-C-Anschluss des Boards
verwenden (auf dem Board als USB-TTL bezeichnet). Den COM-Port bei Bedarf im
Geraetemanager nachsehen:

```powershell
python -m esphome run .\config\makerfabs-tft-v13-test.yaml --device COM5
```

`COM5` durch den tatsaechlichen Port ersetzen. Falls das Flashen nicht startet,
BOOT gedrueckt halten, RESET kurz druecken, RESET loslassen und danach BOOT
loslassen.

Nach dem Start sollte eine dunkle LVGL-Testseite mit einem blauen Touch-Button
erscheinen. Beim Druecken wird der Button gruen; ausserdem erscheinen die
Touchkoordinaten unten im Display und im seriellen Log.

## Auswertung

- Falsche Farben: als ersten Versuch `color_order: BGR` setzen.
- Spiegelverkehrter Touch: `mirror_x` beziehungsweise `mirror_y` einzeln
  deaktivieren.
- Vertauschte Achsen: `swap_xy: true` setzen und danach die Spiegelung erneut
  pruefen.
- Touchcontroller fehlt im I2C-Scan: Reset-Pin GPIO38, Boardrevision und
  I2C-Adresse kontrollieren. GT911 verwendet normalerweise `0x5D`, kann je nach
  Reset-/Interrupt-Beschaltung aber auch `0x14` nutzen.
- Beleuchtung an, aber kein Bild: RGB-Pins, Pixeltakt und Porches anhand des
  seriellen Logs und der exakten Boardrevision kontrollieren.

Die Testkonfiguration enthaelt absichtlich weder WLAN noch Home-Assistant-API
oder OTA. Sobald Display und Touch funktionieren, koennen diese Komponenten
ergaenzt werden.
