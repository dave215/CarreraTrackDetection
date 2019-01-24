# Bibliotheken importieren
import cv2 as cv    # OpenCV
import numpy as np  # NumPy

import sys
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QFileDialog, QLineEdit
from PyQt5.QtGui import QPixmap
from Modellbahnerkennung import *
from GrobeMaske import *
from GenaueMaske import *


#############################
# GLOBALE VARIABLEN         #
#############################

Fehler1 = "Falsches Dateiformat"
Fehler2 = "Wähle Bild aus"
Fehler3 = "Kein Bild benötigt!"


#############################
# FUNKTIONEN                #
#############################


# Funktion glaettet die Kanten im Bild (uebergebener Array mit Koordinaten), indem zwischen
# zwei Punkten mit einstellbarem Abstand eine Linie gezeichnet (interpoliert) wird.
# Zurueckgegeben wird der neue "geglaettete" Array mit neuen Kantenpunkten
def kanten_glaetten(kanten_array, pixel_count, farbe, step_size=50):
    # Startpunkt aus Array holen
    start_x = kanten_array[0, 0]
    start_y = kanten_array[0, 1]

    # Alte Kante schwarz uebermalen
    for a in range(0, pixel_count, 1):
        x = kanten_array[a, 0]
        y = kanten_array[a, 1]
        img_strecke[y - 5:y + 5, x - 5:x + 5] = (0, 0, 0)

    cv.line(img_strecke, (kanten_array[0, 0], kanten_array[0, 1]),
            (kanten_array[pixel_count - step_size, 0], kanten_array[pixel_count - step_size, 1]), (0, 0, 0), 10)

    # In einer Schleife die Kantenpunkte mit bestimmter Schrittweite ablaufen
    for a in range(step_size, pixel_count - step_size, step_size):
        diff_step_x = (kanten_array[a, 0] - start_x) / step_size
        diff_step_y = (kanten_array[a, 1] - start_y) / step_size

        # Zwischen den Kantenpunkten interpolieren (Linie glaetten) und diese Linie zeichnen
        for b in range(a - step_size, a - 1):
            kanten_array[b, 0] = start_x + (b - a + step_size) * diff_step_x  # Neuen Kantenpunkt (X) berechnen
            kanten_array[b, 1] = start_y + (b - a + step_size) * diff_step_y  # Neuen Kantenpunkt (Y) berechnen

        cv.line(img_strecke, (start_x, start_y), (kanten_array[a, 0], kanten_array[a, 1]), farbe)
        # Startpunkt fuer naechsten Schleifendurchlauf speichern
        start_x = kanten_array[a, 0]
        start_y = kanten_array[a, 1]

    # Linie von Startpunkt zum letzten Punkt der Kantenglaettung zeichen --> Umrundung schliessen
    cv.line(img_strecke, (kanten_array[0, 0], kanten_array[0, 1]), (kanten_array[a, 0], kanten_array[a, 1]), farbe)

    return kanten_array  # Neuen Array mit Kantenpunkten zurueckgeben


# Startpunkt auf Rand der Maske finden
def rand_finden(rand_x, rand_y, step_x, step_y):
    # Solange die Maske noch weiss ist (--> Man ist auf der Strecke), gehe eine Schrittweite weiter in Richtung Rand
    # Wenn der Rand der Strecke erreicht ist (--> Maske ist nun schwarz und man ist ausserhalb der Strecke),
    # dann breche die Schleife ab
    while mask[rand_y, rand_x] != 0:
        img_debug[rand_y, rand_x] = (0, 255, 0)  # Laufstrecke markieren (auf Debug Bild)
        rand_x += step_x  # aendere die x-Position um die x-Schrittweite
        rand_y += step_y  # aendere die y-Position um die y-Schrittweite

    # Letzten Schritt rueckgaengig machen, um wieder innerhalb der Maske und damit auf der Strecke zu sein
    rand_x -= step_x
    rand_y -= step_y

    # Ueberpruefen, ob in der Naehe (+-1 Pixel) schon eine Kante markiert worden ist
    if (img_strecke[rand_y - 1:rand_y + 1, rand_x - 1:rand_x + 1] != (0, 0, 0)).any():
        # Wenn ja, dann ist diese Kante schon markiert und braucht nicht nochmal "gefunden" werden
        # Daher wird (0, 0) zurueckgegeben, die aufrufende Instanz weiss nun auch, dass diese Kante schon gefunden wurde
        return 0, 0

    # Markiere Randpunkt im Debug Streckenbild
    cv.circle(img_debug, (rand_x, rand_y), 20, (0, 255, 0), 3)

    # Gebe die Position des Randpunktes zurueck
    return rand_x, rand_y


