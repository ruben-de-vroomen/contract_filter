import pandas as pd
import numpy as numpy
from ship import MyShip
from filters import *
from finances import financials
import pathlib

#initialise here
handymax33 = MyShip('Handymax 33')
handymax32 = MyShip('Handymax 32')

handymax33.from_data(length=229.75, 
                    width=32.21, 
                    draft_full=12.6, 
                    draft_empty=3.28, 
                    plate_strength=20, 
                    max_DWT = 66_758, 
                    max_volume=46_417, 
                    OPEX = 1_874_828, 
                    design_speed = 14, 
                    bunker_level=1400,          # Adjust every round 
                    ice_class=True,             # must be True or False
                    crane_capacity=25,          # either 0 or 25
                    AIS_cost=100,               # either 0 or 100
                    consumption = 39.7,
                    consumption_hotel = 2.5,
                    bunker_value=269,            # needs to be updated continually
                    GT = 28_905,
                    holds=7,
                    )

handymax32.from_name(name='Handymax 32')



def main():
    #! defining your vessel here
    handymax32.update(bunker_value=270, bunker_level=1000, OPEX=2_000_000)
    vessel = handymax33
    week_no = 38

    my_loans = [] # <- your loans here [(200_000, 0.091),(Value, Rate), etc...]

    
    #! VV DONT TOUCH SHIT DOWN HERE VV

    # creatig the week folders
    variable_data = f'week{week_no}'
    variable_next = f'week{week_no + 1}'

    
    pathlib.Path(f'variable/{variable_next}').mkdir(parents=True, exist_ok=True) 


    # importing fixed data and contracts
    port_data = pd.read_csv(f'variable/{variable_data}/Port Data.csv', delimiter=';')
    distances = pd.read_csv('fixed_data/distances.csv', delimiter=';')
    cargo_data = pd.read_csv('fixed_data/cargo_data.csv', delimiter=';')
    
    voyage_charters = pd.read_csv(f'variable/{variable_data}/Voyage Charters.csv', delimiter=';')
    # time_charters = pd.read_csv(f'{variable_data}/Time Charters.csv', delimiter=';')
    # coa_charters = pd.read_csv(f'{variable_data}/Contracts Of Affreightment.csv', delimiter=';')

    contracts = voyage_charters.copy()

    contracts['Allowed'] = ''

    print(f'Total Number of Contracts: \t{contracts.shape[0]}')

    # Filters
    # weight filter
    contracts = weight_filter(vessel, contracts)
    print(f'After Weight Filter: \t\t{contracts.shape[0]}')

    # max volume filter
    contracts = volume_filter(vessel, contracts, cargo_data)
    print(f'After Volume Filter: \t\t{contracts.shape[0]}')
    
    # deck strength filter
    contracts = deck_strength_filter(vessel, contracts, cargo_data)
    print(f'After Deck Strength Filter: \t{contracts.shape[0]}')
    
    # maximum draft filter
    contracts = draft_filter(vessel, contracts, port_data)
    print(f'After Draft Filter: \t\t{contracts.shape[0]}')
    
    # ice-class filter
    contracts = ice_class_filter(vessel, contracts, port_data)
    print(f'After Ice-Class Filter: \t{contracts.shape[0]}')

    # crane filter
    contracts = crane_filter(vessel, contracts, port_data)
    print(f'After Crane Filter: \t\t{contracts.shape[0]}')

    # filters for cargos and deck dimensions
    contracts = dimension_filter(vessel, contracts, cargo_data)
    print(f'After Dimension Filter: \t{contracts.shape[0]}')

    # contracts.to_csv('debug_filter.csv')

    #* Now we begin with some finances:
    contracts = financials(vessel, contracts, port_data, distances, my_loans)

    contracts = contracts.sort_values(['Allowed','Profit'], ascending=[True, False])

    concat = contracts[['Allowed','Start Port', 'Start Week', 'Destination', 'Duration', 'Voyage Distance', 'Cargo','Weight', 'Currency','Rate', 'Break Even Rate', 'Profit','Total Value', 'Total Cost', 'Port Costs', 'Fuel Costs', 'Fixed Costs', 'Canal Costs', 'Port Hours','Predicted Demurage','Minimum Speed', 'Optimal Speed', 'Sailing Duration', 'Non-Sailing Time', 'Bunker Usage', 'Actual Draft']]

    concat.to_csv(f'variable/{variable_data}/output.csv', float_format='%g')

    # print(concat.columns)

if __name__ == "__main__":
    main()