import visualisation as vs
import data_extract as de

if __name__ == '__main__':
    cl = de.DataExtract()
    data = cl.boolian_array_maker(*cl.extract_data())

    vs.DataVisualisation(*data).scatter_graph()