# Gesamten Rand der Maske ablaufen
def rand_ablaufen(kante_x, kante_y, farbe):
    # Uebergebenenen Startpunkt speichern, damit spaeter wieder darauf zugegriffen werden kann
    rand_x = kante_x
    rand_y = kante_y

    # Punkte rund um Testpunkt anschauen, erster Punkt doppelt, damit alle Pixeluebergaenge betrachtet werden koennen
    test_list_x = (-1, 0, 1, 1, 1, 0, -1, -1, -1)
    test_list_y = (-1, -1, -1, 0, 1, 1, 1, 0, -1)

    # Zaehlvariable definieren und nullsetzen
    pixel_count = 0
    kanten_array = np.zeros((10000, 2), dtype=np.int16)
    kanten_array[0, 0] = kante_x
    kanten_array[0, 1] = kante_y

    # Stoppen, falls "verlaufen"
    while pixel_count < 9999:
        pixel_count += 1  # Zaehlvariable um eins erhoehen

        # Zuerst nach Farbe links oben schauen und zwischenspeichern
        last_color = mask[kante_y + test_list_y[0], kante_x + test_list_x[0]]

        # In Schleife alle 9 moeglichen Kanten ueberpruefen
        for index in range(1, 9):
            # Punkte rund um aktuellen Randpunkt anschauen und Farbdifferenz betrachten
            new_x = kante_x + test_list_x[index]  # Koordinaten des zu ueberpruefendnen x-Punktes zwischenspeichern
            new_y = kante_y + test_list_y[index]  # Koordinaten des zu ueberpruefendnen y-Punktes zwischenspeichern
            diff = abs(int(last_color) - int(mask[new_y, new_x]))  # Farbwertdifferenz (Betrag) speichern

            # Wenn Differenz groesser als 100 (also neuer Punkt im anderen Bereich) und Kante dort noch nicht gefunden
            if (img_strecke[kante_y + test_list_y[index - 1], kante_x + test_list_x[index - 1]] == (0, 0, 0)).all() \
                    and (img_strecke[new_y, new_x] == (0, 0, 0)).all() and diff > 100:
                # Wenn Bild nicht schwarz, also in Strecke: vorherigen Punkt nehmen (der in Strecke war),
                # der zuletzt getestet wurde, als neuen Kantenpunkt festlegen
                if last_color != 0:
                    kante_x += test_list_x[index - 1]
                    kante_y += test_list_y[index - 1]
                # Wenn Bild schwarz (also nicht in Strecke): diesen Punkt als neuen Punkt nehmen
                else:
                    kante_x += test_list_x[index]
                    kante_y += test_list_y[index]
                break  # For-Schleife abbrechen, da Kante gefunden

            # Aktuellen Punkt als vorherigen Farbtestpunkt setzen
            last_color = mask[new_y, new_x]

        # Plausibilitaetspruefung: Neuer Punkt muss auf der Strecke liegen
        # Sonst breche die Schleife ab und melde einen Error
        if mask[kante_y, kante_x] == 0:
            print('Error')
            break

        # Ueberpruefen, ob der Startpunkt erreicht wurde
        # Wenn ja, dann beende die Schleife (Beende die Kantenerkennung)
        if kante_x == rand_x and kante_y == rand_y:
            break

        # Gefundenen Punkt der Kante mit der uebergebenen Farbe einfaerben
        img_strecke[kante_y, kante_x] = farbe
        img_debug[kante_y, kante_x] = farbe

        # Punkt in Array abspeichern
        kanten_array[pixel_count, 0] = kante_x
        kanten_array[pixel_count, 1] = kante_y

    # Array auf benoetigte Laenge kuerzen
    kanten_array = kanten_array[0:pixel_count, :]

    # Laenge der Kante (Anzahl der Pixel) zurueckgeben
    return pixel_count, kanten_array


