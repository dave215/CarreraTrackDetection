import cv2 as cv
import numpy as np


# Rand der Maske finden
def rand_finden(rand_x, rand_y, step_x, step_y):
    while mask[rand_y, rand_x] != 0:
        # img_strecke[rand1_y, rand1_x] = (255, 0, 0)  # Strecke blau markieren
        rand_x += step_x
        rand_y += step_y

    # Letzten Schritt rückgängig machen, da nun außerhalb der Strecke
    rand_x -= step_x
    rand_y -= step_y
    # Markiere Randpunkt im neuen Streckenbild
    # cv.circle(img_strecke, (rand1_x, rand1_y), 20, (0, 255, 0), 3)
    return rand_x, rand_y


# Rand der Maske ablaufen
def rand_ablaufen(kante_x, kante_y, farbe):
    # Zaehlvariable definieren
    count = 0
    # Punkte rund um Testpunkt anschauen, erster Punkt doppelt, damit alle Pixelübergänge betrachtet werden können
    test_list_x = (-1, 0, 1, 1, 1, 0, -1, -1, -1)
    test_list_y = (-1, -1, -1, 0, 1, 1, 1, 0, -1)

    # Stoppen, falls "verlaufen"
    while count < 10000:
        count += 1
        # zuerst nach Farbe links oben schauen
        last_color = mask[kante_y + test_list_y[0], kante_x + test_list_x[0]]
        for i in range(1, 9):
            # Punkte rund um aktuellen Randpunkt anschauen, Farbdifferenz betrachten
            new_x = kante_x + test_list_x[i]
            new_y = kante_y + test_list_y[i]
            diff = abs(int(last_color) - int(mask[new_y, new_x]))
            # wenn Differenz größer als 100 (also neuer Punkt im anderen Bereich) und Kante dort noch nicht gefunden
            if diff > 100 and (img_strecke[new_y, new_x, 2] == 0 and img_strecke[new_y, new_x, 0] == 0):
                # wenn Bild nicht schwarz, also in Strecke: vorherigen Punkt nehmen (der in Strecke war),
                # der zuletzt getestet wurde, als neuen Kantenpunkt festlegen
                if last_color != 0:
                    kante_x += test_list_x[i - 1]
                    kante_y += test_list_y[i - 1]
                # wenn Bild schwarz (also nicht in Strecke): diesen Punkt als neuen Punkt nehmen
                else:
                    kante_x += test_list_x[i]
                    kante_y += test_list_y[i]
                # print(test1_x, test1_y, mask[test1_y, test1_x], i)
                break
            # Aktuellen Punkt als vorherigen Farbtestpunkt setzen
            last_color = mask[new_y, new_x]

        if mask[kante_y, kante_x] == 0:
            print('Error')
            break
        if kante_x == rand1_x and kante_y == rand1_y and count > 100:
            print('start reached, count = ', count)
            break
        # gefundenen Punkt der Kante rot einfärben
        img_strecke[kante_y, kante_x] = farbe


# Definiere Farb-Ranges
lower_value = 0    # Untere Wertschwelle für Streckenerkennung (Ganz Schwarz)
upper_value = 110  # Obere Wertschelle (Dunkles Grau)
lower_color = (lower_value, lower_value, lower_value)
upper_color = (upper_value, upper_value, upper_value)

# Lese Bild von Festplatte
img = cv.imread('D:/samir/Dokumente/Studium/DHBW/Semester_5/Studienarbeit/Quellcode/Images/Oval3_7.jpg')

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
x_max = len(frame[:, 0])  # Breite des Bilds
y_max = len(frame[0, :])  # Höhe des Bilds


# Kantenerkennung auf dem Originalbild
# img_canny = cv.Canny(frame, 100, 200)


# Filtere Bild nach Farbgrenzen
mask = cv.inRange(frame, lower_color, upper_color)

# Kleine Bereiche aus der Maske entfernen
mask2 = mask.copy()  # Kopie der Maske erstellen
area = 10  # Größe des Durchsuch-Bereichs festlegen: Hier: 10x10
area2 = int(area / 2)

# Bild durchsuchen
for x in range(area2, y_max - area2, area):  # X-Werte durchgehen # X Y IHR SEID SCHEIßE!!!!!!!!!!!!
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

punkt_x = 0
punkt_y = 0

while (mask[punkt_y, punkt_x] == 0) and (punkt_x <= y_max - x_step):
    punkt_x += x_step
    punkt_y += y_step


# wenn Strecke nicht gefunden, also der Punkt der Maske schwarz: fünffach geringere Schrittweite nehmen:
# maximal 100 mal testen oder wenn Schrittweite bei einem 1 ist
# (also jedes Pixel in einer Richtung quer durchs Bild getestet wird)
# andere Möglichkeiten: doppelte so viele Punkte testen (x_step = int(x_step / 2) oder
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

print('Startpunkt: (', punkt_x, '|', punkt_y, ')')

# Markiere Punkt im neuen Streckenbild
# cv.circle(img_strecke, (punkt_x, punkt_y), 20, (255, 255, 0), 3)

# Gehe von dem Punkt zum Rand der Maske
step_x = 1 # nach rechts
step_y = 0 # nach unten

# Schritt wie oben definiert machen, bis Rand erreicht / bis erster Schritt außerhalb der Strecke
(rand1_x, rand1_y) = rand_finden(punkt_x, punkt_y, step_x, step_y)

