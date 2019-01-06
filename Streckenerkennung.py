# Bibliotheken importieren
import cv2 as cv    # OpenCV
import numpy as np  # NumPy


#############################
# FUNKTIONEN                #
#############################


# Funktion glaettet die Kanten im Bild (uebergebener Array mit Koordinaten), indem zwischen
# zwei Punkten mit einstellbarem Abstand eine Linie gezeichnet (interpoliert) wird.
# Zurueckgegeben wird der neue "geglaettete" Array mit neuen Kantenpunkten
def kanten_glaetten(kanten_array, pixel_count, farbe, step_size=19):
    # Startpunkt aus Array holen
    start_x = kanten_array[0, 0]
    start_y = kanten_array[0, 1]

    # In einer Schleife die Kantenpunkte mit bestimmter Schrittweite ablaufen
    for a in range(step_size, pixel_count - step_size, step_size):
        diff_step_x = (kanten_array[a, 0] - start_x) / step_size
        diff_step_y = (kanten_array[a, 1] - start_y) / step_size

        # Zwischen den Kantenpunkten interpolieren (Linie glaetten) und diese Linie zeichnen
        for b in range(a - step_size, a - 1):
            img_strecke[kanten_array[b, 1], kanten_array[b, 0]] = (0, 0, 0)  # Bisherigen Kantenpunkt schwarz machen
            kanten_array[b, 0] = start_x + (b - a + step_size) * diff_step_x  # Neuen Kantenpunkt (X) berechnen
            kanten_array[b, 1] = start_y + (b - a + step_size) * diff_step_y  # Neuen Kantenpunkt (Y) berechnen
            img_strecke[kanten_array[b, 1], kanten_array[b, 0]] = farbe  # Neuen Punkt in uebergebener Farbe zeichnen

        # Startpunkt fuer naechsten Schleifendurchlauf speichern
        start_x = kanten_array[a, 0]
        start_y = kanten_array[a, 1]

    return kanten_array  # Neuen Array mit Kantenpunkten zurueckgeben


# Rand der Maske finden
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


# Rand der Maske ablaufen
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
    while pixel_count < 10000:
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
            if diff > 100 and (img_strecke[new_y, new_x] == (0, 0, 0)).all() and \
                    (img_strecke[kante_y + test_list_y[index - 1], kante_x + test_list_x[index - 1]] == (0, 0, 0)).all():
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
            # print('Startpunkt erreicht, Laenge = ', pixel_count)
            break

        # Gefundenen Punkt der Kante rot einfaerben
        img_strecke[kante_y, kante_x] = farbe
        img_debug[kante_y, kante_x] = farbe

        # Punkt in Array abspeichern
        kanten_array[pixel_count, 0] = kante_x
        kanten_array[pixel_count, 1] = kante_y

    # Array auf benoetigte Laenge kuerzen
    kanten_array = kanten_array[0:pixel_count, :]

    # Laenge der Kante (Anzahl der Pixel) zurueckgeben
    return pixel_count, kanten_array


#############################
# CODE START                #
#############################

# 1. Bild lesen und bearbeiten

# Lese Bild von Festplatte
# img = cv.imread('D:/samir/Dokumente/Studium/DHBW/Semester_5/Studienarbeit/Quellcode/Images/Oval3_7.jpg')
img = cv.imread('C:/Users/David/Documents/Studium/_Semester 5/Studienarbeit/Streckenbilder/OvaleStrecken/Oval3_7.jpg')


# Erstelle eine Kopie vom Bild
frame = img.copy()

# Bild auf bestimmte Groesse skalieren (verkleinern)
scale = 0.3
frame = cv.resize(frame, (0, 0), fx=scale, fy=scale)


# Bild in den HSV-Farbraum konvertieren
frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
# Bild aufhellen / verdunkeln
frame[:, :, 2] = frame[:, :, 2] - 4
# Bild von HSV zurueck nach BGR konvertieren
frame = cv.cvtColor(frame, cv.COLOR_HSV2BGR)


# Ermittle Bildgroesse
y_max = len(frame[:, 0])  # Breite des Bilds
x_max = len(frame[0, :])  # Hoehe des Bilds


