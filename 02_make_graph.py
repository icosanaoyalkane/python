import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# https://parallelcareerlab.com/?p=2420


def all_gray(dir):

    for i in glob.glob(dir):

        df = pd.read_csv(i)
        x = df.iloc[:,0]
        y = df.iloc[:,1]
        graph = plt.plot(x, y, label=i, linewidth=0.1, color='lightgray')
    
    return graph

def start_goal(dir):

    graphs = []
    l = glob.glob(dir)
    n = len(l)

    # start
    df_start = pd.read_csv(l[0])
    x_start = df_start.iloc[:,0]
    y_start = df_start.iloc[:,1]
    graph_start = plt.plot(x_start, y_start, linewidth=0.5, color='gray')

    # goal
    df_goal = pd.read_csv(l[n-1])
    x_goal = df_goal.iloc[:,0]
    y_goal = df_goal.iloc[:,1]
    graph_goal = plt.plot(x_goal, y_goal, linewidth=0.5, color='firebrick')

    # add
    graphs.append(graph_start)
    graphs.append(graph_goal)
    # plt.show()

    return graph_start, graph_goal

def tracking(dir):

    graphs = []
    for i in range(len(glob.glob(dir))):

        file = glob.glob(dir)[i]
        name = os.path.split(file)[1]

        df = pd.read_csv(file)
        x = df.iloc[:,0]
        y = df.iloc[:,1]

        graph, = plt.plot(x, y,
                         linewidth=0.3,
                         color='indianred',
                         label=name)

        text = plt.text(3500,0.9, name)
        graphs.append([graph, text])

    return graphs

def gif(fig,graphs):

    ani = animation.ArtistAnimation(fig, graphs, interval=200) # interval:speed[ms]
    ani.save('animation.gif', writer='pillow')
    plt.close()

    return

if __name__ == '__main__':

    ### USER INPUT ###
    dir = r"C:\BoxDrive\Box\I_材料技術部_正社員\部共通\01_開発\12_テーマ進行中\S1442_1_微細水(AIR)膜向け材料技術開発\04_材料開発_実験\01_FT-IR\ケモメトリックス\01_加熱データ_to_gif\0125_all\*csv"

    x_min = 1000
    x_max = 4000
    y_min = 0.5
    y_max = 1.0
    ##################

    ### Graph Setting ###
    fig, ax = plt.subplots()
    ax.set_xlim(x_min, x_max, auto=False)  # x軸の範囲
    ax.set_ylim(y_min, y_max, auto=False)  # y軸の範囲
    plt.xlabel("WaveNumber(cm-1)", fontsize=15)
    plt.ylabel("Absorbance", fontsize=15)


    ### all gray line (baseline) ###
    all_gray(dir)
    # plt.show()


    ### add start_goal line ###
    start_goal(dir)
    # plt.show()


    ### add tracking line ###
    gif(fig,tracking(dir))



