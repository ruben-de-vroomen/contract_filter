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