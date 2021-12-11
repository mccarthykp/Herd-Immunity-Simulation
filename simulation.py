import random, sys
random.seed(42)
from person import Person
from logger import Logger
from virus import Virus
class Simulation(object):
    def __init__(self, virus, pop_size, num_vaccinated, initial_infected=1):
        self.pop_size = pop_size # Int
        self.next_person_id = 0 # Int
        self.virus = virus # Virus object
        self.initial_infected = initial_infected # Int
        self.new_infections = 0 # Int
        self.total_infected = 0 # Int
        self.initial_vax = num_vaccinated # saved Int for logging
        self.num_vaccinated = num_vaccinated # Int
        self.new_deaths = 0 # Int
        self.total_dead = 0 # Int
        self.newly_infected = []
        self.current_infected = []
        self.current_uninfected = []
        self.population = self._create_population() # List of Person objects
        self.file_name = f'{virus.name}_simulation_pop_{pop_size}_vp_{num_vaccinated}_infected_{initial_infected}.txt'
        self.total_interactions = 0 # Int
        self.curr_step = 0 # Int

        self.logger = Logger(self.file_name)
        self.logger.write_metadata(pop_size, num_vaccinated, virus.name, mortality_rate, virus.repro_rate)

    def _create_population(self):
        population = []

        # instantiate & append infected people to population list
        for num_infected in range(self.initial_infected):
            self.next_person_id += 1
            self.total_infected += 1
            infected = Person(_id=self.next_person_id, is_vaccinated=False, infection=virus)
            population.append(infected)
            self.current_infected.append(infected)

        # instantiate & append people to population list
        for num_vaccinated in range(self.num_vaccinated):
            self.next_person_id += 1
            uninfected = Person(self.next_person_id, True)
            population.append(uninfected)
            self.current_uninfected.append(uninfected)

        # instantiate & append unvaccinated & uninfected people to population list
        for num_unvaccinated in range(self.pop_size - self.initial_infected - self.num_vaccinated):
            self.next_person_id += 1
            uninfected = Person(self.next_person_id, False)
            population.append(uninfected)
            self.current_uninfected.append(uninfected)

        return population

    # we should continue as long as people are alive and someone still has the virus
    def should_continue(self):
        population_is_alive = False
        population_is_infected = False

        for person in self.population:
            if person.is_alive == True:
                population_is_alive = True
                if person.infection != None:
                    population_is_infected = True

        # we should continue if at least one person is alive and at least one person has the virus
        if population_is_alive and population_is_infected:
            return True
        return False
        
    def time_step(self):
        # call interaction and increment it
        self.curr_step += 1 

        # put people in groups depending on if they are infected or uninfected
        self.current_infected = []
        for person in self.population:
            if person.is_alive == False:
                pass
            elif person.infection != None:
                self.current_infected.append(person)
            else:
                self.current_uninfected.append(person)
        
        # make all infected people interact with 100 uninfected people
        for person in self.current_infected:
            for i in range(100):
                alive_uninfected_person = random.choice(self.current_uninfected)
                while alive_uninfected_person.is_alive == False:
                    alive_uninfected_person = random.choice(self.current_uninfected)
                
                self.interaction(person, alive_uninfected_person)

        
        # for all of the currently infected people 
        for person in self.current_infected:
            # if the infected person survives, they are no longer infected, are now "vaccinated", and we log it
            if person.did_survive_infection():
                self.num_vaccinated += 1
                self.current_uninfected.append(person)
                self.logger.log_infection_survival(person=person._id, did_die_from_infection=False)
            else: # if they didn't survive, they are dead and we need to remove them from the population, newly_infected and total infected, incr the death count and log it
                self.total_dead += 1
                self.new_deaths += 1
                self.logger.log_infection_survival(person=person._id, did_die_from_infection=True)
            self.current_infected.remove(person)
            self.total_infected -= 1

        self.current_infected = self.newly_infected
        self.newly_infected = []

    # interactions between infected and uninfected ALIVE people
    def interaction(self, infected, uninfected):
        assert infected.is_alive == True
        assert uninfected.is_alive == True
        self.total_interactions += 1

        # if the uninfected person is not vaccinated and gets the virus, we increment total and newly infected and log it
        if uninfected.is_vaccinated == False and self.virus.repro_rate >= random.random():
            if uninfected.infection == None:
                uninfected.infection = self.virus
                self.total_infected += 1
                self.newly_infected.append(uninfected)
                self.new_infections += 1
                self.logger.log_interaction(infected=infected._id, uninfected=uninfected._id, did_infect=True)
        else: # otherwise, log that they were not infected
            self.logger.log_interaction(infected=infected._id, uninfected=uninfected._id, did_infect=False)

    def run(self):
        while self.should_continue():
            self.time_step()
            # print('Took a step')
            self.logger.new_step(self.curr_step, self.new_infections, self.new_deaths, self.pop_size - self.total_dead, self.total_dead, self.num_vaccinated)
            self.new_infections = 0
            self.new_deaths = 0

        if self.total_dead == self.pop_size:
            cause = 'Population Died'
        else: 
            cause = 'Virus Died'
            
        self.logger.final_step(self.curr_step, self.pop_size - self.total_dead, self.total_dead, self.num_vaccinated, cause, self.total_interactions, self.num_vaccinated - self.initial_vax, self.total_dead)


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
