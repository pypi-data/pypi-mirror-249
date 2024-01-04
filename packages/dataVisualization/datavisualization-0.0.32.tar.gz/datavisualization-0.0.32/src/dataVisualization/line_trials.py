# libraries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


df = pd.read_excel("../../../Helen/Book1.xlsx", 'line')


# set figure size
my_dpi = 96
plt.figure(dpi=my_dpi)

# plot multiple lines
for column in df.drop(['Year', 'Quarter'], axis=1):
    plt.plot(df['Quarter'], df[column], marker='', color='grey', linewidth=1, alpha=0.4)

# Now re do the interesting curve, but biger with distinct color
plt.plot(df['Quarter'], df['Nestlé'], marker='', color='orange', linewidth=4, alpha=0.7)

# # Change x axis limit
# plt.xlim(0, 12)

# # Let's annotate the plot
# num = 0
# for i in df.values[9][1:]:
#     num += 1
#     name = list(df)[num]
#     if name != 'y5':
#         plt.text(10.2, i, name, horizontalalignment='left', size='small', color='grey')
#
# # And add a special annotation for the group we are interested in
# plt.text(10.2, df.y5.tail(1), 'Mr Orange', horizontalalignment='left', size='small', color='orange')

# Add titles
# plt.title("Evolution of Mr Orange vs other students", loc='left', fontsize=12, fontweight=0, color='orange')
plt.xlabel("Time")
plt.ylabel("Score")

# Show the graph
plt.show()