from __main__ import vtk, qt, ctk, slicer

#
# SlicerRtSliceletTest
#

class SlicerRtSliceletTest:
    def __init__(self, parent):
        parent.title = "Spine Segmentation"
        parent.categories = ["Examples"]
        parent.contributors = ["Steve Pieper (Isomics)"]
        parent.helpText = string.Template("""
        Use this module to calculate counts and volumes for different labels of a label map plus statistics on the grayscale background volume.  Note: volumes must have same dimensions.  See <a href=\"$a/Documentation/$b.$c/Modules/SlicerRtSliceletTest\">$a/Documentation/$b.$c/Modules/SlicerRtSliceletTest</a> for more information.
        """).substitute({ 'a':parent.slicerWikiUrl, 'b':slicer.app.majorVersion, 'c':slicer.app.minorVersion })
        parent.acknowledgementText = """
        Supported by NA-MIC, NAC, BIRN, NCIGT, and the Slicer Community. See http://www.slicer.org for details.  Module implemented by Steve Pieper.
        """
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
        self.outputNode = None
        self.fileName = None
        self.fileDialog = None
        if not parent:
            self.setup()
            self.inputSelector.setMRMLScene(slicer.mrmlScene)
            self.outputSelector.setMRMLScene(slicer.mrmlScene)
            self.parent.show()
                        
    def setup(self):
        
        #
        # input volume selector
        #
        
        self.inputSelectorFrame = qt.QFrame(self.parent)
        self.inputSelectorFrame.setLayout(qt.QHBoxLayout())
        self.parent.layout().addWidget(self.inputSelectorFrame)
        
        self.inputSelectorLabel = qt.QLabel("Input Volume: ", self.inputSelectorFrame)
        self.inputSelectorLabel.setToolTip("Select input volume")
        self.inputSelectorFrame.layout().addWidget(self.inputSelectorLabel)
        
        self.inputSelector = slicer.qMRMLNodeComboBox(self.inputSelectorFrame)
        self.inputSelector.nodeTypes = ("vtkMRMLScalarVolumeNode")
        self.inputSelector.selectNodeUponCreation = False
        self.inputSelector.addEnabled = False
        self.inputSelector.removeEnabled = False
        self.inputSelector.noneEnabled = False
        self.inputSelector.showHidden = False
        self.inputSelector.showChildNodeTypes = False
        self.inputSelector.setMRMLScene( slicer.mrmlScene )
        
        self.inputSelectorFrame.layout().addWidget(self.inputSelector)
        
        #
        # output volume selector
        #
        
        self.outputSelectorFrame = qt.QFrame(self.parent)
        self.outputSelectorFrame.setLayout(qt.QHBoxLayout())
        self.parent.layout().addWidget(self.outputSelectorFrame)
        
        self.outputSelectorLabel = qt.QLabel("Output Volume: ", self.outputSelectorFrame)
        self.outputSelectorLabel.setToolTip("Select output volume")
        self.outputSelectorFrame.layout().addWidget(self.outputSelectorLabel)
        
        self.outputSelector = slicer.qMRMLNodeComboBox(self.outputSelectorFrame)
        self.outputSelector.nodeTypes = ("vtkMRMLScalarVolumeNode")
        self.outputSelector.selectNodeUponCreation = False
        self.outputSelector.addEnabled = False
        self.outputSelector.removeEnabled = False
        self.outputSelector.noneEnabled = False
        self.outputSelector.showHidden = False
        self.outputSelector.showChildNodeTypes = False
        self.outputSelector.setMRMLScene( slicer.mrmlScene )
        
        self.outputSelectorFrame.layout().addWidget(self.outputSelector)
        
        #
        # threshold value
        #
        self.imageThresholdSliderWidget = ctk.ctkSliderWidget()
        self.imageThresholdSliderWidget.singleStep = 0.1
        self.imageThresholdSliderWidget.minimum = -100
        self.imageThresholdSliderWidget.maximum = 100
        self.imageThresholdSliderWidget.value = 0.5
        self.imageThresholdSliderWidget.setToolTip("Set threshold value for computing the output image. Voxels that have intensities lower than this value will set to zero.")
        self.imageThresholdSliderWidget
        
        # Apply button
        self.applyButton = qt.QPushButton("Apply")
        self.applyButton.toolTip = "Run the algorithm."
        self.applyButton.enabled = False
        self.parent.layout().addWidget(self.applyButton)

        # Add vertical spacer
        self.parent.layout().addStretch(1)

        # connections
        self.applyButton.connect('clicked()', self.onApply)
        self.inputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
        self.outputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)

        self.onSelect()

    def onApply(self):
        import SimpleITK as sitk
        import sitkUtils
    
        #ShotNoiseImageFilter
        inputImage = sitkUtils.PullFromSlicer('007.CTDC.nrrd')
        filter1 = sitk.ShotNoiseImageFilter()
        filter1.SetDebug(False)
        filter1.SetNumberOfThreads(4)
        filter1.SetScale(1.0)
        filter1.SetSeed(11)
        outputImage1 = filter1.Execute(inputImage)
    
        #OtsuMultipleThresholdsImageFilter
        filter2 = sitk.OtsuMultipleThresholdsImageFilter()
        filter2.SetDebug(False)
        filter2.SetLabelOffset(0)
        filter2.SetNumberOfHistogramBins(128)
        filter2.SetNumberOfThreads(4)
        filter2.SetNumberOfThresholds(2)
        filter2.SetValleyEmphasis(False)
        outputImage2 = filter2.Execute(outputImage1)
    
        #VotingBinaryHoleFillingImageFilter
        filter3 = sitk.VotingBinaryHoleFillingImageFilter()
        filter3.SetBackgroundValue(0.0)
        filter3.SetDebug(False)
        filter3.SetForegroundValue(1.0)
        filter3.SetMajorityThreshold(50)
        filter3.SetNumberOfThreads(4)
        filter3.SetRadius((2, 2, 2))
        outputImage3 = filter3.Execute(outputImage2)
    
        #Display to the Screen
        sitkUtils.PushToSlicer(outputImage3, 'Volume')
        
    def onSelect(self):
        self.applyButton.enabled = self.inputSelector.currentNode() and self.outputSelector.currentNode()

