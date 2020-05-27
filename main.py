import gi, threading, time, requests#, nfcReader, RPi_I2C_driver
gi.require_version("Gtk", "3.0")
from gi.repository import GLib,Gtk,Gdk

user = {
    "uid" : "",
    "name" : ""
    }
table = {
    "rows" : [],
    "name" : "",
    }


class Window(Gtk.Window) :
    def __init__(self) :
        Gtk.Window.__init__(self, title="MIRO CONNECTIVITY")
        self.set_default_size(500, 300)
        container=Gtk.Box(spacing=6)
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
        
        
        
    def httpThread(self, query, action):
        res = requests.get("http://188.166.21.177:5000/" + query)
        print("http://188.166.21.177:5000/" + query)
        print(res.json())
        if(action == "table"):
            if(res.json()["message"] == "success"):
                global table
                table["name"] = res.json()["tableName"]
                table["rows"] = res.json()["rows"]
            else:
                table["name"] = res.json()["message"]
                table["rows"] = []
            GLib.idle_add(self.query.createTable)
        if(action == "login"):
            global user
            user["name"] = res.json()["name"]
            if user["name"] is not None:
                GLib.idle_add(self.query.studentName.set_text, user["name"])
                #threading.Thread(target=self.login.lcdThread, daemon=True).start()  
                GLib.idle_add(self.login.hide)
                GLib.idle_add(self.query.show_all)
            else:
                GLib.idle_add(self.login.label.set_name, "loginError")
                GLib.idle_add(self.login.label.set_text, "Your ID is not in our list. Please try again")


class Login(Gtk.Box):
    def __init__(self, parent_window):
        Gtk.Box.__init__(self, spacing=30)
        self.parent_window = parent_window
        # Creem un container vertical box:
        self.vBox = Gtk.VBox(spacing=50)
        self.pack_start(self.vBox, True, False, 50)
        
        self.label=Gtk.Label(label="Please, login with your university card")
        self.label.set_name("login")
        self.label.set_property("width-request", 200)
        self.label.set_property("height-request", 50)
        self.vBox.pack_start(self.label,True,False,0)
        
        self.entry = Gtk.Entry()
        self.entry.connect("activate", self.onLogin)
        self.vBox.pack_start(self.entry,True,False,0)

        # self.l=RPi_I2C_driver.lcd()
        # self.l.lcd_display_string_pos("Please, login with",2,1)
        # self.l.lcd_display_string("your university card",3)
        
        threading.Thread(target=self.nfcThread, daemon=True).start()
        
    def onLogin(self, widget) :
        global user
        user["uid"] = self.entry.get_text()
        threading.Thread(target=self.parent_window.httpThread, args=("login?student_id=" + user["uid"], "login"), daemon = True).start()
    
    def lcdThread(self):
        self.l.lcd_clear()
        self.l.lcd_display_string_pos("Welcome",2,6)
        self.l.lcd_display_string_pos(user["name"],3,3)

    def nfcThread(self) :
        rf = nfcReader.Rfid_reader("pn532_i2c:/dev/i2c-1")
        global user
        user["uid"] = rf.read_uid()
        threading.Thread(target=self.parent_window.httpThread, args=("login?student_id=" + user["uid"], "login"), daemon = True).start()
        
        
class Query(Gtk.Box):
    def __init__(self, parent_window):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=30)
        self.parent_window = parent_window
        
        self.hBox = Gtk.HBox(spacing=5)
        self.add(self.hBox)
        self.label = Gtk.Label(label="Welcome", xalign=0)
        self.studentName = Gtk.Label(label = user["name"])
        self.studentName.set_name('Name')
        self.hBox.pack_start(self.label, False, True, 0)
        self.hBox.pack_start(self.studentName, False, True, 0)

        self.button = Gtk.Button(label="Log Out")
        self.button.connect("clicked", self.onLogOut)
        self.hBox.add(self.button)
        self.hBox.set_child_packing(self.button,False,True,0,1)

        self.entry = Gtk.Entry()

        self.add(self.entry)
        self.entry.connect("activate", self.processQuery)

        self.view = Gtk.TreeView()
        self.table=Gtk.Label()

    def createTable(self) :
        global table
        tableName = table["name"]
        rows = table["rows"]
        self.table = Gtk.Label(label=tableName)
        self.table.set_name("Name")
        self.add(self.table)
        if(tableName == "timetables") :
            columns = ["day", "hour", "subject", "room"]
            listmodel = Gtk.ListStore(str, str, str, str)
        elif(tableName == "tasks"):
            columns = ["date", "subject", "name"]
            listmodel = Gtk.ListStore(str, str, str)
        elif(tableName == "marks"):
            columns = ["subject", "name", "mark"]
            listmodel = Gtk.ListStore(str, str, float)
        elif(tableName != ""):
           self.show_all()
           table["name"] = ""
           return
        else: return
            
        # append the values in the model
        for i in range(len(rows)):
            listmodel.append(rows[i])
        # a treeview to see the data stored in the model
        self.view = Gtk.TreeView(model=listmodel)
        self.view.set_hexpand(True)
        self.view.set_grid_lines(1)
        # for each column
        for i, column in enumerate(columns):
            # cellrenderer to render the text
            cell = Gtk.CellRendererText()
            # the column is created
            col = Gtk.TreeViewColumn(column, cell, text=i)
            col.set_expand(True)
            # and it is appended to the treeview
            self.view.append_column(col)
        self.add(self.view)
        self.show_all()
        table["name"] = ""
        table["rows"] = []
           
    def processQuery(self, widget):
        self.remove(self.view)
        self.remove(self.table)
        threading.Thread(target=self.parent_window.httpThread, args=(self.entry.get_text(), "table"), daemon=True).start()
           
    def onLogOut(self, button):
        threading.Thread(target=self.parent_window.httpThread, args=("logout", "logout"), daemon=True).start()
        self.parent_window.destroy()
        win = Window()
        win.connect("destroy", Gtk.main_quit)
        win.show()
        Gtk.main()
        
   
        
if __name__ == "__main__" :
    win = Window()
    win.connect("destroy", Gtk.main_quit)
    win.show()
    Gtk.main()
    
