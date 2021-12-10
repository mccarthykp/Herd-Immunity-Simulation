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
        self.total_infected = 0 # Int
        self.num_vaccinated = num_vaccinated # int
        self.total_dead = 0 # Int
        self.newly_infected = []
        self.population = self._create_population() # List of Person objects
        self.file_name = f'{virus.name}_simulation_pop_{pop_size}_vp_{num_vaccinated}_infected_{initial_infected}.txt'
        self.num_interactions = 0 # Int
        self.curr_step = 0 # Int
        self.logger = Logger(self.file_name)
        self.logger.write_metadata(pop_size, num_vaccinated, virus.name, mortality_rate, virus.repro_rate)

        self.run()

    def _create_population(self):
        population = []

        # instantiate & append infected people to population list
        for num_infected in range(self.initial_infected):
            self.next_person_id += 1
            self.total_infected += 1
            infected = Person(_id=self.next_person_id, is_vaccinated=False, infection=virus)
            population.append(infected)
            self.newly_infected.append(infected)

        # instantiate & append people to population list
        for num_vaccinated in range(self.num_vaccinated):
            self.next_person_id += 1
            population.append(Person(self.next_person_id, True))

        # instantiate & append unvaccinated & uninfected people to population list
        for num_unvaccinated in range(self.pop_size - self.initial_infected - self.num_vaccinated):
            self.next_person_id += 1
            population.append(Person(self.next_person_id, False))

        return population

    def should_continue(self):
        print("total infected", self.total_infected)
        if self.total_dead == self.pop_size or self.total_infected == 0:
            return False
        else:
            return True
        
    def time_step(self):
        
        pop_infected = []
        pop_uninfected = []

        self.curr_step += 1
        self.num_interactions = 0

        for person in self.population:
            if person.infection != None:
                pop_infected.append(person)
            else:
                pop_uninfected.append(person)

        for person in pop_infected:
            for interaction in range(100):
                # TODO: keep from interacting with same person more than once
                self.interaction(person, random.choice(pop_uninfected))

        print(f'newly_infected: {len(self.newly_infected)}')
        for person in self.newly_infected:
            if person.did_survive_infection():
                self.newly_infected.remove(person)
                self.num_vaccinated += 1
                self.total_infected -= 1
                self.logger.log_infection_survival(person=person._id, did_die_from_infection=False)
            else:
                print(f"person in self.population ==", person in self.population)
                if person not in self.population:
                    print(person, person._id, person.is_alive, person.is_vaccinated, person.infection)
                self.population.remove(person)
                self.newly_infected.remove(person)
                self.total_dead += 1
                self.total_infected -= 1
                self.logger.log_infection_survival(person=person._id, did_die_from_infection=True)

    def interaction(self, infected, uninfected):
        self.num_interactions += 1
        assert infected.is_alive == True
        assert uninfected.is_alive == True

        if uninfected.is_vaccinated == False and self.virus.repro_rate >= random.random():
            uninfected.infection = self.virus
            self.total_infected += 1
            self.newly_infected.append(uninfected)
            self.logger.log_interaction(infected=infected._id, uninfected=uninfected._id, did_infect=True)
        else:
            self.logger.log_interaction(infected=infected._id, uninfected=uninfected._id, did_infect=False)

    def run(self):
        self.curr_step = 0
        print(self.should_continue())
        while self.should_continue():
            self.time_step()
            print('Took a step')
            # self.logger.new_step(self.curr_step, self.num_interactions, len(self.num_vaccinated), len(self.total_infected), self.total_dead)
        self.num_interactions = 0

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
