from argparse import ArgumentParser
from matplotlib import pyplot as plt
from greengraph import Greengraph 

def process():
    parser = ArgumentParser(description = "Generating a greengraph by using a start point, an end point, number of steps and the name of the file you want the graph to be stored at.")
    
    parser.add_argument('--from', '-f', dest = 'fromCity')
    parser.add_argument('--to', '-t', dest = 'toCity')
    parser.add_argument('--steps', '-s')
    parser.add_argument('--out', '-o')

    args = parser.parse_args()

    myGraph = Greengraph(args.fromCity, args.toCity)
    data = myGraph.green_between(args.steps)
    plt.plot(data)
    plt.savefig(args.out)
    

if __name__ == "__main__":
    process()

