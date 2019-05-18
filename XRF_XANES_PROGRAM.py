from numpy import loadtxt, array, empty, arange
from numpy.linalg import solve
from pylab import plot, show, xlabel, ylabel, axvline, title, legend
from tkinter import *
from tkinter.ttk import *
import pandas as pd
import tkinter.messagebox

ElementEnergy = array(
    [0, 0, 0, 52, 110, 185, 282, 392, 523, 677, 851, 1041, 1254, 1486, 1739, 2014, 2307, 2621, 2956, 3311, 3689, 4087,
     4507, 4948, 5410, 5893, 6397, 6922, 7470, 8037, 8629, 9245, 9870, 10520, 11200, 11900, 12625, 13370, 14130, 14930,
     15740], float)

k_edges = pd.read_pickle('elements_data.pickle')
kalpha_edges = pd.read_pickle('kalpha_edges.pickle')
elements = pd.read_pickle('elements.pickle')

def minlength(l1, l2):
    a = [len(l1), len(l2)]  # creating a list of the lengths of the lists inputted
    return min(a)  # returning the smallest value of the created list


def mostcounts(l):
    max = 0  # the max number starts at 0, the arrays we are working with have mostly positive values, the max number will be changed when there is a new max
    number = 0  # this will hold the index of the largest number
    for i in range(len(l)):  # setting up a loop to check all the numbers in the array
        if l[
            i] > max:  # if a new max is found the old max is updated and the index of the array it is found at is updated as well
            max = l[i]
            number = i
    return number  # returning the index


# this is a function that removes the largest number in a list
def removemost(l):
    for i in range(len(l)):
        if l[i] == max(l):  # finding the largest number in the list
            return l[:i] + l[i + 1:]  # returning the list without the largest number


# this is a funtion that finds the largest number in the list l1 and returns l2 without the number at the index that the largest number of l1 was
def removemostl2(l1, l2):
    for i in range(len(l1)):
        if l1[i] == max(l1):  # finding the largest number in l1
            return l2[:i] + l2[
                            i + 1:]  # returning l2 without the number at the index corresponding to the largest number of l1


# this is a function that appends the elements of b to the list c in the order of decreasing numbers of the list a
def mosttoleast1(a, b, c):
    if len(a) == 1:  # for when there is only one element left
        return c + b
    else:
        for i in range(len(a)):  # finding the max number of a
            if a[i] == max(a):
                d = b[i]
                c.append(d)  # adding the number of b that corresponds to the max number of a to the end of c
        return mosttoleast1(removemost(a), removemostl2(a, b), c)  # recursing for the rest of the list


# this is a function that lists the elements of l2 based on index corresponding to most to least numbers of l1
def mosttoleast(l1, l2):
    c = []  # this code makes my brain hurt
    return mosttoleast1(l1, l2, c)


def cutArray(array, start, end):
    s = 0
    i = 0
    while array[i] < start:
        i += 1
    j = 0
    while array[j] < end:
        j += 1
    return array[i:j + 1]


