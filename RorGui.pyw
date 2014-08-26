import Tkinter as tk
import ttk

###################################################
# A Frame Classes (BOTTOM)
###################################################
class StatusNotebook(ttk.Notebook):
    def __init__(self, master=None):
        ttk.Notebook.__init__(self, master)        
        self.pack(expand=tk.YES, fill=tk.BOTH)
        
    def InsertTab(self, newTabFrame, myTabName):
        self.add(newTabFrame, text=myTabName)
        
class PlayerStatus(ttk.Frame):
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master, padding=10)
        self.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
        # Create a tree view in the fame        
        self.ps = ttk.Treeview(master=self, show='tree')
        self.ps.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
        # Create a scrollbar        
        self.ysb = ttk.Scrollbar(self, orient='vertical', command=self.ps.yview)
        self.ysb.pack(side=tk.RIGHT, expand=tk.NO, fill=tk.Y)
        self.ps.configure(yscroll=self.ysb.set)
        
    def AddText(self, text):
        self.ps.insert('', 'end', text=text)

###################################################
# B Frame Classes (LEFT)
###################################################
class GamePhaseFrame(ttk.Frame):
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master, padding=10)
        self.pack(expand=tk.NO, fill=tk.X)
        self.make_widgets()
        
    def make_widgets(self):
        widget = ttk.Label(self, text=" MORTALITY ", borderwidth=10, relief=tk.RAISED)
        widget.pack(expand=tk.NO, fill=tk.X)
    
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
class TreeView(ttk.Frame):
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master, padding=10)
        self.pack(expand=tk.YES, fill=tk.BOTH)
        
        colStr = ("Name","Mil","Oratory","Inf","Pop","Knights")
        
        # Create a Treeview
        self.t = ttk.Treeview(master=self, columns=colStr, show='headings')
        self.t.pack(expand=tk.YES, fill=tk.BOTH)
        for c in colStr:
            self.t.heading(c, text=c.title())
            width = 40
            if c == "Name":
                width = 100
            self.t.column(c, width=width, stretch=0, anchor='center')
            
    def InsertItem(self, tup):
        self.t.insert('', 'end', values=tup)
        
