# contract_filter
Filters Contracts for Finance Game

1. Adjust the Ship parameters for your ship - Change the week number
2. load in all the contracts each round of the game
3. Run `python3 main.py`



## CHANGELOG
1. Week folders are now automatically generated for the next week
2. Ships can be automatically imported from the vessel database [Keep in mind there is now an update function for things like bunker value]
3. Various Bug Fixes in Break Even Rate and Sailing Speeds
4. Demurage now also calculated for each journey, and is subtracted from the break even rate to reflect its new position
5. Contracts are now not entirely excluded, but labeled as not possible with a reason why

## WARNINGS

1. SSHINC is only taken into account in an approximate matter
2. Currencies are not taken into account
3. Ice breakers and craneless journeys are excluded, even though these journeys may be technically possible
4. I may have made mistakes, use with caution