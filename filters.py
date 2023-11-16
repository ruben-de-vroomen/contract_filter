from ship import MyShip
import pandas as pd

def weight_filter(vessel: MyShip, contracts):
    cargo_weight = contracts['Weight']

    contracts_filter = contracts.loc[contracts['Weight'] < vessel.get('max_DWT')]

    return contracts_filter 


def volume_filter(vessel: MyShip, contracts, cargo_data):
    cargo_dict = pd.Series(cargo_data['Density'].values,index=cargo_data['Cargo Type']).to_dict()


    contracts['Density'] = contracts['Cargo'].map(cargo_dict)
        
    #todo: check the units of density tonnes/m^3 assumed now, also weight in tonnes
    contracts['Volume'] = contracts['Weight'] / contracts['Density']

    contracts_filter = contracts.loc[contracts['Volume'] < vessel.get('max_vol')]

    return  contracts_filter

def deck_strength_filter(vessel: MyShip, contracts, cargo_data):
    cargo_dict = pd.Series(cargo_data['Minimum Floor Strength'].values,index=cargo_data['Cargo Type']).to_dict()
    contracts['Floor Strength'] = contracts['Cargo'].map(cargo_dict)

    contracts_filter = contracts.loc[contracts['Floor Strength'] < vessel.get('plate_strength')]

    return contracts_filter

def draft_filter(vessel: MyShip, contracts, port_data):

    #todo: check bunker level is in tonnes
    #todo: check that this is true
    contracts['Total DWT'] = contracts['Weight'] + vessel.get('bunker_level')

    # first I need to calculate a draft for each contract
    
    draft_rate = ((vessel.get('draft_max') - vessel.get('draft_min'))/(vessel.get('max_DWT')))
    contracts['Actual Draft'] = draft_rate *  contracts['Total DWT'] + vessel.get('draft_min')


    port_dict = pd.Series(port_data['Port Limit'].values,index=port_data['Name']).to_dict()

    # next I need to check the departure ports for depth restriction
    # next I check the arrival port for depth restriction
    contracts['Departure Limit'] = contracts['Start Port'].map(port_dict)
    contracts['Arrival Limit'] = contracts['Destination'].map(port_dict)

    contracts_filter = contracts.loc[contracts['Actual Draft'] < contracts['Departure Limit']]
    contracts_filter = contracts.loc[contracts['Actual Draft'] < contracts['Arrival Limit']]
    

    


    return contracts_filter
