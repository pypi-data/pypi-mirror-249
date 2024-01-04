import matplotlib.pyplot as plt
import matplotlib.colors as c
import matplotlib.cm as cm

def main():
    colors_li = ['#FFEBB0', '#FFDF91', '#FED272', '#FEC653', '#FDB934', '#FAA438', '#F88F3B', '#F57A3F', '#F36542',
                 '#F05046']
    legend_labels = ['less than 10%', '10%-19%', '20%-29%', '30%-39%', '40%-49%', '50%-59%', '60%-69%', '70%-79%',
                     '80%-89%', '90%-100%']
    fig, ax = plt.subplots(figsize=(1, 10), layout='constrained')
    cbar = plt.gcf().colorbar(cm.ScalarMappable(
        cmap=c.ListedColormap(colors_li)),
        cax=ax,
        orientation='vertical'
    )
    cbar.ax.tick_params(size=0)
    cbar.set_ticks([])
    fig.savefig('tree_legend.svg')

if __name__ == '__main__':
    main()