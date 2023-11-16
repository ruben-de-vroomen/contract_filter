import pandas as pd
import numpy as numpy
from ship import MyShip
from filters import *



def main():
    #! defining your vessel here
    #todo: is vessel volume a given parameter?
    vessel = MyShip(length=100, width=40, draft_full=18, draft_empty=4, plate_strength=15, max_DWT = 80000, max_volume=100000, OPEX = 1300000, design_speed = 14, bunker_level=1400, ice_class=False)


    #! importing fixed data and contracts
    port_data = pd.read_csv('fixed_data/port_data.csv', delimiter=';')
    distances = pd.read_csv('fixed_data/distances.csv', delimiter=';')
    cargo_data = pd.read_csv('fixed_data/cargo_data.csv', delimiter=';')
    contracts = pd.read_csv('contracts.csv', delimiter=';')

    print(f'Total Number of Contracts: \t{contracts.shape[0]}')

    #! Filters
    # weight filter
    contracts = weight_filter(vessel, contracts)
    print(f'After Weight Filter: \t\t{contracts.shape[0]}')

    contracts = volume_filter(vessel, contracts, cargo_data)
    print(f'After Volume Filter: \t\t{contracts.shape[0]}')
    
    contracts = deck_strength_filter(vessel, contracts, cargo_data)
    print(f'After Deck Strength Filter: \t{contracts.shape[0]}')
    
    contracts = draft_filter(vessel, contracts, port_data)
    print(f'After Draft Filter: \t\t{contracts.shape[0]}')
    
    contracts = ice_class_filter(vessel, contracts, port_data)
    print(f'After Ice-Class Filter: \t{contracts.shape[0]}')



if __name__ == "__main__":
    main()