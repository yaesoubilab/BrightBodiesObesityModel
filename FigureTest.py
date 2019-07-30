# to create figure showing differences between model/RCT

# import plotting library
import matplotlib.pyplot as plt

x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
y = [0, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0]
f, ax = plt.subplots()
ax.plot(x, y)
ax.set_title('Difference in Avg BMI by Intervention')
plt.xlim((0.0, 10.5))
plt.xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
plt.yticks([0, 0.5, 1.0, 1.5, 2.0])
plt.xlabel('Sim Years')
plt.ylabel('Difference in BMI (kg/m^2)')
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
