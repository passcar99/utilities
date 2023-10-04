import matplotlib
import matplotlib.pyplot as plt
import numpy as np

### A simple script for converting Uppaal csv traces into images via matplotlib
while True:
    filename = input("Insert the name of the Uppaal trace file: ")
    with open(filename, 'r') as f:
        traces = dict()
        f.readline() #discard first line
        
        while True:
            line = f.readline()
            if len(line)==0: 
                break
            if line.startswith('#'):
                name = line.split('#')[1]
                traces[name] = [[], []]
            else:
                row = line.split(sep=' ')
                traces[name][0].append(float(row[0]))
                traces[name][1].append(float(row[1]))
                
        for trace in traces.keys():
            plt.plot(traces[trace][0], traces[trace][1], label = trace)
        plt.legend(loc='upper right', fancybox=True)
        plt.savefig(filename[:-4] + '.png', bbox_inches='tight')
        plt.show()
    stop = int(input("Press 0 to stop, any number to continue "))
    if stop == 0:
        break
