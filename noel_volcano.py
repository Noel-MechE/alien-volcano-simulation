# Noel A Bobadilla Castillo
# Date: March 2026
# Program: Alien Volcano Simulation
# Description: This program simulates volcanic plumes
# on Io, one of Jupiter's moons. Particles are launched
# from a volcanic vent and fall back down under gravity.
# Each particle has its own gas type, color, speed and direction.

import sys
# so this is basically our exit, when the user closes the window
# sys.exit() is what actually ends the program without it freezing up

import math
# we need this one because of the angles, cos() sin() and radians()
# same math you use in physics class when breaking up velocity into components

import random
# this one is like rolling a dice every time a new particle gets made
# it picks the gas type and the angle so no two particles are the same

import pygame as pg
# this is the big one, pygame runs everything you see on screen
# the window, the image, the drawing, all of it, we write pg so we dont have to type pygame every time

pg.init()
# you have to wake pygame up before using it, think of it like
# turning on the tv before you can watch anything

# colors are defined using RGB, meaning Red Green Blue
# each one goes from 0 which is none of that color to 255 which is full
# so BLACK is zero of everything and WHITE is full of everything
# think of it like mixing paint but with light instead
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LT_GRAY = (180, 180, 180)
GRAY = (120, 120, 120)
DK_GRAY = (80, 80, 80)

# okay so a class is basically a blueprint, like a recipe
# every time the simulation needs a new particle it follows this recipe
# same instructions but different result every time because of random
# think of it like a factory that builds something slightly different each time
class Particle(pg.sprite.Sprite):

    # these are the values that every single particle shares no matter what
    # kind of like the rules that apply to all of them

    gases_colors = {'SO2': LT_GRAY, 'CO2': GRAY, 'H2S': DK_GRAY, 'H2O': WHITE}
    # this is a dictionary, imagine a two column table
    # left side is the gas name, right side is what color it shows up as on screen
    # SO2 shows as light gray, CO2 medium gray, H2S dark gray, H2O white

    VENT_LOCATION_XY = (320, 300)
    # this is the exact pixel on screen where the volcano vent is
    # 320 pixels from the left, 300 pixels from the top
    # every particle starts its life at this exact spot

    IO_SURFACE_Y = 308
    # this is the y coordinate of the ground on Io
    # when a particle reaches this point it hit the floor and gets removed
    # think of it as the ceiling for how low a particle can go

    GRAVITY = 0.5
    # every frame gravity pulls each particle down by 0.5 pixels
    # its a small number but it adds up over time and creates that natural arc
    # all caps because this value never changes, same reason we did it in the C++ project

    VELOCITY_SO2 = 8
    # this is the base speed for SO2 particles in pixels per frame
    # all other gas speeds get calculated from this number
    # all caps because it never changes

    vel_scalar = {'SO2': 1, 'CO2': 1.45, 'H2S': 1.9, 'H2O': 3.6}
    # another dictionary, this one stores the speed multiplier for each gas
    # lighter gases move faster because they weigh less, same science as real life
    # SO2 is heaviest so it stays at 1, H2O is lightest so it gets a 3.6 boost
    # imagine throwing a bowling ball and a tennis ball with the same force

    def __init__(self, screen, background):
        # this runs the moment a new particle gets created, automatically
        # think of it like filling out a birth certificate for each particle
        # every particle gets its own personal copy of all these values

        super().__init__()
        # this activates the parent Sprite class from pygame
        # basically we are plugging in the particle so it works with pygames systems
        # without this line the particle wouldnt behave properly

        self.screen = screen
        # save the game window so we can check later if the particle went off screen
        # self means this specific particle owns this, not all of them just this one

        self.background = background
        # save the background image so we can draw trails directly onto it
        # trails stay on the background permanently which is what creates the plume effect

        self.image = pg.Surface((4, 4))
        # make a tiny 4x4 pixel box to represent this particle on screen
        # pygame sprites need an image to exist inside the sprite group

        self.rect = self.image.get_rect()
        # get the rectangular boundary of our tiny image
        # pygame uses this to track where the particle is located on screen

        self.gas = random.choice(list(Particle.gases_colors.keys()))
        # randomly pick one gas type from our dictionary
        # the keys() gives us the names like SO2 CO2 H2S H2O
        # list() turns those into a list and random.choice() picks one
        # its like pulling a name out of a hat every time

        self.color = Particle.gases_colors[self.gas]
        # now that we know the gas type we look up its color in the dictionary
        # if the gas is H2O the color becomes WHITE and so on

        self.vel = Particle.VELOCITY_SO2 * Particle.vel_scalar[self.gas]
        # calculate this particles speed by multiplying base speed by the gas scalar
        # H2O example, 8 times 3.6 equals 28.8 pixels per frame
        # SO2 example, 8 times 1.0 equals 8 pixels per frame

        self.x, self.y = Particle.VENT_LOCATION_XY
        # place this particle at the volcano vent where it will be born
        # self.x and self.y will keep updating every frame as it moves

        # okay so this is the physics part, same math from the projectile motion calculator
        # we split the launch speed into two pieces
        # dx is how fast it moves left or right each frame
        # dy is how fast it moves up or down each frame
        # picture an arrow pointing in the launch direction
        # dx is the horizontal piece of that arrow, dy is the vertical piece
        angles = [65, 55, 45, 35, 25, 115, 125, 135]
        # these are all the possible launch angles in degrees
        # 25 to 65 send particles to the right side of the plume
        # 115 to 135 send particles to the left side
        # i added the left side angles myself to make a fuller symmetric plume
        # this is my personal customization of the original design

        self.angle = random.choice(angles)
        # randomly pick one angle from the list
        # this is why the plume looks natural, each particle flies a slightly different direction

        radians = math.radians(self.angle)
        # python math functions only work with radians not degrees
        # so we convert before using cos() or sin()

        self.dx = self.vel * math.cos(radians)
        # horizontal speed equals velocity times cosine of the angle
        # cosine gives us the horizontal portion of the velocity

        self.dy = -self.vel * math.sin(radians)
        # vertical speed equals negative velocity times sine of the angle
        # the negative sign is important because in pygame y increases going DOWN
        # so to make a particle go UP we need a negative dy value
        # gravity will slowly increase dy each frame until the particle starts falling

    def update(self):
        # this runs every single frame for every particle that exists
        # its what makes the whole thing feel alive and moving
        # think of it like a flipbook, each frame slightly moves every particle

        old_pos = (self.x, self.y)
        # save where the particle is right now before we move it
        # we need this to draw a line from the old spot to the new spot
        # that line is what creates the visible trail

        self.dy += Particle.GRAVITY
        # add gravity to the vertical speed every frame
        # at launch dy is negative which means going up
        # each frame we add 0.5, slowly making dy less negative then eventually positive
        # once dy is positive the particle starts falling back down
        # same concept as throwing a ball up, it slows, stops, then falls

        self.x += self.dx
        # move the particle horizontally by its horizontal speed
        # dx stays the same every frame so left right movement is always consistent

        self.y += self.dy
        # move the particle vertically by its vertical speed
        # dy changes every frame because gravity keeps adding to it

        pg.draw.line(self.background, self.color, old_pos, (self.x, self.y))
        # draw a colored line from where the particle was to where it is now
        # this gets drawn directly onto the background so it stays there permanently
        # over time thousands of these tiny lines build up into the full plume visual
        # the color matches the gas type so you can see which gas goes where

        if self.x < 0 or self.x > self.screen.get_width() or self.y > Particle.IO_SURFACE_Y:
            self.kill()
        # check if the particle has gone somewhere it shouldnt be anymore
        # off the left edge, off the right edge, or hit the ground means remove it
        # self.kill() only removes this one particle, everything else keeps going

