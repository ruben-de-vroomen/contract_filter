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
<<<<<<< HEAD
    banowati.update(bunker_value=360.00, bunker_level=945, OPEX=2_123_842, current_port='Mina Saqr')
    gdynia.update(bunker_value=313.00, bunker_level=1134, OPEX=2_150_240, current_port='Shanghai')
    four_springs.update(bunker_value=153_920/1000, bunker_level=1000, OPEX=3_044_717, current_port='Batumi')
=======
    banowati.update(bunker_value=97_520/1000, bunker_level=1000, OPEX=2_201_038, current_port='Nouadhibou', layover_start_week=0)
    gdynia.update(bunker_value=113_360/1000, bunker_level=1000, OPEX=2_227_436, current_port='Kashima',layover_start_week=0)
    four_springs.update(bunker_value=153_920/1000, bunker_level=1000, OPEX=3_044_717, current_port='Batumi',layover_start_week=0)
>>>>>>> 803d386 (ice class bug fix and ice fees included, also for layover)
    
    week_no = 40                         # <= change the week number every week

    my_loans = []        # <= your loans here [(200_000, 0.091),(Value, Rate), etc...]
    ships = [banowati, gdynia, four_springs]   # <= your vessels here, or competition

    
    for ship in ships:
        runner(ship, week_no, my_loans) # <= layover start week indicates the week you start sailing to next contract


    print('exit 0')
    

if __name__ == "__main__":
    main()