from math import sin, cos, sqrt, atan2, pi
import glm
import pygame


class Planet:
    dt = 1 / 100
    G = 6.67428e-11  # G constant
    scale = 1 / 1409466.667  # 1 m = 1/1409466.667 pixlar

    def __init__(self, *, pos=glm.vec2(0, 0), radius=0, color=(0, 0, 0), mass=0, vel=glm.vec2(0, 0)):
        self.pos = pos  # y-coordinate pygame-window
        self.radius = radius
        self.color = color
        self.mass = mass
        self.vel = vel  # velocity in the y axis

    def draw(self, screen):
        pygame.draw.circle(screen, self.color,
                           (self.pos.x, self.pos.y), self.radius)

    def orbit(self, trace):
        pygame.draw.rect(trace, self.color, (self.pos.x, self.pos.y, 2, 2))

    def update_vel(self, Fnx, Fny):
        # Calculates acceleration in x- and y-axis for body 1.
        ax = Fnx/self.mass
        ay = Fny/self.mass
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


def motion():
    for i in range(0, len(bodies)):
        Fnx = 0  # net force
        Fny = 0
        for j in range(0, len(bodies)):
            if bodies[i] != bodies[j]:
                Fnx += (bodies[i].move(bodies[j]))[0]
                Fny += (bodies[i].move(bodies[j]))[1]
            elif bodies[i] == bodies[j]:
                continue
        bodies[i].update_vel(Fnx, Fny)
        bodies[i].draw(screen)
        bodies[i].orbit(trace)
        Fnx, Fny = 0, 0


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
        pos=glm.vec2(450, 325),
        radius=30,
        color=(0, 0, 255),
        mass=5.97219 * 10**24,
        vel=glm.vec2(-24.947719394204714 / 2, 0)
    )
    luna = Planet(
        pos=glm.vec2(450, 575 / 11),
        radius=10,
        color=(128, 128, 128),
        mass=7.349 * 10**22,
        vel=glm.vec2(1023, 0)
    )
    moon = Planet()  # the second moon
    bodies = [earth, luna]

    running = True
    clock = pygame.time.Clock()

    while running:  # if user clicks close window
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        pygame.Surface.blit(screen, trace, (0, 0))
        motion()

        pygame.display.flip()  # update? flip?

    pygame.quit()
