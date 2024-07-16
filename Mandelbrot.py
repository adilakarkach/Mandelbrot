import pygame
import numpy as np

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Mandelbrot Viewer")

# Set up the initial view of the Mandelbrot set
x_min, x_max = -2, 1
y_min, y_max = -1.5, 1.5

# Function to calculate the Mandelbrot set
def mandelbrot(h, w, max_iter):
    y, x = np.ogrid[y_min:y_max:h*1j, x_min:x_max:w*1j]
    c = x + y*1j
    z = c
    divtime = max_iter + np.zeros(z.shape, dtype=int)

    for i in range(max_iter):
        z = z**2 + c
        diverge = z*np.conj(z) > 2**2
        div_now = diverge & (divtime == max_iter)
        divtime[div_now] = i
        z[diverge] = 2

    return divtime

# Function to draw the Mandelbrot set
def draw_mandelbrot():
    mandelbrot_set = mandelbrot(height, width, 100)
    # Normalize and scale the values to 0-255 range
    normalized = (mandelbrot_set / mandelbrot_set.max() * 255).astype(np.uint8)
    # Create an RGB array
    rgb_array = np.zeros((height, width, 3), dtype=np.uint8)
    rgb_array[:,:,0] = normalized  # Red channel
    rgb_array[:,:,1] = normalized  # Green channel
    rgb_array[:,:,2] = normalized  # Blue channel
    # Create a surface from the array
    surf = pygame.surfarray.make_surface(rgb_array)
    # Blit the surface to the screen
    screen.blit(surf, (0, 0))
    pygame.display.flip()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                # Get the click position
                mx, my = pygame.mouse.get_pos()

                # Calculate the new center point
                center_x = x_min + (x_max - x_min) * mx / width
                center_y = y_min + (y_max - y_min) * my / height

                # Zoom in (adjust the zoom factor as needed)
                zoom_factor = 0.5
                new_width = (x_max - x_min) * zoom_factor
                new_height = (y_max - y_min) * zoom_factor

                # Update the view boundaries
                x_min = center_x - new_width / 2
                x_max = center_x + new_width / 2
                y_min = center_y - new_height / 2
                y_max = center_y + new_height / 2

                # Redraw the Mandelbrot set
                draw_mandelbrot()

    # Draw the initial Mandelbrot set
    if running:
        draw_mandelbrot()

    # Add a small delay to reduce CPU usage
    pygame.time.wait(100)

# Quit Pygame
pygame.quit()