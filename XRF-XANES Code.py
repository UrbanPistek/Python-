import pandas as pd

k_edges = pd.read_pickle('elements_data.pickle')
kalpha_edges = pd.read_pickle('kalpha_edges.pickle')
'''
elements = pd.read_html('https://sciencenotes.org/list-elements-atomic-number/')
#print(elements)
#print(elements[0][2][1:])

list = (elements[0][2][1:104])
k_edges['Element Names'] = list
#k_edges.rename(columns={'  2': 'Element Name'}, inplace=True)
print(k_edges)
k_edges.to_pickle('elements.pickle')
'''
elements = pd.read_pickle('elements.pickle')

for index in range(1, len(elements['Element Names'])):
    if self.xrfProgram.str(elements['Element Names'][index]).get() == True:
        axvline(ElementEnergy[index])

'''
energies1 = pd.read_html('http://www.kayelaby.npl.co.uk/atomic_and_nuclear_physics/4_2/4_2_1.html')
#print(energies1[0:][6][0])
#print(energies1[0:][6][5], energies1[0:][6][6])

k_edges = pd.read_pickle('elements_data.pickle')
#print(k_edges)

elements = ['H', 'He', 'Li']
ka = [13.6, 24.6, 54.6]
ka2 = [13.6, 24.6, 54.6]

for index in range(1,103):
    for abbv in range(130):
        if str(index)+' '+k_edges['Elements'][index] == energies1[0:][6][0][abbv]:
            #print(energies1[0:][6][0][abbv]+'__'+energies1[0:][6][5][abbv]+'__'+energies1[0:][6][6][abbv])
            elements.append(k_edges['Elements'][index])
            ka.append(float(energies1[0:][6][5][abbv])*1000)
            ka2.append(float(energies1[0:][6][6][abbv])*1000)
energy = pd.DataFrame({'Element':elements, 'Ka':ka, 'Ka2':ka2})
print(energy)
energy.to_pickle('kalpha_edges.pickle')


k_edges = pd.read_pickle('elements_data.pickle')
kalpha_edges = pd.read_pickle('kalpha_edges.pickle')

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

'''

# add two columns to dataframe that contain the tolerance values in them already
# Possibly modify the dataframe column to have only the elemenent array energies