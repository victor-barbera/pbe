import gi, threading, time, requests#, nfcReader, i2c
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk,Gdk


class Window(Gtk.Window) :
    def __init__(self) :
        Gtk.Window.__init__(self, title="COURSE MANAGER")
        
        container=Gtk.Box()
        self.add(container)
        container.show()
        
        self.login=Login(self)
        self.query=Query(self)
        container.add(self.login)
        container.add(self.query)
        self.login.show_all()

class Login(Gtk.Box):
    def __init__(self, parent_window):
        Gtk.Box.__init__(self, spacing=10)
        self.parent_window = parent_window
        # Creem un container vertical box:
        self.vBox = Gtk.VBox(spacing=6)
        self.add(self.vBox)
        
        # Afegim el label en un event box:
        self.evBox = Gtk.EventBox()
        self.evBox.set_size_request(400,100)
        self.evBox.set_name("eBox")
        self.label = Gtk.Label(label="Please, login with your university card")
        self.label.set_name("label")
        self.evBox.add(self.label)
        self.vBox.pack_start(self.evBox,True,True,6)
        
        self.button = Gtk.Button(label="SignIn")
        self.button.connect("clicked", self.onProva)
        self.vBox.pack_start(self.button,True,True,6)

        self.button = Gtk.Button(label="Error")
        self.button.connect("clicked", self.onError)
        self.vBox.pack_start(self.button,True,True,6)
        
        # Creem 2 estils amb CSS:
        self.blue = b"""
        #eBox {
            background-color: blue;
            border-radius: 10px;
        }
        """
        self.red = b"""
        #eBox {
            background-color: red;
            border-radius: 10px;
        }
        """
        self.white_type= b"""
        #label{
            color:white;
        }
        """
        self.style_provider = Gtk.CssProvider()
        self.style_provider.load_from_data(self.blue)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), self.style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        self.style_provider = Gtk.CssProvider()
        self.style_provider.load_from_data(self.white_type)
        Gtk.StyleContext.add_provider_for_screen(
           Gdk.Screen.get_default(), self.style_provider,
           Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
       )
        
        
    def onProva(self, button) :#això és per fer proves i s'haurà de canviar per la lectura del nfc
#      i2c.lcd_display_string("Welcome"+student_name)
        self.hide()
        self.parent_window.query.show_all()
    
    def onError(self,button) :
        self.label.set_text("Your ID is not in our list. Please try again")
        #threading.Thread(target=self.nfcThread, daemon=True).start()
        self.style_provider = Gtk.CssProvider()
        self.style_provider.load_from_data(self.white_type)
        Gtk.StyleContext.add_provider_for_screen(
           Gdk.Screen.get_default(), self.style_provider,
           Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
       )
        
        self.style_provider.load_from_data(self.red)
        Gtk.StyleContext.add_provider_for_screen(
           Gdk.Screen.get_default(), self.style_provider,
           Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
       )

    # def nfcThread(self) :
        
#     #rf = nfcReader.Rfid_reader("pn532_i2c:/dev/i2c-1")
#     #self.label.set_text("UID: " + rf.read_uid())
#     self.style_provider.load_from_data(self.red)
#     Gtk.StyleContext.add_provider_for_screen(
#         Gdk.Screen.get_default(), self.style_provider,
#         Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
#     )
#     #aqui aniria algo del pal si el id llegit esta dintre de student:
#     self.hide()
#   self.parent_window.query.show_all()
#     #else: mostrem missatge d'error (pero on?) i activem funció on error
        
class Query(Gtk.Box):#aqui tot per fer consultes
    def __init__(self, parent_window):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.set_size_request(400,100)
        self.parent_window = parent_window
        self.label = Gtk.Label(label="Welcome", xalign=0)#+student_name
        self.add(self.label)
        self.entry = Gtk.Entry()
        self.entry.set_text("table?constraint&constraint..")#aqui podem ficar el format que volem
        self.add(self.entry)
        self.entry.connect("activate", self.process_query)
        
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
            
        
    
    def process_query(self, widget):
        thread = threading.Thread(target=self.httpThread)
        thread.daemon = True
        thread.start()
        
    def httpThread(self) :
        res = requests.get("https://postman-echo.com/get/" + self.entry.get_text())
        createTable(self,res.json()["tableName"],res.json()["rows"])

        
if __name__ == "__main__" :
    win = Window()
    win.connect("destroy", Gtk.main_quit)
    win.show()
    #threading.Thread(target=win.nfcThread, daemon=True).start()
    Gtk.main()
    
