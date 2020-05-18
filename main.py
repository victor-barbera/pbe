import gi, threading, time, nfcReader
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk,Gdk


class NfcWindow(Gtk.Window) :
	def __init__(self) :
		Gtk.Window.__init__(self, title="Lector RFID")
		
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
		
		self.button = Gtk.Button(label="Clear")
		self.button.connect("clicked", self.onClearClicked)
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
		
	def onClearClicked(self, button) :
		self.label.set_text("Please, login with your university card")
		self.style_provider.load_from_data(self.blue)
		Gtk.StyleContext.add_provider_for_screen(
			Gdk.Screen.get_default(), self.style_provider,
			Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
		)
		threading.Thread(target=self.nfcThread, daemon=True).start()
		
	def nfcThread(self) :
		rf = nfcReader.Rfid_reader("pn532_i2c:/dev/i2c-1")
		self.label.set_text("UID: " + rf.read_uid())
		self.style_provider.load_from_data(self.red)
		Gtk.StyleContext.add_provider_for_screen(
			Gdk.Screen.get_default(), self.style_provider,
			Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
		)
		
if __name__ == "__main__" :
	win = NfcWindow()
	win.connect("destroy", Gtk.main_quit)
	win.show_all()
	threading.Thread(target=win.nfcThread, daemon=True).start()
	Gtk.main()
	
