import Tkinter as tk
import ttk
import sys

###################################################
# A Frame Classes (BOTTOM)
###################################################
class StatusNotebook(ttk.Notebook):
    def __init__(self, master=None):
        ttk.Notebook.__init__(self, master)        
        self.pack(expand=tk.YES, fill=tk.BOTH)
        
    def InsertTab(self, newTabFrame, myTabName):
        self.add(newTabFrame, text=myTabName)
        
class StdoutRedirector(ttk.Frame):
    def __init__(self, text_area):
        self.text_area = text_area
        
    def write(self, strg):
        self.text_area.insert(tk.END, strg)
        #self.text_area.AddText(strg)
        self.text_area.see(tk.END)

class CmdFrame(ttk.LabelFrame):
    def __init__(self, master=None):
        ttk.LabelFrame.__init__(self, master, text="Actions", padding=10)
        self.pack(expand=tk.NO, fill=tk.Y)

        # Create function pointer hooks        
        self.next_phase_hook = self.DummyFunc

        # Create buttons
        self.make_widgets()        
        
    def make_widgets(self):
        self.next_phase = ttk.Button(self, 
                                     command = lambda
                                     arg1='next_phase' :
                                     self.ButtonPressed(arg1))
        self.next_phase["text"] = "Next Phase"   ### (1)
        self.next_phase.pack()
        self.quit_game = ttk.Button(self, 
                                     command = lambda
                                     arg1='quit_game' :
                                     self.ButtonPressed(arg1))
        self.quit_game["text"] = "Quit"   ### (1)
        self.quit_game.pack()
    
    def ButtonPressed(self, arg1):
        try: 
            if arg1 == 'next_phase':
                self.next_phase_hook()
        except:
            print arg1 + ' Button press did not work'
            
    def AddHook(self,button,func):
        try:
            if button == 'next_phase':
                self.next_phase_hook = func
        except:
            print 'function hook did not work for' + button
        
    def DummyFunc(self):
        print 'Dummy Func'
    
###################################################
# B Frame Classes (LEFT)
###################################################
class GamePhaseFrame(ttk.LabelFrame):
    def __init__(self, master=None):
        ttk.LabelFrame.__init__(self, master, text="Game Status", padding=10)
        self.pack(expand=tk.NO, fill=tk.X)
        self.make_widgets()
        
    def make_widgets(self):
        self.TURN = tk.StringVar()
        self.TURN.set(" TURN 1 ")
        self.turn_label = ttk.Label(self, textvariable=self.TURN, borderwidth=10, relief=tk.RAISED)
        self.turn_label.pack(expand=tk.NO, fill=tk.X)
        
        self.PHASE = tk.StringVar()
        self.PHASE.set(" MORTALITY ")
        self.phase_label = ttk.Label(self, textvariable=self.PHASE, borderwidth=10, relief=tk.RAISED)
        self.phase_label.pack(expand=tk.NO, fill=tk.X)
        
    def SetPhase(self, turnNum, phaseText):
        self.TURN.set(" TURN %d " % (turnNum))
        self.PHASE.set(" %s " % (phaseText))
    
class StateFrame(ttk.LabelFrame):
    def __init__(self, master=None):
        ttk.LabelFrame.__init__(self, master, text="State Status", padding=10)
        self.pack(expand=tk.NO, fill=tk.X)
        self.make_widgets()
        
    def make_widgets(self):
        widget = ttk.Label(self, text=" UNREST LEVEL 0 ", borderwidth=10, relief=tk.RAISED)
        widget.pack(expand=tk.NO, fill=tk.X)
        widget6 = ttk.Label(self, text=" ")
        widget6.pack(expand=tk.NO, fill=tk.X)
        widget = ttk.Label(self, text=" TREASURY BALANCE 100 ", borderwidth=10, relief=tk.RAISED)
        widget.pack(expand=tk.NO, fill=tk.X)
        widget3 = ttk.Label(self, text="\n   Income  100")
        widget3.pack(expand=tk.NO, fill=tk.X)
        widget4 = ttk.Label(self, text="   Expenses 0")
        widget4.pack(expand=tk.NO, fill=tk.X)
        widget5 = ttk.Label(self, text="\n   Active Land Bills")
        widget5.pack(expand=tk.NO, fill=tk.X)
        widget6 = ttk.Label(self, text="      None")
        widget6.pack(expand=tk.NO, fill=tk.X)
    
