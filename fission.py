# Author: Bas Zoeteman
# Date: 14-01-2022
# This code aims to simulate particles in a box interacting with each other.


import random as rd
import numpy as np
import matplotlib.pyplot as plt
import csv


class Particle:

    def __init__(self, neutron, position, velocity, acceleration, mass, radius):
        """
        initialization of Particle object
        :param bool neutron: whether the particle is a neutron or not
        :param ndarray position: 2-dimensional positional values in the form [x, y]
        :param ndarray velocity: 2-dimensional velocity values in the form [v_x, v_y]
        :param ndarray acceleration: 2-dimensional acceleration values in the form [a_x, a_y]
        :param float mass: the mass of the particle
        :param float radius: the radius of the particle under spherical assumption
        :return: None
        """
        self.neutron = neutron
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.mass = mass
        self.radius = radius
        self.just_collided = []

        return

    def is_collision(self, compare):
        """
        method for checking whether a collision occurs
        :param Particle compare: the particle with which the current particle is compared
        :return: boolean whether a collision occurs
        """
        assert isinstance(compare, Particle)
        assert not self == compare

        def overlap_check(particle1, particle2):

            distance = np.linalg.norm(particle1.position - particle2.position)

            # distance needs to be smaller than both radii added for collision
            if distance <= particle1.radius + particle2.radius:
                return True

            else:
                return False

        # prevention of looping collisions
        if compare in self.just_collided:

            # check if still colliding
            if not overlap_check(self, compare):
                # remove just collided
                self.just_collided.remove(compare)
                compare.just_collided.remove(self)

        elif overlap_check(self, compare):

            # register just collided
            self.just_collided.append(compare)
            compare.just_collided.append(self)

            return True

        return False

    def collision(self, compare, system):
        """
        method for acting upon a collision
        :param Particle compare: particle with which the collision occurs
        :param System system: system in which the particle exists
        :return bool, int: whether nuclear fission has occurred,
        """
        assert isinstance(compare, Particle)
        assert not self == compare

        # standard reflection
        if sum([self.neutron, compare.neutron]) != 1:
            mass1 = self.mass
            mass2 = compare.mass

            # total momentum at start
            momentum_start = np.multiply(mass1, self.velocity) + np.multiply(mass2, compare.velocity)

            # normal velocity of self particle
            normal = compare.position - self.position
            normal /= np.linalg.norm(normal)
            normal_scalar = (np.dot(normal, self.velocity) * (mass1 - mass2) + 2 * mass2 * compare.velocity * normal) / \
                            (mass1 + mass2)
            velocity_normal = np.multiply(normal_scalar, normal)

            # tangent velocity of self particle
            tangent = np.array([-normal[1], normal[0]])
            tangent_scalar = np.dot(tangent, self.velocity)
            velocity_tangent = np.multiply(tangent_scalar, tangent)

            # change total velocity of self particle
            self.velocity = (velocity_normal + velocity_tangent)

            # change total velocity of compare particle using momentum conservation
            compare.velocity = (momentum_start - np.multiply(mass1, self.velocity)) / mass2

            return False


        # nuclear fission  ############HERE ARE THE NEUTRONS CREATED########
        elif sum([self.neutron, compare.neutron]) == 1:
            if rd.random() < 0.6:
                new_neutrons = 2
            else:
                new_neutrons = 3

            system.n_neutron += new_neutrons - 1

            for i in range(new_neutrons):
                if self.neutron:
                    particle = compare
                else:
                    particle = self

                new_velocity = 0.2 / new_neutrons
                angle = rd.random() * 2 * np.pi
                new_velocity = np.array([
                    new_velocity * np.cos(angle),
                    new_velocity * np.sin(angle)
                ])

                system.add_particle(True, particle.position + new_velocity, new_velocity, np.array([0, 0]), 1, 0.01)

            system.particles.remove(self)
            system.particles.remove(compare)

            return True


