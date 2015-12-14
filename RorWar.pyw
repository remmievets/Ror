from RorData import *
from RorPlayer import *
from RorFaction import *
from RorSenator import *

class War:
    ###########################################################################
    # @brief Keep track of WAR information
    ###########################################################################
    instances = []
    iidList   = []
    
    def __init__(self, listTup):
        ###########################################################################
        # @brief Create a war instance using the WarList Tuple
        ###########################################################################
        self.disasterList = []
        self.matchingList = []
        self.activeMatches = set([])
        _, self.iid, self.name, self.baseArmyStr, self.baseFleetSup, self.baseFleetStr, \
        self.disasterList, self.standoff, self.income, self.active, self.matchingList = listTup
        # Setup variables values
        self.str      = self.baseArmyStr
        self.fleetSup = self.baseFleetSup
        self.fleetStr = self.baseFleetStr
        self.fleetVictory = False
        self.prosecuted   = False
        self.leaderList   = []
        # Add War to list of wars
        War.iidList.append(self.iid)
        # Look for matches to this war
        self.Match(War.iidList)
        # Loop through all other wars and match to this war?
        for w in War.instances:
            w.Match([self.iid], False)
        # Now it is safe to append current war to list of active wars
        War.instances.append(self)
        
    def Match(self, providedList, reset=True):
        ###########################################################################
        # @brief Update strength based on matches
        ###########################################################################
        if reset:
            # Reset strength
            self.str      = self.baseArmyStr
            self.fleetSup = self.baseFleetSup
            if not self.fleetVictory:
                self.fleetStr = self.baseFleetStr
        # look for matches in lists
        providedSet        = set(providedList)
        mySet              = set(self.matchingList)
        intersect          = providedSet & mySet
        if reset:
            self.activeMatches = intersect
        else:
            self.activeMatches.update(intersect)
        print self.name, self.activeMatches
        
    def GetTup(self):
        ###########################################################################
        # @brief Get output information for display purposes
        # @return Output tuple
        ###########################################################################
        #colStr = ("Name","Status","Str","Flt Sup","Flt Str","Reward","Information","")
        statusStr = 'Inactive'
        if self.active and self.prosecuted:
            statusStr = 'Active'
        elif self.active and not self.prosecuted:
            statusStr = 'Unprosecuted'
        # Calculate war strength
        matchCnt = len(self.activeMatches) + 1
        self.str      = self.baseArmyStr * matchCnt
        self.fleetSup = self.baseFleetSup * matchCnt
        if not self.fleetVictory:
            self.fleetStr = self.baseFleetStr * matchCnt
        
        info = 'No Matching Wars'
        if matchCnt > 1:
            info = 'x %d - Matching Wars' % (matchCnt)
        
        return (self.name, statusStr, self.str, self.fleetSup, self.fleetStr, self.income, info)
