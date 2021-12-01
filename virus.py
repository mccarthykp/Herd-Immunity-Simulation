# virus class
class Virus(object):
    ''' Properties and attributes of the virus used in Simulation. '''

    def __init__(self, name, repro_rate, mortality_rate):
        self.name = name
        self.repro_rate = repro_rate
        self.mortality_rate = mortality_rate

# -~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-
# Testing virus class

def test_virus_instantiation():
    #TODO: Create your own test that models the virus you are working with
    ''' Check to make sure that the virus instantiator is working. '''
    virus = Virus('HIV', 0.35, 0.8)
    assert virus.name == 'HIV'
    assert virus.repro_rate == 0.35
    assert virus.mortality_rate == 0.8

    my_virus = Virus('Ebola', 0.25, 0.7)
    assert my_virus.name == 'Ebola'
    assert my_virus.repro_rate == 0.25
    assert my_virus.mortality_rate == 0.7

if __name__ == '__main__':
    test_virus_instantiation()