def main():
    # this is where we set up everything and get the simulation started
    # creates the window, loads the background, and kicks off the game loop

    screen = pg.display.set_mode((639, 360))
    # create the game window, 639 pixels wide and 360 pixels tall
    # think of this as setting up your canvas before painting

    pg.display.set_caption("Io Volcano Simulator")
    # this is just the text that shows up in the title bar of the window

    try:
        background = pg.image.load("tvashtar_plume.gif").convert()
        # try to load the actual photo of Ios surface as the background
        # convert() makes it run faster by optimizing it for pygames display
    except:
        background = pg.Surface((639, 360))
        background.fill(BLACK)
        # if the image file is missing just use a plain black background
        # this stops the program from crashing if the gif isnt found

    # setting up the legend text so viewers know which color is which gas
    # each label is rendered in the matching color of its gas type
    legend_font = pg.font.SysFont('Arial', 20)
    so2_text = legend_font.render('--- SO2', True, LT_GRAY)
    co2_text = legend_font.render('--- CO2', True, GRAY)
    h2s_text = legend_font.render('--- H2S', True, DK_GRAY)
    h2o_text = legend_font.render('--- H2O', True, WHITE)
    title_text = legend_font.render('Io Volcano Simulation, Noel', True, WHITE)
    # render() turns the text string into an image pygame can actually display
    # True enables smooth anti-aliased edges on the text

    particles = pg.sprite.Group()
    # an empty group to hold all active particles
    # think of it like a bucket, we toss new ones in every frame
    # and dead ones get removed automatically when self.kill() is called

    clock = pg.time.Clock()
    # this controls how fast the simulation runs
    # without it the simulation would run at whatever speed the computer allows
    # which could be so fast you wouldnt be able to see anything

    # this is the game loop, it runs forever until the user closes the window
    # every single loop is one frame of the animation
    # think of it like a flipbook being flipped at 25 pages per second
    while True:
        clock.tick(25)
        # lock the simulation to 25 frames per second
        # keeps it consistent no matter what computer its running on

        for _ in range(5):
            particles.add(Particle(screen, background))
        # create 5 brand new particles every frame and add them to our group
        # each one gets built fresh from our blueprint with random characteristics
        # 5 per frame instead of 1 makes the plume look dense and realistic
        # the underscore means we dont care about the loop counter value

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        # check if the user clicked the X button to close the window
        # pg.QUIT is the event that fires when the window gets closed
        # pg.quit() shuts down pygame and sys.exit() ends the program

        screen.blit(background, (0, 0))
        # draw the background onto the screen starting at the top left corner
        # since all the particle trails are drawn onto the background this shows everything
        # blit basically means copy one image onto another surface

        screen.blit(title_text, (220, 10))
        screen.blit(h2o_text, (10, 10))
        screen.blit(h2s_text, (10, 35))
        screen.blit(co2_text, (10, 60))
        screen.blit(so2_text, (10, 85))
        # draw all the legend labels and the title on top of the background
        # the numbers in parentheses are the x and y pixel positions on screen

        particles.update()
        # call update() on every single particle in the group at once
        # this applies gravity, moves them, draws their trails, removes dead ones
        # one line but it triggers hundreds of individual particle updates every frame

        pg.display.flip()
        # this is what actually makes everything visible to the user
        # without flip() nothing would show up on screen
        # think of it like developing a photo, flip() reveals the finished picture

if __name__ == "__main__":
    main()
    # only run main() if this file is being run directly
    # if another program imports this file main() wont start automatically
    # this is just good python practice for any program you write