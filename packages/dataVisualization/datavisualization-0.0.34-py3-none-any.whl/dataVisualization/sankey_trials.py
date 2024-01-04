import os
from pathlib import Path

import plotly.graph_objects as go
import holoviews as hv
import pandas as pd
from holoviews import opts, dim
import matplotlib.pyplot as plt
from sankeyflow import Sankey
from bokeh.io import export_svgs
hv.extension('bokeh')

def export_svg(obj, filename):
    plot_state = hv.renderer('bokeh').get_plot(obj).state
    plot_state.output_backend = 'svg'
    export_svgs(plot_state, filename=filename)

def fmt(x):
    return f'{x}'


def corporate_sankey():
    source = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    target = [6, 6, 6, 7, 7, 7, 10, 10, 10, 10]
    values = [28.2, 11.6, 3.9, 13.9, 9.1, 1.0, 43.7, 24.0, 17.5, 20.2, 105.4]
    labels = ['Powdered & liquid beverages', 'Milk products', 'Water', 'Prepared dishes & cooking aids',
              'Confectionery', 'Ice cream', 'Beverages', 'Food', 'Nutrition & Health Science', 'Petcare', '']

    for i in range(len(labels) - 1):
        labels[i] = labels[i] + '\n' + f'({values[i]})'

    fig = go.Figure(data=[go.Sankey(
        arrangement = 'snap',
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=labels,
            color='rgba(253,185,52,1)'
        ),
        link=dict(
            source=source,
            target=target,
            value=values,
            color='rgba(253,185,52,0.75)'
        ))])
    fig.add_annotation(x=1.0625, y=0.5,
                       text="Nestlé \n(105.4)",
                       showarrow=False,
                       yshift=0)
    fig.update
    fig.show()


def corp_sankey_two():
    source = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    target = [9, 9, 10, 10, 11, 11, 12, 12, 13, 14, 14, 14, 14, 14]
    values = [8.2, 5.2, 8.3, 6.6, 10.7, 2.8, 12.8, 8.6, 2.4, 13.4, 14.9, 13.5, 21.4, 2.4, 65.5]
    labels = ['Hair Care', 'Skin Care', 'Skin Cleansing', 'Deodorant', 'Fabric', 'Home & Hygiene', 'Convenience Foods',
              'Ice Cream', 'Tea', 'Beauty & Wellbeing', 'Personal Care', 'Home Care', 'Foods ', 'Beverages', '']

    for i in range(len(labels) - 1):
        labels[i] = labels[i] + f' ({values[i]})'

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=labels,
            color='rgba(253,185,52,1)'
        ),
        link=dict(
            source=source,
            target=target,
            value=values,
            color='rgba(253,185,52,0.75)'
        ))])
    fig.add_annotation(x=0.5525, y=0.5,
                       text="Unilever (65.5)",
                       showarrow=False,
                       yshift=0)
    fig.update
    fig.show()


def corp_sankey_three():
    source = [0, 1, 2, 3, 4, 5, 6]
    target = [7, 7, 7, 7, 7, 7, 7]
    values = [3.4, 8.2, 9.9, 16.7, 25.1, 31.5, 34.4, 129.2]
    labels = ['ITC', 'Gudang Garam', 'Imperial', 'JTI', 'Altria Group', 'PMI', 'BAT', '']

    for i in range(len(labels) - 1):
        labels[i] = labels[i] + f' ({values[i]})'

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=labels,
            color='rgba(253,185,52,1)'
        ),
        link=dict(
            source=source,
            target=target,
            value=values,
            color='rgba(253,185,52,0.75)'
        ))], layout=dict(
        width=574.11023622,
        height=459.96850394
    ))
    fig.add_annotation(x=1.1525, y=0.5,
                       text="Tobacco (129.2)",
                       showarrow=False,
                       yshift=0)
    fig.update
    fig.show()


def corp_sankey_four():
    source = [0, 1, 2, 3]
    target = [4, 4, 4, 4]
    values = [10.6, 6.2, 3.3, 0.1, 20.2]
    labels = ['Personal Care', 'Consumer Tissue', 'K-C Professional', 'Corporate & other', '']

    for i in range(len(labels) - 1):
        labels[i] = labels[i] + f' ({values[i]})'

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=labels,
            color='rgba(253,185,52,1)'
        ),
        link=dict(
            source=source,
            target=target,
            value=values,
            color='rgba(253,185,52,0.75)'
        ))], layout=dict(
        width=574.11023622,
        height=459.96850394
    ))
    fig.add_annotation(x=1.1525, y=0.5,
                       text="Kimberly-Clark (20.2)",
                       showarrow=False,
                       yshift=0)
    fig.update
    fig.show()


