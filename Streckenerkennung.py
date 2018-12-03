# Bibliotheken importieren
import cv2 as cv    # OpenCV
import numpy as np  # NumPy


#############################
# FUNCTIONS                 #
#############################


# Kanten glätten
def kanten_glaetten(kanten_array, pixel_count, farbe, step_size=19):
    start_x = kanten_array[0, 0]
    start_y = kanten_array[0, 1]
    for i in range(step_size, pixel_count - step_size, step_size):
        diff_step_x = (kanten_array[i, 0] - start_x) / step_size
        diff_step_y = (kanten_array[i, 1] - start_y) / step_size

        for j in range(i - step_size, i - 1):
            img_strecke[kanten_array[j, 1], kanten_array[j, 0]] = (0, 0, 0)
            kanten_array[j, 0] = start_x + (j - i + step_size) * diff_step_x
            kanten_array[j, 1] = start_y + (j - i + step_size) * diff_step_y
            img_strecke[kanten_array[j, 1], kanten_array[j, 0]] = farbe

        start_x = kanten_array[i, 0]
        start_y = kanten_array[i, 1]

    return kanten_array


# Rand der Maske finden
def rand_finden(rand_x, rand_y, step_x, step_y):
    # Solange die Maske noch weiß ist (--> Man ist auf der Strecke), gehe eine Schrittweite weiter in Richtung Rand
    # Wenn der Rand der Strecke erreicht ist (--> Maske ist nun schwarz und man ist außerhalb der Strecke),
    # dann breche die Schleife ab
    while mask[rand_y, rand_x] != 0:
        img_strecke2[rand_y, rand_x] = (0, 255, 0)  # Laufstrecke markieren (auf Debug Bild)
        rand_x += step_x  # Ändere die x-Position um die x-Schrittweite
        rand_y += step_y  # Ändere die y-Position um die y-Schrittweite

    # Letzten Schritt rückgängig machen, um wieder innerhalb der Maske und damit auf der Strecke zu sein
    rand_x -= step_x
    rand_y -= step_y
    # img_strecke[rand_y, rand_x] = (0, 0, 0)  # Letzte Markierung löschen

    # Überprüfen, ob in der Nähe (+-1 Pixel) schon eine Kante markiert worden ist
    if (img_strecke[rand_y - 1:rand_y + 1, rand_x - 1:rand_x + 1] != (0, 0, 0)).any():
        # Wenn ja, dann ist diese Kante schon markiert und braucht nicht nochmal "gefunden" werden
        # Daher wird (0, 0) zurückgegeben, die aufrufende Instanz weiß nun auch, dass diese Kante schon gefunden wurde
        return 0, 0

    # Markiere Randpunkt im neuen Streckenbild
    # cv.circle(img_strecke, (rand1_x, rand1_y), 20, (0, 255, 0), 3)

    # Gebe die Position des Randpunktes zurück
    return rand_x, rand_y


