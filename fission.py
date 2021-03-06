# Authors: Bas Zoeteman, Maksim Kolk and Roshan Baldewsing
# Date: 14-01-2022
# Last edited: 24-01-2022
# This code aims to simulate a simplified model of nuclear fission.


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
            normal_scalar = (np.dot(normal, self.velocity) * (mass1 - mass2) + 2 * mass2 * compare.velocity * normal) /\
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

        # nuclear fission
        elif sum([self.neutron, compare.neutron]) == 1:
            # to know which interacting particle is the neutron
            if self.neutron:
                particle = compare
                neutron = self
            else:
                particle = self
                neutron = compare

            if 0.5 * neutron.mass * np.linalg.norm(neutron.velocity) ** 2 > 0.75 and particle.mass == 235:
                # amount of new neutrons
                if rd.random() < 0.6:
                    new_neutrons = 2
                else:
                    new_neutrons = 3

                for i in range(new_neutrons):
                    # energy distribution in MeV
                    energy = np.random.normal(0.75, 2.2)
                    while energy < 0:
                        energy = np.random.normal(0.75, 2.2)

                    # E = 0.5mv^2 with m = 1 --> v = 2E^0.5
                    new_velocity = (2 * energy) ** 0.5

                    angle = rd.random() * 2 * np.pi
                    new_velocity = np.array([
                        new_velocity * np.cos(angle),
                        new_velocity * np.sin(angle)
                    ])

                    system.add_particle(True, particle.position + new_velocity, new_velocity, np.array([0, 0]), 1, 0.3)

                system.particles.remove(self)
                system.particles.remove(compare)

                system.n_particle -= 1
                system.n_neutron += new_neutrons - 1

            else:
                system.particles.remove(neutron)
                particle.mass += 1

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
        self.n_particle = n_particle
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
                start_radius = 0.3
            else:
                start_radius = 7

            # start position for particle
            R = (self.x_max - self.x_min) / 2
            r = R * rd.random() ** 0.5
            theta = rd.random() * 2 * np.pi
            start_coord = np.array([
                (self.x_min + self.x_max) / 2 + r * np.cos(theta),
                (self.y_min + self.y_max) / 2 + r * np.sin(theta)
            ])

            # start velocity for particle
            if neutron:
                # energy distribution in MeV
                energy = np.random.normal(0.75, 2.2)
                while energy < 0:
                    energy = np.random.normal(0.75, 2.2)

                # E = 0.5mv^2 with m = 1 --> v = 2E^0.5
                init_veloc = (2 * energy) ** 0.5

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
            if particle.neutron:
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
                    for compare in self.particles:
                        if particle != compare:

                            # check for collision
                            if particle.is_collision(compare):
                                # execute collision
                                if particle in self.particles:
                                    particle.collision(compare, self)

        # update particle position
        for particle in self.particles:
            if particle.neutron:
                particle.position += particle.velocity * self.dt

        return


def simulation(n_particle, n_neutron, draw=False, x_min=0, x_max=1000, y_min=0, y_max=1000):
    system = System(n_particle, n_neutron, x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max)

    particles_per_timestep = [n_particle]
    neutrons_per_timestep = [n_neutron]

    while system.n_particle > 0.5 * n_particle and system.n_neutron > 0:
        # execute iteration
        system.iteration()
        particles_per_timestep.append(system.n_particle)
        neutrons_per_timestep.append(system.n_neutron)
        # print(f'particles = {system.n_particle} and neutrons = {system.n_neutron}')

        if draw:
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

    return particles_per_timestep, neutrons_per_timestep


# different values, number of runs
values_run = [(1000, 1183), (1000, 1140), (1000, 1095),
              (1000, 1049), (1000, 1000), (1000, 949),
              (1000, 894), (1000, 837), (1000, 775),
              (600, 775), (700, 837), (800, 894),
              (900, 949), (1000, 1000), (1100, 1049),
              (1200, 1095), (1300, 1140), (1400, 1183)]
amounts_run = 30

with open('data.csv', 'w', newline='') as myfile:
    wr = csv.writer(myfile)
    myfile.write('The experiments 1-9 are the different density value simulations\n')
    myfile.write('and the experiments 10-18 are the different total mass value simulations.\n')
    myfile.write('1-9 all run with 1000 heavy nuclei and varying radius values \n')
    myfile.write('corresponding to steps of 10% in surface area ranging from 60%-140%.\n')
    myfile.write('10-18 run with heavy nuclei values 600-1400 in steps of 100, \n')
    myfile.write('and with corresponding radius values to keep the density of heavy nuclei constant.\n')
    myfile.write('\n')

    count = 1
    for x in values_run:
        print(f'Starting runs with parameters {x}.')

        runcount = 1
        for i in range(amounts_run):
            wr.writerow([f"exp {count}", f"run {runcount}"])
            list_particle_step, list_neutrons_step = simulation(x[0], 25, x_max=x[1], y_max=x[1])
            wr.writerow(list_particle_step)
            wr.writerow(list_neutrons_step)

            print(f'Run {runcount} done.')
            runcount += 1

        print(f'Parameters {x} done.')
        count += 1

# remaining particles after each run
# reaction speed (together 10 time steps)
