import pygame
import numpy as np
#creation date "31-01-2025"
# Constants
WIDTH, HEIGHT = 1000, 800
G = 0.1  # Gravitational constant (adjusted for simulation)
TIMESTEP = 3  # Smaller timestep for stability
BUTTON_COLOR = (50, 50, 50)
BUTTON_HOVER_COLOR = (100, 100, 100)

class Planet:
    def __init__(self, name, mass, color, pos, velocity):
        self.name = name
        self.mass = mass
        self.color = color
        self.x, self.y = pos
        self.velocity = np.array(velocity, dtype=np.float64)
        self.orbit = []

    def update_position(self, sun, dt):
        dx = sun.x - self.x
        dy = sun.y - self.y
        distance_sq = dx**2 + dy**2
        distance = np.sqrt(distance_sq)

        if distance < 1e-6:
            return

        # Gravitational acceleration
        force = G * sun.mass / distance_sq
        theta = np.arctan2(dy, dx)
        acceleration_x = force * np.cos(theta)
        acceleration_y = force * np.sin(theta)

        # Update velocity and position
        self.velocity[0] += acceleration_x * dt
        self.velocity[1] += acceleration_y * dt
        self.x += self.velocity[0] * dt
        self.y += self.velocity[1] * dt

        # Clamp to screen (optional)
        self.x = max(0, min(WIDTH, self.x))
        self.y = max(0, min(HEIGHT, self.y))

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.active = True

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Elliptical Orbit Simulator")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)

    # Create buttons
    buttons = [
        Button(10, 10, 120, 40, "Toggle Orbit"),
        Button(140, 10, 120, 40, "Speed Up (1.5x)"),
        Button(270, 10, 120, 40, "Slow Down (1.5x)")
    ]

    show_orbit = True
    speed_factor = 1.0  # Initial speed multiplier

    # Celestial bodies
    sun = Planet("Sun", 10000, (255, 255, 0), (WIDTH//2, HEIGHT//2), (0, 0))
    earth = Planet(
        name="Earth",
        mass=10,
        color=(0, 0, 255),
        pos=(WIDTH//2 + 300, HEIGHT//2),  # Start 300 pixels to the right
        velocity=(0, 1.4)  # Adjusted for elliptical orbit
    )

    mars = Planet(
        name="Mars",
        mass=8,
        color=(255, 0, 0),
        pos=(WIDTH//2 + 100, HEIGHT//2),  # Start 100 pixels to the right
        velocity=(0, 2.2)  # Adjusted for elliptical orbit
        #when you speed up mars it goes in chaotic motion so if you like to fix it and make it smooth 
        #the smallest value i have find that it works with 1 decimal is 3.1 so comment the above and uncomment  the below
        #velocity=(0,3.1)
    )

    jupiter = Planet(
        name="Jupiter",
        mass=15,
        color=(128, 128, 128),
        pos=(WIDTH//2 + 450, HEIGHT//2),  # Start 450 pixels to the right
        velocity=(0, 1.2)  # Adjusted for elliptical orbit
    )

    running = True
    while running:
        screen.fill((0, 0, 0))
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate(buttons):
                    if button.rect.collidepoint(event.pos):
                        if i == 0:  # Toggle Orbit
                            show_orbit = not show_orbit
                        elif i == 1:  # Speed Up (1.5x)
                            speed_factor = min(speed_factor * 1.5, 10.0)  # Max 10x speed
                        elif i == 2:  # Slow Down (1.5x)
                            speed_factor = max(speed_factor / 1.5, 0.1)  # Min 0.1x speed
        
        # Calculate effective timestep based on speed factor
        effective_dt = TIMESTEP * speed_factor

        # Update positions based on the sun
        earth.update_position(sun, effective_dt)
        mars.update_position(sun, effective_dt)
        jupiter.update_position(sun, effective_dt)

        # Draw celestial bodies
        pygame.draw.circle(screen, sun.color, (int(sun.x), int(sun.y)), 20)
        pygame.draw.circle(screen, earth.color, (int(earth.x), int(earth.y)), 10)
        pygame.draw.circle(screen, mars.color, (int(mars.x), int(mars.y)), 8)
        pygame.draw.circle(screen, jupiter.color, (int(jupiter.x), int(jupiter.y)), 15)

        # Draw orbit trail if enabled
        if show_orbit:
            earth.orbit.append((earth.x, earth.y))
            mars.orbit.append((mars.x, mars.y))
            jupiter.orbit.append((jupiter.x, jupiter.y))
            if len(earth.orbit) > 1:
                pygame.draw.lines(screen, earth.color, False, earth.orbit[-500:], 1)
                pygame.draw.lines(screen, mars.color, False, mars.orbit[-500:], 1)
                pygame.draw.lines(screen, jupiter.color, False, jupiter.orbit[-500:], 1)
        else:
            earth.orbit.clear()
            mars.orbit.clear()
            jupiter.orbit.clear()

        # Draw toggle button
        for button in buttons:
            button_color = BUTTON_HOVER_COLOR if button.rect.collidepoint(pygame.mouse.get_pos()) else BUTTON_COLOR
            pygame.draw.rect(screen, button_color, button.rect)
            text_surf = font.render(button.text, True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=button.rect.center)
            screen.blit(text_surf, text_rect)

        # Display current speed factor
        speed_text = font.render(f"Speed: {speed_factor:.2f}x", True, (255, 255, 255))
        screen.blit(speed_text, (10, HEIGHT - 40))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
