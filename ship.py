import pandas as pd

class MyShip:
    def __init__(self, name:str) -> None:
        #just some random default constructor
        self.name = name


    def from_data(self,length, width, draft_full, draft_empty, plate_strength, max_DWT, max_volume, OPEX, design_speed, bunker_level, ice_class, crane_capacity, AIS_cost, consumption, consumption_hotel, bunker_value, GT, holds):
        self.length = length
        self.width = width
        self.draft_max = draft_full
        self.draft_min = draft_empty
        self.plate_strength = plate_strength
        self.max_DWT = max_DWT
        self.max_vol = max_volume
        self.OPEX = OPEX
        self.design_speed = design_speed
        self.bunker_level = bunker_level
        self.ice_class = ice_class
        self.crane = crane_capacity
        self.AIS = AIS_cost
        self.consumption = consumption
        self.consumption_hotel = consumption_hotel
        self.bunker_value = bunker_value
        self.GT = GT
        self.holds = holds
    

    def from_name(self, name:str) -> None:
        self.name = name
        ship_database = pd.read_csv('fixed_data/Vessels For Sale.csv',delimiter=';')

        vessel = ship_database.loc[ship_database['Name'] == name]

        if vessel.empty:
            raise Exception("The ship name you entered is not in the database!")
        print(f"importing vessel {vessel['Name'].to_string(index=False, header=False)} \n")

        self.length = float(vessel['Length'].values[0])
        self.width = float(vessel['Width'].values[0])
        self.draft_max = float(vessel['Draft'].values[0])
        self.draft_min = float(vessel['Draft Empty'].values[0])
        self.plate_strength = int(vessel['Floor Strength'].values[0])
        self.max_DWT = float(vessel['DWT'].values[0])
        self.max_vol = float(vessel['Cargo Volume'].values[0])
        self.OPEX = float(vessel['Total OPEX'].values[0])
        self.design_speed = float(vessel['Speed'].values[0])
        self.bunker_level = float(vessel['Bunker Capacity'].values[0])
        
        if vessel['Ice Class'].values[0] == False:
            self.ice_class = False
        else:
            self.ice_class = True

        if int(vessel['Cranes'].values[0]) > 0:
            self.crane = 25
        else:
            self.crane = 0
        
        self.AIS = 100 #assumption
        self.consumption = float(vessel['Consumption'].values[0])
        self.consumption_hotel = float(vessel['Hotel Consumption'].values[0])
        self.bunker_value = 300 # assumption
        self.GT = float(vessel['GT'].values[0])
        self.holds = int(vessel['Holds'].values[0])


    def update(self, bunker_value, bunker_level, OPEX, current_port, layover_start_week) -> None:
        self.bunker_level = bunker_level
        self.bunker_value = bunker_value
        self.OPEX = OPEX
        self.current_port = current_port
        self.layover_start_week = layover_start_week


    def get(self, param: str):
        param_dict = {
            'length' : self.length,
            'width' : self.width,
            'draft_max': self.draft_max,
            'draft_min': self.draft_min,
            'plate_strength': self.plate_strength,
            'max_DWT': self.max_DWT,
            'max_vol': self.max_vol,
            'OPEX' : self.OPEX,
            'design_speed' : float(self.design_speed),
            'bunker_level' : self.bunker_level,
            'ice_class' : self.ice_class,
            'crane_capacity' : self.crane,
            'AIS' : self.AIS,
            'consumption' : self.consumption,
            'hotel' : self.consumption_hotel,
            'bunker_value': self.bunker_value,
            'GT' : self.GT,
            'holds' : self.holds,
            'name' : self.name,
            'current_port' : self.current_port,
        }
        return param_dict[param]


