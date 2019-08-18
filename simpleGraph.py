# -*- coding: utf-8 -*-
"""
This is the main source file for the simpleGraph Project. simpleGraph aims to provide an easy and quick interface for importing and plotting
tabulated data. It is primarily aimed at research and development work and is an ideal tool for generating graphs for reports.

AUTHOR: Sam Maxwell
DATE CREATED: 18/08/2019
VERSION: ENTER_VERSION_NUMBER
VERSION DATE: ENTER_VERSION_DATE
"""

#---------------------------------------------------------------------------------------------------------------------------------------------
#MODULES
#---------------------------------------------------------------------------------------------------------------------------------------------
import PyQt4.QtGui as QtGui
import PyQt4.uic as uic

import sys
import pandas

#---------------------------------------------------------------------------------------------------------------------------------------------
#CLASSES
#---------------------------------------------------------------------------------------------------------------------------------------------
#MAIN WINDOW Class - Handles linking to the GUI Elements and generating the UI on start
class MainWindow(QtGui.QMainWindow):
    #Constructor
    def __init__(self):
        #Inheriting from the parent class
        super(MainWindow, self).__init__()        
        
        #Importing the QtDesigner UI file
        uic.loadUi("simpleGraph.ui", self)
        
        #Generating Event Handler Classes
        self.graphTabEventHandler = GraphTabEventHandler(self.graphingWidget)
        self.dataTabEventHandler = DataTabEventHandler(self.dataTableWidget)
        
        #Linking the Graph Tab Buttons
        self.plotDataButton.clicked.connect(self.graphTabEventHandler.plotData)
        
        #Linking the Data Tab Buttons
        self.importDataButton.clicked.connect(self.dataTabEventHandler.importData)
        
        #Showing the GUI
        self.show()

#GRAPH TAB EVENT HANDLER Class - Handles all GUI events on the graph tab
class GraphTabEventHandler():
    #Constructor
    def __init__(self, graphingWidget):
        #Generating Graph Canvas Handle
        self.graphCanvas = graphCanvas(graphingWidget)
    
    #Methods
    """
    PURPOSE:    Plots all of the currently selected lines on the graph.
    """
    def plotData(self):
        self.graphCanvas.plotLines()
        
#DATA TAB EVENT HANDLER Class - Handles all GUI events on the data tab
class DataTabEventHandler():
    #Constructor
    def __init__(self, dataTableWidget):
        self.__dataTable = DataTable(dataTableWidget)
        self.__dataStore = DataStore()
    
    #Methods
    def importData(self):
        """
        PURPOSE:    Imports all data from the selected data file.
        """
        importFileDialog = QtGui.QFileDialog(parent = None, caption = "Select the file you wish to import.")
        filePath = importFileDialog.getOpenFileName()
        
        self.__dataStore.importFromCSV(filePath)
        
        self.__dataTable.populateDataTable(self.__dataStore.getDataFrame())
        

#MATPLOTLIB GRAPH Class - Handles display and plotting of the data on the Matplotlib Graph
class graphCanvas():
    #Constructor
    def __init__(self, graphCanvasWidget):
        self.graphCanvasWidget = graphCanvasWidget
    
    #Methods
    def __plotData(self, xAxisData, yAxisData, showGraph = False):
        """
        PURPOSE:    Plots the given data on the graph.
        INPUT:      xAxisData = The X Axis data points
                    yAxisData = The Y Axis data points
        OUTPUT:     NONE
        """
        self.graphCanvasWidget.axes.plot(xAxisData, yAxisData)
        
        if (showGraph):
            self.graphCanvasWidget.show()
        
    def plotLines(self, lineXAxisData, lineYAxisData):
        """
        PURPOSE:    Plots the given lines on the graph.
        INPUT:      lineXAxisData = The X Axis data points for every line.
                    lineYAxisData = The Y Axis data points for every line.
        OUTPUT:     NONE
        """
        for xAxisData, yAxisData in zip(lineXAxisData, lineYAxisData):
            self.__plotData(xAxisData, yAxisData)

#DATA TABLE Class - Handles and manipulates the data table widget for plotting to
class DataTable():
    #Constructor
    def __init__(self, dataTableWidget):
        self.__dataTable = dataTableWidget
    
    #Methods
    def populateDataTable(self, dataFrame):
        """
        PURPOSE:    Populates the data table with the data from the passed data frame
        INPUT:      dataFrame = The set of data to be populated in the data table
        OUTPUT:     NONE
        """
        #Setting the size of the Data Table to the size of the Data Frame
        self.__dataTable.setRowCount(dataFrame.shape[0])
        self.__dataTable.setColumnCount(dataFrame.shape[1])
        
        #Populating the Data Table Header
        headers = list(dataFrame)
        self.__dataTable.setHorizontalHeaderLabels(headers)
    
        #Populating the data table with the information from the Data Frame
        dataFrameArray = dataFrame.values
        for row in range(dataFrame.shape[0]):
            for column in range(dataFrame.shape[1]):
                self.__dataTable.setItem(row, column, QtGui.QTableWidgetItem(str(dataFrameArray[row,column])))

#DATA STORE Class - Holds and manipulates all of the currently imported data
class DataStore():
    #Constructor
    def __init__(self):
        self.__dataFrame = pandas.DataFrame()
    
    #Methods
    def importFromCSV(self, filePath):
        """
        PURPOSE:    Imports the data from the given data file
        INPUT:      filePath = The path to the file that needs to be imported
        OUTPUT:     NONE
        """
        self.__dataFrame = pandas.read_csv(filePath, sep = ",", header = 0)
    
    def getDataFrame(self):
        """
        PURPOSE:    Returns the currently stored dataFrame
        """
        return self.__dataFrame.copy()
        
#---------------------------------------------------------------------------------------------------------------------------------------------
#APPLICATION EXECUTION CODE
#---------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())