class CenterNotebook(ttk.Notebook):
    def __init__(self, master=None):
        ttk.Notebook.__init__(self, master)        
        self.pack(expand=tk.YES, fill=tk.BOTH)
        
    def InsertTab(self, newTabFrame, myTabName):
        self.add(newTabFrame, text=myTabName)
        

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
        self.status = StatusNotebook(self.bottom_frame)       
        self.p1 = PlayerStatus(self.status)
        self.p2 = PlayerStatus(self.status)
        #self.p3 = PlayerStatus(self.status)
        #self.p4 = PlayerStatus(self.status)
        #self.p5 = PlayerStatus(self.status)
        
        self.status.InsertTab(self.p1, "P1")
        self.status.InsertTab(self.p2, "P2")
        #self.status.InsertTab(self.p3, "P3")
        #self.status.InsertTab(self.p4, "P4")
        #self.status.InsertTab(self.p5, "P5")
        
        self.p1.AddText("Hello my name is joe")
        self.p1.AddText("I have a wife and three kids")
        self.p2.AddText("Hello my name is joe")
        self.p2.AddText("I have a wife and three kids")
        self.p2.AddText("Hello my name is joe")
        self.p2.AddText("I have a wife and three kids")
        self.p2.AddText("Hello my name is joe")
        self.p2.AddText("I have a wife and three kids")
        self.p2.AddText("Hello my name is joe")
        self.p2.AddText("I have a wife and three kids")
        self.p2.AddText("Hello my name is joe")
        self.p2.AddText("I have a wife and three kids")
        self.p2.AddText("Hello my name is joe")
        self.p2.AddText("I have a wife and three kids")
        self.p2.AddText("Hello my name is joe")
        self.p2.AddText("I have a wife and three kids")
        self.p2.AddText("Hello my name is joe")
        self.p2.AddText("I have a wife and three kids")
        self.p2.AddText("Hello my name is joe")
        self.p2.AddText("I have a wife and three kids")
        self.p2.AddText("Hello my name is joe")
        self.p2.AddText("I have a wife and three kids")
        self.p2.AddText("Hello my name is joe")
        self.p2.AddText("I have a wife and three kids")
        self.p2.AddText("Hello my name is joe")
        self.p2.AddText("I have a wife and three kids")
        self.p2.AddText("Hello my name is joe")
        self.p2.AddText("I have a wife and three kids")
        self.p2.AddText("Hello my name is joe")
        self.p2.AddText("I have a wife and three kids")
        self.p2.AddText("Hello my name is joe")
        self.p2.AddText("I have a wife and three kids")
        self.p2.AddText("Hello my name is joe")
        self.p2.AddText("I have a wife and three kids")
        self.p2.AddText("Hello my name is joe")
        self.p2.AddText("I have a wife and three kids")
        self.p2.AddText("Hello my name is joe")
        self.p2.AddText("I have a wife and three kids")
        self.p2.AddText("Hello my name is joe")
        self.p2.AddText("I have a wife and three kids")
        self.p2.AddText("Hello my name is joe")
        self.p2.AddText("I have a wife and three kids")
        self.p2.AddText("Hello my name is joe")
        self.p2.AddText("I have a wife and three kids")
        self.p2.AddText("Hello my name is joe")
        self.p2.AddText("I have a wife and three kids")
        self.p2.AddText("Hello my name is joe")
        self.p2.AddText("I have a wife and three kids")
        self.p2.AddText("Hello my name is joe")
        self.p2.AddText("I have a wife and three kids")
        self.p2.AddText("Hello my name is joe")
        self.p2.AddText("I have a wife and three kids")
        self.p2.AddText("Hello my name is joe")
        self.p2.AddText("I have a wife and three kids")
        self.p2.AddText("Hello my name is joe")
        self.p2.AddText("I have a wife and three kids")
        self.p2.AddText("Hello my name is joe")
        self.p2.AddText("I have a wife and three kids")
        self.p2.AddText("Hello my name is joe")
        self.p2.AddText("I have a wife and three kids")
        self.p2.AddText("Hello my name is joe")
        self.p2.AddText("I have a wife and three kids")

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
        self.nb = CenterNotebook(self.top_frame)
        self.tree1 = TreeView(self.nb)
        self.tree2 = TreeView(self.nb)
        self.nb.InsertTab(self.tree1, "Tab1")
        self.nb.InsertTab(self.tree2, "Cato Family")
        
        self.tree1.InsertItem(("Steve", 1, 1, 1, 2, 0))
        self.tree2.InsertItem(("Cato the Elder", 1, 1, 1, 2, 0))
        self.tree2.InsertItem(("Cato the Younger", 1, 1, 1, 2, 0))
        self.tree2.InsertItem(("Cato the Dumber", 1, 1, 1, 2, 0))
        self.tree2.InsertItem(("Cato's Mom", 1, 1, 1, 2, 0))
        self.tree2.InsertItem(("Cato's Dad", 1, 1, 1, 2, 0))
        self.tree2.InsertItem(("Cato the Old Dud", 1, 1, 1, 2, 0))
        self.tree2.InsertItem(("Cato the Butler", 1, 1, 1, 2, 0))
        self.tree2.InsertItem(("Cato the Dogface", 1, 1, 1, 2, 0))
        self.tree2.InsertItem(("Cato the Very Loud Guy", 1, 1, 1, 2, 0))
        self.tree2.InsertItem(("Cato the Frog", 1, 1, 1, 2, 0))
        self.tree2.InsertItem(("Spartacus", 1, 1, 1, 2, 0))
        self.tree2.InsertItem(("Cato's mailman", 1, 1, 1, 2, 0))
        
        #self.forum = ttk.LabelFrame(self.top_frame, padding="3m", text="Forum")
        #self.forum.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)
        #self.war_frame = ttk.LabelFrame(self.top_frame, padding="3m", text="Wars")
        #self.war_frame.pack(side=tk.TOP, expand=tk.NO, fill=tk.BOTH)
        #self.t4 = ttk.Label(self.forum, text="first")
        #self.t4.pack()
        #self.t5 = ttk.Label(self.war_frame, text="second")
        #self.t5.pack()
        
root = tk.Tk()
app = ROR_GUI(root)
root.mainloop()        