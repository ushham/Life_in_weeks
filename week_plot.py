import visualisation as vs
import data_extract as de

if __name__ == 'main':
    cl = de.DataExtract()
    data = cl.boolian_array_maker()

    x = vs.DataVisualisation(data)
    y = x.scatter_graph()