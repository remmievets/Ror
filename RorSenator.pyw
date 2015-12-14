from RorData import *
from RorPlayer import *
from RorFaction import *
from RorWar import *

class Senator:
###########################################################################
# @brief Document a senator card in ROR
###########################################################################
    instances = []
    
    def __init__(self, famId, name, military, oratory, loyalty, inf = 0, pop = 0, statesman=False):
        # Basic skills
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
        self.minor_corruption = False
        self.major_corruption = False
        self.priorCouncil = False
        self.inRome = True
        self.office = ''
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
    
    def GetName(self):
        nameWithTitle = self.name
        if self.factionLeader:
            nameWithTitle += ' (FL)'            
        if self.office == 'Dictator':
            nameWithTitle += ' (D)'
        elif self.office == 'Master of Horse':
            nameWithTitle += ' (MoH)'
        elif self.office == 'Rome Council':
            nameWithTitle += ' (RC)'
        elif self.office == 'Field Council':
            nameWithTitle += ' (FC)'
        elif self.office == 'Censor':
            nameWithTitle += ' (C)'
        elif self.office == 'Procouncil':
            nameWithTitle += ' (PRO)'
        if self.priorCouncil:
            nameWithTitle += ' (PC)'            
        return nameWithTitle
    
    def GetHraoRank(self):
        rank = 100 - self.influence
        if self.office == 'Dictator':
            rank = 1
        elif self.office == 'Rome Council':
            rank = 2
        elif self.office == 'Field Council':
            rank = 3
        elif self.office == 'Censor':
            rank = 4
        elif self.office == 'Master of Horse':
            rank = 5
        return rank
    
    def GetLocation(self):
        locStr = ''
        if self.inRome:
            locStr = 'Rome'
        return locStr
        
    def GetConcessions(self):
        consessionStr = ''
        return consessionStr        
        
    def GetTup(self):
        #colStr = ("Name","Military","Oratory","Inf","Pop","Loyalty","Knights","Votes","Money","Location","Concessions")
        return (self.GetName(), self.military, self.oratory, self.influence, self.pop, self.loyalty, \
                self.knights, self.oratory+self.knights, self.money, self.GetLocation(), self.GetConcessions())
        
    def dump(self):
        print("%20s m%1d o%1d i%02d p%02d k%1d t%03d" % \
              (self.GetName(), self.military, self.oratory, self.influence, self.pop, self.knights, self.money))
