from ship import MyShip
from runner import runner

#initialise here
banowati = MyShip('Banowati')
gdynia = MyShip('Gdynia')
cape = MyShip('Cape Climber')
competition = MyShip('Competition')


banowati.from_name(name='Banowati')
gdynia.from_name(name='Gdynia')
cape.from_name(name='Cape Climber')
competition.from_name(name='Winning Integrity')


def main():
    #! update your vessel statistics here if needed
    banowati.update(bunker_value=274.00, bunker_level=945, OPEX=1_969_450, current_port='Izmir', layover_start_week=125) 
    cape.update(bunker_value=285.00, bunker_level=1500, OPEX=3_232_597, current_port='New York', layover_start_week=124)
    # gdynia.update(bunker_value=297.00, bunker_level=1134, OPEX=1_995_848, current_port='New York', layover_start_week=124)
    # competition.update(bunker_value=300, bunker_level=1000, OPEX=3_000_000, current_port='San Antonio', layover_start_week=0)
    
    week_no = 119                         # <= change the week number every week

    my_loans = [(4_100_000, 0.1164)]        # <= your loans here [(200_000, 0.091),(Value, Rate), etc...]
    ships = [banowati, cape]   # <= your vessels here, or competition

    
    for ship in ships:
        runner(ship, week_no, my_loans) # <= layover start week indicates the week you start sailing to next contract


    print('exit 0')
    

if __name__ == "__main__":
    main()