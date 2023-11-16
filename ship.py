import math as mt

class MyShip:
    def __init__(self,length, width, draft_full, draft_empty, plate_strength, max_DWT, max_volume, OPEX, design_speed):
        self.length = length
        self.width = width
        self.draft_max = draft_full
        self.draft_min = draft_empty
        self.plate_strength = plate_strength
        self.max_DWT = max_DWT
        self.max_vol = max_volume
        self.OPEX = OPEX
        self.design_speed = design_speed

    def get(self, param: str):
        param_dict = {
            'length' : self.length,
            'width' : self.width,
            'draft_full': self.draft_max,
            'draft_empty': self.draft_min,
            'plate_strength': self.plate_strength,
            'max_DWT': self.max_DWT,
            'max_vol': self.max_vol,
            'OPEX' : self.OPEX,
            'design_speed' : self.design_speed
        }
        return param_dict[param]

    def new_draft(self, cargo_weight):

        # do wat leuks

        return 0

