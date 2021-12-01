import random, sys
random.seed(42)
from person import Person
from logger import Logger
from virus import Virus


class Simulation(object):
    '''
    Main class:
        Expects init parameters passed as CL arguments when file is run.
    '''

    def __init__(self, virus, pop_size, num_vaccinated, initial_infected=1):
        ''' Logger object logger records all events during the simulation.
        Population represents all Persons in the population.
        The next_person_id is the next available id for all created Persons,
        and should have a unique _id value.
        The vaccination percentage represents the total percentage of population
        vaccinated at the start of the simulation.
        You will need to keep track of the number of people currently infected with the disease.
        The total infected people is the running total that have been infected since the
        simulation began, including the currently infected people who died.
        You will also need to keep track of the number of people that have die as a result
        of the infection.

        All arguments will be passed as command-line arguments when the file is run.
        HINT: Look in the if __name__ == "__main__" function at the bottom.
        '''
        # TODO: Create a Logger object and bind it to self.logger.
        # Remember to call the appropriate logger method in the corresponding parts of the simulation.
        # TODO: Call self._create_population() and pass in the correct parameters.
        # Store the array that this method will return in the self.population attribute.
        # TODO: Store each newly infected person's ID in newly_infected attribute.
        # At the end of each time step, call self._infect_newly_infected()
        # and then reset .newly_infected back to an empty list.

        # self.logger = Logger(self.file_name)
        
        self.pop_size = pop_size # Int
        self.next_person_id = 0 # Int
        self.virus = virus # Virus object
        self.initial_infected = initial_infected # Int
        self.total_infected = 0 # Int
        self.current_infected = 0 # Int
        self.num_vaccinated = num_vaccinated # float between 0 and 1
        self.total_dead = 0 # Int
        self.population = self._create_population() # List of Person objects
        self.file_name = f'{virus.name}_simulation_pop_{pop_size}_vp_{num_vaccinated}_infected_{initial_infected}.txt'
        self.newly_infected = []

    def _create_population(self):
        '''This method will create the initial population.
            Args:
                initial_infected (int): The number of infected people that the simulation
                will begin with.

            Returns:
                list: A list of Person objects.

        '''
        # This method should return an array filled with Person objects that matches the specifications of the simulation
        # (correct number of people in the population, correct percentage of
        # people vaccinated, correct number of initially infected people).

        population = []

        # instantiate & append infected people to population list
        for num_infected in range(self.initial_infected):
            self.next_person_id += 1
            population.append(Person(self.next_person_id, False, virus))

        # instantiate & append  people to population list
        for num_vaccinated in range(self.num_vaccinated):
            self.next_person_id += 1
            population.append(Person(self.next_person_id, True))

        # instantiate & append unvaccinated & uninfected people to population list
        for num_unvaccinated in range(self.pop_size - self.initial_infected - self.num_vaccinated):
            self.next_person_id += 1
            population.append(Person(self.next_person_id, False))


        for i in population:
            print(f'{i._id}\n')
        return population

    def _simulation_should_continue(self):
        '''
        The simulation should only end if the entire population is dead
        or everyone is vaccinated.

        Returns:
            bool: True for simulation should continue, False if it should end.
        '''

        # TODO: Complete this helper method.  Returns a Boolean.
        pass

    def run(self):
        '''
        This method should run the simulation until all requirements for ending
        the simulation are met.
        '''
        # TODO: Finish this method.  To simplify the logic here, use the helper method
        # _simulation_should_continue() to tell us whether or not we should continue
        # the simulation and run at least 1 more time_step.

        # TODO: Keep track of the number of time steps that have passed.
        # HINT: You may want to call the logger's log_time_step() method at the end of each time step.
        # TODO: Set this variable using a helper
        time_step_counter = 0
        should_continue = None

        while should_continue:
            # TODO: for every iteration of this loop, call self.time_step() to compute another
            # round of this simulation.
            print(f'The simulation has ended after {time_step_counter} turns.')
            pass

    def time_step(self):
        '''
        This method should contain all the logic for computing one time step
        in the simulation.

        This includes:
            1. 100 total interactions with a randon person for each infected person
                in the population
            2. If the person is dead, grab another random person from the population.
                Since we don't interact with dead people, this does not count as an interaction.
            3. Otherwise call simulation.interaction(person, random_person) and
                increment interaction counter by 1.
        '''

        # TODO: Finish this method.
        pass

    def interaction(self, person, random_person):
        '''
        This method should be called any time two living people are selected for an
        interaction. It assumes that only living people are passed in as parameters.

        Args:
            person1 (person): The initial infected person
            random_person (person): The person that person1 interacts with.
        '''
        # Assert statements are included to make sure that only living people are passed
        # in as params
        assert person.is_alive == True
        assert random_person.is_alive == True

        # TODO: Finish this method.
        #  The possible cases you'll need to cover are listed below:
            # random_person is vaccinated:
            #     nothing happens to random person.
            # random_person is already infected:
            #     nothing happens to random person.
            # random_person is healthy, but unvaccinated:
            #     generate a random number between 0 and 1.  If that number is smaller
            #     than repro_rate, random_person's ID should be appended to
            #     Simulation object's newly_infected array, so that their .infected
            #     attribute can be changed to True at the end of the time step.
        # TODO: Call slogger method during this method.
        pass

    def _infect_newly_infected(self):
        ''' This method should iterate through the list of ._id stored in self.newly_infected
        and update each Person object with the disease. '''
        # TODO: Call this method at the end of every time step and infect each Person.
        # TODO: Once you have iterated through the entire list of self.newly_infected, remember
        # to reset self.newly_infected back to an empty list.
        pass

if __name__ == "__main__":
    params = sys.argv[1:]

    name = str(params[0])
    pop_size = int(params[1])
    repro_rate = float(params[2])
    mortality_rate = float(params[3])
    num_vaccinated = int(params[4])

    if len(params) == 6:
        initial_infected = int(params[5])
    else:
        initial_infected = 1

    virus = Virus(name, repro_rate, mortality_rate)
    # python3 simulation.py Ebola 100 0.9 0.7 25 1
    # python3 simulation.py Ebola 100000 0.9 0.7 25000 10
    sim = Simulation(virus, pop_size, num_vaccinated, initial_infected)

    sim.run()
    print(sim.pop_size)