def corp_sankey_five():
    st = [(0, 1, 28.2), (0, 2, 3.9), (0, 3, 12.6), (0, 4, 13.9), (0, 5, 9.1), (0, 6, 17.5), (0, 7, 20.2),
          (1, 8, 18.9), (1, 9, 9.3), (2, 17, 3.9), (3, 10, 11.6), (3, 11, 1), (4, 12, 6.5), (4, 13, 7.4), (5, 14, 6.9), (5, 15, 0.7), (5, 16, 1.5), (6, 19, 17.5), (7, 20, 20.2),
          (8, 17, 18.9), (9, 17, 9.3), (10, 17, 11.6), (11, 18, 1), (12, 18, 6.5), (13, 18, 7.4), (14, 18, 6.9), (15, 18, 0.7), (16, 18, 1.5)]
    source, target, values = zip(*st)
    labels = ['Nestle',

              'Powdered and liquid beverages', 'Water', 'Milk products and ice cream',
              'Prepared dishes and cooking aids', 'Confectionery', 'Nutrition and Health Science', 'PetCare',

              'Soluble coffee/coffee systems', 'Other', 'Milk products', 'Ice cream', 'Frozen and chilled',
              'Culinary and other', 'Chocolate', 'Sugar confectionery', 'Snacking and biscuits',

              'Beverages', 'Food', 'Personal Care', 'Petcare']
    print(len(st))
    print(source)
    print(target)
    print(len(values))
    print(len(labels))
    for i in range(len(labels)):
        labels[i] = labels[i] + '\n' + f'({values[i]})'

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=labels,
            color='rgba(253,185,52,1)'
        ),
        link=dict(
            source=source,
            target=target,
            value=values,
            color='rgba(253,185,52,0.75)'
        ))])
    fig.show()


def corp_sankey_food():
    source = [0, 1, 1, 3, 4, 0, 2, 2, 5, 6]
    target = [1, 3, 4, 7, 7, 2, 5, 6, 7, 8]
    values = [20, 10, 10, 5, 5, 5, 5, 15, 5, 80]
    labels = ['Nestle', 'Powder', 'MI', 'coffee', 'other', 'Milk', 'Ice', 'Bev', 'Food']

    for i in range(len(labels)):
        labels[i] = labels[i] + f' ({values[i]})'

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=labels,
            color='rgba(253,185,52,1)'
        ),
        link=dict(
            source=source,
            target=target,
            value=values,
            color='rgba(253,185,52,0.75)'
        ))], layout=dict(
        width=574.11023622,
        height=459.96850394
    ))
    fig.update
    fig.show()


