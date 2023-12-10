from ship import MyShip
from runner import runner

#initialise here
abbay_wonz = MyShip('Abbay Wonz')
alam_murrni = MyShip('Alam Murni')


abbay_wonz.from_name(name='Abbay Wonz')
alam_murrni.from_name(name='Alam Murni')



def main():
    #! update your vessel statistics here if needed
    abbay_wonz.update(bunker_value=270, bunker_level=1000, OPEX=2_000_000, current_port='Corpus Christi')
    alam_murrni.update(bunker_value=270, bunker_level=1000, OPEX=2_000_000, current_port='New York')
    
    week_no = 1                         # <= change the week number every week

    my_loans = [(200_000,0.091)]        # <= your loans here [(200_000, 0.091),(Value, Rate), etc...]
    ships = [abbay_wonz, alam_murrni]   # <= your vessels here, or competition

    
    for ship in ships:
        runner(ship, week_no, my_loans, layover_start_week=0) # <= layover start week indicates the week you start sailing to next contract


    print('exit 0')
    

if __name__ == "__main__":
    main()