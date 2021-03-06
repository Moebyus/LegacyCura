__copyright__ = "Released under terms of the AGPLv3 License"


import wx
import wx.wizard


from Cura.util import machineCom
from Cura.util import profile
from Cura.util import resources


from Cura.util import moebyusFactory


class MoebyusInfoPage(wx.wizard.WizardPageSimple):
	def __init__(self, parent, title):
		wx.wizard.WizardPageSimple.__init__(self, parent)

		sizer = wx.GridBagSizer(5, 5)
		self.sizer = sizer
		self.SetSizer(sizer)

		title = wx.StaticText(self, -1, title)
		title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
		sizer.Add(title, pos=(0, 0), span=(1, 2), flag=wx.ALIGN_CENTRE | wx.ALL)
		sizer.Add(wx.StaticLine(self, -1), pos=(1, 0), span=(1, 2), flag=wx.EXPAND | wx.ALL)
		sizer.AddGrowableCol(1)

		self.rowNr = 2

	def AddText(self, info):
		text = wx.StaticText(self, -1, info)
		self.GetSizer().Add(text, pos=(self.rowNr, 0), span=(1, 2), flag=wx.LEFT | wx.RIGHT)
		self.rowNr += 1
		return text

	def AddSeperator(self):
		self.GetSizer().Add(wx.StaticLine(self, -1), pos=(self.rowNr, 0), span=(1, 2), flag=wx.EXPAND | wx.ALL)
		self.rowNr += 1

	def AddHiddenSeperator(self):
		self.AddText("")

	def AddInfoBox(self):
		infoBox = InfoBox(self)
		self.GetSizer().Add(infoBox, pos=(self.rowNr, 0), span=(1, 2), flag=wx.LEFT | wx.RIGHT | wx.EXPAND)
		self.rowNr += 1
		return infoBox

	def AddRadioButton(self, label, style=0):
		radio = wx.RadioButton(self, -1, label, style=style)
		self.GetSizer().Add(radio, pos=(self.rowNr, 0), span=(1, 2), flag=wx.EXPAND | wx.ALL)
		self.rowNr += 1
		return radio

	def AddCheckbox(self, label, checked=False):
		check = wx.CheckBox(self, -1)
		text = wx.StaticText(self, -1, label)
		check.SetValue(checked)
		self.GetSizer().Add(text, pos=(self.rowNr, 0), span=(1, 1), flag=wx.LEFT | wx.RIGHT)
		self.GetSizer().Add(check, pos=(self.rowNr, 1), span=(1, 2), flag=wx.ALL)
		self.rowNr += 1
		return check

	def AddButton(self, label):
		button = wx.Button(self, -1, label)
		self.GetSizer().Add(button, pos=(self.rowNr, 0), span=(1, 2), flag=wx.LEFT)
		self.rowNr += 1
		return button

	def AddDualButton(self, label1, label2):
		button1 = wx.Button(self, -1, label1)
		self.GetSizer().Add(button1, pos=(self.rowNr, 0), flag=wx.RIGHT)
		button2 = wx.Button(self, -1, label2)
		self.GetSizer().Add(button2, pos=(self.rowNr, 1))
		self.rowNr += 1
		return button1, button2

	def AddTextCtrl(self, value):
		ret = wx.TextCtrl(self, -1, value)
		self.GetSizer().Add(ret, pos=(self.rowNr, 0), span=(1, 2), flag=wx.LEFT)
		self.rowNr += 1
		return ret

	def AddLabelTextCtrl(self, info, value):
		text = wx.StaticText(self, -1, info)
		ret = wx.TextCtrl(self, -1, value)
		self.GetSizer().Add(text, pos=(self.rowNr, 0), span=(1, 1), flag=wx.LEFT)
		self.GetSizer().Add(ret, pos=(self.rowNr, 1), span=(1, 1), flag=wx.LEFT)
		self.rowNr += 1
		return ret

	def AddTextCtrlButton(self, value, buttonText):
		text = wx.TextCtrl(self, -1, value)
		button = wx.Button(self, -1, buttonText)
		self.GetSizer().Add(text, pos=(self.rowNr, 0), span=(1, 1), flag=wx.LEFT)
		self.GetSizer().Add(button, pos=(self.rowNr, 1), span=(1, 1), flag=wx.LEFT)
		self.rowNr += 1
		return text, button

	def AddBitmap(self, bitmap):
		bitmap = wx.StaticBitmap(self, -1, bitmap)
		self.GetSizer().Add(bitmap, pos=(self.rowNr, 0), span=(1, 2), flag=wx.LEFT | wx.RIGHT)
		self.rowNr += 1
		return bitmap

	def AddCheckmark(self, label, bitmap):
		check = wx.StaticBitmap(self, -1, bitmap)
		text = wx.StaticText(self, -1, label)
		self.GetSizer().Add(text, pos=(self.rowNr, 0), span=(1, 1), flag=wx.LEFT | wx.RIGHT)
		self.GetSizer().Add(check, pos=(self.rowNr, 1), span=(1, 1), flag=wx.ALL)
		self.rowNr += 1
		return check

	def AddCombo(self, label, options):
		combo = wx.ComboBox(self, -1, options[0], choices=options, style=wx.CB_DROPDOWN|wx.CB_READONLY)
		text = wx.StaticText(self, -1, label)
		self.GetSizer().Add(text, pos=(self.rowNr, 0), span=(1, 1), flag=wx.LEFT | wx.RIGHT)
		self.GetSizer().Add(combo, pos=(self.rowNr, 1), span=(1, 1), flag=wx.LEFT | wx.RIGHT)
		self.rowNr += 1
		return combo

	def AllowNext(self):
		return True

	def AllowBack(self):
		return True

	def StoreData(self):
		pass


