from __main__ import vtk, qt, ctk, slicer

#
# SlicerRtSliceletTest
#

class SlicerRtSliceletTest:
  def __init__(self, parent):
    import string
    parent.title = ""
    parent.categories = ["Quantification"]
    parent.contributors = ["Steve Pieper (Isomics)"]
    parent.helpText = string.Template("""
Use this module to calculate counts and volumes for different labels of a label map plus statistics on the grayscale background volume.  Note: volumes must have same dimensions.  See <a href=\"$a/Documentation/$b.$c/Modules/SlicerRtSliceletTest\">$a/Documentation/$b.$c/Modules/SlicerRtSliceletTest</a> for more information.
    """).substitute({ 'a':parent.slicerWikiUrl, 'b':slicer.app.majorVersion, 'c':slicer.app.minorVersion })
    parent.acknowledgementText = """
    Supported by NA-MIC, NAC, BIRN, NCIGT, and the Slicer Community. See http://www.slicer.org for details.  Module implemented by Steve Pieper.
    """
    self.parent = parent

#
# qSlicerPythonModuleExampleWidget
#

class SlicerRtSliceletTestWidget:
  def __init__(self, parent=None):
    if not parent:
      self.parent = slicer.qMRMLWidget()
      self.parent.setLayout(qt.QVBoxLayout())
      self.parent.setMRMLScene(slicer.mrmlScene)
    else:
      self.parent = parent
    self.logic = None
    self.inputNode = None
    if not parent:
      self.setup()
      self.inputSelector.setMRMLScene(slicer.mrmlScene)
      self.parent.show()

  def setup(self):
    #
    # the input volume selector
    #
    self.inputSelectorFrame = qt.QFrame(self.parent)
    self.inputSelectorFrame.setLayout(qt.QHBoxLayout())
    self.parent.layout().addWidget(self.inputSelectorFrame)

    self.inputSelectorLabel = qt.QLabel("Input Volume: ", self.inputSelectorFrame)
    self.inputSelectorLabel.setToolTip( "Select Input to Apply Segmentation")
    self.inputSelectorFrame.layout().addWidget(self.inputSelectorLabel)

    self.inputSelector = slicer.qMRMLNodeComboBox(self.inputSelectorFrame)
    self.inputSelector.nodeTypes = ( ("vtkMRMLScalarVolumeNode"), "" )
    self.inputSelector.addAttribute( "vtkMRMLScalarVolumeNode", "LabelMap", 0 )
    self.inputSelector.selectNodeUponCreation = False
    self.inputSelector.addEnabled = False
    self.inputSelector.removeEnabled = False
    self.inputSelector.noneEnabled = True
    self.inputSelector.showHidden = False
    self.inputSelector.showChildNodeTypes = False
    self.inputSelector.setMRMLScene( slicer.mrmlScene )
    self.inputSelectorFrame.layout().addWidget(self.inputSelector)

    # Apply button
    self.applyButton = qt.QPushButton("Apply")
    self.applyButton.toolTip = "Calculate Statistics."
    self.parent.layout().addWidget(self.applyButton)

    # Add vertical spacer
    self.parent.layout().addStretch(1)

    # connections
    self.applyButton.connect('clicked()', self.onApply)
    self.inputSelector.connect('currentNodeChanged(vtkMRMLNode*)', self.onInputSelect)

  def onInputSelect(self, node):
    self.inputNode = node

  
  def onApply(self):
    """Calculate the label statistics
    """
    self.applyButton.text = "Working..."
    # TODO: why doesn't processEvents alone make the label text change?
    self.applyButton.repaint()
    slicer.app.processEvents()
    self.filters(self.inputNode)
    self.applyButton.text = "Apply"

  def filters(self, inputNode):
    import SimpleITK as sitk
    import sitkUtils
    
    inputImage = sitkUtils.PullFromSlicer(inputNode)
    # ShotNoiseImageFilter
    filter1 = sitk.ShotNoiseImageFilter()
    filter1.SetDebug(False)
    filter1.SetNumberOfThreads(4)
    filter1.SetScale(1.0)
    filter1.SetSeed(11)
    outputImage1 = filter1.Execute(inputImage)
                                    
    # OtsuMultipleThresholdsImageFilter
    filter2 = sitk.OtsuMultipleThresholdsImageFilter()
    filter2.SetDebug(False)
    filter2.SetLabelOffset(0)
    filter2.SetNumberOfHistogramBins(128)
    filter2.SetNumberOfThreads(4)
    filter2.SetNumberOfThresholds(2)
    filter2.SetValleyEmphasis(False)
    outputImage2 = filter2.Execute(outputImage1)
        
    # VotingBinaryHoleFillingImageFilter
    filter3 = sitk.VotingBinaryHoleFillingImageFilter()
    filter3.SetBackgroundValue(0.0)
    filter3.SetDebug(False)
    filter3.SetForegroundValue(1.0)
    filter3.SetMajorityThreshold(50)
    filter3.SetNumberOfThreads(4)
    filter3.SetRadius((2, 2, 2))
    outputImage3 = filter3.Execute(outputImage2)
        
    # Display to the Screen
    sitkUtils.PushToSlicer(outputImage3, 'Volume')

class SlicerRtSliceletTestLogic:
  """Implement the logic to calculate label statistics.
  Nodes are passed in as arguments.
  Results are stored as 'statistics' instance variable.
  """



class Slicelet(object):
  """A slicer slicelet is a module widget that comes up in stand alone mode
  implemented as a python class.
  This class provides common wrapper functionality used by all slicer modlets.
  """
  # TODO: put this in a SliceletLib
  # TODO: parse command line arge


  def __init__(self, widgetClass=None):
    self.parent = qt.QFrame()
    self.parent.setLayout( qt.QVBoxLayout() )

    # TODO: should have way to pop up python interactor
    self.buttons = qt.QFrame()
    self.buttons.setLayout( qt.QHBoxLayout() )
    self.parent.layout().addWidget(self.buttons)
    self.addDataButton = qt.QPushButton("Add Data")
    self.buttons.layout().addWidget(self.addDataButton)
    self.addDataButton.connect("clicked()",slicer.app.ioManager().openAddDataDialog)

    self.layoutManager = slicer.qMRMLLayoutWidget()
    self.layoutManager.setMRMLScene(slicer.mrmlScene)
    self.layoutManager.setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutConventionalWidescreenView)
    self.parent.layout().addWidget(self.layoutManager)

    if widgetClass:
      self.widget = widgetClass(self.parent)
      self.widget.setup()
    self.parent.show()

class SlicerRtSliceletTestSlicelet(Slicelet):
  """ Creates the interface when module is run as a stand alone gui app.
  """

  def __init__(self):
    super(SlicerRtSliceletTestSlicelet,self).__init__(SlicerRtSliceletTestWidget)

if __name__ == "SlicerRtSliceletTest":
  # TODO: need a way to access and parse command line arguments
  # TODO: ideally command line args should handle --xml

  #import sys
  #print( sys.argv )

  slicelet = SlicerRtSliceletTestSlicelet()
