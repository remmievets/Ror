import Tkinter as tk
import random
import threading
import RorGui
import Queue

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

def Roll1d6():
###########################################################################
# @brief Roll 1 six sided dice
#
# @return die 1 result
###########################################################################
    return random.randint(1,6)
        
def Roll2d6():
###########################################################################
# @brief Roll 2 six sided dice
#
# @return total, die 1 result, die 2 result
###########################################################################
    die1 = random.randint(1,6)
    die2 = random.randint(1,6)
    total = die1 + die2
    return total, die1, die2

def Roll3d6():
###########################################################################
# @brief Roll 3 six sided dice
#
# @return total, die 1 result, die 2 result, die 3 result
###########################################################################
    die1 = random.randint(1,6)
    die2 = random.randint(1,6)
    die3 = random.randint(1,6)
    total = die1 + die2 + die3
    return total, die1, die2, die3

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
        roll = Roll1d6()
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
                shareAmt = Roll1d6()
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
    
class ROR(threading.Thread):
###########################################################################
# @brief
#    Game Engine for Republic of Rome
#
# @var playerCnt - Number of players in the game
# @var factions  - List of player factions
# @var phase     - Current game phase
###########################################################################
    def __init__(self, gui):
        threading.Thread.__init__(self)
        # Number of players
        self.playerCnt = 5
        
        # Save reference to gui
        self.gui = gui
        
        # Faction List
        self.factions = []
        self.players  = []
        
        # Game Info
        self.gameActive = True
        self.turn   = 1
        self.phase  = 0
        self.unrest = 0        
        self.setup = False
        self.curiaFamilies    = []
        self.curiaLeaders     = []
        self.curiaConcessions = []
        self.wars             = []
        self.forumFamilies    = []
        self.forumConcessions = []
        self.forumProvinces   = []
        self.deck             = []
        self.events           = {}
        self.ResetEvents()
        
        # Action queue
        self.jobQueue = Queue.Queue()
        
    def GameSetup(self):
        ###########################################################################
        # @brief Perform initial game setup
        ###########################################################################
        # Only perform setup once
        if self.setup == True:
            return        
        self.setup = True
        
        # Sort initial list of senators for Early Republic
        random.seed()
        sortedFamily = random.sample(familyList, len(familyList))

        # Create initial factions
        for i in range(0, self.playerCnt):
            self.factions.append(Faction("Player %d" % (i)))
            self.players.append(AutoPlayer(self.factions[i], "Player %d" % (i)))
            # Add 3 senators to each faction
            x = 0
            for x in range(i*3, (i*3)+3):
                self.factions[i].AddSenator(sortedFamily[x])

        # First sort by total faction military rating
        sorted_factions = sorted(self.factions, key=lambda fac: (fac.milRating, fac.infRating), reverse=True)
        
        # Remove imperialists from list
        tempImperialFaction = sorted_factions[0]
        tempImperialFaction.name = "Imperialists"
        tempImperialFaction.myPlayer.Configure(leaderOpt='mil', revenueOpt='D6', knightOpt=1)
        sorted_factions.remove(tempImperialFaction)
        
        # Then sort by total faction influence rating
        sorted_factions = sorted(sorted_factions, key=lambda fac: fac.infRating, reverse=True)
        
        # Highest influence is Populists
        sorted_factions[0].name = "Populists"
        sorted_factions[0].myPlayer.Configure(leaderOpt='inf+pop', revenueOpt='1T', knightOpt=1)
        
        # Second most influence is HUMAN
        sorted_factions[1].name = "HUMAN"
        sorted_factions[1].myPlayer.Configure(leaderOpt='inf', revenueOpt='EQ', knightOpt=3)
        
        # Third most influence is Plutocrats 
        sorted_factions[2].name = "Plutocrates"
        sorted_factions[2].myPlayer.Configure(leaderOpt='inf', revenueOpt='EQ', knightOpt=2)
        # Assign one additional Senator (0-14 initially assigned)
        sorted_factions[2].AddSenator(sortedFamily[15])
       
        # Least influence is Conservatives
        sorted_factions[3].name = "Conservatives"
        sorted_factions[3].myPlayer.Configure(leaderOpt='inf', revenueOpt='FF')
        # Assign two additional Senators (0-14 initially assigned)
        sorted_factions[3].AddSenator(sortedFamily[16])
        sorted_factions[3].AddSenator(sortedFamily[17])
        
        # Sort factions on votes / money
        self.factions = sorted(self.factions, reverse=True)
        
        # Randomize player order
        self.players = random.sample(self.players, len(self.players))
        
        # Assign faction leader for each player based on player criteria
        for p in self.players:
            p.myFaction.AssignNewFactionLeader()
            p.myFaction.senatorList[0].priorCouncil = True
            p.myFaction.CreatePlayerFrame(self.gui)
            if p.myFaction.name == 'Populists':
                p.myFaction.SelectOffice('Rome Council')
            
        # Assign callback for next phase button
        self.gui.cmdFrame.AddHook('next_phase', self.CmdNextPhase)
        
        # Setup deck
        self.DeckSetup(sortedFamily[18:])
        
    def DeckSetup(self, remainingSenators):
        ###########################################################################
        # @brief Initial deck setup and card deal to each player
        ###########################################################################
        # Initial deck add all of the RED cards (statesmen, concessions, intrigues)
        for s in statesmenList:
            self.deck.append(('statesmen',) + s)
        for c in concessionList:
            self.deck.append(('concession',) + c)
        for i in intrigueList:
            cnt, cardName = i
            for _ in range(0, cnt):
                self.deck.append(('intrigue',cardName))
        # Shuffle the deck
        self.deck = random.sample(self.deck, len(self.deck))
        # Deal 3 cards to each player
        for f in self.factions:
            for _ in range(0,3):
                f.cards.append(self.deck.pop())
        # Add BLACK cards to the deck (Wars, Leaders, Remaining Senators)
        for w in warList:
            self.deck.append(('war',) + w)
        for e in enemyLeaderList:
            self.deck.append(('leader',) + e)
        for f in remainingSenators:
            self.deck.append(('family',) + f)
        # Shuffle the deck
        self.deck = random.sample(self.deck, len(self.deck))
        print "Cards in deck ", len(self.deck)
        print self.deck

    def UpdateDisplay(self):
        ###########################################################################
        # @brief Update ROR GUI Information
        ###########################################################################
        # Update faction data
        fid = []
        for f in self.factions:
            f.UpdateFrame()
            fid.append(f.name)
        self.gui.factionOverview.SortList(fid)
        
        # Update state data
        ####@todo
        
        # Update active forces
        ####@todo
        
        # Update forum tab
        
        # Update war tab
        for w in self.wars:
            self.gui.warsTab.ModifyItem(w.iid, w.GetTup())
            
    def run(self):
        ###########################################################################
        # @brief Game processing thread
        ###########################################################################
        # Update display info
        #for f in self.factions:
        #    f.InitialFrame()
        print 'Starting game engine thread'
        while self.gameActive:
            self.UpdateDisplay()
            # Block forever until user requests something
            job = self.jobQueue.get(block=True)
            if job == 'next_phase':
                self.phase += 1            
                self.GameTurn()
            elif job == 'game_end':
                self.gameActive = False
            
        print 'Game Over! - Exit Game Engine Loop'
            
    def CmdNextPhase(self):
        #print 'CmdNextPhase pressed - added to job queue'
        self.jobQueue.put('next_phase')
        
    def GameTurn(self):
        ###########################################################################
        # @brief Setup next game phase
        ###########################################################################
        # Check for turn advancement
        if self.phase > 7:
            print "------------------"
            print "-- Turn %d" % (self.turn)
            print "------------------"
            self.phase = 1
            self.turn += 1
            for f in self.factions:
                f.dump()
            
        # Execute phase
        text = 'INVALID'
        if self.phase == 1:
            text = 'MORTALITY'
            self.MortalityPhase()
        
        elif self.phase == 2:
            text = 'REVENUE'
            self.RevenuePhase()
            
        elif self.phase == 3:
            text = 'FORUM'
            self.ForumPhase()
            
        elif self.phase == 4:
            text = 'POPULATION'
            self.PopulationPhase()
            
        elif self.phase == 5:
            text = 'SENATE'
            self.SenatePhase()
            
        elif self.phase == 6:
            text = 'COMBAT'
            self.CombatPhase()
            
        elif self.phase == 7:
            text = 'REVOLUTION'
            self.RevolutionPhase()
            
        self.gui.phase.SetPhase(self.turn, text)
                
    def ResetEvents(self):
        ###########################################################################
        # @brief Clear all events to zero
        ###########################################################################
        self.events['mob violence'] = 0
        self.events['natural disaster'] = 0
        self.events['ally deserts'] = 0
        self.events['evil omens'] = 0
        self.events['refuge'] = 0
        self.events['epidemic'] = 0
        self.events['drought'] = 0
        self.events['storm at sea'] = 0
        self.events['manpower shortage'] = 0
        self.events['allied enthusiasm'] = 0
        self.events['new alliance'] = 0
        self.events['rhodian alliance'] = 0
        self.events['rhodian maritime alliance'] = 0
        self.events['enemy ally deserts'] = 0
        self.events['enemy leader dies'] = 0
        self.events['trial of verres'] = 0
        self.events['internal disorder'] = 0
        self.events['pretender emerges'] = 0
        self.events['barbarian raids'] = 0
        self.events['no recruitment'] = 0
    
    def GetHrao(self):
        ###########################################################################
        # @brief Search all factions for Highest Ranking Available Official
        # @return Return HRAO senator reference, hrao faction
        ###########################################################################
        hraoSenator = None
        hraoFaction = None
        for f in self.factions:
            if not hraoSenator:
                hraoSenator = f.GetHraoInFaction()
                hraoFaction = f
            elif f.GetHraoInFaction().GetHraoRank() < hraoSenator.GetHraoRank():
                hraoSenator = f.GetHraoInFaction()
                hraoFaction = f                
        return hraoSenator, hraoFaction
            
    def DrawMortalityChits(self, drawCount = 1):
        ###########################################################################
        # @brief Draw number of mortality chits and return a list of selected
        #        numbers
        #
        # There are 36 available chits
        #     1-30 are families that need to be searched
        #     31-32 are pick two (pick two are re-added)
        #     33-36 are none
        #
        # @param [in] drawCount - Number of chits to draw
        # @return list of family numbers drawn
        ###########################################################################
        killList = []
        picksRemaining = 1
        
        while (picksRemaining > 0):
            killme = random.randint(1,36)
            print 'Kill value is %d' %(killme)
            picksRemaining -= 1
            if killme <= 30:
                # Determine if player already selected
                if killme in killList:
                    picksRemaining += 1
                    continue
                else:
                    killList.append(killme)
            elif killme <= 32:
                # pick two more
                picksRemaining += 2
        return killList
    
    def EventMob(self, value):
        ###########################################################################
        # @brief A mob attacks senators in Rome.
        # @param value - The number of mortality chits to draw
        ###########################################################################
        print "*** Event Mob ***"
        killList = self.DrawMortalityChits(value)
        for k in killList:
            for f in self.factions:
                s = f.GetSenatorById(k)
                if s:
                    # Unlike mortality phase these deaths only occur to people in Rome
                    if s.GetLocation() == 'Rome':
                        print 'Senator %s from faction %s has died' % (s.name, f.name)
                        # If the faction leader died then allow user to keep
                        if s.factionLeader:
                            print 'Faction Leader died'
                            f.RemoveSenator(s)
                            # Re-adding Senator to the list
                            newsen = f.AddSenator(familyList[k-1], addIndex=0, addToFrame=True)
                            # Re-make senator the faction leader
                            newsen.factionLeader = True
                        else:
                            f.RemoveSenator(s)
                            self.curiaFamilies.append(k)        

    def MortalityPhase(self):
        ###########################################################################
        # @brief Execute Mortality Phase of the game turn.  Draws 1 mortality chit
        #        and process the results.  No user interaction needed.
        ###########################################################################
        print '-----------------------------------------'
        print "-- Mortality Phase"
        killList = self.DrawMortalityChits()
        for k in killList:
            for f in self.factions:
                s = f.GetSenatorById(k)
                if s:
                    print 'Senator %s from faction %s has died' % (s.name, f.name)
                    # If the faction leader died then allow user to keep
                    if s.factionLeader:
                        print 'Faction Leader died'
                        f.RemoveSenator(s)
                        # Re-adding Senator to the list
                        newsen = f.AddSenator(familyList[k-1], addIndex=0, addToFrame=True)
                        # Re-make senator the faction leader
                        newsen.factionLeader = True
                    else:
                        f.RemoveSenator(s)
                        self.curiaFamilies.append(k)
        
    def RevenuePhase(self):
        print '-----------------------------------------'
        print "-- Revenue Phase"
        # Collect personal revenue
        for p in self.players:
            p.CollectPersonalRevenue()
        # Collect state income
        # Get state income from provinces
        # Pay for troops
        
        # Allow players to make donations
        # If State treasury is negative then all players lose
        
    def ExecuteInitiative(self, activeFaction):
        ###########################################################################
        # @brief Execute players initiative from Forum Phase
        #    2d6 - On 7 then 3d6 and lookup event otherwise get a card from the deck
        #    Persuasion
        #    Knight
        #    Faction Leader
        #    Sponsor Games
        # @param activeFaction - current factions turn
        ###########################################################################
        roll = Roll2d6()
        if roll[0] == 7:
            roll = Roll3d6()
            eventName = eventLookup[roll[0]]
            print 'Event has occurred', eventName
            self.events[eventName] += 1
        elif len(self.deck) > 0:
            # draw card
            card = self.deck.pop(0)
            print '%s draws %s card' % (activeFaction.name, card[0])
            if card[0] == 'war':
                self.wars.append(War(card))
            elif card[0] == 'family':
                self.forumFamilies.append(card)
            elif card[0] == 'leader':
                self.curiaLeaders.append(card)
            else:
                activeFaction.cards.append(card)
        #@todo Persuasion attempt
        activeFaction.GetKnight()
        if not activeFaction.AssignNewFactionLeader():
            #@todo Sponsor Games
            pass
    
    def ForumPhase(self):
        print '-----------------------------------------'
        print "-- Forum Phase"
        # Remove old events        
        self.ResetEvents()
        # Initiative x6 - Start with player who holds the HRAO
        _, hraoFaction = self.GetHrao()        
        p = hraoFaction.myPlayer
        try:
            pIndex = self.players.index(p)
        except ValueError:
            pIndex = 0
        # Loop by players in player order
        for _ in range(0,self.playerCnt):
            print '-----------------------------------------'
            print self.players[pIndex].myFaction.name, pIndex
            self.ExecuteInitiative(self.players[pIndex].myFaction)
            pIndex += 1
            if pIndex >= self.playerCnt:
                pIndex = 0
        # Put Rome in Order
        #    All senators holding office get a major marker (corruption)
        #    Roll for tax farmer destroy under certain conditions
        #    Roll 1d6 for every Senator, Concession, or Enemy Leader
        #        5,6 back in game (enemy leader dies)
        
    def PopulationPhase(self):
        ###########################################################################
        # @brief Execute population phase (3d6 - unrest level + HRAO Popularity)
        #
        # Population table
        #   >18        -3 from Unrest level
        #    17        -2 from Unrest level
        #    16        -1 from Unrest level
        #    11-15     No change
        #    10        +1 to Unrest level        
        #     9        +2 to Unrest level
        #     8        +3 to Unrest level
        #     7        +3 to Unrest level, MS
        #     6        +4 to Unrest level
        #     5        +4 to Unrest level, MS
        #     4        +5 to Unrest level
        #     3        +5 to Unrest level, MS
        #     2        +5 to Unrest level, NR
        #     1        +5 to Unrest level, NR, Mob
        #     0        +6 to Unrest level, NR, Mob
        #    <0        People revolt; all players lose
        ###########################################################################
        print '-----------------------------------------'
        print "-- Population Phase"
        mob = False
        # +1 unrest for every Drought and Unprosecuted war
        hrao = self.GetHrao()
        result = Roll3d6()[0] - self.unrest + hrao[0].pop
        print '%s gives the state of the republic address %d' % (hrao[0].name, result)
        if result >= 18:
            self.unrest -= 3
        elif result == 17:
            self.unrest -= 2
        elif result == 16:
            self.unrest -= 1
        elif result == 10:
            self.unrest += 1
        elif result == 9:
            self.unrest += 2
        elif result == 8:
            self.unrest += 3
        elif result == 7:
            self.events['manpower shortage'] += 1
            self.unrest += 3
        elif result == 6:
            self.unrest += 4
        elif result == 5:
            self.unrest += 4
            self.events['manpower shortage'] += 1
        elif result == 4:
            self.unrest += 5
        elif result == 3:
            self.unrest += 5
            self.events['manpower shortage'] += 1
        elif result == 2:
            self.unrest += 5
            self.events['no recruitment'] = 1
        elif result == 1:
            self.unrest += 5
            self.events['no recruitment'] = 1
            mob = True
        elif result == 0:
            self.unrest += 6
            self.events['no recruitment'] = 1
            mob = True
        elif result <= 0:
            self.jobQueue.put('game_end')
        if self.unrest > 9:
            self.jobQueue.put('game_end')
        # Update display with new unrest level
        self.gui.state.SetUnrestLevel(self.unrest)
        # Implement Mob
        if mob:
            # Draw 6 mortality chits and kill all matches of senators in Rome
            self.EventMob(6)
        
    def SenatePhase(self):
        print '-----------------------------------------'
        print "-- Senate Phase"
        # Determine ruling coalition (sorted by votes / money)
        self.factions = sorted(self.factions, reverse=True)
        totalVotes = 0
        for f in self.factions:
            totalVotes += f.votes
            f.ClearOffices()
        majorityVotes = (totalVotes // 2) + 1
        print 'Total votes', totalVotes, majorityVotes        
        # Determine factions in ruling coalition
        rulingCoalition = []
        if self.factions[0].votes >= majorityVotes:
            rulingCoalition.append(self.factions[0])
        elif self.factions[1].votes+self.factions[4].votes >= majorityVotes:
            rulingCoalition.append(self.factions[1])
            rulingCoalition.append(self.factions[4])
        elif self.factions[1].votes+self.factions[3].votes >= majorityVotes:
            rulingCoalition.append(self.factions[1])
            rulingCoalition.append(self.factions[3])
        elif self.factions[1].votes+self.factions[2].votes >= majorityVotes:
            rulingCoalition.append(self.factions[1])
            rulingCoalition.append(self.factions[2])
        elif self.factions[2].votes+self.factions[3].votes+self.factions[4].votes >= majorityVotes:
            rulingCoalition.append(self.factions[2])
            rulingCoalition.append(self.factions[3])
            rulingCoalition.append(self.factions[4])
        elif self.factions[0].votes+self.factions[4].votes >= majorityVotes:
            rulingCoalition.append(self.factions[0])
            rulingCoalition.append(self.factions[4])
        elif self.factions[0].votes+self.factions[3].votes >= majorityVotes:
            rulingCoalition.append(self.factions[0])
            rulingCoalition.append(self.factions[3])
        elif self.factions[0].votes+self.factions[2].votes >= majorityVotes:
            rulingCoalition.append(self.factions[0])
            rulingCoalition.append(self.factions[2])
        elif self.factions[0].votes+self.factions[1].votes >= majorityVotes:
            rulingCoalition.append(self.factions[0])
            rulingCoalition.append(self.factions[1])
        elif self.factions[1].votes+self.factions[2].votes+self.factions[3].votes+self.factions[4].votes >= majorityVotes:
            rulingCoalition.append(self.factions[1])
            rulingCoalition.append(self.factions[2])
            rulingCoalition.append(self.factions[3])
            rulingCoalition.append(self.factions[4])
        else:
            print 'No ruling coalition'
        spoils = ['Rome Council', 'Field Council', 'Censor']
        rIndx = 0
        # Determine spoils
        while len(spoils) > 0:
            print rIndx
            rulingCoalition[rIndx].SelectOffice(spoils[0])
            spoils.pop(0)
            rIndx += 1
            if rIndx >= len(rulingCoalition):
                rIndx = 0       
            
    def CombatPhase(self):
        print '-----------------------------------------'
        print "-- Combat Phase"
        
    def RevolutionPhase(self):
        print '-----------------------------------------'
        print "-- Revolution Phase"
        
# GUI runs in main thread
root = tk.Tk()
gui = RorGui.ROR_GUI(root)

# Create Game Engine    
engine = ROR(gui)
engine.GameSetup()
engine.start()

root.mainloop()        