# Rand der Maske ablaufen
def rand_ablaufen(kante_x, kante_y, farbe):
    # Übergebenenen Startpunkt speichern, damit später wieder darauf zugegriffen werden kann
    rand_x = kante_x
    rand_y = kante_y

    # Punkte rund um Testpunkt anschauen, erster Punkt doppelt, damit alle Pixelübergänge betrachtet werden können
    test_list_x = (-1, 0, 1, 1, 1, 0, -1, -1, -1)
    test_list_y = (-1, -1, -1, 0, 1, 1, 1, 0, -1)

    # Zaehlvariable definieren und nullsetzen
    pixel_count = 0
    kanten_array = np.zeros((10000, 2), dtype=np.int16)
    kanten_array[0, 0] = kante_x
    kanten_array[0, 1] = kante_y

    # Stoppen, falls "verlaufen"
    while pixel_count < 10000:
        pixel_count += 1  # Zählvariable um eins erhöhen

        # Zuerst nach Farbe links oben schauen und zwischenspeichern
        last_color = mask[kante_y + test_list_y[0], kante_x + test_list_x[0]]

        # In Schleife alle 9 möglichen Kanten überprüfen
        for i in range(1, 9):
            # Punkte rund um aktuellen Randpunkt anschauen und Farbdifferenz betrachten
            new_x = kante_x + test_list_x[i]  # Koordianten des zu überprüfendnen x-Punktes zwischenspeichern
            new_y = kante_y + test_list_y[i]  # y-Punkt zwischenspeichern
            diff = abs(int(last_color) - int(mask[new_y, new_x]))  # Farbwertdifferenz (Betrag) speichern

            # Wenn Differenz größer als 100 (also neuer Punkt im anderen Bereich) und Kante dort noch nicht gefunden
            if diff > 100 and (img_strecke[new_y, new_x] == (0, 0, 0)).all() and \
                    (img_strecke[kante_y + test_list_y[i - 1], kante_x + test_list_x[i - 1]] == (0, 0, 0)).all():
                # Wenn Bild nicht schwarz, also in Strecke: vorherigen Punkt nehmen (der in Strecke war),
                # der zuletzt getestet wurde, als neuen Kantenpunkt festlegen
                if last_color != 0:
                    kante_x += test_list_x[i - 1]
                    kante_y += test_list_y[i - 1]
                # Wenn Bild schwarz (also nicht in Strecke): diesen Punkt als neuen Punkt nehmen
                else:
                    kante_x += test_list_x[i]
                    kante_y += test_list_y[i]
                # print(test1_x, test1_y, mask[test1_y, test1_x], i)  # Gefundenen Punkt ausgeben
                break  # For-Schleife abbrechen, da Kante gefunden

            # Aktuellen Punkt als vorherigen Farbtestpunkt setzen
            last_color = mask[new_y, new_x]

        # Plausibilitätsprüfung: Neuer Punkt muss auf der Strecke liegen
        # Sonst breche die Schleife ab und melde einen Error
        if mask[kante_y, kante_x] == 0:
            print('Error')
            break

        # Überprüfen, ob der Startpunkt erreicht wurde
        # Wenn ja, dann beende die Schleife (Beende die Kantenerkennung)
        if kante_x == rand_x and kante_y == rand_y:
            # print('start reached, count = ', pixel_count)
            break

        # Gefundenen Punkt der Kante rot einfärben
        img_strecke[kante_y, kante_x] = farbe
        img_strecke2[kante_y, kante_x] = farbe

        # Punkt in Array abspeichern
        kanten_array[pixel_count, 0] = kante_x
        kanten_array[pixel_count, 1] = kante_y

    # Array auf benötigte Länge kürzen
    kanten_array = kanten_array[0:pixel_count, :]

    # Länge der Kante (Anzahl der Pixel) zurückgeben
    return pixel_count, kanten_array


#############################
# CODE START                #
#############################


# Definiere Farb-Ranges
lower_value = 0    # Untere Wertschwelle für Streckenerkennung (Ganz Schwarz)
upper_value = 110  # Obere Wertschelle (Dunkles Grau)
lower_color = (lower_value, lower_value, lower_value)
upper_color = (upper_value, upper_value, upper_value)


# Lese Bild von Festplatte
# img = cv.imread('D:/samir/Dokumente/Studium/DHBW/Semester_5/Studienarbeit/Quellcode/Images/Oval3_7.jpg')
img = cv.imread('C:/Users/David/Documents/Studium/_Semester 5/Studienarbeit/Streckenbilder/OvaleStrecken/Oval3_7.jpg')


# Erstelle eine Kopie vom Bild
frame = img.copy()

# Bild auf bestimmte Größe skalieren (verkleinern)
scale = 0.3
frame = cv.resize(frame, (0, 0), fx=scale, fy=scale)


