# to create figure showing BMI differences between control/bb in model
# compare to RCT

# import plotting library
import matplotlib.pyplot as plt
import matplotlib.patches as patch

x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
sim_ys = [[0, 1.5, 1, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 1.2, 0.9, 0, 0, 0, 0, 0, 0, 0, 0]]
bb_ys = [1.1, 1.4]

f, ax = plt.subplots()

for sim_y in sim_ys:
    ax.plot(x, sim_y, color='maroon')

# adding bright bodies data
ax.scatter([1, 2], bb_ys, color='orange')
ax.errorbar([1, 2], bb_ys, yerr=[[0.1, 0.2], [0.3, 0.4]], fmt='none', capsize=4, ecolor='orange')

ax.set_title('Difference in Average BMI by Intervention')
plt.xlim((0.0, 10.5))
plt.xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
plt.yticks([0, 0.5, 1.0, 1.5, 2.0])
plt.xlabel('Sim Years')
plt.ylabel('Difference in BMI (kg/m^2)')
# Show legend
model_data_color = patch.Patch(color='maroon', label='Sim: BMI Differences')
rct_data_color = patch.Patch(color='orange', label='RCT: BMI Differences')
plt.legend(loc='upper right', handles=[model_data_color, rct_data_color])
plt.show()


# sim_times = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# RCT_diffs = [2, 1, 0, 0, 0, 0, 0, 0, 0, 0]
# sim_diffs = [1.5, 0.5, 0, 0, 0, 0, 0, 0, 0, 0]
# diffs = []
# for i in range(10):
#     x = RCT_diffs[i] - sim_diffs[i]
#     diffs.append(x)
# print('diffs:', diffs)
#
# # %matplotlib inline
# line, caps, bars = plt.errorbar(
#     sim_times,  # X
#     diffs,  # Y
#     yerr=1,     # Y-errors
#     fmt="rs--",  # format line like for plot()
#     linewidth=3,	 # width of plot line
#     elinewidth=0.5,  # width of error bar line
#     ecolor='c',  # color of error bar
#     capsize=2,  # cap length for error bar
#     capthick=0.5  # cap thickness for error bar
#     )
# plt.setp(line, label='Error Bars')  # give label to returned line
# plt.legend(loc='upper left')  # Show legend
# plt.xlim((0.0, 10.5))
# plt.xticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
# plt.yticks([0, 0.5, 1, 1.5, 2])
# plt.show()  # produce plot
#
#
#
# # # %matplotlib inline
# # line, caps, bars = plt.errorbar(
# #     [1, 2, 3, 4],  # X
# #     [1, 4, 9, 16],  # Y
# #     yerr=5,     # Y-errors
# #     # label="Error bars plot",
# #     fmt="rs--",  # format line like for plot()
# #     linewidth=3,	 # width of plot line
# #     elinewidth=0.5,  # width of error bar line
# #     ecolor='y',  # color of error bar
# #     capsize=5,  # cap length for error bar
# #     capthick=0.5  # cap thickness for error bar
# #     )
# # plt.setp(line, label='Error Bars')  # give label to returned line
# # plt.legend(loc='upper left')  # Show legend
# # plt.xlim((0.5, 4.5))
# # plt.xticks([1, 2, 3, 4])
# # plt.yticks([0, 5, 10, 15, 20])
# # plt.show()  # produce plot
#