class ActiveForcesFrame(ttk.LabelFrame):
    def __init__(self, master=None):
        ttk.LabelFrame.__init__(self, master, text="Active Forces", padding=10)
        self.pack(expand=tk.NO, fill=tk.X)
        self.make_widgets()
        
    def make_widgets(self):
        widget = ttk.Label(self, text=" Legions 4 ")
        widget.pack(expand=tk.NO, fill=tk.X)
        widget2 = ttk.Label(self, text=" Vetarians 0 ")
        widget2.pack(expand=tk.NO, fill=tk.X)
        widget3 = ttk.Label(self, text=" Fleet 2")
        widget3.pack(expand=tk.NO, fill=tk.X)
    
class EventFrame(ttk.LabelFrame):
    def __init__(self, master=None):
        ttk.LabelFrame.__init__(self, master, text="Active Events", padding=10)
        self.pack(expand=tk.YES, fill=tk.BOTH)
        self.make_widgets()
        
    def make_widgets(self):
        pass

###################################################
# C Frame Classes (TOP SIDE)
###################################################
class CenterNotebook(ttk.Notebook):
###########################################################################
# @brief User notebook frame
###########################################################################
    def __init__(self, master=None):
        ttk.Notebook.__init__(self, master)        
        self.pack(expand=tk.YES, fill=tk.BOTH)
        
    def InsertTab(self, newTabFrame, myTabName):
        ###########################################################################
        # @brief Insert frame into Notebook
        # @param newTabFrame - frame to add to notebook
        # @param myTabName - name of tab
        ###########################################################################
        self.add(newTabFrame, text=myTabName)
        
class FactionOverview(ttk.Frame):
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master, padding=10)
        self.pack(expand=tk.YES, fill=tk.BOTH)
        # Column string        
        colStr = ("Faction Name","Military","Oratory","Inf","Votes","Treasury","")
        # Create a Treeview
        self.t = ttk.Treeview(master=self, columns=colStr, show='headings')
        self.t.pack(expand=tk.YES, fill=tk.BOTH)
        for c in colStr:
            self.t.heading(c, text=c.title())
            width = 75
            an    = 'center'
            st    = 0
            if c == "Faction Name":
                width = 200
                an = 'w'
            elif c == "":
                st = 1
            self.t.column(c, width=width, stretch=st, anchor=an)
        
    def InsertItem(self, itemId, tup):
        ###########################################################################
        # @brief Insert item into list at the very end
        # @param itemId - new items iid
        # @param tup - New data
        ###########################################################################
        self.t.insert('', 'end', iid=itemId, values=tup)
        
    def ModifyItem(self, itemId, tup):
        ###########################################################################
        # @brief Modify item from the list where user provided the iid
        # @param itemId - iid of the item to delete
        # @param tup - New data
        ###########################################################################
        self.t.item(itemId, values=tup)
        x = self.t.set(itemId)
        return x
    
    def DeleteItem(self, itemId):
        ###########################################################################
        # @brief Delete item from the list where user provided the iid
        # @param itemId - iid of the item to delete
        ###########################################################################
        if self.t.exists(itemId):
            self.t.delete(itemId)
        
    def SortList(self, itemIdList):
        ###########################################################################
        # @brief Get a list of item ids and sort them in a list
        # @param itemIdList - list of iids for the faction tree
        ###########################################################################
        idx = 0
        for i in itemIdList:
            if self.t.exists(i):
                self.t.move(i, '', idx)
                idx += 1
                
