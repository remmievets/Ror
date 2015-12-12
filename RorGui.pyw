import Tkinter as tk
import ttk
import sys

#==========================================================================
# Miscellaneous classes to support display
#==========================================================================
class MyNotebook(ttk.Notebook):
    ###########################################################################
    # @brief User notebook frame
    ###########################################################################
    def __init__(self, master=None):
        ###########################################################################
        # @brief Initialization of my notebook frame
        # @param master
        ###########################################################################   
        ttk.Notebook.__init__(self, master)        
        self.pack(expand=tk.YES, fill=tk.BOTH)
        
    def InsertTab(self, newTabFrame, myTabName):
        ###########################################################################
        # @brief Insert frame into Notebook
        # @param newTabFrame - frame to add to notebook
        # @param myTabName - name of tab
        ###########################################################################
        self.add(newTabFrame, text=myTabName)

class BaseTreeView(ttk.Frame):
    ###########################################################################
    # @brief Base tree view for ROR
    ###########################################################################
    def __init__(self, columnList, master=None):
        ###########################################################################
        # @brief Initialization of base treeview frame
        # @param columnList - list of columns to add to treeview
        # @param master - owner of this frame
        ###########################################################################   
        ttk.Frame.__init__(self, master, padding=10)
        self.pack(expand=tk.YES, fill=tk.BOTH)
        # Create a Treeview
        self.t = ttk.Treeview(master=self, columns=columnList, show='headings')
        self.t.pack(expand=tk.YES, fill=tk.BOTH)        
        # Setup binding
        self.t.bind("<Double-1>", self.OnDoubleClick)
        # Undefined variables
        self.sortColumnNumber = None
            
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
        # @return Return data from the column if item exists
        ###########################################################################
        if self.t.exists(itemId):
            self.t.item(itemId, values=tup)
            x = self.t.set(itemId)
            return x
        else:
            self.InsertItem(itemId, tup)
    
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
            
    def GetSortCol(self):
        ###########################################################################
        # @brief Return column which user requested to sort view by
        # @return column iid of column to sort by
        ###########################################################################
        return self.sortColumnNumber
    
    def OnDoubleClick(self, event):
        ###########################################################################
        # @brief Event to execute on a double click.  Allows user to sort by col
        # @param event - Details on the user event
        ###########################################################################
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
            self.sortColumnNumber = col
            print 'Sort column by ', col
            
#==========================================================================
# A Frame Classes (BOTTOM)
#==========================================================================
class StdoutRedirector(ttk.Frame):
    def __init__(self, text_area):
        self.text_area = text_area
        
    def write(self, strg):
        self.text_area.insert(tk.END, strg)
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
    
#==========================================================================
# B Frame Classes (LEFT)
#==========================================================================
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
        self.UNREST = tk.StringVar()
        self.UNREST.set(" UNREST 0 ")
        self.unrest_label = ttk.Label(self, textvariable=self.UNREST, borderwidth=10, relief=tk.RAISED)
        self.unrest_label.pack(expand=tk.NO, fill=tk.X)
        self.spacer = ttk.Label(self, text=" ")
        self.spacer.pack(expand=tk.NO, fill=tk.X)
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
        
    def SetUnrestLevel(self, val):
        self.UNREST.set(" UNREST %d " % (val))
    
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

#==========================================================================
# C Frame Classes (TOP SIDE)
#==========================================================================
class FactionOverview(BaseTreeView):
    def __init__(self, master=None):
        # Column string
        colStr = ("Faction Name","Military","Oratory","Inf","Votes","Treasury","")
        BaseTreeView.__init__(self, colStr, master)
        # Setup heading and column size
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
                        
class FactionView(BaseTreeView):
    def __init__(self, master=None):
        # Column string
        colStr = ("Name","Military","Oratory","Inf","Pop","Loyalty","Knights","Votes","Money","Location","Concessions","")
        BaseTreeView.__init__(self, colStr, master)
        # Setup heading and column size
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
            
class ForumView(BaseTreeView):
    def __init__(self, master=None):
        # Column string
        colStr = ("Type","Description","Info","")
        BaseTreeView.__init__(self, colStr, master)
        # Setup heading and column size
        for c in colStr:
            self.t.heading(c, text=c.title())
            width = 50
            an    = 'center'
            st    = 0
            if c == "Type":
                width = 100
                an = 'w'
            elif c == "Description":
                width = 200
                an = 'w'
            elif c == "Info":
                width = 700
                an = 'w'
            elif c == "":
                width = 50
                st = 1
            self.t.column(c, width=width, stretch=st, anchor=an)
            
class WarView(BaseTreeView):
    def __init__(self, master=None):
        # Column string
        colStr = ("Name","Status","Str","Flt Sup","Flt Str","Reward","Information","")
        BaseTreeView.__init__(self, colStr, master)
        # Setup heading and column size
        for c in colStr:
            self.t.heading(c, text=c.title())
            width = 50
            an    = 'center'
            st    = 0
            if c == "Name":
                width = 150
                an = 'w'
            elif c == "Status":
                width = 100
            elif c == "Information":
                width = 500
                an = 'w'
            elif c == "":
                width = 50
                st = 1
            self.t.column(c, width=width, stretch=st, anchor=an)
            
#==========================================================================
# Top level display interface
#==========================================================================
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
        self.statusNotebook = MyNotebook(self.bottom_frame)
        self.statusNotebook.pack(side=tk.LEFT)
        
        # Redirect stdout
        self.outputPanel = tk.Text(self.statusNotebook, wrap='word', height=15)
        self.statusNotebook.InsertTab(self.outputPanel, "LOG")
        sys.stdout = StdoutRedirector(self.outputPanel)
        
        # Forum items
        self.forumTab = ForumView(self.statusNotebook)
        self.statusNotebook.InsertTab(self.forumTab, "FORUM")
        
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
        self.factionNotebook = MyNotebook(self.top_frame)
        self.factionOverview = FactionOverview() 
        self.factionNotebook.InsertTab(self.factionOverview, 'Factions')
        self.playerFaction   = []
        
        # Wars
        self.warsTab = WarView(self.factionNotebook)
        self.factionNotebook.InsertTab(self.warsTab, "WARS")
        
    def AddPlayer(self, name):
        # Add player to faction notebook
        ret = FactionView(self.factionNotebook)
        self.factionNotebook.InsertTab(ret, name)
        self.playerFaction.append(ret)
        return ret, self.factionOverview
    