class System:

    def __init__(self, n_particle, n_neutron, x_min=0, x_max=10, y_min=0, y_max=10):
        """
        initialization of a system where moving neutrons collide with unmoving fission particles and cause fission
        reactions to occur
        :param int n_particle: how many fission particles initially exist in the system
        :param int n_neutron: how many neutrons initially exist in the system
        :param float x_min: minimum x-coordinate of fission particles
        :param float x_max: maximum x-coordinate of fission particles
        :param float y_min: minimum y-coordinate of fission particles
        :param float y_max: maximum y-coordinate of fission particles
        :return: None
        """
        self.n_neutron = n_neutron
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.particles = []
        self.dt = 1

        def init_particle(neutron):
            """
            adds a Particle object to the system with initial conditions
            depending on whether the particle is a neutron or not
            :param bool neutron: whether the particle is a neutron or not
            :return: None
            """
            # start radius for particle
            if neutron:
                start_radius = 0.01
            else:
                start_radius = 0.1

            # start position for particle
            start_coord = np.array([
                self.x_min + rd.random() * ((self.x_max - start_radius) - (self.x_min + start_radius)),
                self.y_min + rd.random() * ((self.y_max - start_radius) - (self.y_min + start_radius))
            ])

            # start velocity for particle
            if neutron:
                init_veloc = 0.1
            else:
                init_veloc = 0

            init_angle = rd.random() * 2 * np.pi
            start_veloc = np.array([
                init_veloc * np.cos(init_angle),
                init_veloc * np.sin(init_angle)
            ])

            # start acceleration for particle
            start_accel = np.array([0, 0])

            # start mass for particle
            if neutron:
                start_mass = 1
            else:
                start_mass = 235

            # create particle with parameters
            self.particles.append(Particle(neutron, start_coord, start_veloc, start_accel, start_mass, start_radius))

            return

        for i in range(n_particle):
            init_particle(False)

        for i in range(n_neutron):
            init_particle(True)

        return

    def add_particle(self, neutron, position, velocity, acceleration, mass, radius):
        """
        adds a Particle object to the system with arbitrary values
        :param bool neutron: whether the particle is a neutron or not
        :param ndarray position: 2-dimensional positional values in the form [x, y]
        :param ndarray velocity: 2-dimensional velocity values in the form [v_x, v_y]
        :param ndarray acceleration: 2-dimensional acceleration values in the form [a_x, a_y]
        :param float mass: the mass of the particle
        :param float radius: the radius of the particle under spherical assumption
        :return: None
        """
        self.particles.append(Particle(neutron, position, velocity, acceleration, mass, radius))

        return

    def iteration(self):
        """
        simulates a single timestep of the system
        :return: None
        """
        # check special cases
        for particle in self.particles:
            # particle reaches the border of the box and gets deleted
            if not (self.x_min < particle.position[0] + particle.radius and
                    particle.position[0] - particle.radius < self.x_max):
                self.particles.remove(particle)
                self.n_neutron -= 1

            elif not (self.y_min < particle.position[1] + particle.radius and
                      particle.position[1] - particle.radius < self.y_max):
                self.particles.remove(particle)
                self.n_neutron -= 1

            else:
                for compare in self.particles[self.particles.index(particle) + 1:]:
                    # check for collision
                    if particle.is_collision(compare):
                        # execute collision
                        if particle in self.particles:
                            particle.collision(compare, self)

        # update particle position
        for particle in self.particles:
            particle.position += particle.velocity * self.dt

        return


def simulation(n_particle, n_neutron, x_min=0, x_max=10, y_min=0, y_max=10):
    system = System(n_particle, n_neutron, x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max)

    neutron_per_timestep = [n_neutron]

    while system.n_neutron > 0:
        # execute iteration
        system.iteration()
        neutron_per_timestep.append(system.n_neutron)

        # calculate values for plot
        dpi = 100
        figsize = [6, 6]
        dots = [figsize[0] * dpi, figsize[1] * dpi]
        dimension_diff = ((x_max - x_min) + (y_max - y_min)) / 2
        dots_per_distance = (sum(dots) / 2) / dimension_diff

        # draw iterations
        plt.figure('particles in a box', figsize=figsize, dpi=dpi)
        for particle in system.particles:
            markersize = dots_per_distance * particle.radius
            plt.plot(particle.position[0], particle.position[1], 'bo', markersize=markersize)
        plt.xlim(x_min, x_max)
        plt.ylim(y_min, y_max)
        plt.draw()
        plt.pause(0.001)
        plt.clf()
    print(neutron_per_timestep)

simulation(20, 20)

# What could be gotten out of the data?
# How many iteration each run takes ( while there are still neutrons left)
# How many remaining particles are left after each run
# If the normal run and the run with a wall have significant differences between them (for example runtime)