# Bild in den HSV-Farbraum konvertieren
frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
# Bild aufhellen / verdunkeln
frame[:, :, 2] = frame[:, :, 2] - 4
# Bild von HSV zurück nach BGR konvertieren
frame = cv.cvtColor(frame, cv.COLOR_HSV2BGR)


# Ermittle Bildgröße
# TODO: Was ist x und was ist y?
x_max = len(frame[:, 0])  # Breite des Bilds
y_max = len(frame[0, :])  # Höhe des Bilds


# Filtere Bild nach Farbgrenzen
mask = cv.inRange(frame, lower_color, upper_color)

# Kleine Bereiche aus der Maske entfernen
mask2 = mask.copy()  # Kopie der Maske erstellen
area = 10  # Größe des Durchsuch-Bereichs festlegen: Hier: 10x10
area2 = int(area / 2)

# Bild durchsuchen
for x in range(area2, y_max - area2, area):  # X-Werte durchgehen    # X Y IHR SEID SCHEIßE!!
    for y in range(area2, x_max - area2, area):   # Y-Werte durchgehen
        # Area of Interest aus kopierter Maske herauskopieren
        copy = (mask2[y - area2:y + area2, x - area2:x + area2])
        summe = sum(sum(copy))  # Summe der Weißen Pixel in dem Bereich berechnen
        if summe <= 5*250:  # Anzahl der Pixel auf Schwellwert überprüfen
            # Wenn zu wenig Pixel in diesem Bereich Weiß sind, dann wird der gesamte Bereich in der Kopie
            # auf Null gesetzt
            mask[y - area2:y + area2, x - area2:x + area2] = 0
        else:
            mask[y - area2:y + area2, x - area2:x + area2] = 255


# Kopie der Maske erstellen und zu Farbbild konvertieren
img_strecke2 = mask.copy()
img_strecke2 = cv.cvtColor(img_strecke2, cv.COLOR_GRAY2BGR)


# Finde Konturen in der Maske, die nur noch zeigt, wo die Strecke ist:
_, contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

# Suche die größte Kontur heraus (diese ist höchst wahrscheinlich die Strecke)
# Nehme dazu die Fläche der Kontur und überprüfe, ob die größer als Null ist
if len(contours) > 0:
    strecke = max(contours, key=cv.contourArea)

    # Zeichne ein Rechteck um die Strecke in das Bild ein:
    x, y, w, h = cv.boundingRect(strecke)
    cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), thickness=30)


# Neues leeres (schwarzes) Bild erstellen
img_strecke = np.zeros((x_max, y_max, 3), np.uint8)

# Grob auf 20 Punkten auf der Diagonale nach Strecke schauen
testpoints = 20
x_step = int(y_max / testpoints)
y_step = int(x_max / testpoints)

# Startpunkt setzen
punkt_x = 0
punkt_y = 0

while (mask[punkt_y, punkt_x] == 0) and (punkt_x <= y_max - x_step):
    punkt_x += x_step
    punkt_y += y_step


# Wenn Strecke nicht gefunden, also der Punkt der Maske schwarz: fünffach geringere Schrittweite nehmen:
# maximal 100 mal testen oder wenn Schrittweite bei einem 1 ist
# (also jedes Pixel in einer Richtung quer durchs Bild getestet wird)
# Andere Möglichkeiten: doppelte so viele Punkte testen (x_step = int(x_step / 2) oder
# testpoints = 5*testpoints und x_step = int(y_max / testpoints)),
# fünf Punkte mehr testen (testpoints = testpoints + 5 und x_step = int(y_max / testpoints))
count = 0
while (mask[punkt_y, punkt_x] == 0) and (count < 100 or x_step == 1 or y_step == 1):
    x_step = int(x_step / 5)
    y_step = int(y_step / 5)
    punkt_x = 0
    punkt_y = 0
    count += 1
    while (mask[punkt_y, punkt_x] == 0) and (punkt_x <= y_max - x_step) and (punkt_y <= x_max - y_step):
        punkt_x += x_step
        punkt_y += y_step