# Funktion zum Erstellen der Maske mit unterschiedlichen Grenzen
def maske_erstellen(orig_img, untere_grenze=0, obere_grenze=80, area_x=14, area_y=14):
    # Definiere Farb-Ranges
    lower_color = (untere_grenze, untere_grenze, untere_grenze)
    upper_color = (obere_grenze, obere_grenze, obere_grenze)

    # Filtere Bild nach Farbgrenzen
    mask_img = cv.inRange(orig_img, lower_color, upper_color)
    # Kopie der Maske erstellen
    mask2 = mask_img.copy()

    # Kleine Bereiche aus der Maske entfernen
    # Schwellwerte in der Maske ueberpruefen
    for x in range(0, x_max - area_x + 1, area_x):  # X-Werte durchgehen
        for y in range(0, y_max - area_y + 1, area_y):  # Y-Werte durchgehen
            # Area of Interest aus kopierter Maske herauskopieren
            copy = (mask2[y:y + area_y, x:x + area_x])
            if copy.sum() <= area_x / 2 * 250:  # Anzahl der Pixel auf Schwellwert ueberpruefen
                # Wenn zu wenig Pixel in diesem Bereich Weiss sind, dann wird der Bereich in der Maske
                # auf Null (Schwarz) gesetzt
                mask_img[y:y + area_y, x:x + area_x] = 0
            else:  # Sonst wird der Bereich auf Weiss gesetzt
                mask_img[y:y + area_y, x:x + area_x] = 255

    # Maske optimieren
    for x in range(0, x_max - area_x + 1, area_x):  # X-Werte durchgehen
        for y in range(0, y_max - area_y + 1, area_y):  # Y-Werte durchgehen
            temp = mask_img[y, x]
            if (x == 0 and y == 0) or (x == 0 and y >= y_max - area_y + 1) or \
                    (x >= x_max - area_x + 1 and y == 0) or \
                    (x >= x_max - area_x + 1 and y >= y_max - area_y + 1):
                continue
            elif (x == 0) and mask_img[y - area_y + 1, x] != temp and mask_img[y + area_y + 1, x] != temp and \
                    mask_img[y, x + area_x + 1] != temp:
                mask_img[y:y + area_y, x:x + area_x] = mask_img[y - area_y + 1, x]
            elif (x >= x_max - area_x + 1) and mask_img[y - area_y + 1, x] != temp and \
                    mask_img[y + area_y + 1, x] != temp and mask_img[y, x - area_x + 1] != temp:
                mask_img[y:y + area_y, x:x + area_x] = mask_img[y - area_y + 1, x]
            elif (y == 0) and mask_img[y + area_y + 1, x] != temp and mask_img[y, x - area_x + 1] != temp and \
                    mask_img[y, x + area_x + 1] != temp:
                mask_img[y:y + area_y, x:x + area_x] = mask_img[y + area_y + 1, x]
            elif y >= y_max - area_y + 1 and mask_img[y - area_y + 1, x] != temp and \
                    mask_img[y, x - area_x + 1] != temp and mask_img[y, x + area_x + 1] != temp:
                mask_img[y:y + area_y, x:x + area_x] = mask_img[y - area_y + 1, x]
            else:
                if mask_img[y - area_y + 1, x] != temp and mask_img[y + area_y + 1, x] != temp and \
                        mask_img[y, x - area_x + 1] != temp and mask_img[y, x + area_x + 1] != temp:
                    mask_img[y:y + area_y, x:x + area_x] = mask_img[y - area_y + 1, x]

    return mask_img  # Maske zurueckgeben


# Bild fuer Streckenerkennung einlesen
def selectInputFile():
    # falls Kamera ausgewaehlt, Fehler anzeigen
    if ui.comboBox.currentText() == "Kamera":
        ui.lineEdit.setText(Fehler3)
        ui.label.clear()
    # Pfad auswaehlen
    else:
        global img_path
        img_path, _ = QFileDialog.getOpenFileName()  # Explorer oeffnen und Pfad waehlen
        laengeImg = len(img_path)
        ending = img_path[laengeImg-4:laengeImg]
        # Dateiformat (Ende des Pfads) auf Bild ueberpruefen
        if ending == ".jpg" or ending == ".png" or ending == ".PNG" or ending == "jpeg" or ending == ".JPG":
            ui.lineEdit.setText(img_path) # Pfad setzen
            ui.label.setPixmap(QtGui.QPixmap(img_path))  # Bild anzeigen
        # Falsches Dateiformat, Fehler ausgeben
        else:
            ui.lineEdit.setText(Fehler1)


