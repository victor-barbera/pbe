import gi, threading, time#, nfcReader
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
        self.style_provider = Gtk.CssProvider()
        self.style_provider.load_from_data(self.blue)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), self.style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
            
    def onProva(self, button) :
    #   i2c.lcd_display_string("Welcome"+student:_id)
        self.hide()
        self.parent_window.query.show_all()
    
    def onError(self, button) :
        self.label.set_text("Error")
        
    # def nfcThread(self) :
        
    #     #rf = nfcReader.Rfid_reader("pn532_i2c:/dev/i2c-1")
    #     #self.label.set_text("UID: " + rf.read_uid())
    #     self.style_provider.load_from_data(self.red)
    #     Gtk.StyleContext.add_provider_for_screen(
    #         Gdk.Screen.get_default(), self.style_provider,
    #         Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    #     )
    #     #aqui aniria algo del pal si el id llegit esta dintre de student:
    #     self._parent_window.query.show_all()
    #     self.hide()
    #     #else: mostrem missatge d'error (pero on?)
        
class Query(Gtk.Box):#aqui tot per fer consultes
    def __init__(self, parent_window):
        Gtk.Box.__init__(self, spacing=10)
        self.parent_window = parent_window
        self.label = Gtk.Label(label="query")
        self.add(self.label)
        #sha de tenir en compte que cridem del pal table?constraint&constraint&...
        #hauriem de fer un if per quan introduim cosillas(tasks, timetables, marks)
        #les cosillas han destar ordenades (notes->assignatura, treballs->data, horaris->data)
        #com agafo les coses de la BD?

# class NfcWindow(Gtk.Window) :
#   def __init__(self) :
#       Gtk.Window.__init__(self, title="COURSE MANAGER")

        
#       # Creem un container vertical box:
#       self.vBox = Gtk.VBox(spacing=6)
#       self.add(self.vBox)
        
#       # Afegim el label en un event box:
#       self.evBox = Gtk.EventBox()
#       self.evBox.set_size_request(400,100)
#       self.evBox.set_name("eBox")
#       self.label = Gtk.Label(label="Please, login with your university card")
#       self.evBox.add(self.label)
#       self.vBox.pack_start(self.evBox,True,True,6)
        
#       self.button = Gtk.Button(label="Clear")
#       self.button.connect("clicked", self.onClearClicked)
#       self.vBox.pack_start(self.button,True,True,6)
        
#       # Creem 2 estils amb CSS:
#       self.blue = b"""
#       #eBox {
#           background-color: blue;
#           border-radius: 10px;
#       }
#       """
#       self.red = b"""
#       #eBox {
#           background-color: red;
#           border-radius: 10px;
#       }
#       """
#       self.style_provider = Gtk.CssProvider()
#       self.style_provider.load_from_data(self.blue)
#       Gtk.StyleContext.add_provider_for_screen(
#           Gdk.Screen.get_default(), self.style_provider,
#           Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
#       )
        
#   def onClearClicked(self, button) :
#       self.label.set_text("Please, login with your university card")
#       self.style_provider.load_from_data(self.blue)
#       Gtk.StyleContext.add_provider_for_screen(
#           Gdk.Screen.get_default(), self.style_provider,
#           Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
#       )
#       threading.Thread(target=self.nfcThread, daemon=True).start()
        
#   def nfcThread(self) :
#       rf = nfcReader.Rfid_reader("pn532_i2c:/dev/i2c-1")
#       self.label.set_text("UID: " + rf.read_uid())
#       self.style_provider.load_from_data(self.red)
#       Gtk.StyleContext.add_provider_for_screen(
#           Gdk.Screen.get_default(), self.style_provider,
#           Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
#       )
        
if __name__ == "__main__" :
    win = Window()
    win.connect("destroy", Gtk.main_quit)
    win.show()
    #threading.Thread(target=win.nfcThread, daemon=True).start()
    Gtk.main()
    
