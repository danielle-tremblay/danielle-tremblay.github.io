# Project: Spine Segmentation
## Contributors: Danielle Tremblay and Rachel Hartley

### Below you will find our individual diaries which will keep track of our contributions to the project, as well as our step-by-step plan we will follow in order to complete this project along with any other information we find useful.

# Plan for Success! 

1. Refresh slicer memories by completing the tutorials given on the assignment page
2. Download data
3. Compare segmentation methods
4. Finalize strategy and begin coding
  - Create a new extension and module
  - Apply thresholding (k-means)
  - Apply edge-detection 
  - Create GUI if time allows 
5. Create slides before final week of classes
  - Tibia CT with k-means applied should be included 

# Danielle's Contribution:
### _March 6, 2017_
- Created wiki page with base content 

### _March 7, 2017_
- Created our plan for success! 

### _March 8, 2017_
- Finished slicer tutorials, memory has been refreshed! 
- Downloaded data
- Goal for over the weekend is to compare and select a segmentation method to apply as well as creating a new extension and module

### _March 12, 2017_
- Created Project module and extension 
- Updated plan for success
- Created additional information on K-means (Can be used in our presentation)
- Uploaded CT of before and after application of K-means (Can be used in our presentation)

### _March 13, 2017_
- Tried to apply the k-means "Simple Filter" from the filters module in slicer but it wasn't working (spent about an hour waiting and trying different things, will ask about this in class tomorrow)
- Added a load data button, when clicked this should prompt the user to load their image. I wasn't able to test this because for some reason everytime I create a module I can't find it in slicer after (Spent a while trying to figure this out, will ask about this in class tomorrow)

### _March 16, 2017_
- Updated plan for success
- Found 3D slicer code that will allow us to create our own custom user interface, allowing for a more genuine software feel: 
https://www.slicer.org/wiki/Documentation/Nightly/Developers/Slicelets
- Followed a tutorial that allows you to modify the image pixels, I applied their code to the CT image (Both the image and code can be found in the repository) using different starting intensities and I actually got some pretty great results. Will ask tomorrow if I should keep segmenting or stop here.  

# Rachel's Contribution: 

### _March 7, 2017_
- Completed the 'Hello Python Programming Tutorial' from slicer.org
- Downloaded the SpineData from OneDrive

### _March 10, 2017_
- Completed the 'Hello Python Tutorial using a Laplacian Filtering and Sharpening'

# `Useful Code` 

## K-Means Information
- Aims to partition n-observations into k-clusters
- Good for medical imaging because this allows for the distinction of different tissues, in our case we can differentiate spinal bone from different soft tissues 
