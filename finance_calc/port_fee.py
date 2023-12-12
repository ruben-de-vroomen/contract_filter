import pandas as pd
from ship import MyShip


def port_fee(vessel: MyShip, contracts, port_data):
    
    port_fee_dict = pd.Series(port_data['Port Tariff'].values,index=port_data['Name']).to_dict()

    contracts['Port Costs'] =  contracts['Destination'].map(port_fee_dict)*vessel.get('GT')
    
    return contracts

def ice_fee(vessel: MyShip, contracts, port_data):

    if vessel.get('ice_class') == True:
        contracts['Ice Fee'] = 0
        return contracts
    
    # basically determines based on previous filter if the ice costs are 0 or non-zero
    contracts.loc[contracts['Departure Ice'] == True, 'Ice Factor Departure'] = 1
    contracts.loc[contracts['Departure Ice'] != True, 'Ice Factor Departure'] = 0

    contracts.loc[contracts['Arrival Ice'] == True, 'Ice Factor Arrival'] = 1
    contracts.loc[contracts['Arrival Ice'] != True, 'Ice Factor Arrival'] = 0


    contracts['Ice Fee'] = contracts['Ice Factor Arrival'] * contracts['Port Costs'] * 2

    
    return contracts