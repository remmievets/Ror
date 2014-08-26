from Tkinter import *
import random

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
            #STATESMEN (Populatiry added)
            #( 1, "P. CORNELIUS SCIPIO AFRICANUS", 5, 5, 7, 6, 0),
            # Nullifies Punic War Disaster/Standoff
            # Cato Faction Loyalty = 0
            #( 2, "Q. FABIUS MAXIMUS VERRUCOSUS CUNCTATOR", 5, 2, 7, 3, 0),
            # Halve all losses in Combat unless Master of Horse (Fractions round up)
            #(18, "T. QUINCTIUS FLAMININUS", 5, 4, 7, 4, 0),
            # Cato Faction Loyalty = 0
            # Nullifies any Macedonian War Disaster/Standoff
            #(19, "L. AEMILIUS PAULLUS MACEDONICUS", 5, 4, 8, 4, 0),
            # Nullifies any Macedonian War Disaster/Standoff
            #(22, "M. PORCIUS CATO THE ELDER", 1, 6, 10, 1, 0),
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

# War Id, Name, Strength, Fleet Support, Fleet Strength, Disaster, Standoff, Income, Active, Matching Wars
warList = [(1, "1st PUNIC WAR",      10,  5, 10, 13, (11,14), 35, False, (2)),
           (2, "2nd PUNIC WAR",      15,  5,  0, 10, (11,15), 25, True,  (1)),
           (3, "1st MACEDONIAN WAR", 12, 10,  0, 12, (11,18), 25, True,  (4)),
           (4, "2nd MACEDONIAN WAR", 10,  5,  0, 13, (14),    45, False, (3)),
           (5, "1st ILLRIAN WAR",     5,  3,  0,  5, (17),    10, False, (6)),
           (6, "2nd ILLYRIAN WAR",    4,  2,  0,  5, (17),    10, True,  (5)),
           (7, "1st GALLIC WAR",     10,  0,  0, 13, (15),    20, True,  (0)),
           (8, "SYRIAN WAR",          6,  2,  0, 16, (15),    45, True,  (0))]

# Leader Id, Name, Strength, Disaster, Standoff, Matching Wars Ids
enemyLeaderList = [( 1, "HANNIBAL",      7,  9, 16, (1,2)),
                   ( 2, "PHILIP V",      6, 15, 14, (3,4)),
                   ( 3, "ANTIOCHUS III", 5, 14, 17, (8)),
                   ( 4, "HAMILCAR",      3,  8, 12, (1,2))]

    
class Senator:
# @brief
#    Document a senator card in ROR
#    
    instances = []
    
    def __init__(self, famId, name, military, oratory, loyalty, inf = 0, pop = 0, statesman=False):
        self.famId = famId
        self.name = name
        self.military = military
        self.oratory = oratory
        self.influence = inf
        self.pop = pop
        self.loyalty = loyalty
        self.money = 0
        self.knights = 0
        self.governer = []
        self.concessions = []
        self.allegiance = []
        self.corruption = False
        self.priorCounsel = False
        self.inRome = True
        self.factionLeader = False
        self.statesman = statesman
        Senator.instances.append(self)
        
    def GetPersonalRevenue(self):
        # Each senator gets 3 coins for being faction leader and 1 for non-faction leader
        if self.factionLeader:
            result = 3
        else:
            result = 1
            
        # Get Money for knights
        result += self.knights
            
        return result
        
    def dump(self):
        print("%20s m%1d o%1d i%02d p%02d k%1d t%03d" % \
              (self.name, self.military, self.oratory, self.influence, self.pop, self.knights, self.money))
        
class Faction:
# @brief
#    Class represents a players faction
#
    def __init__(self, name):
        self.name = name
        self.treasury = 0
        self.milRating = 0
        self.infRating = 0
        self.ortRating = 0
        self.votes     = 0
        self.senatorList = []
        
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.votes == other.votes
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)
        
    def __gt__(self, other):
        if isinstance(other, self.__class__):
            return (self.votes > other.votes) or ((self.votes == other.votes) and (self.treasury > other.treasury))
        else:
            return False
        
    def __lt__(self, other):
        return not self.__gt__(other)
        
    def AssignPlayer(self, player):
        self.myPlayer = player
        
    def AddSenator(self, senatorTuple):
        idNum, name, milR, ortR, loyR, infR = senatorTuple
        newSen = Senator(idNum, name, milR, ortR, loyR, infR)
        self.senatorList.append(newSen)
        # Adjust faction ratings
        self.milRating += milR
        self.infRating += infR
        self.ortRating += ortR
        self.votes     += ortR
        
    def GetPersonalRevenue(self):
        result = 0
        # Collect personal income
        for s in self.senatorList:
            result += s.GetPersonalRevenue()
        return result
        
    def dump(self):
        print "---------------"
        print "Faction : %s  Sen Cnt (%d)" % (self.name,len(self.senatorList))
        print " MIL %d   INF %d   VOTES %d   TREASURY %d" % (self.milRating,self.infRating,self.votes,self.treasury)
        for s in self.senatorList:
            s.dump()

