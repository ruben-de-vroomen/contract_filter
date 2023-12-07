import pandas as pd
from ship import MyShip


def demurage(vessel: MyShip, contracts):
    
    contracts['Port Hours'] = contracts['Port Days'] * 24

    # Demurage = (difference in hours) * (demurage per hour)
    contracts.loc[contracts['Port Hours'] - contracts['Non-Sailing Time'] < 0, 'Predicted Demurage'] = (contracts['Non-Sailing Time'] - contracts['Port Hours']) * (contracts['Demurage']/24) / contracts['SSHINC Factor']
    contracts.loc[contracts['Port Hours'] - contracts['Non-Sailing Time'] >= 0, 'Predicted Demurage'] = 0



    return contracts
