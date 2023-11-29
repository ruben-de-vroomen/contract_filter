from ship import MyShip
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

def weight_filter(vessel: MyShip, contracts):

    contracts.loc[contracts['Weight'] > (vessel.get('max_DWT') - vessel.get('bunker_level'))*1.1, 'Allowed'] = 'Weight'

    return contracts


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

    # print(contracts['Floor Strength'])

    contracts_filter = contracts.loc[contracts['Floor Strength'] <= vessel.get('plate_strength')]

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

    contracts = contracts.loc[contracts['Actual Draft'] < contracts['Departure Limit']]
    contracts_filter = contracts.loc[contracts['Actual Draft'] < contracts['Arrival Limit']]

    return contracts_filter



def ice_class_filter(vessel: MyShip, contracts, port_data):

    if vessel.get('ice_class') == True:
        return contracts

    port_dict = pd.Series(port_data['Ice Class Required'].values,index=port_data['Name']).to_dict()
    
    contracts['Departure Ice'] = contracts['Start Port'].map(port_dict)
    contracts['Arrival Ice'] = contracts['Destination'].map(port_dict)

    contracts = contracts.loc[contracts['Departure Ice'] == False]
    contracts_filter = contracts.loc[contracts['Arrival Ice'] == False]

    return contracts_filter


def crane_filter(vessel: MyShip, contracts, port_data):

    port_dict_loading = pd.Series(port_data['Loading Capacity'].values,index=port_data['Name']).to_dict()
    port_dict_unloading = pd.Series(port_data['Unloading Capacity'].values,index=port_data['Name']).to_dict()


    contracts['Loading Rate'] = contracts['Start Port'].map(port_dict_loading)
    contracts['Unloading Rate'] = contracts['Destination'].map(port_dict_unloading)


    if vessel.get('crane_capacity') > 0:
        return contracts
    else:
        contracts = contracts.loc[contracts['Loading Rate'] > 1]
        contracts_filter = contracts.loc[contracts['Unloading Rate'] > 1]


    return contracts_filter


# todo fix these filters
def dimension_filter(vessel: MyShip, contracts, cargo_data):
    cargo_width_dict = pd.Series(cargo_data['Cargo Width'].values,index=cargo_data['Cargo Type']).to_dict()
    cargo_length_dict = pd.Series(cargo_data['Cargo Length'].values,index=cargo_data['Cargo Type']).to_dict()
    cargo_deck_filter = pd.Series(cargo_data['Transport on Deck'].values,index=cargo_data['Cargo Type']).to_dict()

    contracts['Deck'] = contracts['Cargo'].map(cargo_deck_filter)
    contracts['Cargo Length'] = contracts['Cargo'].map(cargo_length_dict)
    contracts['Cargo Width'] = contracts['Cargo'].map(cargo_width_dict)

    contracts = contracts.loc[((contracts['Deck'] == True) & (vessel.get('width')*0.75 > contracts['Cargo Width']) & (vessel.get('length')*0.75 > contracts['Cargo Length'])) | (contracts['Deck'] == False)]

    # print(contracts)
    
    return contracts