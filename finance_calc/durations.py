import pandas as pd
from ship import MyShip

def duration(vessel: MyShip, contracts, port_data):
    #* ALL DURATION CALCULATIONS TO BE DONE IN HOURS
    #TODO SSHINC not included
    # Waiting times

    sshinc_dict = {True: 1, False: 5/7}
    contracts['SSHINC Factor'] = contracts['SSHINC'].map(sshinc_dict)

    
    port_dict_waiting = pd.Series(port_data['Waiting Time'].values*24,index=port_data['Name']).to_dict()
    
    contracts['Departure Wait Time'] = 0
    contracts['Arrival Wait Time'] = contracts['Destination'].map(port_dict_waiting)

    # loading time
    contracts.loc[contracts['Loading Rate'] >= vessel.get('crane_capacity'), 'Loading Time'] = (contracts['Weight'] / (vessel.get('holds') * contracts['Loading Rate']))/contracts['SSHINC Factor']
    contracts.loc[contracts['Loading Rate'] < vessel.get('crane_capacity'), 'Loading Time'] = (contracts['Weight'] / (vessel.get('holds') *vessel.get('crane_capacity')))/contracts['SSHINC Factor']
    
     
    # unloading time
    contracts.loc[contracts['Unloading Rate'] >= vessel.get('crane_capacity'), 'Unloading Time'] = (contracts['Weight'] / (vessel.get('holds') *contracts['Unloading Rate']))/contracts['SSHINC Factor']
    contracts.loc[contracts['Unloading Rate'] < vessel.get('crane_capacity'), 'Unloading Time'] = (contracts['Weight'] / (vessel.get('holds') *vessel.get('crane_capacity')))/contracts['SSHINC Factor']

    contracts['Non-Sailing Time'] = contracts['Arrival Wait Time'] + contracts['Departure Wait Time'] + contracts['Loading Time'] + contracts['Unloading Time']
    contracts['Load-Sail Time'] = contracts['Arrival Wait Time'] + contracts['Departure Wait Time'] + contracts['Loading Time']
    


    return contracts
