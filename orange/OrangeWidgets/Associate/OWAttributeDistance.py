"""
<name>Attribute Distance</name>
<description>Creates a attribute distance matrix from a set of examples at the input.</description>
<icon>icons/AttributeDistance.png</icon>
<priority>1100</priority>
"""

import orange, math
import OWGUI
from qt import *
from qtcanvas import *
from OWWidget import *
import random
import orngInteract
import warnings
warnings.filterwarnings("ignore", module="orngInteract")

##############################################################################
# main class

class OWAttributeDistance(OWWidget):	
    settingsList = ["ClassInteractions"]

    def __init__(self, parent=None, signalManager = None, name='AttributeDistance'):
        self.callbackDeposit = [] # deposit for OWGUI callback functions
        OWWidget.__init__(self, parent, signalManager, name, 'Attribute Distance') 

        self.inputs = [("Examples", ExampleTable, self.dataset)]
        self.outputs = [("Distance Matrix", orange.SymMatrix)]

        self.ClassInteractions = 0
        self.loadSettings()
        self.classIntCB = OWGUI.checkBox(self.controlArea, self, "ClassInteractions", "Use class information", callback=self.toggleClass, disabled=1)
        self.resize(100,100)

    ##############################################################################
    # callback functions

    def computeMatrix(self):
        if not self.data:
            return
        atts = self.data.domain.attributes
        im = orngInteract.InteractionMatrix(self.data, dependencies_too=1)
        (diss,labels) = im.depExportDissimilarityMatrix(jaccard=1)  # 2-interactions

        matrix = orange.SymMatrix(len(atts))
        matrix.setattr('items', atts)
        for i in range(len(atts)-1):
            for j in range(i+1):
                matrix[i+1, j] = diss[i][j]
        self.send("Distance Matrix", matrix)

    def toggleClass(self):
        pass

    ##############################################################################
    # input signal management

    def dataset(self, data):
        if data and len(data.domain.attributes):
            self.data = orange.Preprocessor_discretize(data, method=orange.EquiNDiscretization(numberOfIntervals=5))
            print self.data.domain
            self.classIntCB.setDisabled(self.data.domain.classVar == None)
            self.computeMatrix()
        else:
            self.send("Distance Matrix", None)

##################################################################################################
# test script

if __name__=="__main__":
    data = orange.ExampleTable(r'../../doc/datasets/voting')
    a = QApplication(sys.argv)
    ow = OWAttributeDistance()
    a.setMainWidget(ow)
    ow.show()
    ow.dataset(data)
    a.exec_loop()
    ow.saveSettings()
