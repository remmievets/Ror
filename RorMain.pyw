import Tkinter as tk
import threading
import Queue
import random

import RorGui
import RorUtils

from RorData import *
from RorPlayer import *
from RorFaction import Faction
from RorSenator import *
from RorWar import *

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
        roll = RorUtils.Roll2d6()
        if roll[0] == 7:
            roll = RorUtils.Roll3d6()
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
        result = RorUtils.Roll3d6()[0] - self.unrest + hrao[0].pop
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