import pandas as pd
from ship import MyShip


def port_fee(vessel: MyShip, contracts, port_data):
    
    port_fee_dict = pd.Series(port_data['Port Tariff'].values,index=port_data['Name']).to_dict()

    contracts['Port Costs'] =  contracts['Destination'].map(port_fee_dict)*vessel.get('GT')
    
    return contracts

def ice_fee(vessel: MyShip, contracts, port_data):
    port_fee_dict = pd.Series(port_data['Port Tariff'].values,index=port_data['Name']).to_dict()    
    port_ice_dict = pd.Series(port_data['Ice Class Required'].values,index=port_data['Name']).to_dict()

    if vessel.get('ice_class') == True:
        contracts['Ice Fee'] = 0
        return contracts
    
    contracts['Ice Fee'] = contracts['Port Costs'] * 2

    
    return contracts