# 2. Maske erstellen und verbessern

# Definiere Farb-Ranges
lower_value = 0    # Untere Wertschwelle fuer Streckenerkennung (Ganz Schwarz)
upper_value = 110  # Obere Wertschelle (Dunkles Grau)
lower_color = (lower_value, lower_value, lower_value)
upper_color = (upper_value, upper_value, upper_value)

# Filtere Bild nach Farbgrenzen
mask = cv.inRange(frame, lower_color, upper_color)

# Kleine Bereiche aus der Maske entfernen
mask2 = mask.copy()  # Kopie der Maske erstellen
# Groesse des Durchsuch-Bereichs festlegen: Hier: 10x10
area_x = 10
area_y = 10
area2_x = int(area_x / 2)  # Hälfte des Bereichs bestimmen (fuer X und Y)
area2_y = int(area_y / 2)

# Schwellwerte in der Maske überprüfen
for x in range(area2_x, x_max - area2_x, area_x):  # X-Werte durchgehen
    for y in range(area2_y, y_max - area2_y, area_x):   # Y-Werte durchgehen
        # Area of Interest aus kopierter Maske herauskopieren
        copy = (mask2[y - area2_y:y + area2_y, x - area2_x:x + area2_x])
        summe = sum(sum(copy))  # Summe der weissen Pixel in dem Bereich berechnen
        if summe <= 5*250:  # Anzahl der Pixel auf Schwellwert ueberpruefen
            # Wenn zu wenig Pixel in diesem Bereich Weiss sind, dann wird der Bereich in der Maske
            # auf Null (Schwarz) gesetzt
            mask[y - area2_y:y + area2_y, x - area2_x:x + area2_x] = 0
        else:  # Sonst wird der Bereich auf Weiss gesetzt
            mask[y - area2_y:y + area2_y, x - area2_x:x + area2_x] = 255


# Kopie der neuen, bearbeiteten Maske erstellen und zu Farbbild konvertieren
img_debug = mask.copy()
img_debug = cv.cvtColor(img_debug, cv.COLOR_GRAY2BGR)


# X. Konturen suchen (unwichtig)

# # Finde Konturen in der Maske, die nur noch zeigt, wo die Strecke ist:
# _, contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
#
# # Suche die groesste Kontur heraus (diese ist hoechst wahrscheinlich die Strecke)
# # Nehme dazu die Flaeche der Kontur und ueberpruefe, ob die groesser als Null ist
# if len(contours) > 0:
#     strecke = max(contours, key=cv.contourArea)
#
#     # Zeichne ein Rechteck um die Strecke in das Bild ein:
#     x, y, w, h = cv.boundingRect(strecke)
#     cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), thickness=30)


# 3. Punkt der Strecke in Maske suchen

# Neues leeres (schwarzes) Bild erstellen
img_strecke = np.zeros((y_max, x_max, 3), np.uint8)

# Grob auf 20 Punkten auf der Diagonale nach Strecke schauen
testpoints = 20
x_step = int(x_max / testpoints)
y_step = int(y_max / testpoints)

# Startpunkt setzen
punkt_x = 0
punkt_y = 0

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
    punkt_x = 0
    punkt_y = 0
    count += 1
    while (mask[punkt_y, punkt_x] == 0) and (punkt_x <= x_max - x_step) and (punkt_y <= y_max - y_step):
        punkt_x += x_step
        punkt_y += y_step

# Gefundener Startpunkt ausgeben
print('Startpunkt: (', punkt_x, '|', punkt_y, ')')

# Markiere Punkt im Debugbild
cv.circle(img_debug, (punkt_x, punkt_y), 20, (0, 255, 0), 3)


# 4. Streckenraender suchen und Kanten ablaufen
# 4.1 Rand finden
# 4.2 Kante ablaufen

# Von dem gefundenen Startpunkt auf der Strecke in verschiedenen Richtungen (insgesamt 8 Richtungen) den Rand der Maske
# suchen und von dort die Kanten ablaufen

