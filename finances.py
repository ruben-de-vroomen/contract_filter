from ship import MyShip
import pandas as pd

def duration(vessel: MyShip, contracts, port_data):
    #* ALL DURATION CALCULATIONS TO BE DONE IN HOURS
    
    # Waiting times
    port_dict_waiting = pd.Series(port_data['Waiting Time'].values*24,index=port_data['Name']).to_dict()
    
    contracts['Departure Wait Time'] = contracts['Start Port'].map(port_dict_waiting)
    contracts['Arrival Wait Time'] = contracts['Destination'].map(port_dict_waiting)

    # loading time
    contracts.loc[contracts['Loading Rate'] >= vessel.get('crane_capacity'), 'Loading Time'] = contracts['Weight'] / contracts['Loading Rate']
    contracts.loc[contracts['Loading Rate'] < vessel.get('crane_capacity'), 'Loading Time'] = contracts['Weight'] / vessel.get('crane_capacity')
    print(contracts)
    # contracts['Loading Time'] = 

    # unloading time
    
    
    return contracts #! warning!

def financials(vessel: MyShip, contracts, port_data, loans):
    
    # determine the weekly fixed costs
    fixed_costs = vessel.get('OPEX') / 52 + vessel.get('AIS')
    
    if loans != []:
        for loan in loans:
            weekly_interest = (loan[0] * loan[1]) / 52
            fixed_costs += weekly_interest

    duration(vessel, contracts, port_data)

    '''
        Plan of Action:
        1. Need to determine loading and unloading times, so that a maximum sailing time can be determined
            1.a. Also determine any port waiting times, canal waiting times?
            1.b. Cranes on board the ship?
            1.c. Use port distances, select canal or other route in necessary
            1.d. Canal fees and Port fees can be determined #todo are these variable?
        2. With maximum sailing time, determine a minimum sailing speed, to bound the speed optimization
        3. Given the contract, optimize for the sailing speed
        4. Calculate the fuel costs used by the trip #? what is the fuel cost? given?
        5. Ice breaker-costs, loading unloading costs...?
        6. Determine the break even going rate given the costs
        7. How profitable? compare with given rate
        8. Sort on profitability (largest difference posted rate and break even rate?)
    '''


    return contracts #!placeholder!!!


