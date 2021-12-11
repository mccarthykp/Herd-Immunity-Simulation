class Logger(object):
    ''' Utility class responsible for logging all interactions during the simulation. '''

    def __init__(self, file_name):
        self.file_name = file_name

    def write_metadata(self, pop_size, vaccinated, virus_name, mortality_rate, repro_rate):
        '''
        The simulation class should use this method immediately to log the specific
        parameters of the simulation as the first line of the file.
        '''
        # TODO: Finish this method. This line of metadata should be tab-delimited
        # it should create the text file that we will store all logs in.
        # TIP: Use 'w' mode when you open the file. For all other methods, use
        # the 'a' mode to append a new log to the end, since 'w' overwrites the file.
        # NOTE: Make sure to end every line with a '/n' character to ensure that each
        # event logged ends up on a separate line!

        file_object = open(self.file_name, 'w')

        file_object.write(f'Population Size: {pop_size}\tNum_Vaccinated: {vaccinated}\tVirus: {virus_name}\tMortality Rate: {mortality_rate}\tReproduction Rate: {repro_rate}\n')

        file_object.close()

    def log_interaction(self, infected, uninfected, did_infect):
        '''
        The Simulation object should use this method to log every interaction
        a sick person has during each time step.

        The format of the log should be: "{person.ID} infects {random_person.ID} \n"
        '''

        # TODO: Finish this method. Think about how the booleans passed (or not passed)
        # represent all the possible edge cases. Use the values passed along with each person,
        # along with whether they are sick or vaccinated when they interact to determine
        # exactly what happened in the interaction and create a String, and write to your logfile.
        if did_infect == True:
            interaction = f'{infected} infects {uninfected}\n'
        else:
            interaction = f'{infected} did not infect {uninfected}\n'

        file_object = open(self.file_name, 'a')
        
        file_object.write(interaction)

        file_object.close()

    def log_infection_survival(self, person, did_die_from_infection):
        ''' The Simulation object uses this method to log the results of every
        call of a Person object's .resolve_infection() method.

        The format of the log should be:
            "{person.ID} died from infection\n" or "{person.ID} survived infection.\n"
        '''
        # TODO: Finish this method. If the person survives, did_die_from_infection
        # should be False.  Otherwise, did_die_from_infection should be True.
        # Append the results of the infection to the logfile
        if did_die_from_infection == True:
            survival = f'{person} died from infection.\n'
        else:
            survival = f'{person} survived infection.\n'

        file_object = open(self.file_name, 'a')
        
        file_object.write(survival)

        file_object.close()

    def new_step(self, curr_step, new_infections, new_deaths, living_population, total_dead, total_vaccinated):
        file_object = open(self.file_name, 'a')

        file_object.write(f'Current Step: {curr_step}\tNew Infections: {new_infections}\tNew Deaths: {new_deaths}\tLiving Population: {living_population}\tTotal Dead: {total_dead}\tTotal Vaccinated: {total_vaccinated}\n')

        file_object.close()

    def final_step(self, curr_step, total_living, total_dead, num_vaccinations, cause_of_end, total_interactions, num_interactions_vax, num_interactions_death):
        file_object = open(self.file_name, 'a')

        file_object.write(f'Current Step: {curr_step}\Total Living: {total_living}\tTotal Deaths: {total_dead}\tNum Vaccinations:  {num_vaccinations}\tCause of Simulation End: {cause_of_end}\tTotal Interactions: {total_interactions}\t"Num Interactions Resulting in Vaccination: {num_interactions_vax}"\t"Num Interactions Resulting in Death: {num_interactions_death}"\n')

        file_object.close()
