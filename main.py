from ship import MyShip
from runner import runner

#initialise here
banowati = MyShip('Banowati')
gdynia = MyShip('Gdynia')
four_springs = MyShip('Four Springs')


banowati.from_name(name='Banowati')
gdynia.from_name(name='Gdynia')
four_springs.from_name(name='Four Springs')



def main():
    #! update your vessel statistics here if needed
    banowati.update(bunker_value=97_520/1000, bunker_level=1000, OPEX=2_201_038, current_port='Nouadhibou')
    gdynia.update(bunker_value=113_360/1000, bunker_level=1000, OPEX=2_227_436, current_port='Kashima')
    four_springs.update(bunker_value=153_920/1000, bunker_level=1000, OPEX=3_044_717, current_port='Batumi')
    
    week_no = 1                         # <= change the week number every week

    my_loans = []        # <= your loans here [(200_000, 0.091),(Value, Rate), etc...]
    ships = [banowati, gdynia, four_springs]   # <= your vessels here, or competition

    
    for ship in ships:
        runner(ship, week_no, my_loans, layover_start_week=0) # <= layover start week indicates the week you start sailing to next contract


    print('exit 0')
    

if __name__ == "__main__":
    main()