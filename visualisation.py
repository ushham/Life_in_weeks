import matplotlib.pyplot as plt
import numpy as np
import control as ct

class DataVisualisation():

    def __init__(self, data, batches, cats, events,):
        self.data = data
        self.batches = batches
        self.categories = cats

        self.events = events

        self.y, self.x, self.cat_num = self.data.shape
    
    def scatter_graph(self):
        rad1 = 1 / len(self.categories)

        fig, ax = plt.subplots(num='My life in weeks', figsize=(12, 8))

        fig.patch.set_facecolor('grey')
        ax.set_facecolor('grey')

        if ct.portrait_view:
            X, Y = np.meshgrid(np.linspace(0, self.x-1, self.x), np.linspace(0, self.y-1, self.y))
        else:
            X, Y = np.meshgrid(np.linspace(0, self.y-1, self.y), np.linspace(0, self.x-1, self.x))

        ax.scatter(X, Y, s=ct.radius * 0.25, facecolors='none', edgecolors='darkgrey')

        for idx, batch_it in enumerate(self.batches):
            
            cat_idx = self.categories.index(batch_it[0])
            x_circ = [0] + np.cos(np.linspace(2 * np.pi * rad1 * cat_idx, 2 * np.pi * rad1 * (cat_idx + 1), 10)).tolist()
            y_circ = [0] + np.sin(np.linspace(2 * np.pi * rad1 * cat_idx, 2 * np.pi * rad1 * (cat_idx + 1), 10)).tolist()
      
            xy = np.column_stack([x_circ, y_circ])
            sxy = np.abs(xy).max()

            blob_size = np.reshape(self.data[:, :, idx], -1) * ct.radius

            if ct.portrait_view:
                ax.scatter(X, Y, marker=xy, s=sxy ** 2 * blob_size, c=batch_it[1])
            else:
                ax.scatter(X.T, Y.T, marker=xy, s=sxy ** 2 * blob_size, c=batch_it[1])

        #Life events recolour scatter
        for ev in self.events:
            if ct.portrait_view:
                ax.scatter(ev[0][1], ev[0][0], s=ct.radius * 0.25, facecolors='none', edgecolors=ev[1], linewidths=1.5)
            else:
                ax.scatter(ev[0][0], ev[0][1], s=ct.radius * 0.25, facecolors='none', edgecolors=ev[1], linewidths=1.5)

        if ct.portrait_view:
            plt.xticks([])
        else:
            plt.yticks([])

        plt.show()
        return 0