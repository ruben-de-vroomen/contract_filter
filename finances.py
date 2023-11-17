from ship import MyShip
import pandas as pd
from finance_calc.durations import duration
from finance_calc.sailing import sailing_speed

def financials(vessel: MyShip, contracts, port_data, port_distances, loans):
    
    # determine the weekly fixed costs
    fixed_costs = vessel.get('OPEX') / 52 + vessel.get('AIS')
    
    if loans != []:
        for loan in loans:
            weekly_interest = (loan[0] * loan[1]) / 52
            fixed_costs += weekly_interest
            

    contracts = duration(vessel, contracts, port_data)
    contracts = sailing_speed(vessel, contracts, port_distances, fixed_costs)

     


    '''
        Plan of Action:
        1. Need to determine loading and unloading times, so that a maximum sailing time can be determined #* DONE
            1.a. Also determine any port waiting times, canal waiting times? #* DONE
            1.b. Cranes on board the ship? #*DONE
            1.c. Use port distances, select canal or other route in necessary #*DONE
            1.d. Canal fees and Port fees can be determined #todo are these variable?
        2. With maximum sailing time, determine a minimum sailing speed, to bound the speed optimization #TODO
        3. Given the contract, optimize for the sailing speed #*DONE
        4. Calculate the fuel costs used by the trip #? what is the fuel cost? given?
        5. Ice breaker-costs, loading unloading costs...?
        6. Determine the break even going rate given the costs
        7. How profitable? compare with given rate
        8. Sort on profitability (largest difference posted rate and break even rate?)
    '''


    return contracts #!placeholder!!!

def bunker_costs(vessel: MyShip, contracts, port_data, port_distances, loans):
    

    return contracts