# Gefundener Startpunkt ausgeben
print('Startpunkt: (', punkt_x, '|', punkt_y, ')')

# Markiere Punkt im neuen Streckenbild
# cv.circle(img_strecke, (punkt_x, punkt_y), 20, (0, 255, 0), 3)


# Von dem gefundenen Startpunkt auf der Strecke in verschiedenen Richtungen (insgesamt 8 Richtungen den Rand der Maske
# suchen und von dort die Kanten ablaufen

# Richtungsvektoren als Liste definieren
step_list_x = (1, 1, 0, -1, -1, -1,  0,  1)
step_list_y = (0, 1, 1,  1,  0, -1, -1, -1)

# Arrays für die gefundenen Daten  erstellen
raender_x = np.zeros(8, dtype=np.int16)  # x-Koordianten der Randpunkte
raender_y = np.zeros(8, dtype=np.int16)  # y-Koordianten der Randpunkte
counts = np.zeros(8, dtype=np.int16)     # Länge der einzelnen Kanten

# 8 unterschiedliche Farben definieren, damit jede Kante seine eigene Farbe hat
# TODO: Sind unterschiedliche Farben wirklich notwendig?
test_farben = ((255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255), (255, 255, 255), (100, 100, 100))

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

    # Nächste Richtung testen
    i += 1


# Unterschiedliche Kantenlängen anzeigen
print('Kantenlängen:', counts)


# Außen (Längste Kante) und Innen (Zweitlängste Kante) der Strecke herausfinden
sorted_array = sorted(counts, reverse=True)  # Array nach Größe abfallend sortieren
# Die erste Position ist die längste Kante --> Das ist wahrscheinlich die äußere Kante
# Die zweite Positon ist die zweitlängste Kante --> Im Normalfall die innere Kante
# Die anderen Postionen sind kleiner und deswegen nicht weiter relevant

# Äußere Kante im orginalen Array suchen und Indexposition speichern
pos_aussen = 0
while sorted_array[0] != counts[pos_aussen]:
    pos_aussen += 1

# Innere Kante im originalen Array suchen und Indexposition speichern
pos_innen = 0
while sorted_array[1] != counts[pos_innen]:
    pos_innen += 1


# Bild wieder komplett schwarz machen
img_strecke[:, :, :] = 0

# Außenkante Rot markieren und Daten umspeichern
rand_aussen_x = raender_x[pos_aussen]
rand_aussen_y = raender_y[pos_aussen]
count_aussen, kante_aussen = rand_ablaufen(rand_aussen_x, rand_aussen_y, (0, 0, 255))

# print(kante_aussen)

# Innenkante Blau markieren und Daten umspeichern
rand_innen_x = raender_x[pos_innen]
rand_innen_y = raender_y[pos_innen]
count_innen, kante_innen = rand_ablaufen(rand_innen_x, rand_innen_y, (255, 0, 0))

# Kantenlängen anzeigen
print('Länge Außenkante:', count_aussen)
print('Länge Innenkante:', count_innen)

# Geraden und Kurven finden

# Kanten glätten (unscharf machen und Mittelwert nehmen)
# img_strecke = cv.blur(img_strecke, (5, 5))
# img_strecke = cv.medianBlur(img_strecke, 7)

kante_innen = kanten_glaetten(kante_innen, count_innen, (255, 0, 0))
kante_innen = kanten_glaetten(kante_innen, count_innen, (255, 0, 0), 13)

kante_aussen = kanten_glaetten(kante_aussen, count_aussen, (0, 0, 255))
# kante_aussen = kanten_glaetten(kante_aussen, count_aussen, (0, 0, 255), 13)

img_strecke[:, :] = (img_strecke[:, :] > 0) * 255

stp = 50

# Richtung für kürzeste Distanz herausfinden
punkt_a_x = kante_innen[i, 0]
punkt_a_y = kante_innen[i, 1]

