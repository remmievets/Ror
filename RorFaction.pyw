import RorUtils
from RorData import *
from RorPlayer import *
from RorSenator import *
from RorWar import *

class Faction:
###########################################################################
# @brief Class represents a players faction
###########################################################################
    def __init__(self, name):
        self.name      = name
        self.treasury  = 0
        self.milRating = 0
        self.infRating = 0
        self.ortRating = 0
        self.votes     = 0
        self.senatorList = []
        self.cards       = []
        # Uninitialized variables
        self.myPlayer = None
        self.playerFrameId = None
        self.overviewId = None
        self.gui = None
        
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
        
    def CreatePlayerFrame(self, gui):
        # create frame for player data        
        self.playerFrameId, self.overviewId = gui.AddPlayer(self.name)
        self.gui = gui
            
    def AssignPlayer(self, player):
        self.myPlayer = player
        
    def InitialFrame(self):        
        # Update frame with senator data
        for s in self.senatorList:
            self.playerFrameId.InsertItem(s.famId, s.GetTup())
        # Add faction cards to faction frame
        cid = 100
        for c in self.cards:
            v = [x for x in c[1:]]
            print v
            self.playerFrameId.InsertItem(cid, v)
            cid += 1
        # Update Faction data
        self.overviewId.InsertItem(self.name, self.GetTup())
        
    def UpdateFrame(self):        
        # Update frame with senator data
        for s in self.senatorList:
            self.playerFrameId.ModifyItem(s.famId, s.GetTup())
        self.SortFrame()
        # Update Faction data
        self.overviewId.ModifyItem(self.name, self.GetTup())

    def SortFrame(self):
        sid = []        
        # Update frame with senator data
        for s in self.senatorList:
            sid.append(s.famId)
        # Update Faction data
        self.playerFrameId.SortList(sid)
        
    def GetHraoInFaction(self):
        ###########################################################################
        # @brief Get highest ranking available official in ROME for Faction
        # @return HRAO - A reference to the new Senator
        ###########################################################################
        hrao = None
        for s in self.senatorList:
            if s.GetLocation() == "Rome":
                if not hrao:
                    hrao = s
                elif s.GetHraoRank() < hrao.GetHraoRank():
                    hrao = s 
        return hrao
        
    def AddSenator(self, senatorTuple, addIndex=-1, addToFrame=False):
        ###########################################################################
        # @brief Add senator to the faction
        # @param [in] senatorTuple (idNum, name, milR, ortR, loyR, infR)
        # @return newSen - A reference to the new Senator
        ###########################################################################
        idNum, name, milR, ortR, loyR, infR = senatorTuple
        newSen = Senator(idNum, name, milR, ortR, loyR, infR)
        # Add to the end of the list
        if addIndex == -1:
            self.senatorList.append(newSen)
        else:
            self.senatorList.insert(addIndex, newSen)
        # Adjust faction ratings
        self.milRating += milR
        self.infRating += infR
        self.ortRating += ortR
        self.votes     += ortR
        # Add to frame
        if addToFrame:
            self.playerFrameId.InsertItem(newSen.famId, newSen.GetTup())
        return newSen
        
    def RemoveSenator(self, sen):
        ###########################################################################
        # @brief Remove senator from the faction
        # @param [in] sen - senator
        ###########################################################################
        # Adjust faction ratings
        self.milRating -= sen.military
        self.infRating -= sen.influence
        self.ortRating -= sen.oratory
        self.votes     -= (sen.oratory + sen.knights)        
        # Adjust lists
        self.senatorList.remove(sen)
        self.playerFrameId.DeleteItem(sen.famId)
        
    def GetSenatorById(self, ident):
        ###########################################################################
        # @brief Lookup senator by id and return Senator
        # @param [in] ident - senator id number
        # @return Senator - If found return senator otherwise return None
        ###########################################################################
        for s in self.senatorList:
            if s.famId == ident:
                return s
        
    def ClearOffices(self):
        #@todo Assign councils / Dictator - Procouncil
        #@todo Mark councils ineligible for office
        for s in self.senatorList:
            s.office = ''
        
    def SelectOffice(self, officeText):
        infGain = 0        
        if officeText == 'Dictator':
            infGain = 7
        elif officeText == 'Master of Horse':
            infGain = 3
        elif officeText == 'Rome Council':
            infGain = 5
        elif officeText == 'Field Council':
            infGain = 5
        elif officeText == 'Censor':
            infGain = 5
        for s in self.senatorList:
            # Is senator eligible
            if s.office == '':
                print '   %s of %s is selected as %s' % (s.name, self.name, officeText)
                s.office       = officeText
                s.influence   += infGain
                s.priorCouncil = True
                break
        
    def GetPersonalRevenue(self):
        result = 0
        # Collect personal income
        for s in self.senatorList:
            result += s.GetPersonalRevenue()
        return result
    
    def GetKnight(self):
        bid = self.myPlayer.GetKnightBid()
        moneyList = sorted(self.senatorList, key=lambda sen: sen.money, reverse=True)        
        roll = RorUtils.Roll1d6()
        if moneyList[0].money < bid:
            bid = moneyList[0].money
        moneyList[0].money -= bid
        if roll+bid >= 6:
            print '   %s attracts a knight with a bid of %d.  Rolls a %d' % (moneyList[0].name, bid, roll)
            moneyList[0].knights += 1
            self.votes           += 1
        else:
            print '   %s FAILS to attract a knight with a bid of %d.  Rolls a %d' % (moneyList[0].name, bid, roll)
    
    def AssignNewFactionLeader(self):
        ###########################################################################
        # @brief Determine if new faction leader needs to be assigned
        # @return True if faction leader changed, otherwise False
        ###########################################################################
        currentFactionLeader = self.senatorList[0]
        self.myPlayer.AssignFactionLeader()
        if currentFactionLeader != self.senatorList[0]:
            print '%s has replaced %s as faction leader for %s' % (self.senatorList[0], currentFactionLeader, self.name)
            currentFactionLeader.factionLeader = False
            return True
        return False
    
    def GetTup(self):
        ###########################################################################
        # @brief Return faction data as a Tuple
        # @return Tuple of faction data
        ###########################################################################
        #colStr = ("Faction Name","Military","Oratory","Inf","Votes","Treasury","")
        return (self.name, self.milRating, self.ortRating, self.infRating, self.votes, self.treasury)
    
    def dump(self):
        ###########################################################################
        # @brief Debug printout of faction data
        ###########################################################################
        print "---------------"
        print "Faction : %s  Sen Cnt (%d)" % (self.name,len(self.senatorList))
        print " MIL %d   INF %d   VOTES %d   TREASURY %d" % (self.milRating,self.infRating,self.votes,self.treasury)
        for s in self.senatorList:
            s.dump()
        # Print cards
        print self.cards