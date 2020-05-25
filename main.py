import gi, threading, time, requests, json, nfcReader#, i2c !s'ha de treure el json
gi.require_version("Gtk", "3.0")
from gi.repository import GLib,Gtk,Gdk

user = {
    "uid" : "00000000",
    "name" : "null"
    }

class Window(Gtk.Window) :
    def __init__(self) :
        Gtk.Window.__init__(self, title="MIRO CONNECTIVITY")
        self.set_default_size(500, 300)
        container=Gtk.Box()
        self.add(container)
        container.show()
        
        self.login=Login(self)
        self.query=Query(self)
        container.pack_start(self.login, True, True, 0)
        container.pack_start(self.query, True, True, 0)
        self.login.show_all()
        
        self.style_provider = Gtk.CssProvider()
        self.style_provider.load_from_path('estilitzat.css')
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), self.style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        
        
    def httpThread(self, query, table):
        res = requests.get("http://188.166.21.177:5000/" + query)
        print("http://188.166.21.177:5000/" + query)
        print(res.json())
        if(table): GLib.idle_add(self.query.createTable, res.json()["tableName"], res.json()["rows"])
        else:
            global user
            user["name"] = res.json()["name"]
            if(user["name"] != "null") :
                GLib.idle_add(self.hide)
                GLib.idle_add(self.parent_window.query.show_all)
            else:
                GLib.idle_add(self.login.set_label, "Your ID is not in our list. Please try again")
                GLib.idle_add(self.login.set_name, "loginError")
        # Per fer proves sense server.
        #res = '{"tableName" : "marks", "rows" : [["icom","guifre","4"],["dsbm", "victor", "8"]]}'
        #eljeison = json.loads(res)
#         self.createTable(eljeison["tableName"],eljeison["rows"])

class Login(Gtk.Box):
    def __init__(self, parent_window):
        Gtk.Box.__init__(self, spacing=30)
        self.parent_window = parent_window
        # Creem un container vertical box:
        self.vBox = Gtk.VBox(spacing=50)
        self.pack_start(self.vBox, True, False, 50)
        
        self.login=Gtk.Button(label="Please, login with your university card")
        self.entry = Gtk.Entry()
        self.entry.connect("activate", self.onLogin)
        
        self.login.set_name("login")
        self.login.set_property("width-request", 200)
        self.login.set_property("height-request", 50)
        self.login.connect("clicked", self.onLogin)#per fer proves sense nfc
        self.vBox.pack_start(self.login,True,False,0)
        self.vBox.pack_start(self.entry,True,False,0)

        #aixo quan hi ha el nfc no es posa
        self.button = Gtk.Button(label="Error")
        self.button.connect("clicked", self.onError)
        self.vBox.pack_start(self.button,True,True,6)
        threading.Thread(target=self.nfcThread, daemon=True).start()
        
        
        
        
    def onLogin(self, widget) :
        global user
        user["uid"] = self.entry.get_text()
        # self.parent_window.httpThread("login?student_id=" + user["uid"], False)
        # if(user["name"] != "null") :
        #     self.hide()
        #     self.parent_window.query.show_all()
        # else:
        #     self.login.set_label("Your ID is not in our list. Please try again")
        #     self.login.set_name("loginError")
        threading.Thread(target=self.parent_window.httpThread, args=["login?student_id=" + user["uid"], False], daemon = True).start()
        #self.parent_window.httpThread(self.entry.get_text(), True)
        #això és per fer proves i s'haurà de canviar per la lectura del nfc
#      i2c.lcd_display_string("Welcome"+student_name)
#         self.hide()
#         self.parent_window.query.show_all()
#         thread = threading.Thread(target=self.parent_window.httpThread, args=["login?id=" + self.uid , False])
#         thread.daemon = True
#         thread.start()

    
    def onError(self,button) :
        pass
#         self.login.set_label("Your ID is not in our list. Please try again")
#         self.login.set_name("loginError")
    
    
    def nfcThread(self) :
       rf = nfcReader.Rfid_reader("pn532_i2c:/dev/i2c-1")
       while(True) :
           global user
           user["uid"] = rf.read_uid()
           self.parent_window.httpThread("login?id=" + user["uid"], False) 
           if(user["name"] != "null") :
               self.hide()
               self.parent_window.query.show_all()
               break
           else:
               self.login.set_label("Your ID is not in our list. Please try again")
               self.login.set_name("loginError")
               print("hola")
               time.sleep(2)
        
        
class Query(Gtk.Box):#aqui tot per fer consultes
    def __init__(self, parent_window):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=30)
        self.parent_window = parent_window
        
        self.hBox = Gtk.HBox(spacing=5)
        self.add(self.hBox)
        self.label = Gtk.Label(label="Welcome", xalign=0)
        self.studentName = Gtk.Label(label = "")
        self.studentName.set_name('studentName')
        self.hBox.pack_start(self.label, False, True, 0)
        self.hBox.pack_start(self.studentName, False, True, 0)
        self.button = Gtk.Button(label="Log Out")
        self.button.connect("clicked", self.onLogOut)
        self.hBox.add(self.button)
        self.hBox.set_child_packing(self.button,False,True,0,1)
        self.entry = Gtk.Entry()
        self.entry.set_has_frame(True)
        #self.entry.set_text("table?constraint&constraint..")#aqui podem ficar el format que volem
        self.add(self.entry)
        self.entry.connect("activate", self.processQuery)
        
        
    def createTable(self, tableName, rows) :
        if(tableName == "timetables") :
            columns = ["day", "hour", "subject", "room"]
            listmodel = Gtk.ListStore(str, str, str, str)
        if(tableName == "tasks"):
            columns = ["date", "subject", "name"]
            listmodel = Gtk.ListStore(str, str, str)
        if(tableName == "marks"):
            columns = ["subject", "name", "mark"]
            listmodel = Gtk.ListStore(str, str, str)
#             {"tableName" : "timetables",
#              "rows" : [
#                 ["icom","guifre","4"],
#                 ["dsbm", "victor", "8"]
#             ]}
        # append the values in the model
        for i in range(len(rows)):
            listmodel.append(rows[i])
        # a treeview to see the data stored in the model
        self.view = Gtk.TreeView(model=listmodel)
        self.view.set_hexpand(True)
        # for each column
        for i, column in enumerate(columns):
            # cellrenderer to render the text
            cell = Gtk.CellRendererText()
            # the column is created
            col = Gtk.TreeViewColumn(column, cell, text=i)
            col.set_expand(True)
            # and it is appended to the treeview
            self.view.append_column(col)
        self.grid = Gtk.Grid()
        self.add(self.grid)
        self.grid.attach(self.view, 0, 0, 1, 1)
        
        #grid.attach(self.label, 0, 1, 1, 1)   
        self.grid.show_all()
        
        
    def processQuery(self, widget):
        thread = threading.Thread(target=self.parent_window.httpThread, args=[self.entry.get_text(), True])
        #self.parent_window.httpThread(self.entry.get_text(), True)
        thread.daemon = True
        thread.start()
        
    
    
    def onLogOut(self, button):
        self.parent_window.destroy()
        win = Window()
        win.connect("destroy", Gtk.main_quit)
        win.show()
        Gtk.main()
        
        
if __name__ == "__main__" :
    win = Window()
    win.connect("destroy", Gtk.main_quit)
    win.show()
    #threading.Thread(target=win.nfcThread, daemon=True).start()
    Gtk.main()
    