class moebyusFirmwareSelector(wx.Dialog) :
	def __init__(self, parent = None)  :
		super(moebyusFirmwareSelector, self).__init__(parent=parent, title="Cargador de Firmware Moebyus Machines", size=(800, 700))

		sizer = wx.GridBagSizer(5, 5)
		self.sizer = sizer
		self.SetSizer(sizer)

		sizer.AddGrowableCol(0)
		self.rowNr = 0
		
		
		self.machineSelection 	= []
		self.lcdSelection 		= []
		self.extruderSelection 	= []
		self.XYSelection 		= []
		self.ZSelection 		= []

		self.machines = [
					("Prusa I3\t\t\t(200x200x200)"			,"PrusaI3MM"),
					("Prusa MM - L\t\t(200x300x200)"		,"PrusaI3MM-L"),
					("Steel MM\t\t\t(200x200x200)"			,"SteelMM"),
					("Steel MM - L\t\t(300x200x200)"		,"SteelMM-L"),
					("Steel MM Marco Sirius\t(300x200x260)"	,"SteelMM-Sirius"),
					("Steel MM S303030\t\t(300x300x300)"	,"SteelMM-S303030"),
					("Melta Kossel\t\t(160x300)"			,"Melta"),
					("[SIRIUS] 1.0\t\t(300x200x200)"		,"Sirius1"),
					("[SIRIUS] 1.1\t\t(300x200x250)"		,"Sirius11")]

		self.lcds = [ ('LCD Full Graphic'  , 'lcdFull') ,
					  ('LCD Smart Discount', 'lcdSmart') ]

		self.extruders = [ ('MK8 Directo'	, 'MK8') ,
						   ('Wades Jhonas'	, 'Wades') ]
						   
		self.XYTypes = [ ('XY GT2'  , 'XYGT2') ,
					  ('XY Husillo', 'XYHusillo') ]

		self.ZTypes = [ ('Z M5'   , 'ZM5') ,
					  ('Z Husillo', 'ZHusillo') ]
					  				   
		self.machineType  = self.machines	[0][1]
		self.lcdType      = self.lcds		[0][1]
		self.extruderType = self.extruders	[0][1]
		self.XYType		  = self.XYTypes	[0][1] 
		self.ZType		  = self.ZTypes		[0][1]
		
		
		title = wx.StaticText(self, -1, 'Selecciona modelo de maquina:')
		title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
		self.GetSizer().Add(title, pos=(self.rowNr, 0), span=(1, 2), flag=wx.EXPAND | wx.ALL)
		self.rowNr += 1
		self.GetSizer().Add(wx.StaticLine(self, -1), pos=(self.rowNr, 0), span=(1, 2), flag=wx.EXPAND | wx.ALL)
		self.rowNr += 1
		

		bitmap = wx.Bitmap(resources.getPathForImage(moebyusFactory.getMachineThumb('PrusaI3MM')))
		self.previewBitmap = wx.StaticBitmap(self, -1, bitmap)
		self.GetSizer().Add(self.previewBitmap, pos=(1, 3), span=(14, 2), flag=wx.LEFT | wx.RIGHT)
		self.rowNr += 1

		i = 0;
		for machine in self.machines:
			if i == 0:
				item = wx.RadioButton(self, -1, machine[0] , style=wx.RB_GROUP)
				self.GetSizer().Add(item, pos=(self.rowNr, 0), span=(1, 2))
				self.rowNr += 1
				i+=1;
				item.data = machine[1:]
				self.machineSelection.append(item)
				item.Bind(wx.EVT_RADIOBUTTON, self.onMachineSelect)
			else:
				item = wx.RadioButton(self, -1, machine[0])
				self.GetSizer().Add(item, pos=(self.rowNr, 0), span=(1, 2))
				self.rowNr += 1
				i+=1;
				item.data = machine[1:]
				self.machineSelection.append(item)
				item.Bind(wx.EVT_RADIOBUTTON, self.onMachineSelect)


		title = wx.StaticText(self, -1, 'Tipo de LCD:')
		title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
		self.GetSizer().Add(title, pos=(self.rowNr, 0), span=(1, 2),flag=wx.EXPAND | wx.ALL)
		self.rowNr += 1
		self.GetSizer().Add(wx.StaticLine(self, -1), pos=(self.rowNr, 0), span=(1, 2), flag=wx.EXPAND | wx.ALL)
		self.rowNr += 1
		i = 0
		for lcd in self.lcds:
			if i == 0:
				item = wx.RadioButton(self, -1, lcd[0] , style=wx.RB_GROUP)
				self.GetSizer().Add(item, pos=(self.rowNr, 0), span=(1, 2))
				self.rowNr += 1
				i+=1;
				item.data = lcd[1:]
				self.lcdSelection.append(item)
				item.Bind(wx.EVT_RADIOBUTTON, self.onLcdSelect)
			else:
				item = wx.RadioButton(self, -1, lcd[0])
				self.GetSizer().Add(item, pos=(self.rowNr, 0), span=(1, 2))
				self.rowNr += 1
				i+=1;
				item.data = lcd[1:]
				self.lcdSelection.append(item)
				item.Bind(wx.EVT_RADIOBUTTON, self.onLcdSelect)

		self.GetSizer().Add(wx.StaticLine(self, -1), pos=(self.rowNr, 0), span=(1, 2), flag=wx.EXPAND | wx.ALL)
		self.rowNr += 1


		title = wx.StaticText(self, -1, 'Tipo de Extrusor:')
		title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
		self.GetSizer().Add(title, pos=(self.rowNr, 0), span=(1, 2),flag=wx.EXPAND | wx.ALL)
		self.rowNr += 1
		self.GetSizer().Add(wx.StaticLine(self, -1), pos=(self.rowNr, 0), span=(1, 2), flag=wx.EXPAND | wx.ALL)
		self.rowNr += 1
		i = 0
		for ex in self.extruders:
			if i == 0:
				item = wx.RadioButton(self, -1, ex[0] , style=wx.RB_GROUP)
				self.GetSizer().Add(item, pos=(self.rowNr, 0), span=(1, 2))
				self.rowNr += 1
				i+=1;
				item.data = ex[1:]
				self.extruderSelection.append(item)
				item.Bind(wx.EVT_RADIOBUTTON, self.onExtruderSelect)
			else:
				item = wx.RadioButton(self, -1, ex[0])
				self.GetSizer().Add(item, pos=(self.rowNr, 0), span=(1, 2))
				self.rowNr += 1
				i+=1;
				item.data = ex[1:]
				self.extruderSelection.append(item)
				item.Bind(wx.EVT_RADIOBUTTON, self.onExtruderSelect)


		self.secondRow = 16
		
		self.GetSizer().Add(wx.StaticLine(self, -1), pos=(self.secondRow, 3), span=(1, 2), flag=wx.EXPAND | wx.ALL)
		self.secondRow += 1

		title = wx.StaticText(self, -1, 'Sistema XY:')
		title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
		self.GetSizer().Add(title, pos=(self.secondRow, 3), span=(1, 2),flag=wx.EXPAND | wx.ALL)
		self.secondRow += 1
		self.GetSizer().Add(wx.StaticLine(self, -1), pos=(self.secondRow, 3), span=(1, 2), flag=wx.EXPAND | wx.ALL)
		self.secondRow += 1
		i = 0
		for xyt in self.XYTypes:
			if i == 0:
				item = wx.RadioButton(self, -1, xyt[0] , style=wx.RB_GROUP)
				self.GetSizer().Add(item, pos=(self.secondRow, 3), span=(1, 2))
				self.secondRow += 1
				i+=1;
				item.data = xyt[1:]
				self.XYSelection.append(item)
				item.Bind(wx.EVT_RADIOBUTTON, self.onXYSelect)
			else:
				item = wx.RadioButton(self, -1, xyt[0])
				self.GetSizer().Add(item, pos=(self.secondRow, 3), span=(1, 2))
				self.secondRow += 1
				i+=1;
				item.data = xyt[1:]
				self.XYSelection.append(item)
				item.Bind(wx.EVT_RADIOBUTTON, self.onXYSelect)

		self.GetSizer().Add(wx.StaticLine(self, -1), pos=(self.secondRow, 3), span=(1, 2), flag=wx.EXPAND | wx.ALL)
		self.secondRow += 1
		
		title = wx.StaticText(self, -1, 'Sistema Z:')
		title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
		self.GetSizer().Add(title, pos=(self.secondRow, 3), span=(1, 2),flag=wx.EXPAND | wx.ALL)
		self.secondRow += 1
		self.GetSizer().Add(wx.StaticLine(self, -1), pos=(self.secondRow, 3), span=(1, 2), flag=wx.EXPAND | wx.ALL)
		self.secondRow += 1
		i = 0
		for zt in self.ZTypes:
			if i == 0:
				item = wx.RadioButton(self, -1, zt[0] , style=wx.RB_GROUP)
				self.GetSizer().Add(item, pos=(self.secondRow, 3), span=(1, 2))
				self.secondRow += 1
				i+=1;
				item.data = zt[1:]
				self.ZSelection.append(item)
				item.Bind(wx.EVT_RADIOBUTTON, self.onZSelect)
			else:
				item = wx.RadioButton(self, -1, zt[0])
				self.GetSizer().Add(item, pos=(self.secondRow, 3), span=(1, 2))
				self.secondRow += 1
				i+=1;
				item.data = zt[1:]
				self.ZSelection.append(item)
				item.Bind(wx.EVT_RADIOBUTTON, self.onZSelect)

		self.GetSizer().Add(wx.StaticLine(self, -1), pos=(self.secondRow, 3), span=(1, 2), flag=wx.EXPAND | wx.ALL)
		self.secondRow += 1

		button_sizer = wx.BoxSizer(wx.HORIZONTAL)
		okButton = wx.Button(self, wx.ID_OK	 , "Cargar Firmware")
		button_sizer.Add(okButton,0,wx.ALL,10)
		cancelButton = wx.Button(self, wx.ID_CANCEL, "Cancelar")
		button_sizer.Add(cancelButton,0,wx.ALL,10)
		self.GetSizer().Add(button_sizer , pos=(self.rowNr, 0), span=(1, 2), flag=wx.EXPAND | wx.ALL)


	def getFilename(self)  :
		return moebyusFactory.getFWNameByFeatures(self.machineType, self.extruderType, self.XYType, self.ZType,self.lcdType )

	def onLcdSelect(self,e) :
		for selected in self.lcdSelection :
			if selected.GetValue():
				values = selected.data
				self.lcdType = values[0]
			
	def onMachineSelect(self, e):
		for selected in self.machineSelection :
			if selected.GetValue():
				values = selected.data
				self.previewBitmap.SetBitmap(wx.Bitmap(resources.getPathForImage(moebyusFactory.getMachineThumb(values[0]))))
				self.machineType = values[0]
				
