import sys
import math
import random
import pygame

# ----------------- CONFIGURATION -----------------
WIDTH, HEIGHT = 720, 1280       # Portrait resolution matching mobile videos
FPS = 60
BG_COLOR = (0, 0, 0)            # Pure Pitch Black

# String Art Geometry Settings
NUM_LINES = 160                 # Dense, delicate string threads
TOTAL_TIME = 32.0               # Smooth, slow and cinematic drawing (32 seconds)
SCALE = 18.0                    # Size of the heart

# Pure Cyan/Electric Blue Color Palette
BLUE_COLOR = (0, 180, 255)      # Crisp solid neon blue line
GLOW_COLOR = (0, 90, 220)       # Soft blue glow layer
CORE_COLOR = (180, 235, 255)     # Hot center accent

class Sparkle:
    """Very fine, delicate glowing blue embers."""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(0.3, 1.4)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed - 0.2  # gentle upward drift
        self.life = 255
        self.decay = random.uniform(3.0, 7.0)
        self.size = random.uniform(1.0, 2.2)     # Barik / very fine size

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= self.decay

    def draw(self, surface):
        if self.life > 0:
            alpha = int(self.life)
            rad = max(1, int(self.size))
            s_surf = pygame.Surface((rad * 4, rad * 4), pygame.SRCALPHA)
            # Soft glowing core
            pygame.draw.circle(s_surf, (0, 180, 255, alpha), (rad * 2, rad * 2), rad)
            pygame.draw.circle(s_surf, (220, 245, 255, alpha), (rad * 2, rad * 2), max(1, rad // 2))
            surface.blit(s_surf, (self.x - rad * 2, self.y - rad * 2))

def heart_point(t, scale=SCALE):
    """Parametric cardioid formula matching the exact video curve."""
    x = 16 * (math.sin(t) ** 3)
    y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
    return x * scale, y * scale

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Electric Blue String Art Heart with Fine Sparkles")
    clock = pygame.time.Clock()

    center_x = WIDTH // 2
    center_y = HEIGHT // 2 - 20

    main_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    glow_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    sparkle_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    sparkles = []
    elapsed_time = 0.0
    prev_drawn_lines = 0
    running = True

    while running:
        dt = clock.tick(FPS) / 1000.0
        elapsed_time += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    elapsed_time = 0.0
                    prev_drawn_lines = 0
                    sparkles.clear()

        # Step-by-step sequential progress (slowed down for cinematic experience)
        progress = min(1.0, elapsed_time / TOTAL_TIME)
        current_lines = int(progress * NUM_LINES)

        main_surface.fill((0, 0, 0, 0))
        glow_surface.fill((0, 0, 0, 0))
        sparkle_surface.fill((0, 0, 0, 0))

        # Bottom tip & top center connection points
        hx_bot, hy_bot = heart_point(math.pi, scale=SCALE)
        bottom_tip = (center_x + hx_bot, center_y + hy_bot)
        top_center = (center_x, center_y - 20)

        # Draw strings sequentially
        for i in range(current_lines):
            t = math.pi + (i / NUM_LINES) * 2 * math.pi
            hx, hy = heart_point(t, scale=SCALE)
            target_pt = (center_x + hx, center_y + hy)

            # Soft blue glow pass
            pygame.draw.line(glow_surface, (*GLOW_COLOR, 50), top_center, target_pt, 3)
            pygame.draw.line(glow_surface, (*GLOW_COLOR, 50), bottom_tip, target_pt, 3)

            # Crisp neon electric blue lines
            pygame.draw.line(main_surface, BLUE_COLOR, top_center, target_pt, 1)
            pygame.draw.line(main_surface, BLUE_COLOR, bottom_tip, target_pt, 1)

        # Spawn fine sparkles at the active drawing tip as heart forms
        if current_lines < NUM_LINES and current_lines > 0:
            active_t = math.pi + (current_lines / NUM_LINES) * 2 * math.pi
            ax, ay = heart_point(active_t, scale=SCALE)
            tip_x, tip_y = center_x + ax, center_y + ay

            # Emit barik / fine sparkles around current active drawing point
            for _ in range(random.randint(2, 4)):
                sparkles.append(Sparkle(tip_x + random.uniform(-4, 4), tip_y + random.uniform(-4, 4)))

        # Update and draw sparkles
        for sp in sparkles[:]:
            sp.update()
            if sp.life <= 0:
                sparkles.remove(sp)
            else:
                sp.draw(sparkle_surface)

        # Subtle bottom baseline in matching deep blue
        pygame.draw.line(main_surface, (0, 45, 100), (center_x - 300, bottom_tip[1] + 30), (center_x + 300, bottom_tip[1] + 30), 1)

        # Render composite
        screen.fill(BG_COLOR)
        screen.blit(glow_surface, (0, 0), special_flags=pygame.BLEND_ADD)
        screen.blit(main_surface, (0, 0))
        screen.blit(sparkle_surface, (0, 0), special_flags=pygame.BLEND_ADD)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