def corp_sankey_six():
    stv = [
            (0, 1, 28.2), (0, 2, 3.9), (0, 3, 12.6), (0, 4, 13.9), (0, 5, 9.1), (0, 6, 17.5), (0, 7, 20.2),

            (1, 8, 18.9), (1, 9, 9.3), (3, 10, 11.6), (3, 11, 1), (4, 12, 6.5), (4, 13, 7.4), (5, 14, 6.9),
            (5, 15, 0.7), (5, 16, 1.5),

            # Change nodes
            (8, 17, 18.9), (9, 18, 9.3), (10, 19, 11.6), (11, 20, 1), (12, 21, 6.5), (13, 22, 7.4), (14, 23, 6.9),
            (15, 24, 0.7), (16, 25, 1.5), (2, 26, 3.9), (6, 27, 5.8), (6, 29, 5.8), (6, 30, 5.8), (7, 28, 20.2),

            # End nodes
            (17, 31, 18.9), (18, 31, 9.3), (19, 31, 11.6), (20, 32, 1), (21, 32, 6.5), (22, 32, 7.4), (23, 32, 6.9),
            (24, 32, 0.7), (25, 32, 1.5), (26, 31, 3.9), (27, 32, 5.8), (28, 34, 20.2), (29, 35, 5.8), (30, 36, 5.8),

            #Extension Nodes
            (31, 37, 10**-10), (32, 37, 10**-10), (33, 37, 10**-10), (34, 37, 10**-10), (35, 37, 10**-10), (36, 37, 10**-10),
           ]
    source, target, values= zip(*stv)

    labels = ['Nestle (105.4)',

              'Powdered and liquid beverages (28.2)', 'Water (3.9)', 'Milk products and ice cream (12.6)',
              'Prepared dishes and cooking aids (13.9)', 'Confectionery (9.1)', 'Nutrition and Health Science (17.5)', 'PetCare (20.2)',

              'Soluble coffee/coffee systems (18.9)', 'Other (9.3)', 'Milk products (11.6)', 'Ice cream (1.0)', 'Frozen and chilled (6.5)',
              'Culinary and other (7.4)', 'Chocolate (6.9)', 'Sugar confectionery (0.7)', 'Snacking and biscuits (1.5)',

              '', '', '', '', '', '', '', '', '', '', '', '', '', '',

              'Beverages (43.7)', 'Food (~29.8)', '', 'Petcare (20.2)', 'Consumer Healthcare (~5.8)', 'Non-FMCG (~5.8)',

              ''
              ]

    node_colors = ['rgba(35, 130, 202, 1)' for i in range(0, 17)] + ['rgba(141, 198, 63, 1)' for i in range(0, 14)] + ['rgba(253,185,52,1)' for i in range(0, 4)] + ['rgba(65, 64, 66, 1)'] + ['rgba(65, 64, 66, 1)']
    link_colors = ['rgba(35, 130, 202, 0.5)' for i in range(0, 30)] + ['rgba(253,185,52,0.5)' for i in range(0, 12)] + ['rgba(65, 64, 66, 0.5)'] + ['rgba(65, 64, 66, 0.5)'] + ['rgba(253,185,52,0)' for i in range(0, 6)]

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(width=0),
            label=labels,
            color=node_colors
        ),
        link=dict(
            source=source,
            target=target,
            value=values,
            color=link_colors
        ))],
        layout=go.Layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        ))
    fig.update_layout(
        font_color='rgb(65, 64, 66)'
    )
    fig.show()


def corp_sankey_seven():
    sankey = hv.Sankey([
        ['A', 'B', 18],
        ['A', 'C', 15],
        ['B', 'D', 5],
        ['B', 'E', 7],
        ['B', 'F', 6],
        ['C', 'G', 2],
        ['C', 'H', 9],
        ['C', 'I', 4]]
    )
    export_svg(sankey, filename='test.svg')


