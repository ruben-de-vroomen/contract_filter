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

    variable_data = 'variable/week1'

    #! importing fixed data and contracts
    port_data = pd.read_csv(f'{variable_data}/Port Data.csv', delimiter=';')
    distances = pd.read_csv('fixed_data/distances.csv', delimiter=';')
    cargo_data = pd.read_csv('fixed_data/cargo_data.csv', delimiter=';')
    
    voyage_charters = pd.read_csv(f'{variable_data}/Voyage Charters.csv', delimiter=';')
    # time_charters = pd.read_csv(f'{variable_data}/Time Charters.csv', delimiter=';')
    # coa_charters = pd.read_csv(f'{variable_data}/Contracts Of Affreightment.csv', delimiter=';')

    contracts = voyage_charters

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

    concat = contracts[['Start Port', 'Start Week', 'Destination', 'Duration', 'Voyage Distance', 'Cargo','Weight', 'Currency','Rate', 'Break Even Rate', 'Profit','Total Value', 'Total Cost', 'Port Costs', 'Fuel Costs', 'Canal Costs', 'Minimum Speed', 'Optimal Speed', 'Sailing Duration', 'Non-Sailing Time']]

    concat.to_csv('output.csv')

    # print(concat.columns)

if __name__ == "__main__":
    main()