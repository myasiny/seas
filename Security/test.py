import matplotlib.pyplot as plt

d ={'5000cca234c1c445': {382877: 7, 382919: 3},
'5000cca234c94a2e': {382873: 1, 382886: 1},
'5000cca234c89421': {383173: 1, 383183: 2, 382917: 1, 382911: 1},
'5000cca234c5d43a': {382889: 1, 382915: 1, 382917: 8},
'5000cca234c56488': {382909: 2, 382911: 5}}

colors = list("rgbcmyk")

for data_dict in d.values():
   x = data_dict.keys()
   y = data_dict.values()
   plt.scatter(x,y,color=colors.pop())

plt.legend(d.keys())
plt.show()