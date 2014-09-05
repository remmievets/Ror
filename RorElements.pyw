import Tkinter as tk
import random
import threading
import RorGui
import Queue

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

    
def Roll1d6(self):
###########################################################################
# @brief Roll 1 six sided dice
#
# @return die 1 result
###########################################################################
    return random.randint(1,6)
        
def Roll2d6(self):
###########################################################################
# @brief Roll 2 six sided dice
#
# @return total, die 1 result, die 2 result
###########################################################################
    die1 = random.randint(1,6)
    die2 = random.randint(1,6)
    total = die1 + die2
    return total, die1, die2

def Roll3d6(self):
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
            print addIndex
            self.senatorList.insert(addIndex, newSen)
        # Adjust faction ratings
        self.milRating += milR
        self.infRating += infR
        self.ortRating += ortR
        self.votes     += ortR
        # Add to frame
        if addToFrame:
            self.myPlayer.playerFrameId.InsertItem(newSen.famId, newSen.GetTup())
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
        self.votes     -= sen.oratory + sen.knights        
        # Adjust lists
        self.senatorList.remove(sen)
        self.myPlayer.playerFrameId.DeleteItem(sen.famId)
        
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
    
    def GetTup(self):
        #colStr = ("Faction Name","Military","Oratory","Inf","Votes","Treasury","")
        return (self.name, self.milRating, self.ortRating, self.infRating, self.votes, self.treasury)
    
    def dump(self):
        print "---------------"
        print "Faction : %s  Sen Cnt (%d)" % (self.name,len(self.senatorList))
        print " MIL %d   INF %d   VOTES %d   TREASURY %d" % (self.milRating,self.infRating,self.votes,self.treasury)
        for s in self.senatorList:
            s.dump()

class Player():
###########################################################################
# @brief
#    Base class for player type
###########################################################################
    def __init__(self, faction, name):
        self.myFaction = faction
        self.name = name
        # Link Player and Faction
        self.myFaction.AssignPlayer(self)
        
    def CreatePlayerFrame(self, gui):
        # create frame for player data        
        self.playerFrameId, self.overviewId = gui.AddPlayer(self.myFaction.name)
        self.gui = gui
            
    def CollectPersonalRevenue(self):
        # Do nothing in base class
        pass
        
    def Phase2Action_Charity(self):
        self.x = 2
        
    def InitialFrame(self):        
        # Update frame with senator data
        for s in self.myFaction.senatorList:
            self.playerFrameId.InsertItem(s.famId, s.GetTup())
        # Update Faction data
        self.overviewId.InsertItem(self.myFaction.name, self.myFaction.GetTup())
            
    def UpdateFrame(self):        
        # Update frame with senator data
        for s in self.myFaction.senatorList:
            self.playerFrameId.ModifyItem(s.famId, s.GetTup())
        # Update Faction data
        self.overviewId.ModifyItem(self.myFaction.name, self.myFaction.GetTup())

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
        self.myFaction.senatorList[0].priorCouncil  = True
    
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
        self.turn  = 1
        self.phase = 0        
        self.setup = False
        self.curiaFamilies    = []
        self.curiaLeaders     = []
        self.curiaConcessions = []
        self.wars             = []
        self.forum            = []
        
        # Action queue
        self.jobQueue = Queue.Queue()
        
    def run(self):
        ###########################################################################
        # @brief Game processing thread
        ###########################################################################
        # Update display info
        for f in self.factions:
            f.myPlayer.InitialFrame()
        print 'Starting game engine thread'
        forever = True
        while forever:
            # Update display info
            self.factions = sorted(self.factions, reverse=True)
            for f in self.factions:
                f.myPlayer.UpdateFrame()
            # Block forever until user requests something
            job = self.jobQueue.get(block=True)
            if job == 'next_phase':
                self.phase += 1            
                self.GameTurn()
            
        print 'Game Over!'
            
    def CmdNextPhase(self):
        print 'CmdNextPhase pressed - added to job queue'
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
            p.CreatePlayerFrame(self.gui)
            if p.myFaction.name == 'Populists':
                p.myFaction.SelectOffice('Rome Council')
            
        # Assign callback for next phase button
        self.gui.cmdFrame.AddHook('next_phase', self.CmdNextPhase)
    
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
                    print 'cont - already in list redo pick'
                    picksRemaining += 1
                    continue
                else:
                    killList.append(killme)
            elif killme <= 32:
                # pick two more
                picksRemaining += 2
        return killList

    def MortalityPhase(self):
        ###########################################################################
        # @brief Execute Mortality Phase of the game turn.  Draws 1 mortality chit
        #        and process the results.  No user interaction needed.
        ###########################################################################
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
        
# GUI runs in main thread
root = tk.Tk()
gui = RorGui.ROR_GUI(root)

# Create Game Engine    
engine = ROR(gui)
engine.GameSetup()
engine.start()

root.mainloop()        