def corp_sankey_eight():
    nodes = [
        [('Nestle', 105.4)],

        [('Powdered and liquid beverages', 28.2), ('Water', 3.9), ('Milk products and ice cream', 12.6),
         ('Prepared dishes and cooking aids', 13.9), ('Confectionery', 9.1), ('Nutrition and Health Science', 17.5), ('PetCare', 20.2)],

        [('Soluble coffee/coffee systems', 18.9), ('Other', 9.3), ('Milk products', 11.6), ('Ice cream', 1.0), ('Frozen and chilled', 6.5),
         ('Culinary and other', 7.4), ('Chocolate', 6.9), ('Sugar confectionery', 0.7), ('Snacking and biscuits', 1.5)],

        [('A', 18.9), ('B', 9.3), ('C', 11.6), ('D', 1.0), ('E', 6.5), ('F', 7.4), ('G', 6.9), ('H', 0.7), ('I', 1.5), ('J', 3.9), ('K', 5.8), ('L', 5.8), ('M', 5.8), ('N', 20.2)],

        [('Beverages', 43.7), ('Food', 24), ('Personal Care', 5.8), ('Petcare', 20.2), ('Consumer Healthcare', 5.8), ('Non-FMCG', 5.8)]
    ]
    flows = [
        ('Nestle', 'Powdered and liquid beverages', 28.2),
        ('Nestle', 'Water', 3.9),
        ('Nestle', 'Milk products and ice cream', 12.6),
        ('Nestle', 'Prepared dishes and cooking aids', 13.9),
        ('Nestle', 'Confectionery', 9.1),
        ('Nestle', 'Nutrition and Health Science', 17.5),
        ('Nestle', 'PetCare', 20.2),

        ('Powdered and liquid beverages', 'Soluble coffee/coffee systems', 18.9),
        ('Powdered and liquid beverages', 'Other', 9.3),
        ('Water', 'J', 3.9),
        ('Milk products and ice cream', 'Milk products', 11.6),
        ('Milk products and ice cream', 'Ice cream', 1.0),
        ('Prepared dishes and cooking aids', 'Frozen and chilled', 6.5),
        ('Prepared dishes and cooking aids', 'Culinary and other', 7.4),
        ('Confectionery', 'Chocolate', 6.9),
        ('Confectionery', 'Sugar confectionery', 0.7),
        ('Confectionery', 'Snacking and biscuits', 1.5),
        ('Nutrition and Health Science', 'K', 5.8),
        ('Nutrition and Health Science', 'L', 5.8),
        ('Nutrition and Health Science', 'M', 5.8),
        ('PetCare', 'N', 20.2),

        ('Soluble coffee/coffee systems', 'A', 18.9),
        ('Other', 'B', 9.3),
        ('Milk products', 'C', 11.6),
        ('Ice cream', 'D', 1.0),
        ('Frozen and chilled', 'E', 6.5),
        ('Culinary and other', 'F', 7.4),
        ('Chocolate', 'G', 6.9),
        ('Sugar confectionery', 'H', 0.7),
        ('Snacking and biscuits', 'I', 1.5),

        ('A', 'Beverages', 18.9),
        ('B', 'Beverages', 9.3),
        ('C', 'Beverages', 11.6),
        ('J', 'Beverages', 3.9),
        ('D', 'Food', 1.0),
        ('E', 'Food', 6.5),
        ('F', 'Food', 7.4),
        ('G', 'Food', 6.9),
        ('H', 'Food', 0.7),
        ('I', 'Food', 1.5),
        ('K', 'Personal Care', 5.8),
        ('L', 'Consumer Healthcare', 5.8),
        ('M', 'Non-FMCG', 5.8),
        ('N', 'Petcare', 20.2),
    ]

    fig = plt.figure(dpi=600)
    s = Sankey(flows=flows, nodes=nodes, flow_opts=dict(curvature=0.5), node_opts=dict(label_format='{label} ({value:.1f})', label_opts=dict(fontsize=8)))
    s.draw()
    fig.savefig('test.svg', bbox_inches='tight', dpi=600)


def auto_test():
    stv = [
        (0, 1, 28.2), (0, 2, 3.9), (0, 3, 12.6), (0, 4, 13.9), (0, 5, 9.1), (0, 6, 17.5), (0, 7, 20.2),

        (1, 8, 18.9), (1, 9, 9.3), (3, 10, 11.6), (3, 11, 1), (4, 12, 6.5), (4, 13, 7.4), (5, 14, 6.9),
        (5, 15, 0.7), (5, 16, 1.5),

        # Change nodes
        (8, 17, 18.9), (9, 18, 9.3), (10, 19, 11.6), (11, 20, 1), (12, 21, 6.5), (13, 22, 7.4), (14, 23, 6.9),
        (15, 24, 0.7), (16, 25, 1.5), (2, 26, 3.9), (6, 27, 5.8), (6, 29, 5.8), (6, 30, 5.8), (7, 28, 20.2),

        # End nodes
        (17, 31, 18.9), (18, 31, 9.3), (19, 31, 11.6), (20, 32, 1), (21, 32, 6.5), (22, 32, 7.4), (23, 32, 6.9),
        (24, 32, 0.7), (25, 32, 1.5), (26, 31, 3.9), (27, 33, 5.8), (28, 34, 20.2), (29, 35, 5.8), (30, 36, 5.8),

        # Extension Nodes
        (31, 37, 10 ** -10), (32, 37, 10 ** -10), (33, 37, 10 ** -10), (34, 37, 10 ** -10), (35, 37, 10 ** -10),
        (36, 37, 10 ** -10),
    ]
    routes = auto_routes(pd.read_excel("../../../Helen/Book1.xlsx", 'Sheet1'))