#				self.extruderSelection.Enable()
#				self.lcdSelection[0].Enable()
#				self.XYSelection[0].Enable()
#				self.ZSelection[0].Enable()
#				
#				if values[0] == 'PrusaI3MM' :
#					self.lcdSelection.SetSelection(0)
#					self.extruderSelection.SetSelection(1)
#					self.XYSelection.SetSelection(0)
#					self.ZSelection.SetSelection(0)
#				elif values[0] == 'Melta' :
#					self.lcdSelection.SetSelection(1)
#					self.extruderSelection.SetSelection(0)
#					self.XYSelection.SetSelection(0)
#					self.ZSelection.SetSelection(0)
#					self.XYSelection.Disable()
#					self.ZSelection.Disable()
#
#				elif values[0] == 'Sirius1' or  values[0] == 'Sirius11' or values[0] == 'SteelMM-Sirius' or values[0] == 'SteelMM-S303030' or values[0] == 'SteelMM-S303030':
#					self.lcdSelection.SetSelection(0)
#					self.extruderSelection.SetSelection(0)
#					self.XYSelection.SetSelection(0)
#					self.ZSelection.SetSelection(1)
#				else :
#					self.lcdSelection.SetSelection(0)
#					self.extruderSelection.SetSelection(1)
#					self.XYSelection.SetSelection(0)
#					self.ZSelection.SetSelection(0)

	def onExtruderSelect(self, e):
		for selected in self.extruderSelection :
			if selected.GetValue():
				values = selected.data
				#self.previewBitmap.SetBitmap(wx.Bitmap(resources.getPathForImage(moebyusFactory.getMachineThumb(values[0]))))
				self.extruderType = values[0]
				
	def onXYSelect(self, e):
		for selected in self.XYSelection :
			if selected.GetValue():
				values = selected.data
				#self.previewBitmap.SetBitmap(wx.Bitmap(resources.getPathForImage(moebyusFactory.getMachineThumb(values[0]))))
				self.XYType = values[0]
				
	def onZSelect(self, e):
		for selected in self.ZSelection :
			if selected.GetValue():
				values = selected.data
				#self.previewBitmap.SetBitmap(wx.Bitmap(resources.getPathForImage(moebyusFactory.getMachineThumb(values[0]))))
				self.ZType = values[0]

		
