import pandas as pd
import numpy as numpy
from ship import MyShip
from filters import *
from finances import financials



def main():
    #! defining your vessel here
    vessel = MyShip(length=100, 
                    width=40, 
                    draft_full=18, 
                    draft_empty=4, 
                    plate_strength=15, 
                    max_DWT = 80000, 
                    max_volume=100000, 
                    OPEX = 2_200_000, 
                    design_speed = 14, 
                    bunker_level=1400, 
                    ice_class=False,            # must be True or False
                    crane_capacity=0,           # either 0 or 25
                    AIS_cost=100,               # either 0 or 100
                    consumption = 50,
                    consumption_hotel = 2,
                    bunker_value=300,            # needs to be updated continually
                    GT = 28905,
                    holds=7,
                    )


    my_loans = [(500_000, 0.091),(100_000, 0.051),] # <- your loans here

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

    contracts = crane_filter(vessel, contracts, port_data)
    print(f'After Crane Filter: \t\t{contracts.shape[0]}')


    #* Now we begin with some finances:
    contracts = financials(vessel, contracts, port_data, distances, my_loans)

    contracts = contracts.sort_values('Profit', ascending=False)

    contracts.to_csv('output.csv')


if __name__ == "__main__":
    main()