def single_layer(file:str):
    datasheets: dict[str, pd.DataFrame] = pd.read_excel(file, sheet_name=None)
    names = list(datasheets.keys())
    dfs = list(datasheets.values())
    for i in range(len(dfs)):
        if not names[i] == '1-tier Sankey':
            df = dfs[i]
            node_labels = df['Business segments'].values.tolist()

            stv = []
            for j in range(len(node_labels)):
                stv.append(tuple((j, len(node_labels), df['Segment Revenues ($bn)'][j])))
                node_labels[j] = node_labels[j] + f" ({round(df['Segment Revenues ($bn)'][j],1)}bn)"

            print(stv)
            node_labels.append(df['Corporate'][0] + f" ({round(df['Total ($bn)'][0],1)}bn)")
            print(node_labels)

            source, target, values = zip(*stv)

            fig = go.Figure(data=[go.Sankey(
                node=dict(
                    pad=15,
                    thickness=20,
                    line=dict(width=0),
                    label=node_labels,
                    color='rgba(253,185,52,1)'
                ),
                link=dict(
                    source=source,
                    target=target,
                    value=values,
                    color='rgba(253,185,52,0.5)'
                ))],
                layout=go.Layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                ))
            fig.update_layout(
                font_color='rgb(65, 64, 66)'
            )

            if not os.path.exists("images"):
                os.mkdir("images")

            fig.write_image(f'images/{names[i]}.svg')


def make_nodes(df:pd.DataFrame) -> dict[str, (int, float)]:
    nodes = {}
    pointer = 0
    corp = df['Corporate'].values.tolist()
    # print(type(df.loc[df['Business segments'] == 'North America ']['Segment Revenues ($bn)'][0]))
    for i in corp:
        if i not in nodes:
            nodes[i] = [pointer, df.loc[df['Corporate'] == i]['Total ($bn)'][0]]
            pointer = pointer + 1
    bus_seg = df['Business segments'].values.tolist()
    for i in bus_seg:
        if i not in nodes:
            nodes[i] = [pointer, df.loc[df['Business segments'] == i]['Segment Revenues ($bn)'].to_list()[0]]
            pointer = pointer + 1
    sector = df['Sector'].values.tolist()
    for i in sector:
        if i not in nodes:
            nodes[i] = [pointer, df.loc[df['Sector'] == i]['Segment Revenues ($bn)'].to_list()[0]]
            pointer = pointer + 1
    nodes['temp_Node'] = [pointer, 0.001]
    return nodes


def susify(x):
    return 'Susmon ' + x


def make_labels(labels, va):
    for lb in range(len(labels)):
        print(va[lb])
        if 'temp_Node' in labels[lb]:
            labels[lb] = labels[lb].replace('temp_Node', '')
            continue
        if 'Susmon ' in labels[lb]:
            labels[lb] = labels[lb].replace('Susmon ', '')
        labels[lb] = labels[lb].strip() + f' ({round(va[lb][1], 2)}bn)'
    return labels


def two_layer(file:str):
    datasheets: dict[str, pd.DataFrame] = pd.read_excel(file, sheet_name=None)
    names = list(datasheets.keys())
    dfs = list(datasheets.values())
    for i in range(len(dfs)):
        if not names[i] == '1-tier Sankey':
            df = dfs[i]
            sector_col = df['Sector']
            new_sector_col = sector_col.apply(susify)
            df['Sector'] = new_sector_col
            node_map = make_nodes(df)
            link_colors = []
            stv = []
            for index, row in df.iterrows():
                stv.append(tuple((node_map[row['Corporate']][0], node_map[row['Business segments']][0], row['Segment Revenues ($bn)'])))
                link_colors.append('rgba(253,185,52,0.5)')
                stv.append(tuple((node_map[row['Business segments']][0], node_map[row['Sector']][0], row['Segment Revenues ($bn)'])))
                link_colors.append('rgba(253,185,52,0.5)')
                stv.append(tuple((node_map[row['Sector']][0], node_map['temp_Node'][0], 0.001)))
                link_colors.append('rgba(253,185,52,0)')

            source, target, values = zip(*stv)
            print(link_colors)
            labels = make_labels(list(node_map.keys()), list(node_map.values()))

            node_colors = []
            for n in range(len(node_map) - 1):
                node_colors.append('rgba(253,185,52,1)')
            node_colors.append('rgba(0,0,0,0)')

            fig = go.Figure(data=[go.Sankey(
                node=dict(
                    pad=15,
                    thickness=20,
                    line=dict(width=0),
                    label=labels,
                    color=node_colors
                ),
                link=dict(
                    source=source,
                    target=target,
                    value=values,
                    color=link_colors
                ))],
                layout=go.Layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                ))
            fig.update_layout(
                font_color='rgb(65, 64, 66)'
            )

            if not os.path.exists("images"):
                os.mkdir("images")

            fig.write_image(f'images/{names[i]}.svg')


if __name__ == '__main__':
    # corporate_sankey()
    # corp_sankey_eight()
    print(os.curdir)
    corp_sankey_six()