# Richtungsvektoren als Liste definieren
step_list_x = (1, 1, 0, -1, -1, -1,  0,  1)
step_list_y = (0, 1, 1,  1,  0, -1, -1, -1)

# Arrays fuer die gefundenen Daten erstellen
raender_x = np.zeros(8, dtype=np.int16)  # x-Koordianten der Randpunkte
raender_y = np.zeros(8, dtype=np.int16)  # y-Koordianten der Randpunkte
counts = np.zeros(8, dtype=np.int16)     # Laenge der einzelnen Kanten

# 8 unterschiedliche Farben definieren, damit jede Kante seine eigene Farbe hat
test_farben = ((255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255),
               (255, 255, 255), (100, 100, 100))

# Alle 8 Richtungen durchtesten
i = 0
while i < 8:
    # Gehe von dem Startpunkt zum Rand der Maske, nutze den vorgegebene Richtungsvektor und speichere die gefundenen
    # Randpunkte im Array ab
    (raender_x[i], raender_y[i]) = rand_finden(punkt_x, punkt_y, step_list_x[i], step_list_y[i])

    # Wenn ein "neuer" Rand gefunden worden ist, dann laufe die Kante ab
    if not(raender_x[i] == 0 and raender_y[i] == 0):
        # Kante ablaufen und mit bestimmter Farbe markieren
        counts[i], _ = rand_ablaufen(raender_x[i], raender_y[i], test_farben[i])

    # Naechste Richtung testen
    i += 1


# Unterschiedliche Kantenlaengen anzeigen
print('Kantenlaengen:', counts)


# 5. Innen- und Aussenkante aus allen Kanten finden, farbig markieren und Daten speichern

# Aussen (Laengste Kante) und Innen (Zweitlaengste Kante) der Strecke herausfinden
sorted_array = sorted(counts, reverse=True)  # Array nach Groesse abfallend sortieren
# Die erste Position ist die laengste Kante --> Das ist die aeussere Kante
# Die zweite Positon ist die zweitlaengste Kante --> Die innere Kante
# Die anderen Postionen sind kleiner und deswegen nicht weiter relevant

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

# print(kante_aussen)  # Alle Kantenpunkte anzeigen

# Innenkante Blau markieren und Daten umspeichern
rand_innen_x = raender_x[pos_innen]
rand_innen_y = raender_y[pos_innen]
count_innen, kante_innen = rand_ablaufen(rand_innen_x, rand_innen_y, (255, 0, 0))

# Kantenlaengen anzeigen
print('Laenge Aussenkante:', count_aussen)
print('Laenge Innenkante:', count_innen)


# 6. Kanten glaetten und Bild aufhellen

# Kanten glaetten (unscharf machen und Mittelwert nehmen)
# img_strecke = cv.blur(img_strecke, (5, 5))
# img_strecke = cv.medianBlur(img_strecke, 7)

kante_innen = kanten_glaetten(kante_innen, count_innen, (255, 0, 0))
# kante_innen = kanten_glaetten(kante_innen, count_innen, (255, 0, 0), 10)

kante_aussen = kanten_glaetten(kante_aussen, count_aussen, (0, 0, 255))
# kante_aussen = kanten_glaetten(kante_aussen, count_aussen, (0, 0, 255), 13)

# Bild aufhellen
img_strecke[:, :] = (img_strecke[:, :] > 0) * 255


# 7. Richtung zwischen Innen- und Aussenkante herausfinden

stp = 50  # Schrittweite

# Richtung fuer kuerzeste Distanz herausfinden
punkt_a_x = kante_innen[0, 0]
punkt_a_y = kante_innen[0, 1]

# Bestimme Anzahl an Pixeln Rand ablaufen
punkt_b_x = kante_innen[stp, 0]
punkt_b_y = kante_innen[stp, 1]

# Berechne Vektor zwischen den beiden Punkten
diff_x = punkt_a_x - punkt_b_x
diff_y = punkt_a_y - punkt_b_y

laenge = np.sqrt(diff_x * diff_x + diff_y * diff_y)
# print(laenge)

abstaende = []  # Leere Liste mit den Laengen anlegen