class Player():
# @brief
#    Base class for player type
#    
    def __init__(self, faction, name):
        self.myFaction = faction
        self.name = name
        # Link Player and Faction
        self.myFaction.AssignPlayer(self)
            
    def CollectPersonalRevenue(self):
        # Do nothing in base class
        pass
        
    def Phase2Action_Charity(self):
        self.x = 2

class AutoPlayer(Player):
# @brief
#    Simulated player with defined behaviors
#    
    def __init__(self, faction, name):
        Player.__init__(self, faction, name)
        self.Configure()
        
    def Configure(self, leaderOpt='inf', charityOpt=False, corruptionOpt=False, revenueOpt='FF', \
                  knightOpt=0, initiativeOpt=0, gamesOpt=False):
        # Setup
        # Leader is
        #    inf - most influence
        #    mil - highest military rating (Influence tie breaker)
        #    ort - highest oratory (Influence tie breaker
        #    inf+pop - highest influence + popularity
        self.leaderSelect = leaderOpt
        
        # Revenue Phase Rules
        self.charity = charityOpt
        self.corruption = corruptionOpt
        # RevenueSplit is
        #    FF - 50% to faction leader and 50% to faction
        #    1T - 1 to each senator and rem to faction
        #    D6 - 1d6 to faction and rem to faction leader
        #    EQ - All senators share equal and any rem to faction
        self.revenueSplit = revenueOpt
        
        # Forum Phase
        self.knightBid     = knightOpt
        self.initiativeBid = initiativeOpt
        self.games         = gamesOpt

    def AssignFactionLeader(self):
        # Sort senator by leaderOpt criteria
        if self.leaderSelect == 'inf':
            self.myFaction.senatorList = sorted(self.myFaction.senatorList, key=lambda sen: sen.influence, reverse=True)            
        elif self.leaderSelect == 'mil':
            self.myFaction.senatorList = sorted(self.myFaction.senatorList, key=lambda sen: sen.military, reverse=True)            
        elif self.leaderSelect == 'ort':
            self.myFaction.senatorList = sorted(self.myFaction.senatorList, key=lambda sen: (sen.oratory, sen.influence), reverse=True)            
        elif self.leaderSelect == 'inf+pop':
            self.myFaction.senatorList = sorted(self.myFaction.senatorList, key=lambda sen: sen.influence+sen.pop, reverse=True)            
        # Assign new faction leader
        self.myFaction.senatorList[0].factionLeader = True
    
    def CollectPersonalRevenue(self):
        moneyPool = self.myFaction.GetPersonalRevenue()
        print("%s = %d" % (self.myFaction.name, moneyPool))
        # Distribute money by criteria
        if self.revenueSplit == 'FF':
            self.myFaction.treasury += moneyPool // 2
            self.myFaction.senatorList[0].money += moneyPool - (moneyPool // 2)
        elif self.revenueSplit == '1T':
            for s in self.myFaction.senatorList:
                s.money += 1
            self.myFaction.treasury += moneyPool - len(self.myFaction.senatorList)
        elif self.revenueSplit == 'D6':
            # D6 to faction treasury rem to faction leader
            if moneyPool >= 6:
                shareAmt = random.randint(1,6)
            else:
                shareAmt = random.randint(1,moneyPool)
            self.myFaction.treasury += shareAmt
            self.myFaction.senatorList[0].money += moneyPool - shareAmt
        elif self.revenueSplit == 'EQ':
            shareAmt = moneyPool // len(self.myFaction.senatorList)
            for s in self.myFaction.senatorList:
                s.money += shareAmt
            self.myFaction.treasury += moneyPool - shareAmt*len(self.myFaction.senatorList)
                
        
class ROR():
# @brief
#    Game Engine for Republic of Rome
#
# @var playerCnt - Number of players in the game
# @var factions  - List of player factions
# @var phase     - Current game phase
    def __init__(self):
        # Number of players
        self.playerCnt = 5
        
        # Faction List    
        self.factions = []
        self.players  = []
        self.turn  = 0        
        self.setup = False
            
    def GameSetup(self):
        # Only perform setup once
        if self.setup == True:
            return
        
        self.setup = True
        
        # Sort initial list of senators for Early Republic
        random.seed()
        sortedFamily = random.sample(familyList, len(familyList))

        # Create initial factions
        for i in range(0, self.playerCnt):
            print "Creating Player %d" % (i)
            self.factions.append(Faction("Player %d" % (i)))
            self.players.append(AutoPlayer(self.factions[i], "Player %d" % (i)))
            # Add 3 senators to each faction
            x = 0
            for x in range(i*3, (i*3)+3):
                print "Adding senator"
                self.factions[i].AddSenator(sortedFamily[x])

        # First sort by total faction military rating
        sorted_factions = sorted(self.factions, key=lambda fac: (fac.milRating, fac.infRating), reverse=True)
        
        # Remove imperialists from list
        tempImperialFaction = sorted_factions[0]
        tempImperialFaction.name = "Imperialists"
        tempImperialFaction.myPlayer.Configure(leaderOpt='mil', revenueOpt='D6')
        sorted_factions.remove(tempImperialFaction)
        
        # Then sort by total faction influence rating
        sorted_factions = sorted(sorted_factions, key=lambda fac: fac.infRating, reverse=True)
        
        # Highest influence is Populists
        sorted_factions[0].name = "Populists"
        sorted_factions[0].myPlayer.Configure(leaderOpt='inf+pop', revenueOpt='1T')
        
        # Second most influence is HUMAN
        sorted_factions[1].name = "HUMAN"
        
        # Third most influence is Plutocrats 
        sorted_factions[2].name = "Plutocrates"
        sorted_factions[2].myPlayer.Configure(leaderOpt='inf', revenueOpt='EQ')
        # Assign one additional Senator (0-14 initially assigned)
        sorted_factions[2].AddSenator(sortedFamily[15])
       
        # Least influence is Conservatives
        sorted_factions[3].name = "Conservatives"
        sorted_factions[3].myPlayer.Configure(leaderOpt='inf', revenueOpt='FF')
        # Assign two additional Senators (0-14 initially assigned)
        sorted_factions[3].AddSenator(sortedFamily[16])
        sorted_factions[3].AddSenator(sortedFamily[17])
        
        # End with sort on votes / money
        self.factions = sorted(self.factions, reverse=True)
        
        # Assign faction leader for each player based on player criteria
        for p in self.players:
            p.AssignFactionLeader()
        
    def GameTurn(self):
        self.turn += 1
        print "------------------"
        print "-- Turn %d" % (self.turn)
        print "------------------"
        self.MortalityPhase()
        self.RevenuePhase()
        self.ForumPhase()
        self.PopulationPhase()
        self.SenatePhase()
        self.CombatPhase()
        self.RevolutionPhase()
        for f in self.factions:
            f.dump()
        
    def MortalityPhase(self):
        print "-- Mortality Phase"
        
    def RevenuePhase(self):
        print "-- Revenue Phase"
        # Collect personal revenue
        for p in self.players:
            p.CollectPersonalRevenue()
        # Collect state income
        # Get state income from provinces
        # Pay for troops
        
        # Allow players to make donations
        # If State treasury is negative then all players lose
    
    def ForumPhase(self):
        print "-- Forum Phase"
        # Remove old events
        # Initiative x6
        #    2d6 - On 7 then 3d6 and lookup event otherwise get a card from the deck
        #    Persuasion
        #    Knight
        #    Faction Leader
        #    Sponsor Games
        # Put Rome in Order
        #    All senators holding office get a major marker (corruption)
        #    Roll for tax farmer destroy under certain conditions
        #    Roll 1d6 for every Senator, Concession, or Enemy Leader
        #        5,6 back in game (enemy leader dies)
        
    def PopulationPhase(self):
        print "-- Population Phase"
        # +1 unrest for every Drought and Unprosecuted war
        # roll 3d6 + HRAO's pop - current unrest level
        # Check results
        
    def SenatePhase(self):
        print "-- Senate Phase"
        
    def CombatPhase(self):
        print "-- Combat Phase"
        
    def RevolutionPhase(self):
        print "-- Revolution Phase"
        
# Main Test Code    
engine = ROR()
engine.GameSetup()

engine.GameTurn()
engine.GameTurn()
engine.GameTurn()