# Bestimme Anzahl an Pixeln Rand ablaufen
punkt_b_x = kante_innen[i + stp, 0]
punkt_b_y = kante_innen[i + stp, 1]

# Berechne Vektor zwischen den beiden Punkten
diff_x = punkt_a_x - punkt_b_x
diff_y = punkt_a_y - punkt_b_y

laenge = np.sqrt(diff_x * diff_x + diff_y * diff_y)
# print(laenge)
# Orthogonalen Einheitsvektor berechnen
vektor_x = -1 / laenge * diff_y
vektor_y = 1 / laenge * diff_x

# Länge zum Außenrand berechnen (in eine Richtung)
i2 = 1
test_x = 1
test_y = 1
while (img_strecke[test_y - 1:test_y + 1, test_x - 1: test_x + 1, 2] == 0).all():
    test_x = int(punkt_a_x + i2 * vektor_x)
    test_y = int(punkt_a_y + i2 * vektor_y)
    img_strecke[int(punkt_a_y + i2 * vektor_y), int(punkt_a_x + i2 * vektor_x), 1] = 255
    i2 += 1

# Orthogonalen Einheitsvektor berechnen (Minus wo anders)
vektor_x = 1 / laenge * diff_y
vektor_y = -1 / laenge * diff_x
i3 = 1
test_x = 1
test_y = 1
while (img_strecke[test_y - 1:test_y + 1, test_x - 1: test_x + 1, 2] == 0).all():
    test_x = int(punkt_a_x + i3 * vektor_x)
    test_y = int(punkt_a_y + i3 * vektor_y)
    img_strecke[int(punkt_a_y + i2 * vektor_y), int(punkt_a_x + i2 * vektor_x), 1] = 255
    i3 += 1


if i2 > i3:
    direction = -1
else:
    direction = 1



for i in range(0, count_innen - stp, stp):
    # Randpunkt innen auswählen
    punkt_a_x = kante_innen[i, 0]
    punkt_a_y = kante_innen[i, 1]

    # Bestimme Anzahl an Pixeln Rand ablaufen
    punkt_b_x = kante_innen[i + stp, 0]
    punkt_b_y = kante_innen[i + stp, 1]

    # Berechne Vektor zwischen den beiden Punkten
    diff_x = punkt_a_x - punkt_b_x
    diff_y = punkt_a_y - punkt_b_y

    # Länge des Vektors berechnen
    laenge = np.double(np.sqrt(diff_x * diff_x + diff_y * diff_y))
    # print(laenge)
    # Orthogonalen Einheitsvektor berechnen
    vektor_x = -direction / laenge * diff_y
    vektor_y = direction / laenge * diff_x

    # Länge zum Außenrand berechnen (in eine Richtung)
    i2 = 1
    test_x = 1
    test_y = 1
    while (img_strecke[test_y - 1:test_y + 1, test_x - 1: test_x + 1, 2] == 0).all():
        test_x = int(punkt_a_x + i2 * vektor_x)
        test_y = int(punkt_a_y + i2 * vektor_y)
        img_strecke[int(punkt_a_y + i2 * vektor_y), int(punkt_a_x + i2 * vektor_x), 1] = 255
        i2 += 1

    print(i2)
    img_strecke[int(punkt_a_y + i2 * vektor_y), int(punkt_a_x + i2 * vektor_x), 1] = 255


# TODO !!

