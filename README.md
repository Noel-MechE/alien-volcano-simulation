# Io Alien Volcano Simulation

I built this program to better understand how physics 
can be turned into a running simulation using code. 
As a mechanical engineering student I already understood 
projectile motion from calculus, this project let me 
apply that same math inside a real visual program.

## What the Program Does

The simulation models volcanic plumes on Io, one of 
Jupiter's most active moons. Each particle launched 
from the volcanic vent has its own gas type, color, 
speed, and launch angle. Particles follow projectile 
physics, launching upward and falling back down under 
gravity, until they hit the surface or leave the screen.

I customized the launch angles to include both left and 
right side angles, creating a fuller and more realistic 
symmetric plume compared to the original design.

## How It Works

The program is built around a Particle class using 
Object Oriented Programming. Each time the simulation 
runs a new particle is created as an instance of that 
class with its own randomly selected characteristics.

The physics behind each particle:
- dx = velocity times cosine of launch angle (horizontal speed)
- dy = negative velocity times sine of launch angle (vertical speed)
- Every frame gravity is added to dy pulling the particle down
- This creates the same projectile arc as real volcanic ejecta

## What I Learned

- Object Oriented Programming — building a class with 
  __init__, vector(), and update() methods
- Applying real physics formulas inside a running simulation
- Using pygame for game loops, drawing, and sprite management
- Using dictionaries to map gas types to colors and velocities
- Debugging indentation errors and file path issues in Python

## How to Run

Make sure tvashtar_plume.gif is in the same folder then run:
python3 noel_volcano.py

## Requirements
pip install pygame