class MoebyusSelectModelPage(MoebyusInfoPage):
	def __init__(self, parent) :
		super(MoebyusSelectModelPage, self).__init__(parent, _("Moebyus Machines"))
		self._printer_info = [
			# max Size x, y, z,machine type
			("One\t\t\t\t\t\t(150x150x150)"				, "MoebyusOne"    ),
			("Prusa i3 MM\t\t\t\t(200x200x200)"			, "PrusaI3MM"  	  ),
			("Prusa i3 MM Large\t\t(200x300x200)"		, "PrusaI3MM-L"	  ),
			("Steel MM\t\t\t\t\t(200x200x200)"			, "SteelMM"	      ),
			("Steel MM Large\t\t\t(300x200x200)"		, "SteelMM-L"  	  ),
			("Steel MM Marco Sirius\t(300x200x250)"		, "SteelMM-Sirius"),
			("Steel MM S303030\t\t(300x300x300)"		, "SteelMM-S303030"),
			("Melta Kossel\t\t\t\t(160x300)"			, "Melta"	 	  ),
			("Melta XL\t\t\t\t\t(400x600)"				, "MeltaXL"		  ),
			("[SIRIUS] 1.0\t\t\t\t(300x200x200)"		, "Sirius1"		  ),
			("[SIRIUS] 1.1\t\t\t\t(300x200x250)"		, "Sirius11"	  ),
			("M3\t\t\t\t\t\t\t(1000x1000x1000)"			, "M3"			  )]
		self.parent = parent