# Dateipfad fuer Bild der Strecke festlegen
def selectOutputFile():
    global img_strecke_path
    img_strecke_path, _ = QFileDialog.getSaveFileName()  # Explorer oeffnen und Pfad waehlen
    laengeImg = len(img_strecke_path)
    ending = img_strecke_path[laengeImg - 4:laengeImg]
    # Dateiformat (Ende des Pfads) auf Bild ueberpruefen
    if ending == ".jpg" or ending == ".png" or ending == ".PNG" or ending == "jpeg" or ending == ".JPG":
        ui.lineEdit_2.setText(img_strecke_path)  # Pfad setzen
    # Falsches Dateiformat, Fehler ausgeben
    else:
        ui.lineEdit_2.setText(Fehler1)


# Pruefen, dass alle benötigten Parameter vorhanden sind
def test_if_parameters_fit():
    # Bild ueber Kamera einlesen
    if ui.comboBox.currentText() == "Kamera":
        # Pfad zu Speicher vorhanden
        if (ui.lineEdit_2.text() != "" and ui.lineEdit_2.text() != Fehler1 and ui.lineEdit_2.text() != Fehler2):
            # TODO: Kamerabild aufnehmen
            # Streckenerkennung()  # Streckenerkennung starten
            ui.lineEdit.setText("Funktion noch in Entwicklung, bitte Bild auswählen")
        else:
            ui.lineEdit_2.setText(Fehler2)  # Fehler ausgeben, dass Datei fehlt
    # Bild über Dateipfad einlesen
    else:
        # Pfad zu Datei und Speicher vorhanden
        if ((ui.lineEdit_2.text() != "" and ui.lineEdit_2.text() != Fehler1 and ui.lineEdit_2.text() != Fehler2) and \
                (ui.lineEdit.text() != "" and ui.lineEdit.text() != Fehler1) and ui.lineEdit.text() != Fehler2):
            Streckenerkennung()  # Streckenerkennung starten
        else:  # Fehler ausgeben, dass Datei fehlt
            if ui.lineEdit.text() == "" or ui.lineEdit.text() == Fehler1:
                ui.lineEdit.setText(Fehler2)
            else:
                ui.lineEdit_2.setText(Fehler2)


