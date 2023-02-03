from math import sin, cos, sqrt, atan2, pi
from pygame.math import Vector2 as vec2
import pygame
import sys


class Planet:
    dt = 1 / 100
    G = 6.67428e-11  # G constant
    scale = 1 / 1409466.667  # 1 m = 1/1409466.667 pixlar

    def __init__(self, *, pos=vec2(0, 0), radius=0, color=(0, 0, 0), mass=0, vel=vec2(0, 0)):
        self.pos = pos  # y-coordinate pygame-window
        self.radius = radius
        self.color = color
        self.mass = mass
        self.vel = vel  # velocity in the y axis
        self.Fnx = None
        self.Fny = None

    def update_vel(self):
        # Calculates acceleration in x- and y-axis for body 1.
        ax = self.Fnx/self.mass
        ay = self.Fny/self.mass
        self.vel.x -= ((ax * Planet.dt)/Planet.scale)
        self.vel.y -= ((ay * Planet.dt)/Planet.scale)
        self.update_pos()

    def update_pos(self):
        # changes position considering each body's velocity.
        self.pos.x += ((self.vel.x * Planet.dt))
        self.pos.y += ((self.vel.y * Planet.dt))

    def move(self, body):
        # Calculates difference in x- and y-axis between the bodies
        dx = (self.pos.x - body.pos.x)
        dy = (self.pos.y - body.pos.y)
        # Calculates the distance between the bodies
        r = (sqrt((dy**2)+(dx**2)))
        # Calculates the angle between the bodies with atan2!
        angle = atan2(dy, dx)
        if r < self.radius:  # Checks if the distance between the bodies is less than the radius of the bodies. Uses then Gauss gravitational law to calculate force.
            F = 4/3 * pi * r
            Fx = cos(angle) * F
            Fy = sin(angle) * F
        else:
            # Newtons gravitational formula.
            F = (Planet.G*self.mass*body.mass)/((r/Planet.scale)**2)
            Fx = cos(angle) * F
            Fy = sin(angle) * F
        return Fx, Fy


class Motion:
    def __init__(self, bodies, screen, trace):
        self.bodies = bodies
        self.screen = screen
        self.trace = trace

    def draw(self, body):
        pygame.draw.circle(
            surface=self.screen,
            color=body.color,
            center=(body.pos.x, body.pos.y),
            radius=body.radius
        )

    def orbit(self, body):
        pygame.draw.rect(
            surface=self.trace,
            color=body.color,
            rect=(body.pos.x, body.pos.y, 2, 2)
        )

    def update(self):
        for bodyi in self.bodies:
            bodyi.Fnx = 0  # net force
            bodyi.Fny = 0
            for bodyj in self.bodies:
                if bodyi != bodyj:
                    dFx, dFy = bodyi.move(bodyj)
                    bodyi.Fnx += dFx
                    bodyi.Fny += dFy
            bodyi.update_vel()
            self.draw(bodyi)
            self.orbit(bodyi)


#
# Main
#
if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode([900, 650])  # width - height
    trace = pygame.Surface((900, 650))
    pygame.display.set_caption("Moon simulation")
    FPS = 60  # how quickly/frames per second our game should update. Change?

    earth = Planet(
        pos=vec2(450, 325),
        radius=30,
        color=(0, 0, 255),
        mass=5.97219e+24,
        vel=vec2(-24.947719394204714 / 2, 0)
    )
    luna = Planet(
        pos=vec2(450, 575 / 11),
        radius=10,
        color=(128, 128, 128),
        mass=7.349e+22,
        vel=vec2(1023, 0)
    )
    moon = Planet()  # the second moon

    bodies = [earth, luna]
    motion = Motion(bodies=bodies, screen=screen, trace=trace)

    clock = pygame.time.Clock()

    while True:  # if user clicks close window
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                pygame.quit()

        screen.fill((0, 0, 0))
        pygame.Surface.blit(screen, trace, (0, 0))
        motion.update()

        pygame.display.flip()  # update? flip?