# step_x = 1
# step_y = 0
# while img_strecke[raender_y[0], raender_x[0], 2] != 0:
#     raender_x[0] += step_x
#     raender_y[0] += step_y
#
# # Letzten Schritt rückgängig machen, da nun außerhalb der Strecke
# raender_x[0] -= step_x
# raender_y[0] -= step_y
#
# test1_x = raender_x[0]
# test1_y = raender_y[0]
#
#
# # Zaehlvariable definieren
# count = 0
# # Punkte rund um Testpunkt anschauen, erster Punkt doppelt, damit alle Pixelübergänge betrachtet werden können
# test_list_x = (-1, 0, 1, 1, 1, 0, -1, -1, -1)
# test_list_y = (-1, -1, -1, 0, 1, 1, 1, 0, -1)
#
# last_x = test1_x
# last_y = test1_y
# last_diff_x = 0
# last_diff_y = 0
#
# # Stoppen, falls "verlaufen"
# while count < 10000:
#     count += 1
#
#     if count % 25 == 0:
#         diff_x = last_x - test1_x
#         diff_y = last_y - test1_y
#         last_x = test1_x
#         last_y = test1_y
#         # print(diff_x, diff_y)
#         if last_diff_x - diff_x < 3 or last_diff_y - diff_y < 3:
#             print('Gerade')
#         else:
#             print('Kurve')
#         last_diff_x = diff_x
#         last_diff_y = diff_y
#
#     # zuerst nach Farbe links oben schauen
#     last_color = img_strecke[test1_y + test_list_y[0], test1_x + test_list_x[0], 2]
#     for i in range(1, 9):
#         # Punkte rund um aktuellen Randpunkt anschauen, Farbdifferenz betrachten
#         new_x = test1_x + test_list_x[i]
#         new_y = test1_y + test_list_y[i]
#         diff = abs(int(last_color) - int(img_strecke[new_y, new_x, 2]))
#         # wenn Differenz größer als 100 (also neuer Punkt im anderen Bereich) und Kante dort noch nicht gefunden
#         if diff > 100 and img_strecke[new_y, new_x, 2] == 0:
#             # wenn Bild nicht schwarz, also in Strecke: vorherigen Punkt nehmen (der in Strecke war),
#             # der zuletzt getestet wurde, als neuen Kantenpunkt festlegen
#             if last_color != 0:
#                 test1_x += test_list_x[i - 1]
#                 test1_y += test_list_y[i - 1]
#             # wenn Bild schwarz (also nicht in Strecke): diesen Punkt als neuen Punkt nehmen
#             else:
#                 test1_x += test_list_x[i]
#                 test1_y += test_list_y[i]
#             # print(test1_x, test1_y, mask[test1_y, test1_x], i)
#             break
#         # Aktuellen Punkt als vorherigen Farbtestpunkt setzen
#         last_color = img_strecke[new_y, new_x, 2]
#
#     if img_strecke[test1_y, test1_x, 2] == 0:
#         print('Error')
#         break
#     if test1_x == raender_x[0] and test1_y == raender_y[0] and count > 100:
#         print('start reached, count = ', count)
#         break


# Zeige Bilder an
# Zeige Originalbild an
cv.namedWindow("Image", cv.WINDOW_NORMAL)
cv.imshow("Image", img)
cv.resizeWindow("Image", 300, 400)

# Zeige die Maske an
cv.namedWindow("Mask", cv.WINDOW_NORMAL)
cv.imshow("Mask", mask)
cv.resizeWindow("Mask", 300, 400)

# Zeige das Bild mit der markierten Strecke an
cv.namedWindow("frame", cv.WINDOW_NORMAL)
cv.imshow("frame", frame)
cv.resizeWindow("frame", 300, 400)

# Zeige das Bild mit dem selbstgezeichneten Streckenverlauf an
cv.namedWindow("Strecke", cv.WINDOW_NORMAL)
cv.imshow("Strecke", img_strecke)
cv.resizeWindow("Strecke", y_max, x_max)

# Speichere Bilder als Datei
cv.imwrite('C:/Users/David/Desktop/test.jpg', img_strecke)
cv.imwrite('C:/Users/David/Desktop/test2.jpg', img_strecke2)


# Warte auf Tastendruck (sonst sieht man das Fenster nicht)
key = cv.waitKey(0)

# Schließe alle Fenster
cv.destroyAllWindows()


