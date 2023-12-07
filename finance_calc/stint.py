import pandas as pd
from ship import MyShip
from finance_calc.sailing import consumption, canal_check


def stint(vessel: MyShip, contracts, port_data):

    #! check for port existance
    if port_data['Name'].eq(vessel.get('current_port')).any() == False:
        print('\nPort Not Found, did you spell it correctly?')
        print('exiting with error code 1')
        exit(1)

    

    return contracts

