from ship import MyShip
import pandas as pd
from finance_calc.durations import duration
from finance_calc.sailing import sailing_speed
from finance_calc.port_fee import port_fee
from finance_calc.port_fee import ice_fee
from finance_calc.demurage import demurage
from finance_calc.stint import stint

def financials(vessel: MyShip, contracts, port_data, port_distances, loans):
    
    # determine the weekly fixed costs
    fixed_costs = vessel.get('OPEX') / 52 + vessel.get('AIS') + vessel.get('hotel')* 7 * vessel.get('bunker_value')

    #* CAPEX costs?
    # capital_costs = 
    
    if loans != []:
        for loan in loans:
            weekly_interest = (loan[0] * loan[1]) / 52
            fixed_costs += weekly_interest
            

    contracts = duration(vessel, contracts, port_data)
    contracts = sailing_speed(vessel, contracts, port_distances, fixed_costs)
    contracts = port_fee(vessel, contracts, port_data)
    contracts = ice_fee(vessel, contracts, port_data)
    contracts = demurage(vessel, contracts)
    contracts = stint(vessel, contracts, port_data, port_distances)
    

    #TODO Check total cost assumption
    contracts['Fixed Costs'] = (fixed_costs / (7*24)) * contracts['Contract Time']
    contracts['Total Cost'] = contracts['Fuel Costs'] + contracts['Port Costs'] + contracts['Canal Costs'] + contracts['Fixed Costs'] + contracts['Ice Fee']

    contracts['Break Even Rate'] = (contracts['Total Cost'] - contracts['Predicted Demurage']) / contracts['Weight']
    contracts['Profit'] = contracts['Total Value'] + contracts['Predicted Demurage'] - contracts['Total Cost']
    

    contracts['Layover Costs'] = contracts['Layover Canal Costs'] + contracts['Layover Port Costs'] + ((fixed_costs / (7*24)) * contracts['Layover Time']) + contracts['Layover Fuel Costs'] + contracts['Layover Ice Costs']

    contracts['Layover Included Profit'] = contracts['Total Value'] + contracts['Predicted Demurage'] - contracts['Total Cost'] - contracts['Layover Costs']
    contracts['Layover Break Even'] = (contracts['Total Cost'] - contracts['Predicted Demurage'] + contracts['Layover Costs']) / contracts['Weight']
    return contracts