# Gehe den Rand der Maske entlang, bis der Anfang wieder erreicht ist
rand_ablaufen(rand1_x, rand1_y, (0, 0, 255))

# Gehe von dem Punkt zum Rand der Maske
step_x = -1 # nach rechts
step_y = 0 # nach unten

# Schritt wie oben definiert machen, bis Rand erreicht / bis erster Schritt außerhalb der Strecke
(rand2_x, rand2_y) = rand_finden(punkt_x, punkt_y, step_x, step_y)

# Gehe den Rand der Maske entlang, bis der Anfang wieder erreicht ist
rand_ablaufen(rand2_x, rand2_y, (255, 0, 0))

# Geraden und Kurven finden

# Kanten glätten (unscharf machen und Mittelwert nehmen)
img_strecke = cv.blur(img_strecke, (5, 5))
img_strecke = cv.medianBlur(img_strecke, 7)

img_strecke[:, :] = (img_strecke[:, :] > 0) * 255

step_x = 1
step_y = 0
while img_strecke[rand1_y, rand1_x, 2] != 0:
    rand1_x += step_x
    rand1_y += step_y

# Letzten Schritt rückgängig machen, da nun außerhalb der Strecke
rand1_x -= step_x
rand1_y -= step_y

test1_x = rand1_x
test1_y = rand1_y

# step_x = -1
# step_y = 0
# while img_strecke[rand2_y, rand2_x, 2] != 0:
#     rand2_x += step_x
#     rand2_y += step_y
#
# # Letzten Schritt rückgängig machen, da nun außerhalb der Strecke
# rand2_x -= step_x
# rand2_y -= step_y
#
# test2_x = rand2_x
# test2_y = rand2_y


# Zaehlvariable definieren
count = 0
# Punkte rund um Testpunkt anschauen, erster Punkt doppelt, damit alle Pixelübergänge betrachtet werden können
test_list_x = (-1, 0, 1, 1, 1, 0, -1, -1, -1)
test_list_y = (-1, -1, -1, 0, 1, 1, 1, 0, -1)

last_x = test1_x
last_y = test1_y
last_diff_x = 0
last_diff_y = 0

# Stoppen, falls "verlaufen"
while count < 10000:
    count += 1

    if count % 25 == 0:
        diff_x = last_x - test1_x
        diff_y = last_y - test1_y
        last_x = test1_x
        last_y = test1_y
        # print(diff_x, diff_y)
        if last_diff_x - diff_x < 3 or last_diff_y - diff_y < 3:
            print('Gerade')
        else:
            print('Kurve')
        last_diff_x = diff_x
        last_diff_y = diff_y

    # zuerst nach Farbe links oben schauen
    last_color = img_strecke[test1_y + test_list_y[0], test1_x + test_list_x[0], 2]
    for i in range(1, 9):
        # Punkte rund um aktuellen Randpunkt anschauen, Farbdifferenz betrachten
        new_x = test1_x + test_list_x[i]
        new_y = test1_y + test_list_y[i]
        diff = abs(int(last_color) - int(img_strecke[new_y, new_x, 2]))
        # wenn Differenz größer als 100 (also neuer Punkt im anderen Bereich) und Kante dort noch nicht gefunden
        if diff > 100 and img_strecke[new_y, new_x, 2] == 0:
            # wenn Bild nicht schwarz, also in Strecke: vorherigen Punkt nehmen (der in Strecke war),
            # der zuletzt getestet wurde, als neuen Kantenpunkt festlegen
            if last_color != 0:
                test1_x += test_list_x[i - 1]
                test1_y += test_list_y[i - 1]
            # wenn Bild schwarz (also nicht in Strecke): diesen Punkt als neuen Punkt nehmen
            else:
                test1_x += test_list_x[i]
                test1_y += test_list_y[i]
            # print(test1_x, test1_y, mask[test1_y, test1_x], i)
            break
        # Aktuellen Punkt als vorherigen Farbtestpunkt setzen
        last_color = img_strecke[new_y, new_x, 2]

    if img_strecke[test1_y, test1_x, 2] == 0:
        print('Error')
        break
    if test1_x == rand1_x and test1_y == rand1_y and count > 100:
        print('start reached, count = ', count)
        break

# Zeige Bilder an
# Zeige Originalbild an
cv.namedWindow("Image", cv.WINDOW_NORMAL)
cv.imshow("Image", img)
cv.resizeWindow("Image", 300, 400)

# Zeige die erkannten Kanten auf dem Originalbild am
# cv.namedWindow("Canny", cv.WINDOW_NORMAL)
# cv.imshow("Canny", img_canny)
# cv.resizeWindow("Canny", 600, 800)

# Zeige die erkannten Kanten auf dem bearbeiteten Bild an
# cv.namedWindow("Canny3", cv.WINDOW_NORMAL)
# cv.imshow("Canny3", img_canny2)
# cv.resizeWindow("Canny3", 600, 800)

# Zeige das bearbeitete Bild an
# cv.namedWindow("Img Edit", cv.WINDOW_NORMAL)
# cv.imshow("Img Edit", img_edit)
# cv.resizeWindow("Img Edit", 300, 400)

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


# Warte auf Tastendruck (sonst sieht man das Fenster nicht)
key = cv.waitKey(0)

# Schließe alle Fenster
cv.destroyAllWindows()



