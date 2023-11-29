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
        self.GT = GT,
        self.holds = holds
    

    def from_name(self, name:str) -> None:
        self.name = name
        database = pd.read_csv('fixed_data/Vessels For Sale.csv')
        print(database)


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
        }
        return param_dict[param]