class SlicerRtSliceletTestLogic:
    """Implement the logic to calculate label statistics.
        Nodes are passed in as arguments.
        Results are stored as 'statistics' instance variable.
    """
    def hasImageData(self,volumeNode):
        """This is an example logic method that
            returns true if the passed in volume
            node has valid image data
            """
        if not volumeNode:
            logging.debug('hasImageData failed: no volume node')
            return False
        if volumeNode.GetImageData() is None:
            logging.debug('hasImageData failed: no image data in volume node')
            return False
        return True
                                        
    def isValidInputOutputData(self, inputVolumeNode, outputVolumeNode):
        """Validates if the output is not the same as input
            """
        if not inputVolumeNode:
            logging.debug('isValidInputOutputData failed: no input volume node defined')
            return False
        if not outputVolumeNode:
            logging.debug('isValidInputOutputData failed: no output volume node defined')
            return False
        if inputVolumeNode.GetID()==outputVolumeNode.GetID():
            logging.debug('isValidInputOutputData failed: input and output volume is the same. Create a new volume for output to avoid this error.')
            return False
        return True
                                        
    def run(self, inputVolume, outputVolume, imageThreshold, enableScreenshots=0):
        """
            Run the actual algorithm
            """
        
        if not self.isValidInputOutputData(inputVolume, outputVolume):
            slicer.util.errorDisplay('Input volume is the same as output volume. Choose a different output volume.')
            return False
        
        logging.info('Processing started')
        
        # Compute the thresholded output volume using the Threshold Scalar Volume CLI module
        cliParams = {'InputVolume': inputVolume.GetID(), 'OutputVolume': outputVolume.GetID(), 'ThresholdValue' : imageThreshold, 'ThresholdType' : 'Above'}
        cliNode = slicer.cli.run(slicer.modules.thresholdscalarvolume, None, cliParams, wait_for_completion=True)
        
        logging.info('Processing completed')
        
        return True

class Slicelet(object):
    """A slicer slicelet is a module widget that comes up in stand alone mode
        implemented as a python class.
        This class provides common wrapper functionality used by all slicer modlets.
    """
            
    def __init__(self, widgetClass=None):
        self.parent = qt.QFrame()
        self.parent.setLayout(qt.QVBoxLayout())
    
        self.buttons = qt.QFrame()
        self.buttons.setLayout( qt.QHBoxLayout() )
        self.parent.layout().addWidget(self.buttons)
        self.addDataButton = qt.QPushButton("Add Data")
        self.buttons.layout().addWidget(self.addDataButton)
        self.addDataButton.connect("clicked()",slicer.app.ioManager().openAddDataDialog)
        self.applyButton = qt.QPushButton("Apply")
        self.buttons.layout().addWidget(self.applyButton)
        self.applyButton.connect('clicked()', self.onApply)


    
        self.layoutWidget = slicer.qMRMLLayoutWidget()
        self.layoutWidget.setMRMLScene(slicer.mrmlScene)
        self.layoutWidget.setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutConventionalWidescreenView)
        self.parent.layout().addWidget(self.layoutWidget)
    
        if widgetClass:
            self.widget = widgetClass(self.parent)
            self.widget.setup()
        self.parent.show()

    def onApply(self):
        import SimpleITK as sitk
        import sitkUtils
        
        #ShotNoiseImageFilter
        inputImage = sitkUtils.PullFromSlicer('007.CTDC.nrrd')
        filter1 = sitk.ShotNoiseImageFilter()
        filter1.SetDebug(False)
        filter1.SetNumberOfThreads(4)
        filter1.SetScale(1.0)
        filter1.SetSeed(11)
        outputImage1 = filter1.Execute(inputImage)
        
        #OtsuMultipleThresholdsImageFilter
        filter2 = sitk.OtsuMultipleThresholdsImageFilter()
        filter2.SetDebug(False)
        filter2.SetLabelOffset(0)
        filter2.SetNumberOfHistogramBins(128)
        filter2.SetNumberOfThreads(4)
        filter2.SetNumberOfThresholds(2)
        filter2.SetValleyEmphasis(False)
        outputImage2 = filter2.Execute(outputImage1)
        
        #VotingBinaryHoleFillingImageFilter
        filter3 = sitk.VotingBinaryHoleFillingImageFilter()
        filter3.SetBackgroundValue(0.0)
        filter3.SetDebug(False)
        filter3.SetForegroundValue(1.0)
        filter3.SetMajorityThreshold(50)
        filter3.SetNumberOfThreads(4)
        filter3.SetRadius((2, 2, 2))
        outputImage3 = filter3.Execute(outputImage2)
        
        #Display to the Screen
        sitkUtils.PushToSlicer(outputImage3, 'Volume')


class SlicerRtSliceletTestSlicelet(Slicelet):
    """ Creates the interface when module is run as a stand alone gui app.
    """
            
    def __init__(self):
        super(SlicerRtSliceletTestSlicelet,self).__init__(SlicerRtSliceletTestWidget)


if __name__ == "SlicerRtSliceletTest":
    # TODO: need a way to access and parse command line arguments
    # TODO: ideally command line args should handle --xml
    
    #import sys
    #print(sys.args)
            
    slicelet = SlicerRtSliceletTestSlicelet()
