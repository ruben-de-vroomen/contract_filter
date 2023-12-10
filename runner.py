import pandas as pd
import numpy as numpy
from ship import MyShip
from filters import *
from finances import financials
import pathlib



def runner(vessel: MyShip, week_no, my_loans, testing_mode=False, layover_start_week=0):

    #! VV DONT TOUCH SHIT DOWN HERE VV
    print(f"working on vessel :\t\t{vessel.get('name')}")


    # creatig the week folders
    variable_data = f'week{week_no}'
    variable_next = f'week{week_no + 1}'

    if layover_start_week == 0:
        layover_start_week = week_no



    
    pathlib.Path(f'variable/{variable_next}').mkdir(parents=True, exist_ok=True) 


    # importing fixed data and contracts
    port_data = pd.read_csv(f'variable/{variable_data}/Port Data.csv', delimiter=';')
    distances = pd.read_csv('fixed_data/distances.csv', delimiter=';')
    cargo_data = pd.read_csv('fixed_data/cargo_data.csv', delimiter=';')


    if testing_mode == True:
        charters = pd.read_csv(f'fixed_data/charters.csv', delimiter=';')
        voyage_charters = charters.loc[charters['Type'] == 'Voyage Charter']
        voyage_charters = voyage_charters.drop(columns=['Type'])
    else:
        voyage_charters = pd.read_csv(f'variable/{variable_data}/Voyage Charters.csv', delimiter=';')


    # time_charters = pd.read_csv(f'{variable_data}/Time Charters.csv', delimiter=';')
    # coa_charters = pd.read_csv(f'{variable_data}/Contracts Of Affreightment.csv', delimiter=';')

    contracts = voyage_charters.copy()

    contracts['Current Week'] = layover_start_week

    contracts['Allowed'] = ''

    # Filters
    # weight filter
    contracts = weight_filter(vessel, contracts)
    # print(f'After Weight Filter: \t\t{contracts.shape[0]}')

    # max volume filter
    contracts = volume_filter(vessel, contracts, cargo_data)
    # print(f'After Volume Filter: \t\t{contracts.shape[0]}')
    
    # deck strength filter
    contracts = deck_strength_filter(vessel, contracts, cargo_data)
    # print(f'After Deck Strength Filter: \t{contracts.shape[0]}')
    
    # maximum draft filter
    contracts = draft_filter(vessel, contracts, port_data)
    # print(f'After Draft Filter: \t\t{contracts.shape[0]}')
    
    # ice-class filter
    contracts = ice_class_filter(vessel, contracts, port_data)
    # print(f'After Ice-Class Filter: \t{contracts.shape[0]}')

    # crane filter
    contracts = crane_filter(vessel, contracts, port_data)
    # print(f'After Crane Filter: \t\t{contracts.shape[0]}')

    # filters for cargos and deck dimensions
    contracts = dimension_filter(vessel, contracts, cargo_data)
    # print(f'After Dimension Filter: \t{contracts.shape[0]}')

    # contracts.to_csv('debug_filter.csv')

    #* Now we begin with some finances:
    contracts = financials(vessel, contracts, port_data, distances, my_loans)

    contracts = contracts.sort_values(['Allowed','Layover Included Profit'], ascending=[True, False])

    concat = contracts[['Allowed','Start Port', 'Start Week', 'Destination', 'Duration', 'Voyage Distance', 'Cargo', 'Weight', 'Currency','Rate', 'Break Even Rate', 'Layover Break Even', 'Profit','Layover Included Profit','Total Value', 'Total Cost', 'Port Costs', 'Fuel Costs', 'Fixed Costs', 'Canal Costs', 'Port Hours','Predicted Demurage','Minimum Speed', 'Optimal Speed', 'Sailing Duration', 'Non-Sailing Time', 'Bunker Usage', 'Actual Draft', 'Layover Speed', 'Layover Costs', 'Layover Bunker Usage']]

    
    print(f"Available Contracts: \t\t{contracts[contracts['Allowed'] == ''].shape[0]}")
    
    concat.to_csv(f"variable/{variable_data}/output_{vessel.get('name')}.csv", float_format='%g')

    print('done!\n')