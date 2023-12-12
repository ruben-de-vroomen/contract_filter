import pandas as pd
from ship import MyShip
import numpy as np
from finance_calc.sailing import consumption, canal_check


def stint(vessel: MyShip, contracts, port_data, distances):

    port_fee_dict = pd.Series(port_data['Port Tariff'].values,index=port_data['Name']).to_dict()

    #! check for port existance
    if port_data['Name'].eq(vessel.get('current_port')).any() == False:
        print('\nPort Not Found, did you spell it correctly?')
        print('exiting with error code 1')
        exit(1)

    contracts['Current Port'] = vessel.get('current_port')
    contracts['Layover Distance'] = 0


    contracts = contracts.reset_index()

    for idx, single_contract in contracts.iterrows():
        layover_distances = distances
        layover_distances = layover_distances.reset_index()
        suez_check, panama_check = canal_check(vessel, single_contract)

        layover_distances.loc[(layover_distances['Start Port'] == single_contract['Current Port']) & (layover_distances['End Port'] == single_contract['Start Port']), 'Valid Layover'] = True
        layover_distances = distances.loc[layover_distances['Valid Layover'] == True]

        
        
        if layover_distances.shape[0] != 1: #! This should never occur....
            print('Woah wasn\'t expecting that!\nexiting with code 2')
            exit(2)

        

        if layover_distances['Canal'].eq('No').any() == True:
            # print(f"{layover_distances['Canal']}")
            contracts.at[idx, 'Layover Canal Costs'] = layover_distances['Canal Fee'].values[0] * vessel.get('GT')
            contracts.at[idx, 'Layover Distance'] = layover_distances['Distance Not Using Canal'].values[0]

        elif layover_distances['Canal'].eq('Suez').any() == True and suez_check == True:
            contracts.at[idx, 'Layover Canal Costs'] = layover_distances['Canal Fee'].values[0] * vessel.get('GT')
            contracts.at[idx, 'Layover Distance'] = layover_distances['Distance Using Canal'].values[0]

        elif layover_distances['Canal'].eq('Suez').any() == True and suez_check == False:
            # suez_counter += 1
            # print(single_contract['Actual Draft'])
            contracts.at[idx, 'Layover Canal Costs'] = layover_distances['Canal Fee'].values[0] * vessel.get('GT')
            contracts.at[idx, 'Layover Distance'] = layover_distances['Distance Not Using Canal'].values[0]

        elif layover_distances['Canal'].eq('Panama').any() == True and panama_check == True:
            contracts.at[idx, 'Layover Canal Costs'] = layover_distances['Canal Fee'].values[0] * vessel.get('GT')
            contracts.at[idx, 'Layover Distance'] = layover_distances['Distance Using Canal'].values[0]

        elif layover_distances['Canal'].eq('Panama').any() == True and panama_check == False:
            # panama_counter += 1
            contracts.at[idx, 'Layover Canal Costs'] = layover_distances['Canal Fee'].values[0] * vessel.get('GT')
            contracts.at[idx, 'Layover Distance'] = layover_distances['Distance Not Using Canal'].values[0]
        else:
            print('failed at the canal check...')
            exit(2)



    # get layover time available in hours (approximated due to week innacuracies)
    contracts.loc[contracts['Current Week'] - contracts['Start Week'] < 0, 'Layover Time'] = (contracts['Start Week'] - contracts['Current Week'])*7*24 - contracts['Departure Wait Time']
    contracts.loc[contracts['Current Week'] - contracts['Start Week'] >= 0, 'Layover Time'] = pd.NA

    contracts['Layover Speed'] = contracts['Layover Distance'] / (contracts['Layover Time'])


    contracts['Layover Port Costs'] = contracts['Start Port'].map(port_fee_dict)*vessel.get('GT')

    if vessel.get('ice_class') == False:
        contracts['Layover Ice Costs'] = contracts['Layover Port Costs'] * 2
    else:
        contracts['Layover Ice Costs'] = contracts['Layover Port Costs'] * 2
    #contracts['Layover Costs'] = contracts['Layover Canal Costs'] + contracts['Layover Port Costs'] + contracts['Layover Ice Costs']
    

    for idx, single_contract in contracts.iterrows():
        contracts.at[idx, 'Layover Bunker Usage'] = consumption(single_contract['Layover Speed'], vessel, single_contract) * single_contract['Layover Time']

    contracts['Layover Fuel Costs'] = contracts['Layover Bunker Usage'] * vessel.get('bunker_value')

    return contracts

