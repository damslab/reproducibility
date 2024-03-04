import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import plot_util as pu
import numpy as np
import math

all_names = []
all_unique = []
all_rows = []

def add(n,d):
	all_names.append(n)
	unique = list(d.nunique())
	all_unique.append(unique)
	rows = d.shape[0]
	all_rows.append(rows)

def add2(n ,u, r):
	all_names.append(n)
	all_unique.append(u)
	all_rows.append(r)

def addNoMaterialize(n, p, header=None, delimiter = '\t'):
	cols = None
	rows = 0
	with open(p) as f:
		for l in f:
			sp = l.split(delimiter)

			if cols == None:
				cols = []
				for i in range(len(sp)):
					cols.append(set()) # add empty dicts
		
			for id, s in enumerate(sp):
				cols[id].add(s)
			rows += 1
			# if rows % 10000 == 0:
			# 	print(rows)

	cols = [len(x) for x in cols]
	all_names.append(n)
	all_unique.append(cols)
	all_rows.append(rows)


add("Adult",pd.read_csv("data/adult/adult.csv", header=None))
add("Cat",pd.read_csv("data/cat/train.csv"))
# addNoMaterialize("Criteo 10k", "data/criteo/day_0_10000.tsv")
# addNoMaterialize("Criteo 100k", "data/criteo/day_0_100000.tsv")
# addNoMaterialize("Criteo 1M", "data/criteo/day_0_1000000.tsv")
# addNoMaterialize("Criteo Day_0","data/criteo/day_0.tsv")
add2("Criteo Day0",[2, 31350, 8001, 1459, 29994, 4123, 866, 610, 11570, 1642, 15, 225, 725558, 4671, 18576837, 29427, 15127, 7295, 19901, 3, 6465, 1310, 61, 11700067, 622921, 219556, 10, 2209, 9779, 71, 4, 963, 14, 22022124, 4384510, 15960286, 290588, 10829, 95, 34], 195841983 )
# add("Crypto",pd.read_csv("data/crypto/train.csv"))
add2("Crypto",[1956782, 14, 21443, 9932783, 2800549, 2688809, 9909377, 22521865, 23561248, 22176025], 24236806 )
# add("HomeCredit",pd.read_csv("data/home/train.csv"))
add2("Home",[ 2, 2, 3, 2, 2, 15, 2548, 5603, 13672, 1002, 7, 8, 5, 6, 6, 81, 17460, 12574, 15688, 6168, 62, 2, 2, 2, 2, 2, 2, 18, 17, 3, 3, 7, 24, 2, 2, 2, 2, 2, 2, 58, 114584, 119831, 814, 2339, 3780, 285, 149, 3181, 257, 285, 403, 305, 3527, 1868, 5199, 386, 3290, 760, 3841, 221, 154, 3128, 26, 30, 25, 25, 3563, 736, 5301, 167, 3327, 1148, 3772, 245, 151, 3202, 46, 46, 49, 47, 3560, 1097, 5281, 214, 3323, 4, 3, 5116, 7, 2, 33, 10, 33, 9, 3773, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 5, 9, 9, 24, 11, 25], 307511)
# add("KDD98",pd.read_csv("data/kdd98/cup98val.csv", low_memory=False))
add2("KDD",[56, 898, 54, 59, 16508, 2, 3, 941, 4, 2, 2, 2, 2, 30, 17, 54, 93, 3, 3, 4, 4, 4, 4, 7, 7, 5, 10, 82, 7, 4, 10, 7, 10, 5, 5, 7, 5, 10, 10, 10, 3, 10, 4, 95, 91, 95, 100, 52, 64, 58, 5, 9, 2, 10, 8, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 2, 9817, 4803, 5714, 100, 100, 100, 84, 84, 100, 100, 84, 95, 100, 21, 59, 61, 59, 34, 34, 46, 97, 42, 79, 63, 73, 67, 59, 66, 62, 55, 60, 88, 69, 80, 95, 68, 57, 40, 44, 63, 78, 63, 49, 67, 55, 93, 99, 85, 100, 97, 85, 96, 85, 69, 54, 95, 53, 62, 99, 399, 385, 100, 100, 71, 100, 100, 100, 96, 90, 87, 4416, 4575, 14, 14, 100, 100, 95, 96, 100, 96, 99, 100, 91, 100, 100, 66, 16, 63, 83, 82, 59, 52, 95, 100, 46, 80, 51, 100, 100, 100, 100, 100, 100, 94, 100, 81, 79, 26, 24, 98, 100, 100, 98, 83, 100, 50, 100, 100, 100, 100, 300, 204, 206, 1120, 1224, 1094, 1152, 21679, 100, 66, 59, 63, 71, 54, 40, 31, 71, 95, 71, 70, 72, 74, 60, 45, 39, 78, 100, 75, 100, 91, 99, 100, 94, 99, 69, 74, 71, 49, 29, 17, 84, 55, 83, 99, 72, 65, 63, 99, 99, 100, 99, 100, 98, 98, 100, 99, 96, 92, 70, 63, 38, 61, 59, 25, 37, 71, 73, 56, 56, 42, 44, 79, 55, 51, 74, 41, 34, 41, 69, 51, 45, 51, 40, 58, 64, 61, 58, 56, 64, 58, 64, 89, 58, 24, 78, 76, 66, 76, 63, 38, 64, 69, 76, 94, 17, 56, 98, 84, 96, 42, 66, 91, 29, 96, 85, 100, 97, 62, 53, 29, 82, 21, 15, 41, 46, 48, 57, 31, 31, 21, 27, 16, 91, 100, 100, 100, 76, 78, 95, 100, 80, 32, 53, 83, 100, 100, 100, 100, 100, 89, 55, 100, 94, 100, 98, 19, 93, 100, 100, 100, 53, 72, 22, 6, 35, 46, 2, 2, 9, 1, 2, 3, 4, 3, 2, 4, 4, 3, 2, 1, 3, 3, 9, 3, 2, 2, 5, 3, 2, 14, 67, 67, 41, 108, 104, 105, 109, 94, 105, 108, 88, 99, 34, 126, 121, 125, 113, 82, 105, 118, 88, 97, 59, 5, 162, 21, 60, 16, 24, 6, 17, 10, 16, 7, 7, 9, 9, 15, 11, 16, 18, 11, 15, 13, 10, 12, 12, 16, 14, 31, 28, 8, 38, 81, 105, 94, 79, 94, 129, 78, 93, 76, 98, 65, 85, 88, 74, 78, 92, 69, 90, 2129, 90, 35, 208, 146, 278, 146, 238, 24, 175, 180, 64, 7735, 96367, 2, 1, 4, 4, 5, 4, 5, 62, 5], 96367)
# add("Salaries",pd.read_csv("data/salaries/salaries.csv"))
# add("Santander",pd.read_csv("data/santander/train.csv"))
add2("Santander",[2, 94672, 108932, 86555, 74597, 63515, 141029, 38599, 103063, 98617, 49417, 128764, 130193, 9561, 115181, 79122, 19810, 86918, 137823, 139515, 144180, 127764, 140062, 90660, 24913, 105101, 14853, 127089, 60185, 35859, 88339, 145977, 77388, 85964, 112239, 25164, 122384, 96404, 79040, 115366, 112674, 141878, 131896, 31592, 15188, 127702, 169968, 93450, 154781, 152039, 140641, 32308, 143455, 121313, 33460, 144776, 128077, 103045, 35545, 113907, 37744, 113763, 159369, 74777, 97098, 59379, 108347, 47722, 137253, 451, 110346, 153193, 13527, 110114, 142582, 161058, 129383, 139317, 106809, 72254, 53212, 136432, 79065, 144829, 144281, 133766, 108437, 140594, 125296, 84918, 103522, 157210, 7962, 110743, 26708, 89146, 29387, 148099, 158739, 33266, 69300, 150727, 122295, 146237, 9376, 72627, 39115, 71065, 137827, 8525, 112172, 106121, 46464, 60482, 116496, 43084, 86729, 63467, 164469, 143667, 112403, 158269, 64695, 121767, 129893, 91022, 16059, 32411, 95710, 98200, 113425, 36638, 21464, 57923, 19236, 131619, 140774, 156615, 144397, 117428, 137294, 121384, 134443, 128613, 94372, 40595, 108526, 84314, 137559, 10608, 148504, 83660, 109667, 95823, 73728, 119342, 127457, 40634, 126534, 144556, 112830, 156274, 11071, 57396, 123168, 122744, 119403, 17902, 140954, 97227, 18242, 113720, 125914, 143366, 128120, 134945, 92659, 142521, 85720, 145235, 90090, 123477, 56164, 149195, 117529, 145184, 120747, 98060, 157031, 108813, 41764, 114959, 94266, 59065, 110557, 97069, 57870, 125560, 40537, 94153, 149430], 200000)


