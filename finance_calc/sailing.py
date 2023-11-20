import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import pandas as pd
from ship import MyShip
from scipy.optimize import minimize

# todo finish this
def canal_check(vessel: MyShip, single_contract):
    panama = [0, 32.53, 12.6] # [length, width, depth]
    suez = [0, 77.5, 20]

    if vessel.get('width') > suez[1] and single_contract['Actual Draft'] < suez[2]:
        suez_check = True
    else:
        suez_check = False
        
    if vessel.get('width') > panama[1] and single_contract['Actual Draft'] < panama[2]:
        panama_check = True
    else:
        panama_check = False


    return suez_check, panama_check

# def optimize_hourly(x, vessel: MyShip, single_contract, OPEX):

#     adjusted_consumption = (((vessel.get('consumption')/24)*(x / vessel.get('design_speed'))**3 * (single_contract['Actual Draft'] / vessel.get('draft_max'))**(2/3)))[0]

#     fuel_cost = adjusted_consumption * vessel.get('bunker_value') #* (single_contract['Voyage Distance'] / x)

#     OPEX_hour = OPEX / (7 * 24) + vessel.get('hotel') / 24 * vessel.get('bunker_value')


#     single_contract['Sailing Duration'] = single_contract['Voyage Distance'] / x + single_contract['Non-Sailing Time']

#     loss_hour = -(single_contract['Total Value'] / single_contract['Sailing Duration']) + OPEX_hour + fuel_cost

#     return loss_hour

def consumption(x, vessel, single_contract):
    adjusted_consumption = (((vessel.get('consumption')/24)*(x / vessel.get('design_speed'))**3 * (single_contract['Actual Draft'] / vessel.get('draft_max'))**(2/3)))
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

    
    for idx, single_contract in contracts.iterrows():
        port_distances = distances
        port_distances = port_distances.reset_index()
        suez_check, panama_check = canal_check(vessel, single_contract)
        
        
        port_distances.loc[(port_distances['Start Port'] == single_contract['Start Port']) & (port_distances['End Port'] == single_contract['Destination']), 'Valid Voyage'] = True
        port_distances = port_distances.loc[port_distances['Valid Voyage'] == True]

        if port_distances.shape[0] > 1 and panama_check == True or suez_check == True: #! THIS FUNCTION HAS NOT BEEN CALLED, OR TESTED
            contracts.at[idx, 'Canal Costs'] = port_distances['Canal Fee'] * vessel.get('GT')
            contracts.at[idx, 'Voyage Distance'] = min(port_distances.at[0,'Distance Using Canal'], port_distances.at[1,'Distance Using Canal'])
            print(port_distances)
            
        else:
            contracts.at[idx, 'Voyage Distance'] = port_distances['Distance Not Using Canal']

    
    # voyage distance now found...
    contracts['Optimal Speed'] = 0
    contracts['Bunker Usage'] = 0
    contracts['Minimum Speed'] = 0
    

    contracts['Total Value'] = contracts['Rate'] * contracts['Weight'] * (1 - contracts['Signing Fee'])

    bnds = [(1.0, vessel.get('design_speed'))]

    for idx, single_contract in contracts.iterrows():
        speed_optimal = minimize(optimize_total, args=(vessel, single_contract, OPEX), x0=10.0, bounds=bnds).x[0]

        contracts.at[idx, 'Optimal Speed'] = speed_optimal
        contracts.at[idx, 'Sailing Duration'] = contracts.at[idx, 'Voyage Distance'] / speed_optimal
        contracts.at[idx, 'Bunker Usage'] = consumption(speed_optimal, vessel, single_contract) * single_contract['Sailing Duration']

    
    contracts['Minimum Speed'] = contracts['Voyage Distance'] / (contracts['Duration']*7*24 - contracts['Non-Sailing Time']) 
    

    contracts['Fuel Costs'] = contracts['Bunker Usage'] * vessel.get('bunker_value')
    return contracts


