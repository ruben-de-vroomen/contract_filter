import math as mt

class MyShip:
    def __init__(self,length, width, draft_full, draft_empty, plate_strength, max_DWT, max_volume, OPEX, design_speed):
        self.length = length
        self.width = width
        self.draft_max = draft_full
        self.draft_min = draft_empty
        self.plate_strength = plate_strength
        self.max_DWT = max_DWT
        self.max_volume = max_volume
        self.OPEX = OPEX
        self.design_speed = design_speed

    def new_draft(self, cargo_weight):

        # do wat leuks

        return 0

