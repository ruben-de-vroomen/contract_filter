import pandas as pd
from ship import MyShip

def duration(vessel: MyShip, contracts, port_data):
    #* ALL DURATION CALCULATIONS TO BE DONE IN HOURS
    
    # Waiting times
    port_dict_waiting = pd.Series(port_data['Waiting Time'].values*24,index=port_data['Name']).to_dict()
    
    contracts['Departure Wait Time'] = contracts['Start Port'].map(port_dict_waiting)
    contracts['Arrival Wait Time'] = contracts['Destination'].map(port_dict_waiting)

    # loading time
    contracts.loc[contracts['Loading Rate'] >= vessel.get('crane_capacity'), 'Loading Time'] = contracts['Weight'] / contracts['Loading Rate']
    contracts.loc[contracts['Loading Rate'] < vessel.get('crane_capacity'), 'Loading Time'] = contracts['Weight'] / vessel.get('crane_capacity')

    # unloading time
    contracts.loc[contracts['Unloading Rate'] >= vessel.get('crane_capacity'), 'Unloading Time'] = contracts['Weight'] / contracts['Unloading Rate']
    contracts.loc[contracts['Unloading Rate'] < vessel.get('crane_capacity'), 'Unloading Time'] = contracts['Weight'] / vessel.get('crane_capacity')


    return contracts
