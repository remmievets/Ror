
# War Id, Name, Strength, Fleet Support, Fleet Strength, Disaster, Standoff, Income, Active, Matching Wars
warList = [(1, "1st PUNIC WAR",      10,  5, 10, 13, (11,14), 35, False, (2,0)),
           (2, "2nd PUNIC WAR",      15,  5,  0, 10, (11,15), 25, True,  (1,0)),
           (3, "1st MACEDONIAN WAR", 12, 10,  0, 12, (11,18), 25, True,  (4,0)),
           (4, "2nd MACEDONIAN WAR", 10,  5,  0, 13, (14,0),    45, False, (3,0)),
           (5, "1st ILLRIAN WAR",     5,  3,  0,  5, (17,0),    10, False, (6,0)),
           (6, "2nd ILLYRIAN WAR",    4,  2,  0,  5, (17,0),    10, True,  (5,0)),
           (7, "1st GALLIC WAR",     10,  0,  0, 13, (15,0),    20, True,  (0,0)),
           (8, "SYRIAN WAR",          6,  2,  0, 16, (15,0),    45, True,  (0,0))]

# Leader Id, Name, Strength, Disaster, Standoff, Matching Wars Ids
enemyLeaderList = [( 1, "HANNIBAL",      7,  9, 16, (1,2)),
                   ( 2, "PHILIP V",      6, 15, 14, (3,4)),
                   ( 3, "ANTIOCHUS III", 5, 14, 17, (8)),
                   ( 4, "HAMILCAR",      3,  8, 12, (1,2))]

# @brief
#    constant holds all possible family cards
#
# Packing consists of 
#    Family Id Number, Name, military, oratory, loyalty, influence 
familyList = [( 1, "CORNELIUS", 4, 3,  9, 5),
              ( 2, "FABIUS",    4, 2,  9, 5),
              ( 3, "VALERIUS",  1, 2, 10, 5),
              ( 4, "JULIUS",    4, 3,  9, 4),
              ( 5, "CLAUDIUS",  2, 3,  7, 4),
              ( 6, "MANLIUS",   3, 2,  7, 4),
              ( 7, "FULVIUS",   2, 2,  8, 4),
              ( 8, "FURIUS",    3, 3,  8, 3),
              ( 9, "AURELIUS",  2, 3,  7, 3),
              (10, "JUNIUS",    1, 2,  8, 3),
              (11, "PAPIRIUS",  1, 2,  6, 3),
              (12, "ACILIUS",   2, 2,  7, 3),
              (13, "FLAMINIUS", 4, 2,  6, 3),
              (14, "AELIUS",    3, 4,  7, 2),
              (15, "SULPICIUS", 3, 2,  8, 2),
              (16, "CALPURNIUS",1, 2,  9, 2),
              (17, "PLAUTIUS",  2, 1,  6, 2),
              (18, "QUINCTIUS", 3, 2,  6, 1),
              (19, "AEMILIUS",  4, 2,  8, 1),
              (20, "TERENTIUS", 2, 1,  6, 1)]

# @brief Statesmen
#    Same as family card, but popularity added
statesmenList = [( 1, "P. CORNELIUS SCIPIO AFRICANUS", 5, 5, 7, 6, 0),
                    # Nullifies Punic War Disaster/Standoff
                    # Cato Faction Loyalty = 0
                 ( 2, "Q. FABIUS MAXIMUS VERRUCOSUS CUNCTATOR", 5, 2, 7, 3, 0),
                    # Halve all losses in Combat unless Master of Horse (Fractions round up)
                 (18, "T. QUINCTIUS FLAMININUS", 5, 4, 7, 4, 0),
                    # Cato Faction Loyalty = 0
                    # Nullifies any Macedonian War Disaster/Standoff
                 (19, "L. AEMILIUS PAULLUS MACEDONICUS", 5, 4, 8, 4, 0),
                    # Nullifies any Macedonian War Disaster/Standoff
                 (22, "M. PORCIUS CATO THE ELDER", 1, 6, 10, 1, 0)]
                    # 1 Free Tribune Per Year
                    # Faction Loyalty 0 on Scipios / Flamininus

concessionList = [( 1, "TAX FARMER 1", 2),
                  ( 2, "TAX FARMER 2", 2),
                  ( 3, "TAX FARMER 3", 2),
                  ( 4, "TAX FARMER 4", 2),
                  ( 5, "TAX FARMER 5", 2),
                  ( 6, "TAX FARMER 6", 2),
                  ( 7, "HARBOR FEES",  3),
                  ( 8, "MINING",       3),
                  ( 9, "LAND COMMISSIONER", 3), #SPECIAL must have a land bill in effect to own
                  (10, "SICILIAN GRAIN",    4), #SPECIAL x2 if drought or pirates
                  (11, "EGYPTIAN GRAIN",    5), #SPECIAL x2 if drought or pirates
                  (12, "ARMAMENTS",         2), #SPECIAL per legion recruited
                  (13, "SHIP BUILDING",     3)] #SPECIAL per fleet built

intrigueList = [(9, "Tribune"),             # 9 Tribunes
                (1, "Influence Peddling"),  # Draw unplayed card at random from an opponent of your choice
                (1, "Secret Bodyguard"),    # Playable after assassination attempt (subtract one form dr)
                (1, "Assassin"),            # Add 1 to your assassin dr
                (1, "Seduction"),           # Unopposed persuasion attempt during initiative
                (1, "Blackmail")]           # Unopposed persuasion attempt during initiative (fail -> reduce inf / popularity by amount equal to DR)
                                            # Not playable vs Cicero or Catos 

eventLookup = { 3 : 'mob violence',
                4 : 'natural disaster',
                5 : 'ally deserts',
                6 : 'evil omens',
                7 : 'refuge',
                8 : 'epidemic',
                9 : 'drought',
               10 : 'evil omens',
               11 : 'storm at sea',
               12 : 'manpower shortage',
               13 : 'allied enthusiasm',
               14 : 'new alliance',
               15 : 'rhodian alliance',
               16 : 'enemy ally deserts',
               17 : 'enemy leader dies',
               18 : 'trial of verres'}
