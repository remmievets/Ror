import random

import RorUtils
from RorData import *
from RorPlayer import *
from RorFaction import *
from RorSenator import *
from RorWar import *

class Player():
###########################################################################
# @brief Base class for player type
###########################################################################
    def __init__(self, faction, name):
        self.myFaction = faction
        self.name = name
        # Link Player and Faction
        self.myFaction.AssignPlayer(self)
        
    def CollectPersonalRevenue(self):
        # Do nothing in base class
        pass
        
    def Phase2Action_Charity(self):
        pass
        
class AutoPlayer(Player):
###########################################################################
# @brief
#    Simulated player with defined behaviors
###########################################################################
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
                shareAmt = RorUtils.Roll1d6()
            else:
                shareAmt = random.randint(1,moneyPool)
            self.myFaction.treasury += shareAmt
            self.myFaction.senatorList[0].money += moneyPool - shareAmt
        elif self.revenueSplit == 'EQ':
            shareAmt = moneyPool // len(self.myFaction.senatorList)
            for s in self.myFaction.senatorList:
                s.money += shareAmt
            self.myFaction.treasury += moneyPool - shareAmt*len(self.myFaction.senatorList)
    
    def GetKnightBid(self):
        return self.knightBid
        
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
