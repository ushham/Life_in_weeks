import matplotlib.pyplot as plt
import numpy as np
import control as ct

class DataVisualisation():

    radius = 250

    def __init__(self, data):
        self.data = data
        self.y, self.x, self.cat = self.data.shape
    
    def scatter_graph(self):
        cols = ['green', 'red', 'b', 'pink', 'lightblue']
        rad1 = 1 / self.cat
        fig, ax = plt.subplots()

        fig.patch.set_facecolor('grey')
        ax.set_facecolor('grey')

        X, Y = np.meshgrid(np.linspace(0, self.x, self.x), np.linspace(0, self.y, self.y))
        ax.scatter(X, Y, s=self.radius * 0.25, facecolors='none', edgecolors='darkgrey')
        for c in range(self.cat):
            x_circ = [0] + np.cos(np.linspace(2 * np.pi * rad1 * c, 2 * np.pi * rad1 * (c + 1), 10)).tolist()
            y_circ = [0] + np.sin(np.linspace(2 * np.pi * rad1 * c, 2 * np.pi * rad1 * (c + 1), 10)).tolist()
      
            xy = np.column_stack([x_circ, y_circ])
            sxy = np.abs(xy).max()

            blob_size = np.reshape(self.data[:, :, c], -1) * self.radius

            ax.scatter(X, Y, marker=xy, s=sxy ** 2 * blob_size, c=cols[c])

        plt.xticks([])
        plt.show()

import data_extract as de
cl = de.DataExtract()
data = cl.boolian_array_maker()

x = DataVisualisation(data)
y = x.scatter_graph()