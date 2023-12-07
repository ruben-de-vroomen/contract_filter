from ship import MyShip
from runner import runner

#initialise here
handymax33 = MyShip('Handymax 33')
handymax32 = MyShip('Handymax 32')

handymax33.from_data(length=229.75, 
                    width=32.21, 
                    draft_full=12.6, 
                    draft_empty=3.28, 
                    plate_strength=20, 
                    max_DWT = 66_758, 
                    max_volume=46_417, 
                    OPEX = 1_874_828, 
                    design_speed = 14, 
                    bunker_level=1400,          # Adjust every round 
                    ice_class=True,             # must be True or False
                    crane_capacity=25,          # either 0 or 25
                    AIS_cost=100,               # either 0 or 100
                    consumption = 39.7,
                    consumption_hotel = 2.5,
                    bunker_value=269,            # needs to be updated continually
                    GT = 28_905,
                    holds=7,
                    )

handymax32.from_name(name='Handymax 32')




def main():
    #! defining your vessel here
    handymax32.update(bunker_value=270, bunker_level=1000, OPEX=2_000_000, current_port='Corpus Christi')
    handymax33.update(bunker_value=270, bunker_level=1000, OPEX=2_000_000, current_port='New York')
    
    week_no = 38

    my_loans = [] # <- your loans here [(200_000, 0.091),(Value, Rate), etc...]
    ships = [handymax32, handymax33]
    
    for ship in ships:
        runner(ship, week_no, my_loans, testing_mode=True)


    print('exit 0')
    

if __name__ == "__main__":
    main()