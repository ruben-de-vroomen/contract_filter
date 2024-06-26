import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import pandas as pd
from ship import MyShip
from scipy.optimize import minimize

# info: this should return True if its possible...
def canal_check(vessel: MyShip, single_contract):
    panama = [0, 32.53, 12.6] # [length, width, depth]
    suez = [0, 77.5, 20]

    if vessel.get('width') < suez[1] and single_contract['Actual Draft'] < suez[2]:
        suez_check = True
    else:
        suez_check = False
        
    if vessel.get('width') < panama[1] and single_contract['Actual Draft'] < panama[2]:
        panama_check = True
    else:
        panama_check = False


    return suez_check, panama_check


def consumption(x, vessel, single_contract):
    adjusted_consumption = (((vessel.get('consumption')/24)*(x / vessel.get('design_speed'))**3 * (single_contract['Actual Draft'] / vessel.get('draft_max'))**(2/3)))
    return adjusted_consumption

def consumption_empty(x, vessel, single_contract):
    adjusted_consumption = (((vessel.get('consumption')/24)*(x / vessel.get('design_speed'))**3 * (vessel.get('draft_min') / vessel.get('draft_max'))**(2/3)))
    return adjusted_consumption

def optimize_total(x, vessel: MyShip, single_contract, OPEX):
    single_contract['Sailing Duration'] = single_contract['Voyage Distance'] / x
    
    # (total costs)
    adjusted_consumption = (((vessel.get('consumption')/24)*(x / vessel.get('design_speed'))**3 * (single_contract['Actual Draft'] / vessel.get('draft_max'))**(2/3)))[0]
    fuel_cost = adjusted_consumption * vessel.get('bunker_value') * single_contract['Sailing Duration']

    OPEX_total = (OPEX / (7 * 24) ) * single_contract['Sailing Duration']
    
    loss_total = fuel_cost + OPEX_total - single_contract['Total Value']

    return loss_total


def sailing_speed(vessel: MyShip, contracts, distances, OPEX):
    
    contracts = contracts.reset_index()  # make sure indexes pair with number of rows
    contracts['Voyage Distance'] = 0
    contracts['Canal Costs'] = 0
    contracts['Sailing Duration'] = 0 

    
    # panama_counter = 0
    # suez_counter = 0

    for idx, single_contract in contracts.iterrows():
        port_distances = distances
        port_distances = port_distances.reset_index()
        suez_check, panama_check = canal_check(vessel, single_contract)
        
        
        port_distances.loc[(port_distances['Start Port'] == single_contract['Start Port']) & (port_distances['End Port'] == single_contract['Destination']), 'Valid Voyage'] = True
        port_distances = port_distances.loc[port_distances['Valid Voyage'] == True]

        # print(f"hi: {port_distances['Canal Fee'].values[0]}") # debug statement

        if port_distances.shape[0] != 1: #! This should never occur....
            print('Woah wasn\'t expecting that!\nexiting with code 2')
            exit(2)

        

        if port_distances['Canal'].eq('No').any() == True:
            # print(f"{port_distances['Canal']}")
            contracts.at[idx, 'Canal Costs'] = port_distances['Canal Fee'].values[0] * vessel.get('GT')
            contracts.at[idx, 'Voyage Distance'] = port_distances['Distance Not Using Canal'].values[0]

        elif port_distances['Canal'].eq('Suez').any() == True and suez_check == True:
            contracts.at[idx, 'Canal Costs'] = port_distances['Canal Fee'].values[0] * vessel.get('GT')
            contracts.at[idx, 'Voyage Distance'] = port_distances['Distance Using Canal'].values[0]

        elif port_distances['Canal'].eq('Suez').any() == True and suez_check == False:
            # suez_counter += 1
            # print(single_contract['Actual Draft'])
            contracts.at[idx, 'Canal Costs'] = port_distances['Canal Fee'].values[0] * vessel.get('GT')
            contracts.at[idx, 'Voyage Distance'] = port_distances['Distance Not Using Canal'].values[0]

        elif port_distances['Canal'].eq('Panama').any() == True and panama_check == True:
            contracts.at[idx, 'Canal Costs'] = port_distances['Canal Fee'].values[0] * vessel.get('GT')
            contracts.at[idx, 'Voyage Distance'] = port_distances['Distance Using Canal'].values[0]

        elif port_distances['Canal'].eq('Panama').any() == True and panama_check == False:
            # panama_counter += 1
            contracts.at[idx, 'Canal Costs'] = port_distances['Canal Fee'].values[0] * vessel.get('GT')
            contracts.at[idx, 'Voyage Distance'] = port_distances['Distance Not Using Canal'].values[0]
        else:
            print('failed at the canal check...')
            exit(2)
        

    
    # voyage distance now found...
    contracts['Optimal Speed'] = 0
    contracts['Bunker Usage'] = 0
    contracts['Minimum Speed'] = 0
    

    contracts['Total Value'] = contracts['Rate'] * contracts['Weight'] * (1 - contracts['Commission'])

    bnds = [(1.0, vessel.get('design_speed'))]

    for idx, single_contract in contracts.iterrows():
        speed_optimal = minimize(optimize_total, args=(vessel, single_contract, OPEX), x0=10.0, bounds=bnds).x[0]

        contracts.at[idx, 'Optimal Speed'] = speed_optimal
        contracts.at[idx, 'Sailing Duration'] = contracts.at[idx, 'Voyage Distance'] / speed_optimal
        contracts.at[idx, 'Bunker Usage'] = consumption(speed_optimal, vessel, single_contract) * single_contract['Sailing Duration']

    
    contracts['Minimum Speed'] = contracts['Voyage Distance'] / (contracts['Duration']*7*24 - contracts['Load-Sail Time']) 
    contracts['Contract Time'] = contracts['Non-Sailing Time'] + contracts['Sailing Duration']

    contracts['Finish Week'] = (contracts['Contract Time'] / (24 * 7)) + contracts['Start Week']

    contracts['Fuel Costs'] = contracts['Bunker Usage'] * vessel.get('bunker_value')
    return contracts


