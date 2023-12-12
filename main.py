from ship import MyShip
from runner import runner

#initialise here
banowati = MyShip('Banowati')
gdynia = MyShip('Gdynia')
four_springs = MyShip('Four Springs')
competition = MyShip('Competition')


banowati.from_name(name='Banowati')
gdynia.from_name(name='Gdynia')
four_springs.from_name(name='Four Springs')
#competition.from_name(name='')


def main():
    #! update your vessel statistics here if needed
    banowati.update(bunker_value=360.00, bunker_level=945, OPEX=2_123_842, current_port='Mina Saqr')
    gdynia.update(bunker_value=313.00, bunker_level=1134, OPEX=2_150_240, current_port='Shanghai')
    four_springs.update(bunker_value=153_920/1000, bunker_level=1000, OPEX=3_044_717, current_port='Batumi')
    
    week_no = 40                         # <= change the week number every week

    my_loans = []        # <= your loans here [(200_000, 0.091),(Value, Rate), etc...]
    ships = [banowati, gdynia, four_springs]   # <= your vessels here, or competition

    
    for ship in ships:
        runner(ship, week_no, my_loans, layover_start_week=0) # <= layover start week indicates the week you start sailing to next contract


    print('exit 0')
    

if __name__ == "__main__":
    main()