#Seleccion de maquina
		self.AddText(_("Select Model:"))
		self._printers = []
		i = 0;
		for printer in self._printer_info:
			if i == 0:
				item = self.AddRadioButton(printer[0], style=wx.RB_GROUP)
				i+=1;
				item.data = printer[1:]
				self._printers.append(item)
				item.Bind(wx.EVT_RADIOBUTTON, self.OnMachineSelect)
			else:
				item = self.AddRadioButton(printer[0])
				item.data = printer[1:]
				self._printers.append(item)
				item.Bind(wx.EVT_RADIOBUTTON, self.OnMachineSelect)
		
		bitmap = wx.Bitmap(resources.getPathForImage(moebyusFactory.getMachineThumb('MoebyusOne')))
		self.previewBitmap = wx.StaticBitmap(self, -1, bitmap)
		self.GetSizer().Add(self.previewBitmap, pos=(1, 3), span=(14, 2), flag=wx.LEFT | wx.RIGHT)
		self.rowNr += 1
		self.AddSeperator()

		filaments = ['1.75','3.0']
		self.comboFilaments = wx.ComboBox(self, -1, filaments[0], choices=filaments, style=wx.CB_DROPDOWN|wx.CB_READONLY)
		text = wx.StaticText(self, -1, "Filament size")
		self.GetSizer().Add(text,  pos=(self.rowNr, 0), span=(1, 1), flag=wx.LEFT | wx.RIGHT)
		self.GetSizer().Add(self.comboFilaments, pos=(self.rowNr, 1), span=(1, 1), flag=wx.LEFT | wx.RIGHT)

		nozzles = ['0.2','0.3','0.35','0.4','0.5','0.6','0.8','1.0']
		self.comboNozzles = wx.ComboBox(self, -1, nozzles[3], choices=nozzles, style=wx.CB_DROPDOWN|wx.CB_READONLY)
		text = wx.StaticText(self, -1, "Nozzle size")
		self.GetSizer().Add(text,  pos=(self.rowNr, 2), span=(1, 1), flag=wx.LEFT | wx.RIGHT)
		self.GetSizer().Add(self.comboNozzles, pos=(self.rowNr, 3), span=(1, 1), flag=wx.LEFT | wx.RIGHT)
		self.rowNr += 1
		
		self.comboNozzles.Disable()
		self.comboFilaments.Disable()
		self.comboNozzles.SetSelection(3)
		self.comboFilaments.SetSelection(0)