class xrfFile:
    def __init__(self, file, XRF, Row):
        self.ElementEnergy = array(
            [0, 0, 0, 52, 110, 185, 282, 392, 523, 677, 851, 1041, 1254, 1486, 1739, 2014, 2307, 2621, 2956, 3311, 3689,
             4087, 4507, 4948, 5410, 5893, 6397, 6922, 7470, 8037, 8629, 9245, 9870, 10520, 11200, 11900, 12625, 13370,
             14130, 14930, 15740], float)
        self.xrfProgram = XRF
        self.row = Row
        self.data = loadtxt(file + ".txt")
        self.energy = self.data[:, 0]
        self.counts = self.data[:, 1]
        self.peaks = []
        self.peakse = []
        for i in range(len(self.energy)):
            if i != 0 and i != len(self.energy) - 1:
                if self.counts[i - 1] < self.counts[i] and self.counts[i + 1] < self.counts[i] and (
                        self.counts[i - 1] + self.counts[i] + self.counts[i + 1]) > (
                        self.counts[i - 4] + self.counts[i - 3] + self.counts[i - 2]) and (
                        self.counts[i - 1] + self.counts[i] + self.counts[i + 1]) > (
                        self.counts[i + 4] + self.counts[i + 3] + self.counts[i + 2]) and self.counts[i] > max(
                        self.counts) / 500:
                    self.peaks.append(self.counts[i])
                    self.peakse.append(self.energy[i])

    # this is a function that prints all the elements that are in the sample
    def composition(self):
        elements_contained = []
        for index in range(len(self.peakse)):
            for row in range(len(kalpha_edges['Ka'])):
                if (self.peakse[index] > (kalpha_edges['Ka2'][row] - 20)) and (
                        self.peakse[index] < (kalpha_edges['Ka'][row] + 20)):
                    elements_contained.append(kalpha_edges['Element'][row])
        messagebox.showinfo("Composition", 'Your sample has '+str(elements_contained))

    # this is a function that lets the user know what they have the highest concentration of in their sample
    def mostprominent(self):
        elements_contained = ''
        print(self.peakse[mostcounts(self.peaks)])
        for row in range(len(kalpha_edges['Ka'])):
            if (self.peakse[mostcounts(self.peaks)] > (kalpha_edges['Ka2'][row] - 20)) and (
                    self.peakse[mostcounts(self.peaks)] < (kalpha_edges['Ka'][row] + 20)):
                elements_contained = kalpha_edges['Element'][row]
        messagebox.showinfo("Element of most concentration", str(elements_contained))

        def orderedConcentration(self):
            self.peakse = mosttoleast(self.peaks, self.peakse)
            self.composition()

        def graph(self, label):
            lab = label
            plot(self.energy, self.counts, label=lab)
            for i in range(3, 41):
                if vars(self.xrfProgram)["self." + ElementNames[i]].get() == True:
                    axvline(ElementEnergy[i])
            xlabel("Energy(eV)")
            ylabel("Photon Counts")
            seepeaks1 = messagebox.askquestion("Sample Peaks", "Would you like to better see the peaks of your sample?")
            if seepeaks1 == "yes":
                plot(self.peakse, self.peaks, 'ro')
            legend()
            Title = self.row.title1entry.get()
            title(Title)
            show()

        def scattercounts(self, scatter):
            for i in range(len(self.energy)):
                if self.energy[i] == scatter:
                    return (self.counts[i])

        def normalGraph(self, label, scatter1):
            scatter = float(scatter1)
            normcounts = self.counts / self.scattercounts(scatter)
            lab = label
            plot(self.energy, normcounts, label=lab)
            for i in range(3, 41):
                if vars(self.xrfProgram)["self.xrfProgram." + ElementNames[i]].get() == True:
                    axvline(ElementEnergy[i])
            xlabel("Energy(eV)")
            ylabel("Normalized Photon Counts")
            seepeaks1 = messagebox.askquestion("Sample Peaks", "Would you like to better see the peaks of your sample?")
            if seepeaks1 == "yes":
                normpeaks = array(self.peaks) / self.scattercounts(scatter)
                plot(array(self.peakse), normpeaks, 'ro')
            legend()
            Title = self.row.title1entry.get()
            title(Title)
            show()

    class xrfSubtractionFile:
        def __init__(self, file, XRF, Row):
            self.ElementEnergy = array(
                [0, 0, 0, 52, 110, 185, 282, 392, 523, 677, 851, 1041, 1254, 1486, 1739, 2014, 2307, 2621, 2956, 3311,
                 3689, 4087, 4507, 4948, 5410, 5893, 6397, 6922, 7470, 8037, 8629, 9245, 9870, 10520, 11200, 11900,
                 12625, 13370, 14130, 14930, 15740], float)
            self.xrfProgram = XRF
            self.row = Row
            self.data = loadtxt(file + ".txt")
            self.energy = self.data[:, 0]
            self.counts = self.data[:, 1]
            self.peaks = []
            self.peakse = []
            for i in range(len(self.energy)):
                if i != 0 and i != len(self.energy) - 1:
                    if self.counts[i - 1] < self.counts[i] and self.counts[i + 1] < self.counts[i] and (
                            self.counts[i - 1] + self.counts[i] + self.counts[i + 1]) > (
                            self.counts[i - 4] + self.counts[i - 3] + self.counts[i - 2]) and (
                            self.counts[i - 1] + self.counts[i] + self.counts[i + 1]) > (
                            self.counts[i + 4] + self.counts[i + 3] + self.counts[i + 2]) and self.counts[i] > max(
                            self.counts) / 500:
                        self.peaks.append(self.counts[i])
                        self.peakse.append(self.energy[i])

        def graphSubtraction(self, file2, label1):
            if len(self.energy) == len(
                    file2.energy):  # determining the energy to use, this only works if the incrementation is the same
                energyu = self.energy
            elif len(self.energy) == minlength(self.energy, file2.energy):
                energyu = self.energy
                file2.counts = file2.counts[:len(self.energy) + 1]
            elif len(file2.energy) == minlength(self.energy, file2.energy):
                energyu = file2.energy
                self.counts = self.counts[:len(self.energy) + 1]
            difference = self.counts - file2.counts
            lab = label1
            plot(energyu, difference, label=lab)
            seepeaks1 = messagebox.askquestion("Sample Peaks",
                                               "Would you like to better see the peaks of the difference?")
            if seepeaks1 == "yes":
                peaks = []  # creating empty lists to store information about the peaks in the smaple
                peakse = []
                for i in range(len(
                        energyu)):  # this section stores information about the peaks in the sample in the empty lists
                    if i != 0 and i != len(energyu) - 1:
                        if difference[i - 1] < difference[i] and difference[i + 1] < difference[i] and (
                                difference[i - 1] + difference[i] + difference[i + 1]) > (
                                difference[i - 4] + difference[i - 3] + difference[i - 2]) and (
                                difference[i - 1] + difference[i] + difference[i + 1]) > (
                                difference[i + 4] + difference[i + 3] + difference[i + 2]) and difference[i] > max(
                            difference) / 500:
                            peaks.append(difference[i])
                            peakse.append(energyu[i])
                plot(peakse, peaks, 'ro')
            for i in range(3, 41):
                if vars(self)["self.xrfProgram." + ElementNames[i]].get() == True:
                    axvline(ElementEnergy[i])
            legend()
            xlabel("Energy(eV)")
            ylabel("Difference(counts)")
            Title = self.row.title1entry.get()
            title(Title)
            show()

        def scattercounts(self, scatter):
            for i in range(len(self.energy)):  # finding the scatter ebergy
                if self.energy[i] == scatter:
                    return (self.counts[i])  # returning the scatter peaks

        def graphNormalSubtraction(self, file2, label1, scatter1, scatter2):
            if len(self.energy) == len(
                    file2.energy):  # determining the energy to use, this only works if the incrementation is the same
                energyu = self.energy
            elif len(self.energy) == minlength(self.energy, file2.energy):
                energyu = self.energy
                file2.counts = file2.counts[:len(self.energy) + 1]
            elif len(file2.energy) == minlength(self.energy, file2.energy):
                energyu = file2.energy
                self.counts = self.counts[:len(self.energy) + 1]
            difference = self.counts / self.scattercounts(scatter1) - file2.counts / file2.scattercounts(scatter2)
            lab = label1
            plot(energyu, difference, label=lab)
            seepeaks1 = messagebox.askquestion("Sample Peaks", "Would you like to better see the peaks of your sample?")
            if seepeaks1 == "yes":
                peaks = []  # creating empty lists to store information about the peaks in the smaple
                peakse = []
                for i in range(len(
                        energyu)):  # this section stores information about the peaks in the sample in the empty lists
                    if i != 0 and i != len(energyu) - 1:
                        if difference[i - 1] < difference[i] and difference[i + 1] < difference[i] and (
                                difference[i - 1] + difference[i] + difference[i + 1]) > (
                                difference[i - 4] + difference[i - 3] + difference[i - 2]) and (
                                difference[i - 1] + difference[i] + difference[i + 1]) > (
                                difference[i + 4] + difference[i + 3] + difference[i + 2]) and difference[i] > max(
                                difference) / 500:
                            peaks.append(difference[i])
                            peakse.append(energyu[i])
                plot(peakse, peaks, 'ro')
            for i in range(3, 41):
                if vars(self)["self.xrfProgram." + ElementNames[i]].get() == True:
                    axvline(ElementEnergy[i])
            legend()
            xlabel("Energy(eV)")
            ylabel("Difference(normalized counts)")
            Title = self.row.title1entry.get()
            title(Title)
            show()

    class xrfRow:
        def __init__(self, XRFProgram, r):
            self.isSub = False
            self.XRFProgram = XRFProgram
            self.enterfile1 = Entry(self.XRFProgram.XRF)
            self.enterfile1.grid(row=r, column=0)
            self.compositionbutton1 = Button(self.XRFProgram.XRF, text="Composition")
            self.compositionbutton1.grid(row=r, column=6)
            self.compositionbutton1.bind("<Button-1>", self.file1composition)
            self.title1entry = Entry(self.XRFProgram.XRF)
            self.title1entry.grid(row=r, column=3)
            self.sample1entry = Entry(self.XRFProgram.XRF)
            self.sample1entry.grid(row=r, column=2)
            self.graph1button = Button(self.XRFProgram.XRF, text="Graph this data")
            self.graph1button.grid(row=r, column=9)
            self.graph1button.bind("<Button-1>", self.graphSample)
            self.scatter1entry = Entry(self.XRFProgram.XRF)
            self.scatter1entry.grid(row=r, column=4)
            self.normalgraph1button = Button(self.XRFProgram.XRF, text="Graph Normalized")
            self.normalgraph1button.grid(row=r, column=10)
            self.normalgraph1button.bind("<Button-1>", self.graphNormSample)
            self.shouldgraph1 = IntVar(self.XRFProgram.XRF)
            self.graph1check = Checkbutton(self.XRFProgram.XRF, text="graph this data", variable=self.shouldgraph1)
            self.graph1check.grid(row=r, column=11)
            self.mostConcentrationButton = Button(self.XRFProgram.XRF, text="Most Concentration")
            self.mostConcentrationButton.bind("<Button-1>", self.showMostConcentration)
            self.mostConcentrationButton.grid(row=r, column=7)
            self.orderedConcentrationButton = Button(self.XRFProgram.XRF, text="Ordered Concentration")
            self.orderedConcentrationButton.bind("<Button-1>", self.orderedConcentration)
            self.orderedConcentrationButton.grid(row=r, column=8)

        def file1composition(self, event):
            file1 = self.enterfile1.get()
            xrfFile1 = xrfFile(file1, self.XRFProgram, self)
            xrfFile1.composition()

        def showMostConcentration(self, event):
            file1 = self.enterfile1.get()
            xrfFile1 = xrfFile(file1, self.XRFProgram, self)
            xrfFile1.mostprominent()

        def orderedConcentration(self, event):
            file1 = self.enterfile1.get()
            xrfFile1 = xrfFile(file1, self.XRFProgram, self)
            xrfFile1.orderedConcentration()

        def graphSample(self, event):
            file1 = self.enterfile1.get()
            xrfFile1 = xrfFile(file1, self.XRFProgram, self)
            xrfFile1.graph(self.sample1entry.get())

        def graphNormSample(self, event):
            file1 = self.enterfile1.get()
            xrfFile1 = xrfFile(file1, self.XRFProgram, self)
            xrfFile1.normalGraph(self.sample1entry.get(), self.scatter1entry.get())

        def destroy(self):
            self.enterfile1.destroy()
            self.compositionbutton1.destroy()
            self.graph1button.destroy()
            self.normalgraph1button.destroy()
            self.graph1check.destroy()
            self.sample1entry.destroy()
            self.scatter1entry.destroy()
            self.title1entry.destroy()
            self.mostConcentrationButton.destroy()
            self.orderedConcentrationButton.destroy()

    class xrfRowSubtract:
        def __init__(self, XRFProgram, r):
            self.isSub = True
            self.XRFProgram = XRFProgram
            self.enterfile1 = Entry(self.XRFProgram.XRF)
            self.enterfile1.grid(row=r, column=0)
            self.enterFile2 = Entry(self.XRFProgram.XRF)
            self.enterFile2.grid(row=r, column=1)
            self.scatter1Entry = Entry(self.XRFProgram.XRF)
            self.scatter1Entry.grid(row=r, column=4)
            self.scatter2Entry = Entry(self.XRFProgram.XRF)
            self.scatter2Entry.grid(row=r, column=5)
            self.labelEntry = Entry(self.XRFProgram.XRF)
            self.labelEntry.grid(row=r, column=2)
            self.title1entry = Entry(self.XRFProgram.XRF)
            self.title1entry.grid(row=r, column=3)
            self.graphSubtractionButton = Button(self.XRFProgram.XRF, text="Graph subtraction")
            self.graphSubtractionButton.bind("<Button-1>", self.graphSubtraction)
            self.graphSubtractionButton.grid(row=r, column=9)
            self.graphNormalSubtractionButton = Button(self.XRFProgram.XRF, text="Graph normal subtraction")
            self.graphNormalSubtractionButton.bind("<Button-1>", self.graphNormalSubtraction)
            self.graphNormalSubtractionButton.grid(row=r, column=10)
            self.shouldgraph1 = IntVar(self.XRFProgram.XRF)
            self.graph1check = Checkbutton(self.XRFProgram.XRF, text="graph this data", variable=self.shouldgraph1)
            self.graph1check.grid(row=r, column=11)

        def graphSubtraction(self, event):
            file1 = xrfSubtractionFile(self.enterfile1.get(), self.XRFProgram, self)
            file2 = xrfSubtractionFile(self.enterFile2.get(), self.XRFProgram, self)
            file1.graphSubtraction(file2, self.labelEntry.get())

        def graphNormalSubtraction(self, event):
            file1 = xrfSubtractionFile(self.enterfile1.get(), self.XRFProgram, self)
            file2 = xrfSubtractionFile(self.enterFile2.get(), self.XRFProgram, self)
            file1.graphNormalSubtraction(file2, self.labelEntry.get(), float(self.scatter1Entry.get()),
                                         float(self.scatter2Entry.get()))

        def destroy(self):
            self.enterfile1.destroy()
            self.enterFile2.destroy()
            self.scatter1Entry.destroy()
            self.scatter2Entry.destroy()
            self.labelEntry.destroy()
            self.title1entry.destroy()
            self.graphSubtractionButton.destroy()
            self.graphNormalSubtractionButton.destroy()
            self.graph1check.destroy()

    class xrfProgram:
        def __init__(self):
            self.XRF = Tk()
            self.XRF.title("XRF Analysis")
            self.file1label = Label(self.XRF, text="File1")
            self.file1label.grid(row=0, column=0)
            self.file2label = Label(self.XRF, text="File2")
            self.file2label.grid(row=0, column=1)
            self.labellabel = Label(self.XRF, text="Label")
            self.labellabel.grid(row=0, column=2)
            self.titlelabel = Label(self.XRF, text="Title")
            self.titlelabel.grid(row=0, column=3)
            self.scatterlabel1 = Label(self.XRF, text="File1 Scatter")
            self.scatterlabel1.grid(row=0, column=4)
            self.scatterlabel2 = Label(self.XRF, text="File2 Scatter")
            self.scatterlabel2.grid(row=0, column=5)
            self.currentRow = 1
            self.titleLabel = Label(self.XRF, text="Title:")
            self.titleLabel.grid(row=self.currentRow, column=0)
            self.titleEntry = Entry(self.XRF)
            self.titleEntry.grid(row=self.currentRow, column=1)
            self.graphButton = Button(self.XRF, text="Graph selected")
            self.graphButton.bind("<Button-1>", self.graphSelected)
            self.graphButton.grid(row=self.currentRow, column=2)
            self.graphNormalButton = Button(self.XRF, text="Graph normal selected")
            self.graphNormalButton.bind("<Button-1>", self.graphNormalSelected)
            self.graphNormalButton.grid(row=self.currentRow, column=3)
            self.lastRow = self.makeRow()
            self.menu = Menu(self.XRF)
            self.fileMenu = Menu(self.menu)
            self.fileMenu.add_command(label="Add more data", command=self.makeRow)
            self.fileMenu.add_command(label="Add subtraction data", command=self.makeSubtractionRow)
            self.fileMenu.add_command(label="Delete row of data", command=self.removeRow)
            self.menu.add_cascade(label="File", menu=self.fileMenu)
            self.graphMenu = Menu(self.menu)
            self.elements = Menu(self.graphMenu)
            for i in range(3, 41):
                vars(self)["self." + ElementNames[i]] = IntVar(self.XRF)
                vars(self)["self." + ElementNames[i]].set(0)
            for i in range(3, 41):
                self.elements.add_checkbutton(label=ElementNames[i], variable=vars(self)["self." + ElementNames[i]],
                                              onvalue=1, offvalue=0)
            self.graphMenu.add_cascade(label="add element", menu=self.elements)
            self.menu.add_cascade(label="Graph", menu=self.graphMenu)
            self.elementMenu = Menu(self.menu)
            self.elementMenu.add_command(label="Lithium", command=self.lithiumPeak)
            self.elementMenu.add_command(label="Beryllium", command=self.berylliumPeak)
            self.elementMenu.add_command(label="Boron", command=self.boronPeak)
            self.elementMenu.add_command(label="Carbon", command=self.carbonPeak)
            self.elementMenu.add_command(label="Nitrogen", command=self.nitrogenPeak)
            self.elementMenu.add_command(label="Oxygen", command=self.oxygenPeak)
            self.elementMenu.add_command(label="Fluorine", command=self.fluorinePeak)
            self.elementMenu.add_command(label="Neon", command=self.neonPeak)
            self.elementMenu.add_command(label="Sodium", command=self.sodiumPeak)
            self.elementMenu.add_command(label="Mgagnesium", command=self.magnesiumPeak)
            self.elementMenu.add_command(label="Aluminium", command=self.aluminiumPeak)
            self.elementMenu.add_command(label="Silicon", command=self.siliconPeak)
            self.elementMenu.add_command(label="Phosphorus", command=self.phosphorusPeak)
            self.elementMenu.add_command(label="Sulfur", command=self.sulfurPeak)
            self.elementMenu.add_command(label="Chlorine", command=self.chlorinePeak)
            self.elementMenu.add_command(label="Argon", command=self.argonPeak)
            self.elementMenu.add_command(label="Potassium", command=self.potassiumPeak)
            self.elementMenu.add_command(label="Calcium", command=self.calciumPeak)
            self.elementMenu.add_command(label="Scandium", command=self.scandiumPeak)
            self.elementMenu.add_command(label="Titanium", command=self.titaniumPeak)
            self.elementMenu.add_command(label="Vanadium", command=self.vanadiumPeak)
            self.elementMenu.add_command(label="Chromium", command=self.chromiumPeak)
            self.elementMenu.add_command(label="Manganese", command=self.manganesePeak)
            self.elementMenu.add_command(label="Iron", command=self.ironPeak)
            self.elementMenu.add_command(label="Cobalt", command=self.cobaltPeak)
            self.elementMenu.add_command(label="Nickle", command=self.nicklePeak)
            self.elementMenu.add_command(label="Copper", command=self.copperPeak)
            self.elementMenu.add_command(label="Zinc", command=self.zincPeak)
            self.elementMenu.add_command(label="Gallium", command=self.galliumPeak)
            self.elementMenu.add_command(label="Germanium", command=self.germaniumPeak)
            self.elementMenu.add_command(label="Arsenic", command=self.arsenicPeak)
            self.elementMenu.add_command(label="Selenium", command=self.seleniumPeak)
            self.elementMenu.add_command(label="Bromine", command=self.brominePeak)
            self.elementMenu.add_command(label="Krypton", command=self.kryptonPeak)
            self.elementMenu.add_command(label="Rubidium", command=self.rubidiumPeak)
            self.elementMenu.add_command(label="Strontium", command=self.strontiumPeak)
            self.elementMenu.add_command(label="Yttirium", command=self.yttiriumPeak)
            self.elementMenu.add_command(label="Zirconium", command=self.zirconiumPeak)
            self.menu.add_cascade(label="Element Peaks", menu=self.elementMenu)
            self.XRF.config(menu=self.menu)

        def lithiumPeak(self):
            messagebox.showinfo("Lithium K edge Peak",
                                "You can find the peak at " + str(ElementEnergy[3]) + " electronvolts")

        def berylliumPeak(self):
            messagebox.showinfo("Beryllium K edge Peak",
                                "You can find the peak at " + str(ElementEnergy[4]) + " electronvolts")

        def boronPeak(self):
            messagebox.showinfo("Lithium K edge Peak",
                                "You can find the peak at " + str(ElementEnergy[5]) + " electronvolts")

        def carbonPeak(self):
            messagebox.showinfo("Lithium K edge Peak",
                                "You can find the peak at " + str(ElementEnergy[6]) + " electronvolts")

        def nitrogenPeak(self):
            messagebox.showinfo("Lithium K edge Peak",
                                "You can find the peak at " + str(ElementEnergy[7]) + " electronvolts")

        def oxygenPeak(self):
            messagebox.showinfo("Lithium K edge Peak",
                                "You can find the peak at " + str(ElementEnergy[8]) + " electronvolts")

        def fluorinePeak(self):
            messagebox.showinfo("Lithium K edge Peak",
                                "You can find the peak at " + str(ElementEnergy[9]) + " electronvolts")

        def neonPeak(self):
            messagebox.showinfo("Lithium K edge Peak",
                                "You can find the peak at " + str(ElementEnergy[10]) + " electronvolts")

        def sodiumPeak(self):
            messagebox.showinfo("Lithium K edge Peak",
                                "You can find the peak at " + str(ElementEnergy[1]) + " electronvolts")

        def magnesiumPeak(self):
            messagebox.showinfo("Lithium K edge Peak",
                                "You can find the peak at " + str(ElementEnergy[12]) + " electronvolts")

        def aluminiumPeak(self):
            messagebox.showinfo("Lithium K edge Peak",
                                "You can find the peak at " + str(ElementEnergy[13]) + " electronvolts")

        def siliconPeak(self):
            messagebox.showinfo("Lithium K edge Peak",
                                "You can find the peak at " + str(ElementEnergy[14]) + " electronvolts")

        def phosphorusPeak(self):
            messagebox.showinfo("Lithium K edge Peak",
                                "You can find the peak at " + str(ElementEnergy[15]) + " electronvolts")

        def sulfurPeak(self):
            messagebox.showinfo("Lithium K edge Peak",
                                "You can find the peak at " + str(ElementEnergy[16]) + " electronvolts")

        def chlorinePeak(self):
            messagebox.showinfo("Lithium K edge Peak",
                                "You can find the peak at " + str(ElementEnergy[17]) + " electronvolts")

        def argonPeak(self):
            messagebox.showinfo("Lithium K edge Peak",
                                "You can find the peak at " + str(ElementEnergy[18]) + " electronvolts")

        def potassiumPeak(self):
            messagebox.showinfo("Lithium K edge Peak",
                                "You can find the peak at " + str(ElementEnergy[19]) + " electronvolts")

        def calciumPeak(self):
            messagebox.showinfo("Lithium K edge Peak",
                                "You can find the peak at " + str(ElementEnergy[20]) + " electronvolts")

        def scandiumPeak(self):
            messagebox.showinfo("Lithium K edge Peak",
                                "You can find the peak at " + str(ElementEnergy[21]) + " electronvolts")

        def titaniumPeak(self):
            messagebox.showinfo("Lithium K edge Peak",
                                "You can find the peak at " + str(ElementEnergy[22]) + " electronvolts")

        def vanadiumPeak(self):
            messagebox.showinfo("Lithium K edge Peak",
                                "You can find the peak at " + str(ElementEnergy[23]) + " electronvolts")

        def chromiumPeak(self):
            messagebox.showinfo("Lithium K edge Peak",
                                "You can find the peak at " + str(ElementEnergy[24]) + " electronvolts")

        def manganesePeak(self):
            messagebox.showinfo("Lithium K edge Peak",
                                "You can find the peak at " + str(ElementEnergy[25]) + " electronvolts")

        def ironPeak(self):
            messagebox.showinfo("Lithium K edge Peak",
                                "You can find the peak at " + str(ElementEnergy[26]) + " electronvolts")

        def cobaltPeak(self):
            messagebox.showinfo("Lithium K edge Peak",
                                "You can find the peak at " + str(ElementEnergy[27]) + " electronvolts")

        def nicklePeak(self):
            messagebox.showinfo("Lithium K edge Peak",
                                "You can find the peak at " + str(ElementEnergy[28]) + " electronvolts")

        def copperPeak(self):
            messagebox.showinfo("Lithium K edge Peak",
                                "You can find the peak at " + str(ElementEnergy[29]) + " electronvolts")

        def zincPeak(self):
            messagebox.showinfo("Lithium K edge Peak",
                                "You can find the peak at " + str(ElementEnergy[30]) + " electronvolts")

        def galliumPeak(self):
            messagebox.showinfo("Lithium K edge Peak",
                                "You can find the peak at " + str(ElementEnergy[31]) + " electronvolts")

        def germaniumPeak(self):
            messagebox.showinfo("Lithium K edge Peak",
                                "You can find the peak at " + str(ElementEnergy[32]) + " electronvolts")

        def arsenicPeak(self):
            messagebox.showinfo("Lithium K edge Peak",
                                "You can find the peak at " + str(ElementEnergy[33]) + " electronvolts")

        def seleniumPeak(self):
            messagebox.showinfo("Lithium K edge Peak",
                                "You can find the peak at " + str(ElementEnergy[34]) + " electronvolts")

        def brominePeak(self):
            messagebox.showinfo("Lithium K edge Peak",
                                "You can find the peak at " + str(ElementEnergy[35]) + " electronvolts")

        def kryptonPeak(self):
            messagebox.showinfo("Lithium K edge Peak",
                                "You can find the peak at " + str(ElementEnergy[36]) + " electronvolts")

        def rubidiumPeak(self):
            messagebox.showinfo("Lithium K edge Peak",
                                "You can find the peak at " + str(ElementEnergy[37]) + " electronvolts")

        def strontiumPeak(self):
            messagebox.showinfo("Lithium K edge Peak",
                                "You can find the peak at " + str(ElementEnergy[38]) + " electronvolts")

        def yttiriumPeak(self):
            messagebox.showinfo("Lithium K edge Peak",
                                "You can find the peak at " + str(ElementEnergy[39]) + " electronvolts")

        def zirconiumPeak(self):
            messagebox.showinfo("Lithium K edge Peak",
                                "You can find the peak at " + str(ElementEnergy[40]) + " electronvolts")

        def makeRow(self):
            vars(self)["self.row" + str(self.currentRow)] = xrfRow(self, self.currentRow)
            self.lastRow = vars(self)["self.row" + str(self.currentRow)]
            self.currentRow += 1
            self.titleLabel.grid(row=self.currentRow, column=0)
            self.titleEntry.grid(row=self.currentRow, column=1)
            self.graphButton.grid(row=self.currentRow, column=2)
            self.graphNormalButton.grid(row=self.currentRow, column=3)

        def makeSubtractionRow(self):
            vars(self)["self.row" + str(self.currentRow)] = xrfRowSubtract(self, self.currentRow)
            self.lastRow = vars(self)["self.row" + str(self.currentRow)]
            self.currentRow += 1
            self.titleLabel.grid(row=self.currentRow, column=0)
            self.titleEntry.grid(row=self.currentRow, column=1)
            self.graphButton.grid(row=self.currentRow, column=2)
            self.graphNormalButton.grid(row=self.currentRow, column=3)

        def removeRow(self):
            self.lastRow.destroy()
            self.currentRow -= 2
            self.lastRow = vars(self)["self.row" + str(self.currentRow)]
            self.currentRow += 1
            self.titleLabel.grid(row=self.currentRow, column=0)
            self.titleEntry.grid(row=self.currentRow, column=1)
            self.graphButton.grid(row=self.currentRow, column=2)
            self.graphNormalButton.grid(row=self.currentRow, column=3)

        def graphSelected(self, event):
            for i in range(1, self.currentRow):
                if vars(self)["self.row" + str(i)].shouldgraph1.get() == True:
                    if not vars(self)["self.row" + str(i)].isSub:
                        file = xrfFile(vars(self)["self.row" + str(i)].enterfile1.get(), self,
                                       vars(self)["self.row" + str(i)])
                        lab = vars(self)["self.row" + str(i)].sample1entry.get()
                        plot(file.energy, file.counts, label=lab)
                    elif vars(self)["self.row" + str(i)].isSub:
                        file1 = xrfSubtractionFile(vars(self)["self.row" + str(i)].enterfile1.get(), self,
                                                   vars(self)["self.row" + str(i)])
                        file2 = xrfSubtractionFile(vars(self)["self.row" + str(i)].enterFile2.get(), self,
                                                   vars(self)["self.row" + str(i)])
                        if len(file1.energy) == len(
                                file2.energy):  # determining the energy to use, this only works if the incrementation is the same
                            energyu = file1.energy
                        elif len(file1.energy) == minlength(file1.energy, file2.energy):
                            energyu = file1.energy
                            file2.counts = file2.counts[:len(file1.energy) + 1]
                        elif len(file2.energy) == minlength(file1.energy, file2.energy):
                            energyu = file2.energy
                            file1.counts = file1.counts[:len(file1.energy) + 1]
                        difference = file1.counts - file2.counts
                        lab = vars(self)["self.row" + str(i)].labelEntry.get()
                        plot(energyu, difference, label=lab)
            seepeaks1 = messagebox.askquestion("Sample Peaks", "Would you like to better see the peaks of your sample?")
            if seepeaks1 == "yes":
                for i in range(1, self.currentRow):
                    if vars(self)["self.row" + str(i)].shouldgraph1.get() == True:
                        if not vars(self)["self.row" + str(i)].isSub:
                            file = xrfFile(vars(self)["self.row" + str(i)].enterfile1.get(), self,
                                           vars(self)["self.row" + str(i)])
                            plot(file.peakse, file.peaks, 'ro')
                        elif vars(self)["self.row" + str(i)].isSub:
                            file1 = xrfSubtractionFile(vars(self)["self.row" + str(i)].enterfile1.get(), self,
                                                       vars(self)["self.row" + str(i)])
                            file2 = xrfSubtractionFile(vars(self)["self.row" + str(i)].enterFile2.get(), self,
                                                       vars(self)["self.row" + str(i)])
                            if len(file1.energy) == len(
                                    file2.energy):  # determining the energy to use, this only works if the incrementation is the same
                                energyu = file1.energy
                            elif len(file1.energy) == minlength(file1.energy, file2.energy):
                                energyu = file1.energy
                                file2.counts = file2.counts[:len(file1.energy) + 1]
                            elif len(file2.energy) == minlength(file1.energy, file2.energy):
                                energyu = file2.energy
                                file1.counts = file1.counts[:len(file1.energy) + 1]
                            peaks = []  # creating empty lists to store information about the peaks in the smaple
                            peakse = []
                            for i in range(len(
                                    energyu)):  # this section stores information about the peaks in the sample in the empty lists
                                if i != 0 and i != len(energyu) - 1:
                                    if difference[i - 1] < difference[i] and difference[i + 1] < difference[i] and (
                                            difference[i - 1] + difference[i] + difference[i + 1]) > (
                                            difference[i - 4] + difference[i - 3] + difference[i - 2]) and (
                                            difference[i - 1] + difference[i] + difference[i + 1]) > (
                                            difference[i + 4] + difference[i + 3] + difference[i + 2]) and difference[
                                        i] > max(difference) / 500:
                                        peaks.append(difference[i])
                                        peakse.append(energyu[i])
                            plot(peakse, peaks, 'ro')
            xlabel("Energy(eV)")
            ylabel("Photon Counts")
            for i in range(3, 41):
                if vars(self)["self." + ElementNames[i]].get() == True:
                    axvline(ElementEnergy[i])
            legend()
            Title = self.titleEntry.get()
            title(Title)
            show()

        def graphNormalSelected(self, event):
            for i in range(1, self.currentRow):
                if vars(self)["self.row" + str(i)].shouldgraph1.get() == True:
                    if not vars(self)["self.row" + str(i)].isSub:
                        file = xrfFile(vars(self)["self.row" + str(i)].enterfile1.get(), self,
                                       vars(self)["self.row" + str(i)])
                        scatter = float(vars(self)["self.row" + str(i)].scatter1entry.get())
                        normcounts = file.counts / file.scattercounts(scatter)
                        lab = vars(self)["self.row" + str(i)].sample1entry.get()
                        plot(file.energy, normcounts, label=lab)
                    elif vars(self)["self.row" + str(i)].isSub:
                        file1 = xrfSubtractionFile(vars(self)["self.row" + str(i)].enterfile1.get(), self,
                                                   vars(self)["self.row" + str(i)])
                        file2 = xrfSubtractionFile(vars(self)["self.row" + str(i)].enterFile2.get(), self,
                                                   vars(self)["self.row" + str(i)])
                        scatter1 = float(vars(self)["self.row" + str(i)].scatter1Entry.get())
                        scatter2 = float(vars(self)["self.row" + str(i)].scatter2Entry.get())
                        if len(file1.energy) == len(
                                file2.energy):  # determining the energy to use, this only works if the incrementation is the same
                            energyu = file1.energy
                        elif len(file1.energy) == minlength(file1.energy, file2.energy):
                            energyu = file1.energy
                            file2.counts = file2.counts[:len(file1.energy) + 1]
                        elif len(file2.energy) == minlength(self.energy, file2.energy):
                            energyu = file2.energy
                            file1.counts = file1.counts[:len(file1.energy) + 1]
                        lab = vars(self)["self.row" + str(i)].labelEntry.get()
                        difference = file1.counts / file1.scattercounts(scatter1) - file2.counts / file2.scattercounts(
                            scatter2)
                        plot(energyu, difference, label=lab)
            seepeaks1 = messagebox.askquestion("Sample Peaks", "Would you like to better see the peaks of your sample?")
            if seepeaks1 == "yes":
                for i in range(1, self.currentRow):
                    if vars(self)["self.row" + str(i)].shouldgraph1.get() == True:
                        if vars(self)["self.row" + str(i)].isSub == False:
                            file = xrfFile(vars(self)["self.row" + str(i)].enterfile1.get(), self,
                                           vars(self)["self.row" + str(i)])
                            scatter = float(vars(self)["self.row" + str(i)].scatter1entry.get())
                            normpeaks = array(file.peaks) / file.scattercounts(scatter)
                            plot(array(file.peakse), normpeaks, 'ro')
                        elif vars(self)["self.row" + str(i)].isSub == True:
                            file1 = xrfSubtractionFile(vars(self)["self.row" + str(i)].enterfile1.get(), self,
                                                       vars(self)["self.row" + str(i)])
                            file2 = xrfSubtractionFile(vars(self)["self.row" + str(i)].enterFile2.get(), self,
                                                       vars(self)["self.row" + str(i)])
                            scatter1 = float(vars(self)["self.row" + str(i)].scatter1Entry.get())
                            scatter2 = float(vars(self)["self.row" + str(i)].scatter2Entry.get())
                            if len(file1.energy) == len(
                                    file2.energy):  # determining the energy to use, this only works if the incrementation is the same
                                energyu = file1.energy
                            elif len(file1.energy) == minlength(file1.energy, file2.energy):
                                energyu = file1.energy
                                file2.counts = file2.counts[:len(file1.energy) + 1]
                            elif len(file2.energy) == minlength(self.energy, file2.energy):
                                energyu = file2.energy
                                file1.counts = file1.counts[:len(file1.energy) + 1]
                            peaks = []  # creating empty lists to store information about the peaks in the smaple
                            peakse = []
                            for i in range(len(
                                    energyu)):  # this section stores information about the peaks in the sample in the empty lists
                                if i != 0 and i != len(energyu) - 1:
                                    if difference[i - 1] < difference[i] and difference[i + 1] < difference[i] and (
                                            difference[i - 1] + difference[i] + difference[i + 1]) > (
                                            difference[i - 4] + difference[i - 3] + difference[i - 2]) and (
                                            difference[i - 1] + difference[i] + difference[i + 1]) > (
                                            difference[i + 4] + difference[i + 3] + difference[i + 2]) and difference[
                                        i] > max(difference) / 500:
                                        peaks.append(difference[i])
                                        peakse.append(energyu[i])
                            plot(peakse, peaks, 'ro')
            xlabel("Energy(eV)")
            ylabel("Photon Counts")
            for i in range(3, 41):
                if vars(self)["self." + ElementNames[i]].get() == True:
                    axvline(ElementEnergy[i])
            legend()
            Title = self.titleEntry.get()
            title(Title)
            show()

    def runXRF(event):
        a = xrfProgram()
        a.XRF.mainloop()

    class xanesFile:
        def __init__(self, file, XANES, Row):
            self.XANESProgram = XANES
            self.row = Row
            self.data = loadtxt(file + ".txt")
            if len(self.data[0]) >= 13:
                self.energy = self.data[:, 12]
                self.counts = self.data[:, 13]
            elif len(self.data[0]) < 13:
                self.energy = self.data[:, 0]
                self.counts = self.data[:, 7]
            self.peaks = []
            self.peakse = []
            self.peaksIndex = []
            for i in range(len(self.energy) - 4):
                if i != 0 and i != len(self.energy) - 1:
                    if self.counts[i - 1] < self.counts[i] and self.counts[i + 1] < self.counts[i] and (
                            self.counts[i - 1] + self.counts[i] + self.counts[i + 1]) > (
                            self.counts[i - 4] + self.counts[i - 3] + self.counts[i - 2]) and (
                            self.counts[i - 1] + self.counts[i] + self.counts[i + 1]) > (
                            self.counts[i + 4] + self.counts[i + 3] + self.counts[i + 2]) and self.counts[i] > max(
                            self.counts) / 500:
                        self.peaks.append(self.counts[i])
                        self.peakse.append(self.energy[i])
                        self.peaksIndex.append(i)
            self.differences = [0]
            for i in range(1, len(self.peaksIndex)):
                self.differences.append(self.counts[self.peaksIndex[i]] - self.counts[self.peaksIndex[i - 1]])
            self.upperIndex = self.peaksIndex[mostcounts(self.differences)]
            self.lowerIndex = self.peaksIndex[mostcounts(self.differences) - 1]
            self.counts1 = []
            self.energy1 = []
            for i in range(self.lowerIndex, self.upperIndex + 1):
                self.counts1.append(self.counts[i])
                self.energy1.append(self.energy[i])
            self.deriv = []
            for j in range(1, len(self.counts1) - 1):
                self.deriv.append(
                    (self.counts1[j + 1] - self.counts1[j - 1]) / (self.energy1[j + 1] - self.energy1[j - 1]))
            self.absorptionedge = self.counts1[mostcounts(self.deriv) + 1]
            self.absorptionedgee = self.energy1[mostcounts(self.deriv) + 1]

        def absorptionEdge(self):
            messagebox.showinfo("Absoption Edge", str(self.absorptionedgee) + "eV")

        def graph(self):
            lab = self.row.labelEntry.get()
            plot(self.energy, self.counts, label=lab)
            seepeaks1 = messagebox.askquestion("Sample Peaks", "Would you like to better see the peaks of your sample?")
            if seepeaks1 == "yes":
                plot(self.peakse, self.peaks, 'ro')
            showabs = messagebox.askquestion("Absorption Edge", "Would you like to better see the absorption edge?")
            if showabs == "yes":
                axvline(x=self.absorptionedgee)
            legend()
            Title = self.row.titleEntry.get()
            title(Title)
            show()

        def normalGraph(self):
            plot(self.energy, self.counts / self.absorptionedge, label=self.row.labelEntry.get())
            seepeaks1 = messagebox.askquestion("Sample Peaks", "Would you like to better see the peaks of your sample?")
            if seepeaks1 == "yes":
                plot(self.peakse, self.peaks / self.absorptionedge, 'ro')
            showabs = messagebox.askquestion("Absorption Edge", "Would you like to see the absorption edge?")
            if showabs == "yes":
                axvline(x=self.absorptionedgee)
            legend()
            title(self.row.titleEntry.get())
            show()

        def Peaks(self):
            s = ""
            for i in range(len(self.peakse)):
                s += str(self.peakse[i]) + "eV, "
            messagebox.showinfo("Peak Energy", s[:len(s) - 2])

    class xanesSubtractionFile:
        def __init__(self, file, XANES, Row):
            self.XANESProgram = XANES
            self.row = Row
            self.data = loadtxt(file + ".txt")
            if len(self.data[0]) >= 13:
                self.energy = self.data[:, 12]
                self.counts = self.data[:, 13]
            elif len(self.data[0]) < 13:
                self.energy = self.data[:, 0]
                self.counts = self.data[:, 7]
            self.peaks = []
            self.peakse = []
            self.peaksIndex = []
            for i in range(len(self.energy) - 4):
                if i != 0 and i != len(self.energy) - 1:
                    if self.counts[i - 1] < self.counts[i] and self.counts[i + 1] < self.counts[i] and (
                            self.counts[i - 1] + self.counts[i] + self.counts[i + 1]) > (
                            self.counts[i - 4] + self.counts[i - 3] + self.counts[i - 2]) and (
                            self.counts[i - 1] + self.counts[i] + self.counts[i + 1]) > (
                            self.counts[i + 4] + self.counts[i + 3] + self.counts[i + 2]) and self.counts[i] > max(
                            self.counts) / 500:
                        self.peaks.append(self.counts[i])
                        self.peakse.append(self.energy[i])
                        self.peaksIndex.append(i)
            self.differences = [0]
            for i in range(1, len(self.peaksIndex)):
                self.differences.append(self.counts[self.peaksIndex[i]] - self.counts[self.peaksIndex[i - 1]])
            self.upperIndex = self.peaksIndex[mostcounts(self.differences)]
            self.lowerIndex = self.peaksIndex[mostcounts(self.differences) - 1]
            self.counts1 = []
            self.energy1 = []
            for i in range(self.lowerIndex, self.upperIndex + 1):
                self.counts1.append(self.counts[i])
                self.energy1.append(self.energy[i])
            self.deriv = []
            for j in range(1, len(self.counts1) - 1):
                self.deriv.append(
                    (self.counts1[j + 1] - self.counts1[j - 1]) / (self.energy1[j + 1] - self.energy1[j - 1]))
            self.absorptionedge = self.counts1[mostcounts(self.deriv) + 1]
            self.absorptionedgee = self.energy1[mostcounts(self.deriv) + 1]

        def graphSubtraction(self):
            file2 = xanesSubtractionFile(self.row.file2Entry.get(), self.XANESProgram, self.row)
            if len(self.energy) == len(
                    file2.energy):  # determining the energy to use, this only works if the incrementation is the same
                energyu = self.energy
            elif len(self.energy) == minlength(self.energy, file2.energy):
                energyu = self.energy
                file2.counts = file2.counts[:len(self.energy) + 1]
            elif len(file2.energy) == minlength(self.energy, file2.energy):
                energyu = file2.energy
                self.counts = self.counts[:len(self.energy) + 1]
            difference = self.counts - file2.counts
            plot(energyu, difference, label=self.row.labelEntry.get())
            seepeaks1 = messagebox.askquestion("Sample Peaks", "Would you like to better see the peaks of your sample?")
            if seepeaks1 == "yes":
                peaks = []  # creating empty lists to store information about the peaks in the smaple
                peakse = []
                for i in range(len(
                        energyu)):  # this section stores information about the peaks in the sample in the empty lists
                    if i != 0 and i != len(energyu) - 1:
                        if difference[i - 1] < difference[i] and difference[i + 1] < difference[i] and (
                                difference[i - 1] + difference[i] + difference[i + 1]) > (
                                difference[i - 4] + difference[i - 3] + difference[i - 2]) and (
                                difference[i - 1] + difference[i] + difference[i + 1]) > (
                                difference[i + 4] + difference[i + 3] + difference[i + 2]) and difference[i] > max(
                                difference) / 500:
                            peaks.append(difference[i])
                            peakse.append(energyu[i])
                plot(peakse, peaks, 'ro')
            legend()
            title(self.row.titleEntry.get())
            show()

        def graphNormalSubtraction(self):
            file2 = xanesSubtractionFile(self.row.file2Entry.get(), self.XANESProgram, self.row)
            if len(self.energy) == len(
                    file2.energy):  # determining the energy to use, this only works if the incrementation is the same
                energyu = self.energy
            elif len(self.energy) == minlength(self.energy, file2.energy):
                energyu = self.energy
                file2.counts = file2.counts[:len(self.energy) + 1]
            elif len(file2.energy) == minlength(self.energy, file2.energy):
                energyu = file2.energy
                self.counts = self.counts[:len(self.energy) + 1]
            difference = self.counts / self.absorptionedge - file2.counts / file2.absorptionedge
            plot(energyu, difference, label=self.row.labelEntry.get())
            seepeaks1 = messagebox.askquestion("Sample Peaks", "Would you like to better see the peaks of your sample?")
            if seepeaks1 == "yes":
                peaks = []  # creating empty lists to store information about the peaks in the smaple
                peakse = []
                for i in range(len(
                        energyu)):  # this section stores information about the peaks in the sample in the empty lists
                    if i != 0 and i != len(energyu) - 1:
                        if difference[i - 1] < difference[i] and difference[i + 1] < difference[i] and (
                                difference[i - 1] + difference[i] + difference[i + 1]) > (
                                difference[i - 4] + difference[i - 3] + difference[i - 2]) and (
                                difference[i - 1] + difference[i] + difference[i + 1]) > (
                                difference[i + 4] + difference[i + 3] + difference[i + 2]) and difference[i] > max(
                                difference) / 500:
                            peaks.append(difference[i])
                            peakse.append(energyu[i])
                plot(peakse, peaks, 'ro')
            legend()
            title(self.row.titleEntry.get())
            show()

    class xanesRow:
        def __init__(self, XANESProgram, r):
            self.isSub = False
            self.XANESProgram = XANESProgram
            self.file1Entry = Entry(self.XANESProgram.XANES)
            self.file1Entry.grid(row=r, column=0)
            self.labelEntry = Entry(self.XANESProgram.XANES)
            self.labelEntry.grid(row=r, column=2)
            self.titleEntry = Entry(self.XANESProgram.XANES)
            self.titleEntry.grid(row=r, column=3)
            self.graphButton = Button(self.XANESProgram.XANES, text="Graph")
            self.graphButton.bind("<Button-1>", self.plot)
            self.graphButton.grid(row=r, column=4)
            self.graphNormalButton = Button(self.XANESProgram.XANES, text="Graph normal")
            self.graphNormalButton.bind("<Button-1>", self.plotNormal)
            self.graphNormalButton.grid(row=r, column=5)
            self.absorptionEdgeButton = Button(self.XANESProgram.XANES, text="Absorption Edge")
            self.absorptionEdgeButton.bind("<Button-1>", self.absorptionEdge)
            self.absorptionEdgeButton.grid(row=r, column=6)
            self.peaksButton = Button(self.XANESProgram.XANES, text="Peaks")
            self.peaksButton.bind("<Button-1>", self.getPeaks)
            self.peaksButton.grid(row=r, column=7)
            self.shouldgraph1 = IntVar(self.XANESProgram.XANES)
            self.graph1check = Checkbutton(self.XANESProgram.XANES, text="graph this data", variable=self.shouldgraph1)
            self.graph1check.grid(row=r, column=8)

        def destroy(self):
            self.file1Entry.destroy()
            self.labelEntry.destroy()
            self.titleEntry.destroy()
            self.absorptionEdgeButton.destroy()
            self.graph1check.destroy()
            self.graphButton.destroy()
            self.graphNormalButton.destroy()
            self.absorptionEdgeButton.destroy()
            self.peaksButton.destroy()

        def absorptionEdge(self, event):
            file1 = xanesFile(self.file1Entry.get(), self.XANESProgram, self)
            file1.absorptionEdge()

        def plot(self, event):
            file1 = xanesFile(self.file1Entry.get(), self.XANESProgram, self)
            file1.graph()

        def plotNormal(self, event):
            file1 = xanesFile(self.file1Entry.get(), self.XANESProgram, self)
            file1.normalGraph()

        def getPeaks(self, event):
            file1 = xanesFile(self.file1Entry.get(), self.XANESProgram, self)
            file1.Peaks()

    class xanesSubtractionRow:
        def __init__(self, XANESProgram, r):
            self.XANESProgram = XANESProgram
            self.isSub = True
            self.file1Entry = Entry(XANESProgram.XANES)
            self.file1Entry.grid(row=r, column=0)
            self.file2Entry = Entry(XANESProgram.XANES)
            self.file2Entry.grid(row=r, column=1)
            self.labelEntry = Entry(XANESProgram.XANES)
            self.labelEntry.grid(row=r, column=2)
            self.titleEntry = Entry(XANESProgram.XANES)
            self.titleEntry.grid(row=r, column=3)
            self.graphButton = Button(self.XANESProgram.XANES, text="Graph")
            self.graphButton.bind("<Button-1>", self.graphSubtraction)
            self.graphButton.grid(row=r, column=4)
            self.graphNormalButton = Button(self.XANESProgram.XANES, text="Graph normal")
            self.graphNormalButton.bind("<Button-1>", self.graphNormalSubtraction)
            self.graphNormalButton.grid(row=r, column=5)
            self.shouldgraph1 = IntVar(self.XANESProgram.XANES)
            self.graph1check = Checkbutton(self.XANESProgram.XANES, text="graph this data", variable=self.shouldgraph1)
            self.graph1check.grid(row=r, column=8)

        def destroy(self):
            self.file1Entry.destroy()
            self.file2Entry.destroy()
            self.labelEntry.destroy()
            self.titleEntry.destroy()
            self.graphButton.destroy()
            self.graphNormalButton.destroy()
            self.graph1check.destroy()

        def graphSubtraction(self, event):
            file1 = xanesSubtractionFile(self.file1Entry.get(), self.XANESProgram, self)
            file1.graphSubtraction()

        def graphNormalSubtraction(self, event):
            file1 = xanesSubtractionFile(self.file1Entry.get(), self.XANESProgram, self)
            file1.graphNormalSubtraction()

    class standardNFile:
        def __init__(self, LCF, Row):
            self.LCFProgram = LCF
            self.row = Row
            self.data = loadtxt(self.row.standardEntry.get() + ".txt")
            if len(self.data[0]) >= 13:
                self.energy = self.data[:, 12]
                self.counts = self.data[:, 13]
            elif len(self.data[0]) < 13:
                self.energy = self.data[:, 0]
                self.counts = self.data[:, 7]
            self.counts1 = array([0])
            self.energy1 = array([0])
            self.peaks = []
            self.peakse = []
            self.peaksIndex = []
            for i in range(len(self.energy) - 4):
                if i != 0 and i != len(self.energy) - 1:
                    if self.counts[i - 1] < self.counts[i] and self.counts[i + 1] < self.counts[i] and (
                            self.counts[i - 1] + self.counts[i] + self.counts[i + 1]) > (
                            self.counts[i - 4] + self.counts[i - 3] + self.counts[i - 2]) and (
                            self.counts[i - 1] + self.counts[i] + self.counts[i + 1]) > (
                            self.counts[i + 4] + self.counts[i + 3] + self.counts[i + 2]) and self.counts[i] > max(
                            self.counts) / 500:
                        self.peaks.append(self.counts[i])
                        self.peakse.append(self.energy[i])
                        self.peaksIndex.append(i)
            self.differences = [0]
            for i in range(1, len(self.peaksIndex)):
                self.differences.append(self.counts[self.peaksIndex[i]] - self.counts[self.peaksIndex[i - 1]])
            self.upperIndex = self.peaksIndex[mostcounts(self.differences)]
            self.lowerIndex = self.peaksIndex[mostcounts(self.differences) - 1]
            self.counts1 = []
            self.energy1 = []
            for i in range(self.lowerIndex, self.upperIndex + 1):
                self.counts1.append(self.counts[i])
                self.energy1.append(self.energy[i])
            self.deriv = []
            for j in range(1, len(self.counts1) - 1):
                self.deriv.append(
                    (self.counts1[j + 1] - self.counts1[j - 1]) / (self.energy1[j + 1] - self.energy1[j - 1]))
            self.absorptionedge = self.counts1[mostcounts(self.deriv) + 1]
            self.absorptionedgee = self.energy1[mostcounts(self.deriv) + 1]

        def cutCounts(self, start, end):
            i = 0
            while self.energy[i] < start:
                i += 1
            j = 0
            while self.energy[j] < end:
                j += 1
            self.counts1 = self.counts[i:j + 1]
            self.energy1 = self.energy[i:j + 1]

    class standardNRow:
        def __init__(self, LCF, r):
            self.LCFProgram = LCF
            self.standardLabel = Label(self.LCFProgram.LCF, text="Standard " + str(r - 1))
            self.standardLabel.grid(row=r, column=0)
            self.standardEntry = Entry(self.LCFProgram.LCF)
            self.standardEntry.grid(row=r, column=1)
            self.coefficientLabel = Label(self.LCFProgram.LCF, text="0")
            self.coefficientLabel.grid(row=r, column=2)

        def destroyCoefficients(self):
            self.coefficientLabel.destroy()

        def destroy(self):
            self.standardLabel.destroy()
            self.standardEntry.destroy()
            self.coefficientLabel.destroy()

    class sampleNFile:
        def __init__(self, LCF):
            self.LCFProgram = LCF
            self.data = loadtxt(self.LCFProgram.fileEntry.get() + ".txt")
            if len(self.data[0]) >= 13:
                self.energy = self.data[:, 12]
                self.counts = self.data[:, 13]
            elif len(self.data[0]) < 13:
                self.energy = self.data[:, 0]
                self.counts = self.data[:, 7]
            self.counts1 = array([0])
            self.energy1 = array([0])
            self.peaks = []
            self.peakse = []
            self.peaksIndex = []
            for i in range(len(self.energy) - 4):
                if i != 0 and i != len(self.energy) - 1:
                    if self.counts[i - 1] < self.counts[i] and self.counts[i + 1] < self.counts[i] and (
                            self.counts[i - 1] + self.counts[i] + self.counts[i + 1]) > (
                            self.counts[i - 4] + self.counts[i - 3] + self.counts[i - 2]) and (
                            self.counts[i - 1] + self.counts[i] + self.counts[i + 1]) > (
                            self.counts[i + 4] + self.counts[i + 3] + self.counts[i + 2]) and self.counts[i] > max(
                            self.counts) / 500:
                        self.peaks.append(self.counts[i])
                        self.peakse.append(self.energy[i])
                        self.peaksIndex.append(i)
            self.differences = [0]
            for i in range(1, len(self.peaksIndex)):
                self.differences.append(self.counts[self.peaksIndex[i]] - self.counts[self.peaksIndex[i - 1]])
            self.upperIndex = self.peaksIndex[mostcounts(self.differences)]
            self.lowerIndex = self.peaksIndex[mostcounts(self.differences) - 1]
            self.counts1 = []
            self.energy1 = []
            for i in range(self.lowerIndex, self.upperIndex + 1):
                self.counts1.append(self.counts[i])
                self.energy1.append(self.energy[i])
            self.deriv = []
            for j in range(1, len(self.counts1) - 1):
                self.deriv.append(
                    (self.counts1[j + 1] - self.counts1[j - 1]) / (self.energy1[j + 1] - self.energy1[j - 1]))
            self.absorptionedge = self.counts1[mostcounts(self.deriv) + 1]
            self.absorptionedgee = self.energy1[mostcounts(self.deriv) + 1]

        def cutCounts(self, start, end):
            i = 0
            while self.energy[i] < start:
                i += 1
            j = 0
            while self.energy[j] < end:
                j += 1
            self.counts1 = self.counts[i:j + 1]
            self.energy1 = self.energy[i:j + 1]

    class lcfNProgram:
        def __init__(self):
            self.LCF = Tk()
            self.LCF.title("Linear Combination Fitting")
            self.filelabel = Label(self.LCF, text="File")
            self.filelabel.grid(row=0, column=1)
            self.sampleLabel = Label(self.LCF, text="Sample")
            self.sampleLabel.grid(row=1, column=0)
            self.coefficientsLabel = Label(self.LCF, text="Coeficcients")
            self.coefficientsLabel.grid(row=0, column=2)
            self.coefficientsButton = Button(self.LCF, text="get coefficients")
            self.coefficientsButton.bind("<Button-1>", self.getCoefficients)
            self.coefficientsButton.grid(row=0, column=3)
            self.rangeLabel = Label(self.LCF, text="Fit range")
            self.rangeLabel.grid(row=0, column=4)
            self.rangeEntry1 = Entry(self.LCF)
            self.rangeEntry1.grid(row=0, column=5)
            self.toLabel = Label(self.LCF, text=":")
            self.toLabel.grid(row=0, column=6)
            self.rangeEntry2 = Entry(self.LCF)
            self.rangeEntry2.grid(row=0, column=7)
            self.plotButton = Button(self.LCF, text="Plot LCF")
            self.plotButton.bind("<Button-1>", self.plotLCF)
            self.plotButton.grid(row=0, column=8)
            self.plotDifferenceButton = Button(self.LCF, text="Plot Difference")
            self.plotDifferenceButton.bind("<Button-1>", self.plotSubtraction)
            self.plotDifferenceButton.grid(row=0, column=9)
            self.plotAllButton = Button(self.LCF, text="Plot LCF, Difference, and Sample")
            self.plotAllButton.bind("<Button-1>", self.plotAll)
            self.plotAllButton.grid(row=0, column=10)
            self.fileEntry = Entry(self.LCF)
            self.fileEntry.grid(row=1, column=1)
            self.currentRow = 2
            self.addStandard()
            self.menu = Menu(self.LCF)
            self.fileMenu = Menu(self.menu)
            self.fileMenu.add_command(label="add a standard", command=self.addStandard)
            self.fileMenu.add_command(label="remove a standard", command=self.destroyRow)
            self.menu.add_cascade(label="File", menu=self.fileMenu)
            self.LCF.config(menu=self.menu)

        def addStandard(self):
            vars(self)["self.row" + str(self.currentRow)] = standardNRow(self, self.currentRow)
            self.lastRow = vars(self)["self.row" + str(self.currentRow)]
            self.currentRow += 1

        def destroyRow(self):
            self.lastRow.destroy()
            self.currentRow -= 2
            self.lastRow = vars(self)["self.row" + str(self.currentRow)]
            self.currentRow += 1

        def getCoefficients(self, event):
            if self.currentRow == 3:
                a1 = 1
                vars(self)["self.row" + str(2)].coefficientLabel = Label(self.LCF, text=str(a1))
                vars(self)["self.row" + str(2)].coefficientLabel.grid(row=2, column=2)
            elif self.currentRow == 4:
                sample = sampleNFile(self)
                sample.cutCounts(float(self.rangeEntry1.get()), float(self.rangeEntry2.get()))
                standard1 = standardNFile(self, vars(self)["self.row" + str(2)])
                standard2 = standardNFile(self, vars(self)["self.row" + str(3)])
                standard1.cutCounts(float(self.rangeEntry1.get()), float(self.rangeEntry2.get()))
                standard2.cutCounts(float(self.rangeEntry1.get()), float(self.rangeEntry2.get()))
                a1 = sum(
                    sample.counts1 * standard1.counts1 - sample.counts1 * standard2.counts1 - standard1.counts1 * standard2.counts1 + standard2.counts1 * standard2.counts1) / sum(
                    standard1.counts1 * standard1.counts1 - 2 * standard1.counts1 * standard2.counts1 + standard2.counts1 * standard2.counts1)
                a2 = 1 - a1
                vars(self)["self.row" + str(2)].coefficientLabel = Label(self.LCF, text=str(a1))
                vars(self)["self.row" + str(2)].coefficientLabel.grid(row=2, column=2)
                vars(self)["self.row" + str(3)].coefficientLabel = Label(self.LCF, text=str(a2))
                vars(self)["self.row" + str(3)].coefficientLabel.grid(row=3, column=2)
            elif self.currentRow > 4:
                sample = sampleNFile(self)
                sample.cutCounts(float(self.rangeEntry1.get()), float(self.rangeEntry2.get()))
                for i in range(2, self.currentRow):
                    vars(self)["standard" + str(i - 1)] = standardNFile(self, vars(self)["self.row" + str(i)])
                    vars(self)["standard" + str(i - 1)].cutCounts(float(self.rangeEntry1.get()),
                                                                  float(self.rangeEntry2.get()))
                A = empty([self.currentRow - 3, self.currentRow - 3])
                for i in range(self.currentRow - 3):
                    for j in range(self.currentRow - 3):
                        A[i][j] = sum(
                            vars(self)["standard" + str(i + 1)].counts1 * vars(self)["standard" + str(j + 1)].counts1 -
                            vars(self)["standard" + str(self.currentRow - 2)].counts1 * vars(self)[
                                "standard" + str(i + 1)].counts1 - vars(self)["standard" + str(j + 1)].counts1 *
                            vars(self)["standard" + str(self.currentRow - 2)].counts1 + vars(self)[
                                "standard" + str(self.currentRow - 2)].counts1 * vars(self)[
                                "standard" + str(self.currentRow - 2)].counts1)
                X = empty([self.currentRow - 3])
                for i in range(self.currentRow - 3):
                    X[i] = sum(
                        sample.counts1 * vars(self)["standard" + str(i + 1)].counts1 - sample.counts1 * vars(self)[
                            "standard" + str(self.currentRow - 2)].counts1 - vars(self)[
                            "standard" + str(self.currentRow - 2)].counts1 * vars(self)[
                            "standard" + str(i + 1)].counts1 + vars(self)[
                            "standard" + str(self.currentRow - 2)].counts1 * vars(self)[
                            "standard" + str(self.currentRow - 2)].counts1)
                V = solve(A, X)
                for i in range(self.currentRow - 3):
                    vars(self)["a" + str(i + 1)] = V[i]
                vars(self)["a" + str(self.currentRow - 2)] = 1
                for i in range(self.currentRow - 3):
                    vars(self)["a" + str(self.currentRow - 2)] -= vars(self)["a" + str(i + 1)]
                for i in range(2, self.currentRow):
                    vars(self)["self.row" + str(i)].destroyCoefficients()
                    vars(self)["self.row" + str(i)].coefficientLabel = Label(self.LCF,
                                                                             text=str(vars(self)["a" + str(i - 1)]))
                    vars(self)["self.row" + str(i)].coefficientLabel.grid(row=i, column=2)

        def plotLCF(self, event):
            if self.currentRow == 3:
                a1 = 1
                standard1 = standardNFile(self, vars(self)["self.row" + str(2)])
                plot(sample.energy, sample.counts / sample.absorptionedge, label="Sample")
                plot(sample.energy, standard1.counts / standard1.absorptionedge, label="LCF")
            elif self.currentRow == 4:
                sample = sampleNFile(self)
                sample.cutCounts(float(self.rangeEntry1.get()), float(self.rangeEntry2.get()))
                standard1 = standardNFile(self, vars(self)["self.row" + str(2)])
                standard2 = standardNFile(self, vars(self)["self.row" + str(3)])
                standard1.cutCounts(float(self.rangeEntry1.get()), float(self.rangeEntry2.get()))
                standard2.cutCounts(float(self.rangeEntry1.get()), float(self.rangeEntry2.get()))
                a1 = sum(
                    sample.counts1 * standard1.counts1 - sample.counts1 * standard2.counts1 - standard1.counts1 * standard2.counts1 + standard2.counts1 * standard2.counts1) / sum(
                    standard1.counts1 * standard1.counts1 - 2 * standard1.counts1 * standard2.counts1 + standard2.counts1 * standard2.counts1)
                a2 = 1 - a1
                LCFcounts = a1 * standard1.counts + a2 * standard2.counts
                counts1 = array([0])
                energy1 = array([0])
                peaks = []
                peakse = []
                peaksIndex = []
                for i in range(len(LCFcounts) - 4):
                    if i != 0 and i != len(LCFcounts) - 1:
                        if LCFcounts[i - 1] < LCFcounts[i] and LCFcounts[i + 1] < LCFcounts[i] and (
                                LCFcounts[i - 1] + LCFcounts[i] + LCFcounts[i + 1]) > (
                                LCFcounts[i - 4] + LCFcounts[i - 3] + LCFcounts[i - 2]) and (
                                LCFcounts[i - 1] + LCFcounts[i] + LCFcounts[i + 1]) > (
                                LCFcounts[i + 4] + LCFcounts[i + 3] + LCFcounts[i + 2]) and LCFcounts[i] > max(
                                LCFcounts) / 500:
                            peaks.append(LCFcounts[i])
                            peakse.append(sample.energy[i])
                            peaksIndex.append(i)
                differences = [0]
                for i in range(1, len(peaksIndex)):
                    differences.append(counts[peaksIndex[i]] - counts[peaksIndex[i - 1]])
                upperIndex = peaksIndex[mostcounts(differences)]
                lowerIndex = peaksIndex[mostcounts(differences) - 1]
                counts1 = []
                energy1 = []
                for i in range(lowerIndex, upperIndex + 1):
                    counts1.append(counts[i])
                    energy1.append(energy[i])
                deriv = []
                for j in range(1, len(scounts1) - 1):
                    deriv.append((counts1[j + 1] - counts1[j - 1]) / (energy1[j + 1] - energy1[j - 1]))
                absorptionedge = counts1[mostcounts(deriv) + 1]
                absorptionedgee = energy1[mostcounts(deriv) + 1]
                plot(sample.energy, sample.counts / sample.absorptionedge, label="Sample")
                plot(standard2.energy, LCFcounts / absorptionedge, 'r-', label="LCF")
            elif self.currentRow > 4:
                sample = sampleNFile(self)
                sample.cutCounts(float(self.rangeEntry1.get()), float(self.rangeEntry2.get()))
                for i in range(2, self.currentRow):
                    vars(self)["standard" + str(i - 1)] = standardNFile(self, vars(self)["self.row" + str(i)])
                    vars(self)["standard" + str(i - 1)].cutCounts(float(self.rangeEntry1.get()),
                                                                  float(self.rangeEntry2.get()))
                A = empty([self.currentRow - 3, self.currentRow - 3])
                for i in range(self.currentRow - 3):
                    for j in range(self.currentRow - 3):
                        A[i][j] = sum(
                            vars(self)["standard" + str(i + 1)].counts1 * vars(self)["standard" + str(j + 1)].counts1 -
                            vars(self)["standard" + str(self.currentRow - 2)].counts1 * vars(self)[
                                "standard" + str(i + 1)].counts1 - vars(self)["standard" + str(j + 1)].counts1 *
                            vars(self)["standard" + str(self.currentRow - 2)].counts1 + vars(self)[
                                "standard" + str(self.currentRow - 2)].counts1 * vars(self)[
                                "standard" + str(self.currentRow - 2)].counts1)
                X = empty([self.currentRow - 3])
                for i in range(self.currentRow - 3):
                    X[i] = sum(
                        sample.counts1 * vars(self)["standard" + str(i + 1)].counts1 - sample.counts1 * vars(self)[
                            "standard" + str(self.currentRow - 2)].counts1 - vars(self)[
                            "standard" + str(self.currentRow - 2)].counts1 * vars(self)[
                            "standard" + str(i + 1)].counts1 + vars(self)[
                            "standard" + str(self.currentRow - 2)].counts1 * vars(self)[
                            "standard" + str(self.currentRow - 2)].counts1)
                V = solve(A, X)
                for i in range(self.currentRow - 3):
                    vars(self)["a" + str(i + 1)] = V[i]
                vars(self)["a" + str(self.currentRow - 2)] = 1
                for i in range(self.currentRow - 3):
                    vars(self)["a" + str(self.currentRow - 2)] -= vars(self)["a" + str(i + 1)]
                LCFcounts = vars(self)["standard" + str(1)].counts
                for i in range(1, self.currentRow - 1):
                    LCFcounts += vars(self)["a" + str(i)] * vars(self)["standard" + str(i)].counts
                counts1 = array([0])
                energy1 = array([0])
                peaks = []
                peakse = []
                peaksIndex = []
                for i in range(len(LCFcounts) - 4):
                    if i != 0 and i != len(LCFcounts) - 1:
                        if LCFcounts[i - 1] < LCFcounts[i] and LCFcounts[i + 1] < LCFcounts[i] and (
                                LCFcounts[i - 1] + LCFcounts[i] + LCFcounts[i + 1]) > (
                                LCFcounts[i - 4] + LCFcounts[i - 3] + LCFcounts[i - 2]) and (
                                LCFcounts[i - 1] + LCFcounts[i] + LCFcounts[i + 1]) > (
                                LCFcounts[i + 4] + LCFcounts[i + 3] + LCFcounts[i + 2]) and LCFcounts[i] > max(
                                LCFcounts) / 500:
                            peaks.append(LCFcounts[i])
                            peakse.append(sample.energy[i])
                            peaksIndex.append(i)
                differences = [0]
                for i in range(1, len(peaksIndex)):
                    differences.append(LCFcounts[peaksIndex[i]] - LCFcounts[peaksIndex[i - 1]])
                upperIndex = peaksIndex[mostcounts(differences)]
                lowerIndex = peaksIndex[mostcounts(differences) - 1]
                counts1 = []
                energy1 = []
                for i in range(lowerIndex, upperIndex + 1):
                    counts1.append(LCFcounts[i])
                    energy1.append(sample.energy[i])
                deriv = []
                for j in range(1, len(counts1) - 1):
                    deriv.append((counts1[j + 1] - counts1[j - 1]) / (energy1[j + 1] - energy1[j - 1]))
                absorptionedge = counts1[mostcounts(deriv) + 1]
                absorptionedgee = energy1[mostcounts(deriv) + 1]
                plot(sample.energy, sample.counts / sample.absorptionedge, label="Sample")
                plot(vars(self)["standard" + str(1)].energy, LCFcounts / absorptionedge, 'r-', label="LCF")
            legend()
            xlabel("Energy(eV)")
            ylabel("Counts")
            title("LCF and Sample")
            show()

        def plotSubtraction(self, event):
            if self.currentRow == 3:
                a1 = 1
                standard1 = standardNFile(self, vars(self)["self.row" + str(2)])
                plot(sample.energy, sample.counts / sample.absorptionedge - standard1.counts / standard1.absorptionedge,
                     'g-', label="Difference")
            elif self.currentRow == 4:
                sample = sampleNFile(self)
                sample.cutCounts(float(self.rangeEntry1.get()), float(self.rangeEntry2.get()))
                standard1 = standardNFile(self, vars(self)["self.row" + str(2)])
                standard2 = standardNFile(self, vars(self)["self.row" + str(3)])
                standard1.cutCounts(float(self.rangeEntry1.get()), float(self.rangeEntry2.get()))
                standard2.cutCounts(float(self.rangeEntry1.get()), float(self.rangeEntry2.get()))
                a1 = sum(
                    sample.counts1 * standard1.counts1 - sample.counts1 * standard2.counts1 - standard1.counts1 * standard2.counts1 + standard2.counts1 * standard2.counts1) / sum(
                    standard1.counts1 * standard1.counts1 - 2 * standard1.counts1 * standard2.counts1 + standard2.counts1 * standard2.counts1)
                a2 = 1 - a1
                counts1 = array([0])
                energy1 = array([0])
                peaks = []
                peakse = []
                peaksIndex = []
                for i in range(len(LCFcounts) - 4):
                    if i != 0 and i != len(LCFcounts) - 1:
                        if LCFcounts[i - 1] < LCFcounts[i] and LCFcounts[i + 1] < LCFcounts[i] and (
                                LCFcounts[i - 1] + LCFcounts[i] + LCFcounts[i + 1]) > (
                                LCFcounts[i - 4] + LCFcounts[i - 3] + LCFcounts[i - 2]) and (
                                LCFcounts[i - 1] + LCFcounts[i] + LCFcounts[i + 1]) > (
                                LCFcounts[i + 4] + LCFcounts[i + 3] + LCFcounts[i + 2]) and LCFcounts[i] > max(
                                LCFcounts) / 500:
                            peaks.append(LCFcounts[i])
                            peakse.append(sample.energy[i])
                            peaksIndex.append(i)
                differences = [0]
                for i in range(1, len(peaksIndex)):
                    differences.append(LCFcounts[peaksIndex[i]] - LCFcounts[peaksIndex[i - 1]])
                upperIndex = peaksIndex[mostcounts(differences)]
                lowerIndex = peaksIndex[mostcounts(differences) - 1]
                counts1 = []
                energy1 = []
                for i in range(lowerIndex, upperIndex + 1):
                    counts1.append(LCFcounts[i])
                    energy1.append(sample.energy[i])
                deriv = []
                for j in range(1, len(counts1) - 1):
                    deriv.append((counts1[j + 1] - counts1[j - 1]) / (energy1[j + 1] - energy1[j - 1]))
                absorptionedge = counts1[mostcounts(deriv) + 1]
                absorptionedgee = energy1[mostcounts(deriv) + 1]
                plot(sample.energy, sample.counts / sample.absorptionedge - LCFcounts / absorptionedge, 'g-',
                     label="Difference")
            elif self.currentRow > 4:
                sample = sampleNFile(self)
                sample.cutCounts(float(self.rangeEntry1.get()), float(self.rangeEntry2.get()))
                for i in range(2, self.currentRow):
                    vars(self)["standard" + str(i - 1)] = standardNFile(self, vars(self)["self.row" + str(i)])
                    vars(self)["standard" + str(i - 1)].cutCounts(float(self.rangeEntry1.get()),
                                                                  float(self.rangeEntry2.get()))
                A = empty([self.currentRow - 3, self.currentRow - 3])
                for i in range(self.currentRow - 3):
                    for j in range(self.currentRow - 3):
                        A[i][j] = sum(
                            vars(self)["standard" + str(i + 1)].counts1 * vars(self)["standard" + str(j + 1)].counts1 -
                            vars(self)["standard" + str(self.currentRow - 2)].counts1 * vars(self)[
                                "standard" + str(i + 1)].counts1 - vars(self)["standard" + str(j + 1)].counts1 *
                            vars(self)["standard" + str(self.currentRow - 2)].counts1 + vars(self)[
                                "standard" + str(self.currentRow - 2)].counts1 * vars(self)[
                                "standard" + str(self.currentRow - 2)].counts1)
                X = empty([self.currentRow - 3])
                for i in range(self.currentRow - 3):
                    X[i] = sum(
                        sample.counts1 * vars(self)["standard" + str(i + 1)].counts1 - sample.counts1 * vars(self)[
                            "standard" + str(self.currentRow - 2)].counts1 - vars(self)[
                            "standard" + str(self.currentRow - 2)].counts1 * vars(self)[
                            "standard" + str(i + 1)].counts1 + vars(self)[
                            "standard" + str(self.currentRow - 2)].counts1 * vars(self)[
                            "standard" + str(self.currentRow - 2)].counts1)
                V = solve(A, X)
                for i in range(self.currentRow - 3):
                    vars(self)["a" + str(i + 1)] = V[i]
                vars(self)["a" + str(self.currentRow - 2)] = 1
                for i in range(self.currentRow - 3):
                    vars(self)["a" + str(self.currentRow - 2)] -= vars(self)["a" + str(i + 1)]
                LCFcounts = vars(self)["standard" + str(1)].counts
                for i in range(1, self.currentRow - 1):
                    LCFcounts += vars(self)["a" + str(i)] * vars(self)["standard" + str(i)].counts
                counts1 = array([0])
                energy1 = array([0])
                peaks = []
                peakse = []
                peaksIndex = []
                for i in range(len(LCFcounts) - 4):
                    if i != 0 and i != len(LCFcounts) - 1:
                        if LCFcounts[i - 1] < LCFcounts[i] and LCFcounts[i + 1] < LCFcounts[i] and (
                                LCFcounts[i - 1] + LCFcounts[i] + LCFcounts[i + 1]) > (
                                LCFcounts[i - 4] + LCFcounts[i - 3] + LCFcounts[i - 2]) and (
                                LCFcounts[i - 1] + LCFcounts[i] + LCFcounts[i + 1]) > (
                                LCFcounts[i + 4] + LCFcounts[i + 3] + LCFcounts[i + 2]) and LCFcounts[i] > max(
                                LCFcounts) / 500:
                            peaks.append(LCFcounts[i])
                            peakse.append(sample.energy[i])
                            peaksIndex.append(i)
                differences = [0]
                for i in range(1, len(peaksIndex)):
                    differences.append(LCFcounts[peaksIndex[i]] - LCFcounts[peaksIndex[i - 1]])
                upperIndex = peaksIndex[mostcounts(differences)]
                lowerIndex = peaksIndex[mostcounts(differences) - 1]
                counts1 = []
                energy1 = []
                for i in range(lowerIndex, upperIndex + 1):
                    counts1.append(LCFcounts[i])
                    energy1.append(sample.energy[i])
                deriv = []
                for j in range(1, len(counts1) - 1):
                    deriv.append((counts1[j + 1] - counts1[j - 1]) / (energy1[j + 1] - energy1[j - 1]))
                absorptionedge = counts1[mostcounts(deriv) + 1]
                absorptionedgee = energy1[mostcounts(deriv) + 1]
                plot(vars(self)["standard" + str(1)].energy,
                     sample.counts / sample.absorptionedge - LCFcounts / absorptionedge, 'g-', label="Difference")
            legend()
            xlabel("Energy(eV)")
            ylabel("Counts")
            title("Difference")
            show()

        def plotAll(self, event):
            if self.currentRow == 3:
                a1 = 1
                standard1 = standardNFile(self, vars(self)["self.row" + str(2)])
                plot(sample.energy, sample.counts / sample.absorptionedge - standard1.counts / standard1.absorptionedge,
                     'g-', label="Difference")
                plot(sample.energy, sample.counts / sample.absorptionedge, label="Sample")
                plot(sample.energy, standard1.counts / standard1.absorptionedge, label="LCF")
            elif self.currentRow == 4:
                sample = sampleNFile(self)
                sample.cutCounts(float(self.rangeEntry1.get()), float(self.rangeEntry2.get()))
                standard1 = standardNFile(self, vars(self)["self.row" + str(2)])
                standard2 = standardNFile(self, vars(self)["self.row" + str(3)])
                standard1.cutCounts(float(self.rangeEntry1.get()), float(self.rangeEntry2.get()))
                standard2.cutCounts(float(self.rangeEntry1.get()), float(self.rangeEntry2.get()))
                a1 = sum(
                    sample.counts1 * standard1.counts1 - sample.counts1 * standard2.counts1 - standard1.counts1 * standard2.counts1 + standard2.counts1 * standard2.counts1) / sum(
                    standard1.counts1 * standard1.counts1 - 2 * standard1.counts1 * standard2.counts1 + standard2.counts1 * standard2.counts1)
                a2 = 1 - a1
                LCFcounts = a1 * standard1.counts + a2 * standard2.counts
                counts1 = array([0])
                energy1 = array([0])
                peaks = []
                peakse = []
                peaksIndex = []
                for i in range(len(LCFcounts) - 4):
                    if i != 0 and i != len(LCFcounts) - 1:
                        if LCFcounts[i - 1] < LCFcounts[i] and LCFcounts[i + 1] < LCFcounts[i] and (
                                LCFcounts[i - 1] + LCFcounts[i] + LCFcounts[i + 1]) > (
                                LCFcounts[i - 4] + LCFcounts[i - 3] + LCFcounts[i - 2]) and (
                                LCFcounts[i - 1] + LCFcounts[i] + LCFcounts[i + 1]) > (
                                LCFcounts[i + 4] + LCFcounts[i + 3] + LCFcounts[i + 2]) and LCFcounts[i] > max(
                                LCFcounts) / 500:
                            peaks.append(LCFcounts[i])
                            peakse.append(sample.energy[i])
                            peaksIndex.append(i)
                differences = [0]
                for i in range(1, len(peaksIndex)):
                    differences.append(LCFcounts[peaksIndex[i]] - LCFcounts[peaksIndex[i - 1]])
                upperIndex = peaksIndex[mostcounts(differences)]
                lowerIndex = peaksIndex[mostcounts(differences) - 1]
                counts1 = []
                energy1 = []
                for i in range(lowerIndex, upperIndex + 1):
                    counts1.append(LCFcounts[i])
                    energy1.append(sample.energy[i])
                deriv = []
                for j in range(1, len(counts1) - 1):
                    deriv.append((counts1[j + 1] - counts1[j - 1]) / (energy1[j + 1] - energy1[j - 1]))
                absorptionedge = counts1[mostcounts(deriv) + 1]
                absorptionedgee = energy1[mostcounts(deriv) + 1]
                plot(sample.energy, sample.counts / sample.absorptionedge, label="Sample")
                plot(standard2.energy, LCFcounts / absorptionedge, 'r-', label="LCF")
                plot(sample.energy, sample.counts / sample.absorptionedge - LCFcounts / absorptionedge, 'g-',
                     label="Difference")
            elif self.currentRow > 4:
                sample = sampleNFile(self)
                sample.cutCounts(float(self.rangeEntry1.get()), float(self.rangeEntry2.get()))
                for i in range(2, self.currentRow):
                    vars(self)["standard" + str(i - 1)] = standardNFile(self, vars(self)["self.row" + str(i)])
                    vars(self)["standard" + str(i - 1)].cutCounts(float(self.rangeEntry1.get()),
                                                                  float(self.rangeEntry2.get()))
                A = empty([self.currentRow - 3, self.currentRow - 3])
                for i in range(self.currentRow - 3):
                    for j in range(self.currentRow - 3):
                        A[i][j] = sum(
                            vars(self)["standard" + str(i + 1)].counts1 * vars(self)["standard" + str(j + 1)].counts1 -
                            vars(self)["standard" + str(self.currentRow - 2)].counts1 * vars(self)[
                                "standard" + str(i + 1)].counts1 - vars(self)["standard" + str(j + 1)].counts1 *
                            vars(self)["standard" + str(self.currentRow - 2)].counts1 + vars(self)[
                                "standard" + str(self.currentRow - 2)].counts1 * vars(self)[
                                "standard" + str(self.currentRow - 2)].counts1)
                X = empty([self.currentRow - 3])
                for i in range(self.currentRow - 3):
                    X[i] = sum(
                        sample.counts1 * vars(self)["standard" + str(i + 1)].counts1 - sample.counts1 * vars(self)[
                            "standard" + str(self.currentRow - 2)].counts1 - vars(self)[
                            "standard" + str(self.currentRow - 2)].counts1 * vars(self)[
                            "standard" + str(i + 1)].counts1 + vars(self)[
                            "standard" + str(self.currentRow - 2)].counts1 * vars(self)[
                            "standard" + str(self.currentRow - 2)].counts1)
                V = solve(A, X)
                for i in range(self.currentRow - 3):
                    vars(self)["a" + str(i + 1)] = V[i]
                vars(self)["a" + str(self.currentRow - 2)] = 1
                for i in range(self.currentRow - 3):
                    vars(self)["a" + str(self.currentRow - 2)] -= vars(self)["a" + str(i + 1)]
                LCFcounts = vars(self)["standard" + str(1)].counts
                for i in range(1, self.currentRow - 1):
                    LCFcounts += vars(self)["a" + str(i)] * vars(self)["standard" + str(i)].counts
                counts1 = array([0])
                energy1 = array([0])
                peaks = []
                peakse = []
                peaksIndex = []
                for i in range(len(LCFcounts) - 4):
                    if i != 0 and i != len(LCFcounts) - 1:
                        if LCFcounts[i - 1] < LCFcounts[i] and LCFcounts[i + 1] < LCFcounts[i] and (
                                LCFcounts[i - 1] + LCFcounts[i] + LCFcounts[i + 1]) > (
                                LCFcounts[i - 4] + LCFcounts[i - 3] + LCFcounts[i - 2]) and (
                                LCFcounts[i - 1] + LCFcounts[i] + LCFcounts[i + 1]) > (
                                LCFcounts[i + 4] + LCFcounts[i + 3] + LCFcounts[i + 2]) and LCFcounts[i] > max(
                            LCFcounts) / 500:
                            peaks.append(LCFcounts[i])
                            peakse.append(sample.energy[i])
                            peaksIndex.append(i)
                differences = [0]
                for i in range(1, len(peaksIndex)):
                    differences.append(LCFcounts[peaksIndex[i]] - LCFcounts[peaksIndex[i - 1]])
                upperIndex = peaksIndex[mostcounts(differences)]
                lowerIndex = peaksIndex[mostcounts(differences) - 1]
                counts1 = []
                energy1 = []
                for i in range(lowerIndex, upperIndex + 1):
                    counts1.append(LCFcounts[i])
                    energy1.append(sample.energy[i])
                deriv = []
                for j in range(1, len(counts1) - 1):
                    deriv.append((counts1[j + 1] - counts1[j - 1]) / (energy1[j + 1] - energy1[j - 1]))
                absorptionedge = counts1[mostcounts(deriv) + 1]
                absorptionedgee = energy1[mostcounts(deriv) + 1]
                plot(vars(self)["standard" + str(1)].energy,
                     sample.counts / sample.absorptionedge - LCFcounts / absorptionedge, 'g-', label="Difference")
                plot(sample.energy, sample.counts / sample.absorptionedge, label="Sample")
                plot(vars(self)["standard" + str(1)].energy, LCFcounts / absorptionedge, 'r-', label="LCF")
            legend()
            xlabel("Energy(eV)")
            ylabel("Counts")
            title("LCF, Sample, and Difference")
            show()

    class intFile:
        def __init__(self, INT, Row):
            self.INTProgram = INT
            self.row = Row
            self.data = loadtxt(self.row.fileEntry.get() + ".txt")
            if len(self.data[0]) >= 13:
                self.energy = self.data[:, 12]
                self.counts = self.data[:, 13]
            elif len(self.data[0]) < 13:
                self.energy = self.data[:, 0]
                self.counts = self.data[:, 7]

        def interpolate(self, energy):
            deg = int(self.row.degreeEntry.get())
            points = [1]
            j = deg
            while j < len(self.energy):
                points.append(j)
                j += (deg - 1)
            points.append(len(self.energy))
            k = 0
            for i in range(len(self.energy)):
                if self.energy[i] <= energy <= self.energy[i + 1]:
                    k = i + 1
            for i in range(len(points)):
                if points[i] <= k <= points[i + 1]:
                    counts = 0
                    for l in range(points[i], points[i + 1] + 1):
                        counts1 = 1
                        for m in range(points[i], points[i + 1] + 1):
                            if m != l:
                                counts1 *= (energy - self.energy[m - 1]) / (self.energy[l - 1] - self.energy[m - 1])
                        counts += counts1 * self.counts[l - 1]
            return counts

        def getCounts(self):
            messagebox.showinfo("Counts", str(int(self.interpolate(float(self.row.energyEntry.get())))) + " counts")

        def plotInt(self):
            energies = arange(self.energy[0], self.energy[len(self.energy) - 1], 0.1)
            counts = []
            for i in energies:
                counts.append(self.interpolate(i))
            plot(energies, counts, label="Interpolation")
            if self.row.showPoints.get() == True:
                plot(self.energy, self.counts, 'ro')
            legend()
            xlabel("energy(eV)")
            ylabel("Counts")
            show()

        def derivative(self):
            energies = arange(self.energy[0], self.energy[len(self.energy) - 1], 0.1)
            derivatives = []
            for i in range(2, len(energies) - 1):
                derivatives.append((self.interpolate(energies[i + 1]) - self.interpolate(energies[i - 1])) / (
                            energies[i + 1] - energies[i - 1]))
            plot(energies[2:len(energies) - 1], derivatives)
            title("Derivative")
            show()

    class intRow:
        def __init__(self, INT, r):
            self.INTProgram = INT
            self.fileEntry = Entry(self.INTProgram.INT)
            self.fileEntry.grid(row=r, column=0)
            self.degreeEntry = Entry(self.INTProgram.INT)
            self.degreeEntry.grid(row=r, column=1)
            self.energyEntry = Entry(self.INTProgram.INT)
            self.energyEntry.grid(row=r, column=2)
            self.countsButton = Button(self.INTProgram.INT, text="Get counts")
            self.countsButton.bind("<Button-1>", self.getCounts)
            self.countsButton.grid(row=r, column=3)
            self.plotButton = Button(self.INTProgram.INT, text="Graph")
            self.plotButton.bind("<Button-1>", self.graphInterpolation)
            self.plotButton.grid(row=r, column=4)
            self.derivativeButton = Button(self.INTProgram.INT, text="Plot Derivative")
            self.derivativeButton.bind("<Button-1>", self.derivative)
            self.derivativeButton.grid(row=r, column=5)
            self.showPoints = IntVar(self.INTProgram.INT)
            self.showPointsCheck = Checkbutton(self.INTProgram.INT, text="Show data points", variable=self.showPoints)
            self.showPointsCheck.grid(row=r, column=6)

        def destroy(self):
            self.fileEntry.destroy()
            self.degreeEntry.destroy()
            self.energyEntry.destroy()
            self.countsButton.destroy()
            self.plotButton.destroy()
            self.showPointsCheck.destroy()
            self.derivativeButton.destroy()

        def getCounts(self, event):
            file = intFile(self.INTProgram, self)
            file.getCounts()

        def graphInterpolation(self, event):
            file = intFile(self.INTProgram, self)
            file.plotInt()

        def derivative(self, event):
            file = intFile(self.INTProgram, self)
            file.derivative()

    class interpolationProgram:
        def __init__(self):
            self.INT = Tk()
            self.INT.title("Interpolate")
            self.fileLabel = Label(self.INT, text="File")
            self.fileLabel.grid(row=0, column=0)
            self.degreeLabel = Label(self.INT, text="Degree")
            self.degreeLabel.grid(row=0, column=1)
            self.energyLabel = Label(self.INT, text="Energy")
            self.energyLabel.grid(row=0, column=2)
            self.currentRow = 1
            self.lastRow = self.makeRow()
            self.menu = Menu(self.INT)
            self.fileMenu = Menu(self.menu)
            self.fileMenu.add_command(label="Add data", command=self.makeRow)
            self.fileMenu.add_command(label="Remove a row of data", command=self.destroyRow)
            self.menu.add_cascade(label="File", menu=self.fileMenu)
            self.INT.config(menu=self.menu)

        def makeRow(self):
            vars(self)["self.row" + str(self.currentRow)] = intRow(self, self.currentRow)
            self.lastRow = vars(self)["self.row" + str(self.currentRow)]
            self.currentRow += 1

        def destroyRow(self):
            self.lastRow.destroy()
            self.currentRow -= 2
            self.lastRow = vars(self)["self.row" + str(self.currentRow)]
            self.currentRow += 1

    class xanesProgram:
        def __init__(self):
            self.XANES = Tk()
            self.XANES.title("XANES Analysis")
            self.file1label = Label(self.XANES, text="File1")
            self.file1label.grid(row=0, column=0)
            self.file2label = Label(self.XANES, text="File2")
            self.file2label.grid(row=0, column=1)
            self.labellabel = Label(self.XANES, text="Label")
            self.labellabel.grid(row=0, column=2)
            self.titlelabel = Label(self.XANES, text="Title")
            self.titlelabel.grid(row=0, column=3)
            self.currentRow = 1
            self.title1Label = Label(self.XANES, text="Title:")
            self.title1Label.grid(row=self.currentRow, column=0)
            self.title1Entry = Entry(self.XANES)
            self.title1Entry.grid(row=self.currentRow, column=1)
            self.graph1Button = Button(self.XANES, text="Graph selected")
            self.graph1Button.bind("<Button-1>", self.graphSelected)
            self.graph1Button.grid(row=self.currentRow, column=2)
            self.graph1NormalButton = Button(self.XANES, text="Graph normal selected")
            self.graph1NormalButton.bind("<Button-1>", self.graphNormalSelected)
            self.graph1NormalButton.grid(row=self.currentRow, column=3)
            self.lastRow = self.makeRow()
            self.menu = Menu(self.XANES)
            self.fileMenu = Menu(self.menu)
            self.fileMenu.add_command(label="Add data", command=self.makeRow)
            self.fileMenu.add_command(label="Add subtraction row", command=self.makeSubtractionRow)
            self.fileMenu.add_command(label="Remove row", command=self.destroyRow)
            self.menu.add_cascade(label="File", menu=self.fileMenu)
            self.fittingMenu = Menu(self.menu)
            self.fittingMenu.add_command(label="Linear Combination Fitting", command=self.startNLCF)
            self.fittingMenu.add_command(label="Interpolation", command=self.startInterpolation)
            self.menu.add_cascade(label="Fitting", menu=self.fittingMenu)
            self.XANES.config(menu=self.menu)

        def makeRow(self):
            vars(self)["self.row" + str(self.currentRow)] = xanesRow(self, self.currentRow)
            self.lastRow = vars(self)["self.row" + str(self.currentRow)]
            self.currentRow += 1
            self.title1Label.grid(row=self.currentRow, column=0)
            self.title1Entry.grid(row=self.currentRow, column=1)
            self.graph1Button.grid(row=self.currentRow, column=2)
            self.graph1NormalButton.grid(row=self.currentRow, column=3)

        def makeSubtractionRow(self):
            vars(self)["self.row" + str(self.currentRow)] = xanesSubtractionRow(self, self.currentRow)
            self.lastRow = vars(self)["self.row" + str(self.currentRow)]
            self.currentRow += 1
            self.title1Label.grid(row=self.currentRow, column=0)
            self.title1Entry.grid(row=self.currentRow, column=1)
            self.graph1Button.grid(row=self.currentRow, column=2)
            self.graph1NormalButton.grid(row=self.currentRow, column=3)

        def destroyRow(self):
            self.lastRow.destroy()
            self.currentRow -= 2
            self.lastRow = vars(self)["self.row" + str(self.currentRow)]
            self.currentRow += 1
            self.title1Label.grid(row=self.currentRow, column=0)
            self.title1Entry.grid(row=self.currentRow, column=1)
            self.graph1Button.grid(row=self.currentRow, column=2)
            self.graph1NormalButton.grid(row=self.currentRow, column=3)

        def graphSelected(self, event):
            for i in range(1, self.currentRow):
                if vars(self)["self.row" + str(i)].shouldgraph1.get() == True:
                    if not vars(self)["self.row" + str(i)].isSub:
                        file = xanesFile(vars(self)["self.row" + str(i)].file1Entry.get(), self,
                                         vars(self)["self.row" + str(i)])
                        lab = vars(self)["self.row" + str(i)].labelEntry.get()
                        plot(file.energy, file.counts, label=lab)
                    elif vars(self)["self.row" + str(i)].isSub:
                        file1 = xanesSubtractionFile(vars(self)["self.row" + str(i)].file1Entry.get(), self,
                                                     vars(self)["self.row" + str(i)])
                        file2 = xanesSubtractionFile(vars(self)["self.row" + str(i)].file2Entry.get(), self,
                                                     vars(self)["self.row" + str(i)])
                        if len(file1.energy) == len(
                                file2.energy):  # determining the energy to use, this only works if the incrementation is the same
                            energyu = file1.energy
                        elif len(file1.energy) == minlength(file1.energy, file2.energy):
                            energyu = file1.energy
                            file2.counts = file2.counts[:len(file1.energy) + 1]
                        elif len(file2.energy) == minlength(file1.energy, file2.energy):
                            energyu = file2.energy
                            file1.counts = file1.counts[:len(file1.energy) + 1]
                        difference = file1.counts - file2.counts
                        lab = vars(self)["self.row" + str(i)].labelEntry.get()
                        plot(energyu, difference, label=lab)
            seepeaks1 = messagebox.askquestion("Sample Peaks", "Would you like to better see the peaks of your sample?")
            if seepeaks1 == "yes":
                for i in range(1, self.currentRow):
                    if vars(self)["self.row" + str(i)].shouldgraph1.get() == True:
                        if not vars(self)["self.row" + str(i)].isSub:
                            file = xanesFile(vars(self)["self.row" + str(i)].file1Entry.get(), self,
                                             vars(self)["self.row" + str(i)])
                            plot(file.peakse, file.peaks, 'ro')
                        elif vars(self)["self.row" + str(i)].isSub:
                            file1 = xanesSubtractionFile(vars(self)["self.row" + str(i)].file1Entry.get(), self,
                                                         vars(self)["self.row" + str(i)])
                            file2 = xanesSubtractionFile(vars(self)["self.row" + str(i)].file2Entry.get(), self,
                                                         vars(self)["self.row" + str(i)])
                            if len(file1.energy) == len(
                                    file2.energy):  # determining the energy to use, this only works if the incrementation is the same
                                energyu = file1.energy
                            elif len(file1.energy) == minlength(file1.energy, file2.energy):
                                energyu = file1.energy
                                file2.counts = file2.counts[:len(file1.energy) + 1]
                            elif len(file2.energy) == minlength(file1.energy, file2.energy):
                                energyu = file2.energy
                                file1.counts = file1.counts[:len(file1.energy) + 1]
                            peaks = []  # creating empty lists to store information about the peaks in the smaple
                            peakse = []
                            for i in range(len(
                                    energyu) - 4):  # this section stores information about the peaks in the sample in the empty lists
                                if i != 0 and i != len(energyu) - 1:
                                    if difference[i - 1] < difference[i] and difference[i + 1] < difference[i] and (
                                            difference[i - 1] + difference[i] + difference[i + 1]) > (
                                            difference[i - 4] + difference[i - 3] + difference[i - 2]) and (
                                            difference[i - 1] + difference[i] + difference[i + 1]) > (
                                            difference[i + 4] + difference[i + 3] + difference[i + 2]) and difference[
                                        i] > max(difference) / 500:
                                        peaks.append(difference[i])
                                        peakse.append(energyu[i])
                            plot(peakse, peaks, 'ro')
            showabs = messagebox.askquestion("Sample Peaks",
                                             "Would you like to better see the absorption edges of your data that was not subtracted?")
            if showabs == "yes":
                for i in range(1, self.currentRow):
                    if vars(self)["self.row" + str(i)].shouldgraph1.get() == True:
                        if vars(self)["self.row" + str(i)].isSub == False:
                            file = xanesFile(vars(self)["self.row" + str(i)].file1Entry.get(), self,
                                             vars(self)["self.row" + str(i)])
                            axvline(x=file.absorptionedge)
            xlabel("Energy(eV)")
            ylabel("Photon Counts")
            legend()
            Title = self.title1Entry.get()
            title(Title)
            show()

        def graphNormalSelected(self, event):
            for i in range(1, self.currentRow):
                if vars(self)["self.row" + str(i)].shouldgraph1.get() == True:
                    if not vars(self)["self.row" + str(i)].isSub:
                        file = xanesFile(vars(self)["self.row" + str(i)].file1Entry.get(), self,
                                         vars(self)["self.row" + str(i)])
                        scatter = file.absorptionedge
                        normcounts = file.counts / scatter
                        lab = vars(self)["self.row" + str(i)].labelEntry.get()
                        plot(file.energy, normcounts, label=lab)
                    elif vars(self)["self.row" + str(i)].isSub:
                        file1 = xanesSubtractionFile(vars(self)["self.row" + str(i)].file1Entry.get(), self,
                                                     vars(self)["self.row" + str(i)])
                        file2 = xanesSubtractionFile(vars(self)["self.row" + str(i)].file2Entry.get(), self,
                                                     vars(self)["self.row" + str(i)])
                        scatter1 = file1.absorptionedge
                        scatter2 = file2.absorptionedge
                        if len(file1.energy) == len(
                                file2.energy):  # determining the energy to use, this only works if the incrementation is the same
                            energyu = file1.energy
                        elif len(file1.energy) == minlength(file1.energy, file2.energy):
                            energyu = file1.energy
                            file2.counts = file2.counts[:len(file1.energy) + 1]
                        elif len(file2.energy) == minlength(self.energy, file2.energy):
                            energyu = file2.energy
                            file1.counts = file1.counts[:len(file1.energy) + 1]
                        lab = vars(self)["self.row" + str(i)].labelEntry.get()
                        difference = file1.counts / scatter1 - file2.counts / scatter2
                        plot(energyu, difference, label=lab)
            seepeaks1 = messagebox.askquestion("Sample Peaks", "Would you like to better see the peaks of your sample?")
            if seepeaks1 == "yes":
                for i in range(1, self.currentRow):
                    if vars(self)["self.row" + str(i)].shouldgraph1.get() == True:
                        if vars(self)["self.row" + str(i)].isSub == False:
                            file = xanesFile(vars(self)["self.row" + str(i)].file1Entry.get(), self,
                                             vars(self)["self.row" + str(i)])
                            scatter = file.absorptionedge
                            normpeaks = array(file.peaks) / scatter
                            plot(array(file.peakse), normpeaks, 'ro')
                        elif vars(self)["self.row" + str(i)].isSub == True:
                            file1 = xanesSubtractionFile(vars(self)["self.row" + str(i)].file1Entry.get(), self,
                                                         vars(self)["self.row" + str(i)])
                            file2 = xanesSubtractionFile(vars(self)["self.row" + str(i)].file2Entry.get(), self,
                                                         vars(self)["self.row" + str(i)])
                            scatter1 = file1.absorptionedge
                            scatter2 = file2.absorptionedge
                            if len(file1.energy) == len(
                                    file2.energy):  # determining the energy to use, this only works if the incrementation is the same
                                energyu = file1.energy
                            elif len(file1.energy) == minlength(file1.energy, file2.energy):
                                energyu = file1.energy
                                file2.counts = file2.counts[:len(file1.energy) + 1]
                            elif len(file2.energy) == minlength(self.energy, file2.energy):
                                energyu = file2.energy
                                file1.counts = file1.counts[:len(file1.energy) + 1]
                            peaks = []  # creating empty lists to store information about the peaks in the smaple
                            peakse = []
                            for i in range(len(
                                    energyu) - 4):  # this section stores information about the peaks in the sample in the empty lists
                                if i != 0 and i != len(energyu) - 1:
                                    if difference[i - 1] < difference[i] and difference[i + 1] < difference[i] and (
                                            difference[i - 1] + difference[i] + difference[i + 1]) > (
                                            difference[i - 4] + difference[i - 3] + difference[i - 2]) and (
                                            difference[i - 1] + difference[i] + difference[i + 1]) > (
                                            difference[i + 4] + difference[i + 3] + difference[i + 2]) and difference[
                                        i] > max(difference) / 500:
                                        peaks.append(difference[i])
                                        peakse.append(energyu[i])
                            plot(peakse, peaks, 'ro')
            showabs = messagebox.askquestion("Sample Peaks",
                                             "Would you like to better see the absorption edges of your data that was not subtracted?")
            if showabs == "yes":
                for i in range(1, self.currentRow):
                    if vars(self)["self.row" + str(i)].shouldgraph1.get() == True:
                        if vars(self)["self.row" + str(i)].isSub == False:
                            file = xanesFile(vars(self)["self.row" + str(i)].file1Entry.get(), self,
                                             vars(self)["self.row" + str(i)])
                            axvline(x=file.absorptionedge)
            xlabel("Energy(eV)")
            ylabel("Photon Counts")
            legend()
            Title = self.title1Entry.get()
            title(Title)
            show()

        def startNLCF(self):
            a = lcfNProgram()
            a.LCF.mainloop()

        def startInterpolation(self):
            a = interpolationProgram()
            a.INT.mainloop()

    def runXANES(event):
        a = xanesProgram()
        a.XANES.mainloop()

    class analysisProgram:
        def __init__(self):
            self.program = Tk()
            self.program.title("Analysis Program")
            self.xrfButton = Button(self.program, text="XRF Analysis")
            self.xrfButton.bind("<Button-1>", runXRF)
            self.xrfButton.pack()
            self.xanesButton = Button(self.program, text="XANES Analysis")
            self.xanesButton.bind("<Button-1>", runXANES)
            self.xanesButton.pack()

    def main():
        a = analysisProgram()
        a.program.mainloop()

    if __name__ == "__main__":
        main()


