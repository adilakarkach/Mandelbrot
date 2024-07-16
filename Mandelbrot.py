import pygame
import numpy as np

# Pygame initialisieren
pygame.init()

# Fenstergröße festlegen
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Mandelbrot-Betrachter")

# Anfangsbereich des Mandelbrot-Sets
x_min, x_max = -2.0, 1.0
y_min, y_max = -1.5, 1.5

# Maximaler Zoomfaktor
max_zoom = 100

# Funktion zur Berechnung des Mandelbrot-Sets
def mandelbrot(h, w, max_iter):
    # Gitter von komplexen Zahlen entsprechend unserer Ansicht erstellen
    y, x = np.ogrid[y_min:y_max:h*1j, x_min:x_max:w*1j]
    c = x + y*1j
    z = c
    divtime = max_iter + np.zeros(z.shape, dtype=int)

    # Überprüfen, ob Punkte entkommen (nicht im Mandelbrot-Set sind)
    for i in range(max_iter):
        z = z**2 + c
        diverge = z*np.conj(z) > 2**2
        div_now = diverge & (divtime == max_iter)
        divtime[div_now] = i
        z[diverge] = 2

    return divtime

# Funktion zum Zeichnen des Mandelbrot-Sets auf dem Bildschirm
def draw_mandelbrot():
    mandelbrot_set = mandelbrot(height, width, 100)
    normalized = (mandelbrot_set / mandelbrot_set.max() * 255).astype(np.uint8)

    rgb_array = np.zeros((height, width, 3), dtype=np.uint8)
    rgb_array[:,:,0] = normalized
    rgb_array[:,:,1] = (normalized + 85) % 255
    rgb_array[:,:,2] = (normalized + 170) % 255

    surf = pygame.surfarray.make_surface(rgb_array)
    screen.blit(surf, (0, 0))
    pygame.display.flip()

# Haupt-Programmschleife
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Linksklick
                mx, my = pygame.mouse.get_pos()

                # Berechnung des neuen Zentrumspunkts und Zoombereichs
                center_x = x_min + (x_max - x_min) * mx / width
                center_y = y_min + (y_max - y_min) * my / height

                zoom_factor = 1.5  # Zoomfaktor
                new_width = (x_max - x_min) / zoom_factor
                new_height = (y_max - y_min) / zoom_factor

                # Neue Ansichtsbereiche festlegen
                x_min = max(center_x - new_width / 2, -2.0)
                x_max = min(center_x + new_width / 2, 1.0)
                y_min = max(center_y - new_height / 2, -1.5)
                y_max = min(center_y + new_height / 2, 1.5)

                # Mandelbrot neu zeichnen
                draw_mandelbrot()

    # Mandelbrot initial zeichnen
    if running:
        draw_mandelbrot()

    pygame.time.wait(50)  # Kurze Pause für die Animation

# Pygame beenden
pygame.quit()
