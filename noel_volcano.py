import sys
import math
import random
import pygame as pg

pg.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LT_GRAY = (180, 180, 180)
GRAY = (120, 120, 120)
DK_GRAY = (80, 80, 80)

class Particle(pg.sprite.Sprite):
    gases_colors = {'SO2': LT_GRAY, 'CO2': GRAY, 'H2S': DK_GRAY, 'H2O': WHITE}
    VENT_LOCATION_XY = (320, 300)
    IO_SURFACE_Y = 308
    GRAVITY = 0.5
    VELOCITY_SO2 = 8
    vel_scalar = {'SO2': 1, 'CO2': 1.45, 'H2S': 1.9, 'H2O': 3.6}

    def __init__(self, screen, background):
        super().__init__()
        self.screen = screen
        self.background = background
        self.image = pg.Surface((4, 4))
        self.rect = self.image.get_rect()
        self.gas = random.choice(list(Particle.gases_colors.keys()))
        self.color = Particle.gases_colors[self.gas]
        self.vel = Particle.VELOCITY_SO2 * Particle.vel_scalar[self.gas]
        self.x, self.y = Particle.VENT_LOCATION_XY
        
        # Removed self.vector() and handled math here:
        angles = [65, 55, 45, 35, 25, 115, 125, 135] # Added some left-side angles for a fuller plume
        self.angle = random.choice(angles)
        radians = math.radians(self.angle)
        self.dx = self.vel * math.cos(radians)
        self.dy = -self.vel * math.sin(radians)

    def update(self):
        old_pos = (self.x, self.y)
        self.dy += Particle.GRAVITY
        self.x += self.dx
        self.y += self.dy
        
        # This draws the line onto the background surface permanently
        pg.draw.line(self.background, self.color, old_pos, (self.x, self.y))
        
        if self.x < 0 or self.x > self.screen.get_width() or self.y > Particle.IO_SURFACE_Y:
            self.kill()

def main():
    # FIXED INDENTATION START
    screen = pg.display.set_mode((639, 360))
    pg.display.set_caption("Io Volcano Simulator")
    
    try:
        background = pg.image.load("tvashtar_plume.gif").convert()
    except:
        background = pg.Surface((639, 360))
        background.fill(BLACK)

    legend_font = pg.font.SysFont('Arial', 22)
    text = legend_font.render('Io Volcano Simulation - Noel', True, WHITE)
    
    particles = pg.sprite.Group()
    clock = pg.time.Clock()

    while True:
        clock.tick(25)
        
        # Add a new particle each frame
        particles.add(Particle(screen, background))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        # Draw the background (which now contains all the accumulated lines)
        screen.blit(background, (0, 0))
        screen.blit(text, (320, 170))
        
        particles.update()
        # No need for particles.draw(screen) since the update() draws lines to background
        
        pg.display.flip()
    # FIXED INDENTATION END

if __name__ == "__main__":
    main()