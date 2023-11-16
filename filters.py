from ship import MyShip
import pandas as pd

def weight_filter(vessel: MyShip, contracts):
    cargo_weight = contracts['Weight']

    contracts_filter = contracts.loc[contracts['Weight'] < vessel.max_DWT]

    return contracts_filter 


def volume_filter(vessel: MyShip, contracts, cargo_data):

    # print(cargo_data)

    cargo_dict = pd.Series(cargo_data['Density'].values,index=cargo_data['Cargo Type']).to_dict()
    print(cargo_dict)
    
    contracts['Density'] = 0
    
    for index, row in contracts.iterrows():
        row['Density'] = cargo_dict[row['Cargo Type']]
        
    print(contracts['Density'])

    return  contracts_filter

def deck_strength(vessel: MyShip, contracts, cargo_data):
    
    cargo_dict = pd.Series(cargo_data['Minimum Floor Strength'].values,index=cargo_data['Cargo Type']).to_dict()
    print(cargo_dict)
    
    contracts.insert(-1, 'Minimum Floor Strength')

    for index, row in contracts.iterrows():
        continue
    
    return contracts_filter