# Wandelt Bild um, sodass es im Label anzeigbar wird
def bild_umwandeln(mask):
    img_debug = cv.cvtColor(mask, cv.COLOR_GRAY2BGR)  # Bild in BGR konvertieren
    height, width, channels = img_debug.shape
    bytesPerLine = channels * width
    # Format umformen, sodass es anzeigbar wird
    masktest = QtGui.QImage(img_debug.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
    tempPic1 = QtGui.QPixmap.fromImage(masktest)
    tempPic2 = QtGui.QPixmap(tempPic1)
    return tempPic2


# Fenster mit den genauen Masken anzeigen
def open_GenaueMaske(ersteMaske):
    # Neue obere Wertschelle (Dunkles Grau)
    untereGrenze = 10
    obereGrenze = 15
    # Fuer den Fall, dass 100 oder 120 als erster Wert ausgewaehlt wurde, die Grenzen anpassen
    if ersteMaske == 100 or ersteMaske == 120:
        untereGrenze = 15
        obereGrenze = 10

    global mask_genau
    mask_genau = []
    # Fuer alle angegebenen oberen Grenzwerte Masken zeichnen und ausgeben
    for upper_value in range(ersteMaske - untereGrenze, ersteMaske + obereGrenze + 5, 5):
        # Maske in Funktion erstellen
        temp = maske_erstellen(frame, lower_value, upper_value, area_x, area_y)
        mask_genau.append(temp)  # Erstelle Maske in Array speichern

    # GUI
    # Masken anzeigbar machen
    mask1 = bild_umwandeln(mask_genau[0])
    mask2 = bild_umwandeln(mask_genau[1])
    mask3 = bild_umwandeln(mask_genau[2])
    mask4 = bild_umwandeln(mask_genau[3])
    mask5 = bild_umwandeln(mask_genau[4])
    mask6 = bild_umwandeln(mask_genau[5])

    # Masken anzeigen
    ui2.label1.setPixmap(mask1)
    ui2.label2.setPixmap(mask2)
    ui2.label3.setPixmap(mask3)
    ui2.label4.setPixmap(mask4)
    ui2.label5.setPixmap(mask5)
    ui2.label6.setPixmap(mask6)

    # Fenster mit genauen Masken anzeigen
    Dialog2.show()


# Alle offenen Dialoge schliessen und beste Maske speichern
def close_diaglogs(zweiteMaske):
    global mask
    mask = mask_genau[zweiteMaske]  # Beste Maske speichern

    # Fesnter schließen
    Dialog2.close()
    Dialog1.close()

    # Starte den zweiten Teil der Streckenerkennung
    Streckenerkennung2()


# Streckenerkennung Teil 1
def Streckenerkennung():
    # 1. Bild lesen und bearbeiten

    # Lese Bild von Festplatte ueber gewaehlten Pfad
    global img
    img = cv.imread(img_path)

    # Erstelle eine Kopie vom Bild
    global frame
    frame = img.copy()

    # Bild auf bestimmte Groesse skalieren (verkleinern)
    global scale
    scale = 0.5
    frame = cv.resize(frame, (0, 0), fx=scale, fy=scale)

    # Bild in den HSV-Farbraum konvertieren
    frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    # Bild aufhellen / verdunkeln
    frame[:, :, 2] = frame[:, :, 2] - 4
    # Bild von HSV zurueck nach BGR konvertieren
    frame = cv.cvtColor(frame, cv.COLOR_HSV2BGR)

    # Ermittle Bildgroesse
    global y_max
    global x_max
    y_max = len(frame[:, 0])  # Hoehe des Bilds
    x_max = len(frame[0, :])  # Breite des Bilds

    # Ueberpruefen, ob das Bild im Hochformat ist. Wenn ja, das Bild auf Querformat drehen
    if x_max < y_max:
        frame = cv.rotate(frame, cv.ROTATE_90_COUNTERCLOCKWISE)  # Bild um 90° drehen
        # Bildgroessen an Rotation anpassen
        temp = x_max
        x_max = y_max
        y_max = temp


    # 2. Masken erstellen und auswaehlen

    # Definiere Farb-Ranges
    global lower_value
    lower_value = 0  # Untere Wertschwelle fuer Streckenerkennung (Ganz Schwarz)

    # Groesse des Durchsuch-Bereichs festlegen. Hier: 26x26
    global area_x
    global area_y
    area_x = 14
    area_y = 14

    mask_array = []
    # Fuer alle angegebenen oberen Grenzwerte Masken zeichnen und ausgeben
    for upper_value in range(60, 140, 20):
        # Maske in Funktion erstellen
        temp = maske_erstellen(frame, lower_value, upper_value, area_x, area_y)
        mask_array.append(temp)

    # GUI
    # Masken anzeigbar machen
    mask60 = bild_umwandeln(mask_array[0])
    mask80 = bild_umwandeln(mask_array[1])
    mask100 = bild_umwandeln(mask_array[2])
    mask120 = bild_umwandeln(mask_array[3])

    # Masken anzeigen
    ui1.label60.setPixmap(mask60)
    ui1.label80.setPixmap(mask80)
    ui1.label100.setPixmap(mask100)
    ui1.label120.setPixmap(mask120)

    # Fenster mit Masken (grobe Schwellwerte) anzeigen
    Dialog1.show()


# Streckenerkennung Teil 2
def Streckenerkennung2():
    # 3. Punkt der Strecke in Maske suchen
    
    # Kopie der neuen, bearbeiteten Maske erstellen und zu Farbbild konvertieren
    global img_debug
    img_debug = mask.copy()
    img_debug = cv.cvtColor(img_debug, cv.COLOR_GRAY2BGR)
    
    # Grob auf 20 Punkten auf der Diagonale nach Strecke schauen
    testpoints = 20
    x_step = int(x_max / testpoints)
    y_step = int(y_max / testpoints)

    # Startpunkt setzen
    start_x = int(x_max / 2)
    start_y = int(y_max / 2)
    punkt_x = start_x
    punkt_y = start_y

    # Nach Strecke auf Maske suchen
    while (mask[punkt_y, punkt_x] == 0) and (punkt_x <= x_max - x_step):
        punkt_x += x_step
        punkt_y += y_step

    # Wenn Strecke nicht gefunden, also der Punkt der Maske schwarz: fuenffach geringere Schrittweite nehmen:
    # maximal 100 mal testen oder wenn Schrittweite bei einem 1 ist
    # (also jedes Pixel in einer Richtung quer durchs Bild getestet wird)
    # Andere Moeglichkeiten: doppelte so viele Punkte testen (x_step = int(x_step / 2) oder
    # testpoints = 5*testpoints und x_step = int(y_max / testpoints)),
    # fuenf Punkte mehr testen (testpoints = testpoints + 5 und x_step = int(y_max / testpoints))
    count = 0
    while (mask[punkt_y, punkt_x] == 0) and (count < 100 or x_step == 1 or y_step == 1):
        x_step = int(x_step / 5)
        y_step = int(y_step / 5)
        punkt_x = start_x
        punkt_y = start_y
        count += 1
        while (mask[punkt_y, punkt_x] == 0) and (punkt_x <= x_max - x_step) and (punkt_y >= 0):
            punkt_x += x_step
            punkt_y -= y_step

    # Gefundener Startpunkt ausgeben
    # print('Startpunkt: (', punkt_x, '|', punkt_y, ')')

    # Markiere Punkt im Debugbild
    cv.circle(img_debug, (punkt_x, punkt_y), 20, (0, 255, 0), 3)


    # 4. Streckenraender suchen und Kanten ablaufen
    # 4.1 Rand finden
    # 4.2 Kante ablaufen

    # Neues leeres (schwarzes) Bild erstellen
    global img_strecke
    img_strecke = np.zeros((y_max, x_max, 3), np.uint8)

    # Von dem gefundenen Startpunkt auf der Strecke in verschiedenen Richtungen (insgesamt 8 Richtungen) den Rand der
    # Maske suchen und von dort die Kanten ablaufen

    # Richtungsvektoren als Liste definieren
    step_list_x = (1, 1, 0, -1, -1, -1, 0, 1)
    step_list_y = (0, 1, 1, 1, 0, -1, -1, -1)

    # Arrays fuer die gefundenen Daten erstellen
    raender_x = np.zeros(8, dtype=np.int16)  # x-Koordianten der Randpunkte
    raender_y = np.zeros(8, dtype=np.int16)  # y-Koordianten der Randpunkte
    counts = np.zeros(8, dtype=np.int16)  # Laenge der einzelnen Kanten

    # Farbe fuer Kanten definieren
    test_farbe = (255, 255, 255)

    # Alle 8 Richtungen durchtesten
    for i in range(0, 8, 1):
        # Gehe von dem Startpunkt zum Rand der Maske, nutze den vorgegebene Richtungsvektor und
        # speichere die gefundenen Randpunkte im Array ab
        (raender_x[i], raender_y[i]) = rand_finden(punkt_x, punkt_y, step_list_x[i], step_list_y[i])

        # Wenn ein "neuer" Rand gefunden worden ist, dann laufe die Kante ab
        if not(raender_x[i] == 0 and raender_y[i] == 0):
            # Kante ablaufen und mit bestimmter Farbe markieren
            counts[i], _ = rand_ablaufen(raender_x[i], raender_y[i], test_farbe)

    # Unterschiedliche Kantenlaengen anzeigen
    # print('Kantenlaengen:', counts)


    # 5. Innen- und Aussenkante aus allen Kanten finden, farbig markieren und Daten speichern

    # Aussen (Laengste Kante) und Innen (Zweitlaengste Kante) der Strecke herausfinden
    sorted_array = sorted(counts, reverse=True)  # Array nach Groesse abfallend sortieren
    # Die erste Position ist die laengste Kante --> Das ist die aeussere Kante
    # Die zweite Positon ist die zweitlaengste Kante --> Die innere Kante
    # Die anderen Postionen sind kleiner und deswegen nicht relevant

    # Aeussere Kante im originalen Array suchen und Indexposition speichern
    pos_aussen = 0
    while sorted_array[0] != counts[pos_aussen]:
        pos_aussen += 1

    # Innere Kante im originalen Array suchen und Indexposition speichern
    pos_innen = 0
    while sorted_array[1] != counts[pos_innen]:
        pos_innen += 1

    # Bild wieder komplett schwarz machen
    img_strecke[:, :, :] = 0

    # Aussenkante Rot markieren und Daten umspeichern
    rand_aussen_x = raender_x[pos_aussen]
    rand_aussen_y = raender_y[pos_aussen]
    count_aussen, kante_aussen = rand_ablaufen(rand_aussen_x, rand_aussen_y, (0, 0, 255))

    # Innenkante Blau markieren und Daten umspeichern
    rand_innen_x = raender_x[pos_innen]
    rand_innen_y = raender_y[pos_innen]
    count_innen, kante_innen = rand_ablaufen(rand_innen_x, rand_innen_y, (255, 0, 0))

    # Kantenlaengen anzeigen
    # print('Laenge Aussenkante:', count_aussen)
    # print('Laenge Innenkante:', count_innen)


    # 6. Kanten glaetten

    # Innenkante glaetten
    kante_innen = kanten_glaetten(kante_innen, count_innen, (255, 0, 0))
    kante_innen = kanten_glaetten(kante_innen, count_innen, (255, 0, 0), 100)

    # Aussenkante glaetten
    kante_aussen = kanten_glaetten(kante_aussen, count_aussen, (0, 0, 255))
    kante_aussen = kanten_glaetten(kante_aussen, count_aussen, (0, 0, 255), 100)


    # 7. Richtung zwischen Innen- und Aussenkante herausfinden

    stp = 50  # Schrittweite

    # Richtung fuer kuerzeste Distanz herausfinden
    punkt_a_x = kante_innen[0, 0]
    punkt_a_y = kante_innen[0, 1]

    # Bestimme Anzahl an Pixeln Rand ablaufen
    punkt_b_x = kante_innen[2 * stp, 0]
    punkt_b_y = kante_innen[2 * stp, 1]

    # Berechne Vektor zwischen den beiden Punkten
    diff_x = punkt_a_x - punkt_b_x
    diff_y = punkt_a_y - punkt_b_y

    laenge = np.sqrt(diff_x * diff_x + diff_y * diff_y)

    abstaende = []  # Leere Liste mit den Laengen anlegen

    # Test der Richtungen -1 und 1
    for richtung in range(-1, 3, 2):
        # Orthogonalen Einheitsvektor berechnen (jeweils in eine andere Richtung)
        vektor_x = richtung / laenge * diff_y
        vektor_y = -richtung / laenge * diff_x

        # Abstand zur aeusseren Kante berechnen
        abstand = 1  # Abstand auf 1 Pixel setzen
        test_x = punkt_a_x  # Testpunkt auf startpunkt setzen
        test_y = punkt_a_y
        while (img_strecke[test_y - 1:test_y + 1, test_x - 1: test_x + 1, 2] == 0).all():
            test_x = int(punkt_a_x + abstand * vektor_x)  # Neuen Testpunkt (X) berechnen
            test_y = int(punkt_a_y + abstand * vektor_y)  # Neuen Testpunkt (Y) berechnen
            abstand += 1  # Ein Pixel zum Abstand hochzaehlen

        abstaende.append(abstand)  # Abstand dem Array hinzufuegen

    # Kuerzester Abstand herausfinden
    if abstaende[0] > abstaende[1]:
        richtung = -1
    else:
        richtung = 1


    # 8. Abstaende zwischen Innen- und Aussenkante auf gesamter Strecke herausfinden und speichern

    # Array fuer Abstaende anlegen
    abstaende = np.zeros(int((count_innen - stp) / stp + 2), dtype=np.int16)

    # Gesamte Strecke ablaufen
    for i in range(stp, count_innen, stp): # - stp, stp):
        # Randpunkt innen auswaehlen
        punkt_a_x = kante_innen[i - stp, 0]
        punkt_a_y = kante_innen[i - stp, 1]

        if i < count_innen - stp:
            # Bestimme Anzahl an Pixeln Rand ablaufen
            punkt_b_x = kante_innen[i + stp, 0]
            punkt_b_y = kante_innen[i + stp, 1]
        else:
            punkt_b_x = kante_innen[i, 0]
            punkt_b_y = kante_innen[i, 1]

        # Berechne Vektor zwischen den beiden Punkten
        diff_x = punkt_a_x - punkt_b_x
        diff_y = punkt_a_y - punkt_b_y

        # Laenge des Vektors berechnen
        laenge = np.double(np.sqrt(diff_x * diff_x + diff_y * diff_y))

        # Orthogonalen Einheitsvektor berechnen (mit vorher berechneter Richtung)
        vektor_x = -richtung / laenge * diff_y
        vektor_y = richtung / laenge * diff_x

        # Laenge zum Aussenrand berechnen (in richtige Richtung)
        abstand = 1  # Abstand auf 1 Pixel setzen
        test_x = punkt_a_x  # Testpunkt auf startpunkt setzen
        test_y = punkt_a_y
        while (img_strecke[test_y - 1:test_y + 1, test_x - 1: test_x + 1, 2] == 0).all():
            test2_x = test_x
            test2_y = test_y
            test_x = int(kante_innen[i, 0] + abstand * vektor_x)  # Neuen Testpunkt (X) berechnen
            test_y = int(kante_innen[i, 1] + abstand * vektor_y)  # Neuen Testpunkt (Y) berechnen
            # Punkt auf Bild gruen markieren
            if (test2_x != test_x) or (test2_y != test_y):
                if (abs(test_x) < x_max) and (abs(test_y) < y_max):
                    if img_strecke[test_y, test_x, 1] == 0:
                        img_strecke[test_y, test_x, 1] = 255
                    else:
                        abstand = -1
                        break
                else:
                    break
            abstand += 1  # Ein Pixel zum Abstand hochzaehlen

        abstaende[int(i / stp)] = abstand  # Abstand in Array speichern
        a = int(i / stp)

    i = 0
    while i <= a:
        if abstaende[i] == -1:
            abstaende = np.delete(abstaende, i)
            a -= 1
            i -= 1
        i += 1

    # Alle Laengen ausgeben
    # print('Streckenbreiten: ', abstaende)


    # 9. Bilder anzeigen und speichern

    # Zeige Bilder an
    # Zeige das Bild mit dem selbstgezeichneten Streckenverlauf an
    # cv.namedWindow('Strecke', cv.WINDOW_NORMAL)
    # cv.imshow('Strecke', img_strecke)
    # cv.resizeWindow('Strecke', x_max, y_max)
    # Warte auf Tastendruck (sonst sieht man die cv Fenster nicht)
    # key = cv.waitKey(0)
    # Schliesse alle cv Fenster
    # cv.destroyAllWindows()

    # Debugbild speichern
    # cv.imwrite("C:/Users/samir/Desktop/test2.jpg", img_debug)

    # Strecke in festgelegtem Bild speichern und im Hauptfenster anzeigen
    cv.imwrite(img_strecke_path, img_strecke)
    ui.label.setPixmap(QtGui.QPixmap(img_strecke_path))


#############################
# CODE START                #
#############################

# GUI: Verbinden der Buttons mit Funktionen

# Start-Button druecken
ui.pushButton.clicked.connect(test_if_parameters_fit)

# Datei auswaehlen Button
ui.pushButton_2.clicked.connect(selectInputFile)

# Speicherdatei auswaehlen Button
ui.pushButton_3.clicked.connect(selectOutputFile)

# Buttons zum Auswaehlen der groben Maske
ui1.pushButton.clicked.connect(lambda: open_GenaueMaske(60))
ui1.pushButton_2.clicked.connect(lambda: open_GenaueMaske(80))
ui1.pushButton_3.clicked.connect(lambda: open_GenaueMaske(100))
ui1.pushButton_4.clicked.connect(lambda: open_GenaueMaske(120))

# Buttons zum Auswaehlen der genauen Maske
ui2.pushButton.clicked.connect(lambda: close_diaglogs(0))
ui2.pushButton_2.clicked.connect(lambda: close_diaglogs(1))
ui2.pushButton_3.clicked.connect(lambda: close_diaglogs(2))
ui2.pushButton_4.clicked.connect(lambda: close_diaglogs(3))
ui2.pushButton_5.clicked.connect(lambda: close_diaglogs(4))
ui2.pushButton_6.clicked.connect(lambda: close_diaglogs(5))

# GUI (Programm) ausfuehren
sys.exit(app.exec_())
