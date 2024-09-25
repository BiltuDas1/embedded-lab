# CH340 Stable Driver (v3.5.2019.1)

### Why this exists

Newer CH340 drivers pushed by Windows Update are broken for many ESP8266 and Arduino clones. They cause a "PermissionError(13)" or "device not functioning" error in the Arduino IDE and esptool. This 2019 version is the last one that actually works reliably.

### How to install

1. Run `SETUP.EXE` and click Install.
2. Open Device Manager and find your board under Ports (COM & LPT).
3. Right-click it, select Update driver, then Browse my computer for drivers.
4. Click "Let me pick from a list" and select the 2019 version.
5. If Windows updates it again later, just repeat step 4.

### Credits

This driver belongs to [WCH](https://www.google.com/search?q=wch-ic.com). It is kept here for backup and version control.
