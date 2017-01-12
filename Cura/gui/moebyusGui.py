__copyright__ = "Released under terms of the AGPLv3 License"


import wx
import wx.wizard

from Cura.gui  import firmwareInstall
from Cura.util import machineCom
from Cura.util import profile

class MoebyusFactory(wx.Dialog) :
	def __init__(self,parent):
		super(MoebyusFactory, self).__init__(parent=parent, title="Moebyus Machines", size=(250, 100))

	def genProfile(machineType = "PrusaI3MM", filamentSize = '3' , nozzleSize = '0.4') :
		print("Gen profile")