fig_size = (3.33,1)
fig, axi = plt.subplots(1, len(all_unique),  num=None, figsize=fig_size,
        dpi=pu.dpi, facecolor="w", edgecolor="k")



# all_unique = []

# print(all_unique[2])
# print(all_unique[3])
# plt.rc('axes', labelsize=4)

for idx,ax in enumerate(axi):
	u = all_unique[idx]
	u.sort(reverse=True)
	ax.set_xmargin(0.05)
	ax.set_ymargin(0)
	u = np.array(u) /  all_rows[idx] * 100
	max_x = len(u)
	max_y = max(u)
	red = np.array([196/256, 13/256, 30/256])
	blue = np.array([ 42/256,186/256,212/256])

	max_change = red - blue

	colors = [((math.log(x) - math.log(0.001)) / (math.log(100) - math.log(0.0001)) ) for x in u]
	colors = [ blue + max_change * x for x in colors]
	colors = [ (max(x[0], blue[0]),min(x[1], blue[1]), min(x[2], blue[2])) for x in colors]

	ax.bar(range(len(u)), height = u , width=0.9, color = colors)
	ax.set_yscale('log', base=10)
	ax.set_xticks([])
	
	ytics = pu.set_tics_y_log10(ax,0.00001, 100)
	# ax.tick_params(axis="y",direction="in", pad=-22, labelsize=4)
	# ax.tick_params(axis="x",direction="in", pad=-15, labelsize=4)
		
	ax.tick_params(axis="y",labelsize=7)
	# ax.tick_params(axis="x",labelsize=4)

	if idx == 0:
		ax.set_ylabel("% Distinct", size= 8)
	else:
		ax.set_yticklabels(["" for x in range(len(ytics))])

	if idx == 3:
		ax.set_xlabel("Columns Sorted by # Distinct",size= 8)
		ax.xaxis.set_label_coords(0.5, -0.07)

	# ax.set_xlabel(all_names[idx])
	# ax.text(max_x-(max_x * 0.01),max_y-(max_y * 0.01),
	if idx == 0 or idx == 3 or idx == 5 or idx == 6:
		ax.text(0.06,0.01, all_names[idx],
				 bbox=dict(boxstyle="square",pad=0.1, fc="w", ec="k", lw=0.1),
				  rotation=90, size=6, ha="left", va="bottom",transform=ax.transAxes)
	else:
		ax.text(0.94,0.97, all_names[idx],
				 bbox=dict(boxstyle="square",pad=0.1, fc="w", ec="k", lw=0.1),
				  rotation=90, size=6, ha="right", va="top",transform=ax.transAxes)
	# ax.text(0.94,0.99, all_names[idx],
	# 			 bbox=dict(boxstyle="square",pad=0.1, fc="w", ec="k", lw=0.1),
	# 			  rotation=90,size=3, ha="right", va="top",transform=ax.transAxes)
	ax.grid(True, "major", axis="both", ls="--", linewidth=0.4, alpha=0.8)

# fig.supxlabel('Distinct Columns')

plt.subplots_adjust(left=0.17, right=0.99, top=0.95,
                        bottom=0.2, wspace=0.17, hspace=0.30)
# plt.show()
out  ="plotting/plots/micro/DistinctDatasets.pdf"
print("Script","plotting/scripts/plot_distinct_motivation.py","out", out)
plt.savefig(out)

# [print(x) for x in all_unique]