#Configuracion del perfil
	def StoreData(self):
		mType = "PrusaI3MM"
		for selected in self._printers:
			if selected.GetValue():
				print(selected.GetLabel())
				values = selected.data
				mType = values[0];
		moebyusFactory.genProfileForMachine(mType, self.comboFilaments.GetValue(),self.comboNozzles.GetValue())
		profile.checkAndUpdateMachineName()

	def OnMachineSelect(self, e):
		for selected in self._printers:
			if selected.GetValue():
				print(selected.GetLabel())
				values = selected.data
				self.previewBitmap.SetBitmap(wx.Bitmap(resources.getPathForImage(moebyusFactory.getMachineThumb(values[0]))))
				if values[0] == 'MoebyusOne' :
					self.comboNozzles.Disable()
					self.comboFilaments.Disable()
					self.comboNozzles.SetSelection(3)
					self.comboFilaments.SetSelection(0)
				elif values[0] == 'M3' :
					self.comboNozzles.Enable()
					self.comboFilaments.Disable()
					self.comboNozzles.SetSelection(6)
					self.comboFilaments.SetSelection(0)
				elif values[0] == 'MeltaXL' :
					self.comboNozzles.Enable()
					self.comboFilaments.Disable()
					self.comboNozzles.SetSelection(6)
					self.comboFilaments.SetSelection(0)
				elif values[0] == 'Sirius1' or  values[0] == 'Sirius11' or values[0] == 'SteelMM-Sirius' or values[0] == 'Melta' or values[0] == 'SteelMM-S303030':
					self.comboNozzles.Enable()
					self.comboFilaments.Enable()
					self.comboNozzles.SetSelection(3)
					self.comboFilaments.SetSelection(0)
				else :
					self.comboNozzles.Enable()
					self.comboFilaments.Enable()
					self.comboNozzles.SetSelection(3)
					self.comboFilaments.SetSelection(1)					


class MoebyusDonePage(MoebyusInfoPage):
	def __init__(self, parent):
		super(MoebyusDonePage, self).__init__(parent, _("Cura ya esta listo!"))
		self.AddSeperator()
		self.AddText(_("Gracias por elegir nuestro software, estamos listos para imprimir!"))
		self.AddHiddenSeperator()
		self.AddHiddenSeperator()
		self.AddText(_("Puede encontrar la ultima version de este software en: "))
		self.AddText(_("https://github.com/moebyus/cura/releases"))
		self.AddHiddenSeperator()		
		self.AddText(_("Tambien puede descargar los ficheros relativos a su maquina en: "))
		self.AddText(_("https://github.com/moebyus"))
		self.AddHiddenSeperator()
		self.AddHiddenSeperator()
		self.AddText(_("May the force be with you...."))				

class moebyusGCodeFeaturesDialog(wx.Dialog) :
	def __init__(self, parent = None)  :
		super(moebyusGCodeFeaturesDialog, self).__init__(parent=parent, title="Special Features", size=(800, 600))