# Test der Richtungen -1 und 1
for richtung in range(-1, 3, 2):
    # Orthogonalen Einheitsvektor berechnen (jeweils in eine andere Richtung)
    vektor_x = richtung / laenge * diff_y
    vektor_y = -richtung / laenge * diff_x

    # Abstand zum Aussenrand / Aussenkante berechnen
    abstand = 1  # Abstand auf 1 Pixel setzen
    test_x = 1  # Testpunkt auf linken oberen Rand setzen (sollte ausserhalb der Strecke sein)
    test_y = 1
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
abstaende = np.zeros(int((count_innen - stp) / stp + 1), dtype=np.int16)

# Gesamte Strecke ablaufen
for i in range(0, count_innen - stp, stp):
    # Randpunkt innen auswaehlen
    punkt_a_x = kante_innen[i, 0]
    punkt_a_y = kante_innen[i, 1]

    # Bestimme Anzahl an Pixeln Rand ablaufen
    punkt_b_x = kante_innen[i + stp, 0]
    punkt_b_y = kante_innen[i + stp, 1]

    # Berechne Vektor zwischen den beiden Punkten
    diff_x = punkt_a_x - punkt_b_x
    diff_y = punkt_a_y - punkt_b_y

    # Laenge des Vektors berechnen
    laenge = np.double(np.sqrt(diff_x * diff_x + diff_y * diff_y))
    # print(laenge)

    # Orthogonalen Einheitsvektor berechnen (mit vorher berechneter Richtung)
    vektor_x = -richtung / laenge * diff_y
    vektor_y = richtung / laenge * diff_x

    # Laenge zum Aussenrand berechnen (in richtige Richtung)
    abstand = 1  # Abstand auf 1 Pixel setzen
    test_x = 1  # Testpunkt auf linken oberen Rand setzen (sollte ausserhalb der Strecke sein)
    test_y = 1
    while (img_strecke[test_y - 1:test_y + 1, test_x - 1: test_x + 1, 2] == 0).all():
        test_x = int(punkt_a_x + abstand * vektor_x)  # Neuen Testpunkt (X) berechnen
        test_y = int(punkt_a_y + abstand * vektor_y)  # Neuen Testpunkt (Y) berechnen
        # Punkt auf Bild gruen markieren
        img_strecke[int(punkt_a_y + abstand * vektor_y), int(punkt_a_x + abstand * vektor_x), 1] = 255
        abstand += 1  # Ein Pixel zum Abstand hochzaehlen

    # print(distanz)  # Distanz ausgeben
    abstaende[int(i / stp)] = abstand  # Abstand in Array speichern
    img_strecke[int(punkt_a_y + abstand * vektor_y), int(punkt_a_x + abstand * vektor_x), 1] = 255

# Alle Laengen ausgeben
print('Streckenbreiten: ', abstaende)


# TODO !!


# 9. Bilder anzeigen und speichern

# Zeige Bilder an
# Zeige Originalbild an
cv.namedWindow('Image', cv.WINDOW_NORMAL)
cv.imshow('Image', img)
cv.resizeWindow('Image', 300, 400)

# Zeige die Maske an
cv.namedWindow('Mask', cv.WINDOW_NORMAL)
cv.imshow('Mask', mask)
cv.resizeWindow('Mask', 300, 400)

# Zeige das Bild mit der markierten Strecke an
cv.namedWindow('Frame', cv.WINDOW_NORMAL)
cv.imshow('Frame', frame)
cv.resizeWindow('Frame', 300, 400)

# Zeige das Bild mit dem selbstgezeichneten Streckenverlauf an
cv.namedWindow('Strecke', cv.WINDOW_NORMAL)
cv.imshow('Strecke', img_strecke)
cv.resizeWindow('Strecke', x_max, y_max)

# Speichere Bilder als Datei
cv.imwrite('C:/Users/David/Desktop/test.jpg', img_strecke)
cv.imwrite('C:/Users/David/Desktop/test2.jpg', img_debug)


# Warte auf Tastendruck (sonst sieht man die Fenster nicht)
key = cv.waitKey(0)

# Schliesse alle Fenster
cv.destroyAllWindows()
