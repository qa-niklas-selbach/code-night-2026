# 🌦️ Weather Illustration Generator

Dieses Programm erstellt automatisch ein **kunstvolles 3D-Miniatur-Bild einer Stadt** – passend zum aktuellen Wetter dort. Du gibst einfach einen Stadtnamen ein, und das Programm erledigt den Rest:

1. Es sucht die Stadt und ihre Koordinaten.
2. Es fragt das aktuelle Wetter ab (Temperatur, Wind, Wetterlage).
3. Es lässt eine KI (Google Gemini) ein isometrisches Miniatur-Stadtbild mit den bekanntesten Wahrzeichen der Stadt generieren, in dem das aktuelle Wetter dargestellt wird.
4. Das fertige Bild wird als PNG-Datei im Ordner `output/` gespeichert.

**Beispiel:** Gibst du „Paris" ein und es regnet dort gerade, bekommst du ein niedliches 3D-Miniatur-Paris mit Eiffelturm im Regen. ☔

---

## 📋 Voraussetzungen

Bevor du loslegst, brauchst du:

- **Python 3.9 oder neuer** – prüfe das mit `python --version` im Terminal
- **Einen Google Gemini API-Schlüssel** (kostenlos erhältlich) – siehe Schritt 3 unten
- Eine Internetverbindung (das Programm spricht mit zwei Online-Diensten)

---

## 🚀 Installation – Schritt für Schritt

### Schritt 1: Projekt herunterladen

Lege die Datei `weather.py` in einen Ordner deiner Wahl, z. B. `weather-illustrator/`.

### Schritt 2: Benötigte Pakete installieren

Öffne ein Terminal in diesem Ordner und führe aus:

```bash
pip install requests python-dotenv google-genai
```

Was diese Pakete tun:

| Paket | Zweck |
|---|---|
| `requests` | Daten aus dem Internet abrufen (Wetter & Koordinaten) |
| `python-dotenv` | Liest deinen API-Schlüssel aus einer `.env`-Datei |
| `google-genai` | Verbindung zur Google-Gemini-KI für die Bildgenerierung |


### Schritt 3: API-Schlüssel speichern

Erstelle im Projektordner eine Datei namens **`.env`** (genau so, mit Punkt am Anfang) mit folgendem Inhalt:

```
GEMINI_API_KEY=dein-api-schlüssel-hier
```

⚠️ **Wichtig:** Teile diese Datei niemals öffentlich (z. B. auf GitHub) – der Schlüssel ist wie ein Passwort!

---

## ▶️ Benutzung

Führe das Programm im Terminal aus und gib den Stadtnamen in Anführungszeichen an:

```bash
python weather.py "Berlin"
```

Auch Städte mit Leerzeichen funktionieren:

```bash
python weather.py "New York"
```

### Was du dann siehst

Das Programm gibt Schritt für Schritt Statusmeldungen aus:

```
Geocoding 'Berlin'...
  Found: Berlin, Germany
  Coordinates: 52.52437, 13.41053

Fetching weather...
  Condition: partly cloudy
  Temperature: 18.3°C
  Wind Speed: 12.5 km/h

Generated prompt:
  Present a clear, 45° top-down view of ...

Generating isometric weather illustration...
  Saved to: /pfad/zum/projekt/output/weather_illustration_20260611_143052.png
```

Das fertige Bild findest du im Unterordner **`output/`**. Der Ordner wird automatisch erstellt, falls er noch nicht existiert. Jedes Bild bekommt einen Zeitstempel im Dateinamen, sodass nichts überschrieben wird.

---

## ⚙️ Wie funktioniert das Programm intern?

Das Skript besteht aus fünf Funktionen, die nacheinander ablaufen:

1. **`geocode_city(city_name)`** – Wandelt den Stadtnamen in Koordinaten (Breiten-/Längengrad) um. Nutzt dafür die kostenlose [Open-Meteo Geocoding API](https://open-meteo.com/) – kein API-Schlüssel nötig.

2. **`get_weather(latitude, longitude)`** – Holt das aktuelle Wetter für diese Koordinaten von der Open-Meteo Forecast API: Temperatur, Windgeschwindigkeit und einen Wettercode, der über die Tabelle `WEATHER_CODES` in Klartext übersetzt wird (z. B. Code 61 = „slight rain").

3. **`build_prompt(city, country, weather)`** – Baut aus Stadt, Land und Wetterlage eine detaillierte englische Beschreibung („Prompt") für die KI zusammen. Der Prompt beschreibt den gewünschten Stil: isometrische 45°-Ansicht, Miniatur-3D-Cartoon-Look, Wahrzeichen der Stadt, ein Wetter-Icon oben mittig – und ausdrücklich **kein Text** im Bild.

4. **`generate_image(prompt, output_dir)`** – Schickt den Prompt an das Gemini-Modell `gemini-3.1-flash-image`, holt das generierte Bild aus der Antwort und speichert es als PNG-Datei.

5. **`main()`** – Die Steuerzentrale: liest den Stadtnamen aus der Kommandozeile und ruft die obigen Schritte nacheinander auf.

---

## ❗ Häufige Probleme & Lösungen

| Problem | Lösung |
|---|---|
| `GEMINI_API_KEY environment variable not set.` | Die `.env`-Datei fehlt, liegt im falschen Ordner oder der Schlüsselname ist falsch geschrieben. Sie muss im selben Ordner wie `weather.py` liegen. |
| `City 'XYZ' not found.` | Stadtname prüfen – versuche die englische Schreibweise (z. B. „Munich" statt „München" kann helfen, meist gehen aber beide). |
| `ModuleNotFoundError: No module named 'requests'` | Die Pakete aus Schritt 2 wurden nicht installiert. Führe den `pip install`-Befehl erneut aus. |
| `Usage: python weather.py "City Name"` | Du hast keinen Stadtnamen angegeben. Hänge ihn als Argument an. |
| Fehler bei der Bildgenerierung | Prüfe, ob dein API-Schlüssel gültig ist und dein Google-Konto Zugriff auf die Bildgenerierung hat. Auch ein kurzzeitiges Limit der API kann die Ursache sein – einfach erneut versuchen. |

---

## 🌐 Verwendete Dienste

- **[Open-Meteo](https://open-meteo.com/)** – kostenlose Wetter- und Geocoding-API, kein Schlüssel erforderlich
- **[Google Gemini](https://aistudio.google.com/)** – KI-Bildgenerierung, API-Schlüssel erforderlich

Viel Spaß beim Generieren! 🎨
