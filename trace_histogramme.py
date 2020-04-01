import numpy as np
import matplotlib.pyplot as plt
def trace_histogramme(data,title="",texte="",nb_classes=50,data_min=0.,data_max=100.):
    ''' tracé de l'histogramme des valeurs de la liste "data" '''
    n,bins,patches = plt.hist(data,nb_classes, density=True, facecolor='g', alpha=0.75)  # the histogram of the data
    plt.xlabel('Smarts')
    plt.ylabel('Probability')
    plt.title(title)
    plt.text(60, .025,texte)
    plt.xlim(data_min,data_max)
    plt.ylim(0, 0.2)
    plt.grid(True)
    plt.show()
"""
np.random.seed(19680801)  # Fixing random state for reproducibility
mu,sigma = 100, 15
x = mu + sigma * np.random.randn(1000)
trace_histogramme(x)
"""