class FactionView(ttk.Frame):
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master, padding=10)
        self.pack(expand=tk.YES, fill=tk.BOTH)
        # Column string
        colStr = ("Name","Military","Oratory","Inf","Pop","Loyalty","Knights","Votes","Money","Location","Concessions","")
        # Create a Treeview
        self.t = ttk.Treeview(master=self, columns=colStr, show='headings')
        self.t.pack(expand=tk.YES, fill=tk.BOTH)
        for c in colStr:
            self.t.heading(c, text=c.title())
            width = 50
            an    = 'center'
            st    = 0
            if c == "Name":
                width = 200
                an = 'w'
            elif c == "Location":
                width = 70
                an = 'center'
            elif c == "Concessions":
                width = 350
                an = 'w'
            elif c == "":
                st = 1
            self.t.column(c, width=width, stretch=st, anchor=an)
        
        # Setup binding
        self.t.bind("<Double-1>", self.OnDoubleClick)
            
    def InsertItem(self, itemId, tup):
        ###########################################################################
        # @brief Insert item into list at the very end
        # @param itemId - new items iid
        # @param tup - New data
        ###########################################################################
        self.t.insert('', 'end', iid=itemId, values=tup)
        
    def ModifyItem(self, itemId, tup):
        ###########################################################################
        # @brief Modify item from the list where user provided the iid
        # @param itemId - iid of the item to delete
        # @param tup - New data
        ###########################################################################
        if self.t.exists(itemId):
            self.t.item(itemId, values=tup)
            x = self.t.set(itemId)
            return x
    
    def DeleteItem(self, itemId):
        ###########################################################################
        # @brief Delete item from the list where user provided the iid
        # @param itemId - iid of the item to delete
        ###########################################################################
        if self.t.exists(itemId):
            self.t.delete(itemId)
            
    def SortList(self, itemIdList):
        ###########################################################################
        # @brief Get a list of item ids and sort them in a list
        # @param itemIdList - list of iids for the faction tree
        ###########################################################################
        idx = 0
        for i in itemIdList:
            if self.t.exists(i):
                self.t.move(i, '', idx)
                idx += 1
            
    def SortCol(self, col):
        print 'Sort by ', col
        x = self.t.get_children()
        #self.myFaction.senatorList = sorted(self.myFaction.senatorList, key=lambda sen: sen.influence, reverse=True)            
        return x
    
    def OnDoubleClick(self, event):
        tv = event.widget
        try:
            col = tv.identify_column(event.x)
            print col
        except:
            col = ''
        try:
            row = tv.identify_row(event.y)
            print row
        except:
            row = ''
        if (row == '') and (col != ''):
            self.SortCol(col)
                
class ROR_GUI:
    def __init__(self, master=None):
        # Setup Master Window fields
        master.title("Republic of Rome")
        master.geometry("1280x800")
        master.iconbitmap("question")
        
        # Window Layout
        # -----------------------
        # |left(B)| top frame   |
        # |frame  |    (C)      |
        # -----------------------
        # | bottom frame  (A)   |
        # -----------------------
        # Frame A
        self.bottom_frame = ttk.Frame(master, padding="3m")
        self.bottom_frame.pack(side=tk.BOTTOM, expand=tk.NO, fill=tk.X)
        
        # Frame B
        self.left_frame = ttk.Frame(master, padding="3m")
        self.left_frame.pack(side=tk.LEFT, expand=tk.NO, fill=tk.Y)
        
        # Frame C
        self.top_frame = ttk.Frame(master, padding="3m")
        self.top_frame.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)
        
        ###################################################
        # Populate A Frames (BOTTOM)
        ###################################################
        self.statusNotebook = StatusNotebook(self.bottom_frame)
        self.statusNotebook.pack(side=tk.LEFT)
        
        # Redirect stdout
        self.outputPanel = tk.Text(self.statusNotebook, wrap='word', height=15)
        self.statusNotebook.InsertTab(self.outputPanel, "LOG")
        sys.stdout = StdoutRedirector(self.outputPanel)
        
        # Cmd frame contains the various options user can select
        self.cmdFrame = CmdFrame(self.bottom_frame)
        self.cmdFrame.pack(side=tk.RIGHT)      

        ###################################################
        # Populate B Frames (LEFT SIDE)
        ###################################################
        self.phase   = GamePhaseFrame(self.left_frame)
        self.state   = StateFrame(self.left_frame)
        self.forces  = ActiveForcesFrame(self.left_frame)
        self.event   = EventFrame(self.left_frame)
        
        ###################################################
        # Populate C Frames (TOP)
        ###################################################
        self.factionNotebook = CenterNotebook(self.top_frame)
        self.factionOverview = FactionOverview() 
        self.factionNotebook.InsertTab(self.factionOverview, 'Factions')
        self.playerFaction   = []
        
    def AddPlayer(self, name):
        # Add player to faction notebook
        ret = FactionView(self.factionNotebook)
        self.factionNotebook.InsertTab(ret, name)
        self.playerFaction.append(ret)
        return ret, self.factionOverview
    