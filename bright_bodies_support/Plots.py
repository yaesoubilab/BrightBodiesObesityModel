import matplotlib.pyplot as plt
import numpy
from matplotlib import collections as matcoll
import matplotlib.patches as mpatches

import SimPy.Plots.FigSupport as Fig
import SimPy.Plots.SamplePaths as Path
import bright_bodies_support.Inputs as I


# Yearly difference in BMI under control and bright bodies
YEARLY_DIFF_BMI_CONTROL = [1.9, 0.0]
YEARLY_DIFF_BMI_CONTROL_LB = [.8, 1.0]
YEARLY_DIFF_BMI_CONTROL_UB = [.9, 1.0]
YEARLY_DIFF_BMI_BB = [-1.8, 0.9]
YEARLY_DIFF_BMI_BB_LB = [.6, .8]
YEARLY_DIFF_BMI_BB_UB = [.7, .8]


def add_yearly_change_in_bmi_to_ax(ax, sim_outcomes, intervention):
    """ add yearly change in BMI to provided axis """

    # BMI difference by year
    year_one_vs_zero = []
    year_two_vs_one = []

    for cohortID in range(len(sim_outcomes.pathsOfCohortAveBMI)):
        bmi_values = sim_outcomes.pathsOfCohortAveBMI[cohortID].get_values()

        # year 1 minus year 0
        year_one_vs_zero.append(bmi_values[1] - bmi_values[0])
        # year 2 minus year 1
        year_two_vs_one.append(bmi_values[2] - bmi_values[1])

    if intervention == I.Interventions.BRIGHT_BODIES:
        ys = YEARLY_DIFF_BMI_BB
        lbs = YEARLY_DIFF_BMI_BB_LB
        ubs = YEARLY_DIFF_BMI_BB_UB
        ax.set_title('\nBright Bodies')
        ax.text(-0.05, 1.025, 'B)', transform=ax.transAxes, size=11, weight='bold')
    else:
        ys = YEARLY_DIFF_BMI_CONTROL
        lbs = YEARLY_DIFF_BMI_CONTROL_LB
        ubs = YEARLY_DIFF_BMI_CONTROL_UB
        ax.set_title('\nClinical Control')
        ax.text(-0.05, 1.025, 'A)', transform=ax.transAxes, size=11, weight='bold')

    # adding simulation outcomes
    for this_y in year_one_vs_zero:
        ax.scatter(1, this_y, color='plum', marker='_', s=200, alpha=0.5, label='Model', zorder=1)
    for this_y in year_two_vs_one:
        ax.scatter(2, this_y, color='plum', marker='_', s=200, alpha=0.5, zorder=1)

    # adding RCT data
    ax.scatter([1, 2], ys, color='purple', label='RCT', zorder=2)
    # adding error bars
    ax.errorbar([1, 2], ys, yerr=(lbs, ubs), fmt='none', capsize=4, color='purple', zorder=2)

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1][:2], labels[::-1][:2], loc='upper right')
    #ax.legend(loc='upper right')

    ax.axhline(y=0, color='k', ls='--', linewidth=0.5)

    ax.set_xlim((0.5, 2.5))
    ax.set_xticks([1, 2])
    ax.set_xticklabels(['Year 1 to 0', 'Year 2 to 1'])
    ax.set_ylim((-3.5, 3.5))
    if intervention == I.Interventions.CONTROL:
        ax.set_ylabel('Difference in BMI (kg/m'+r"$^2$"+')')
    else:
        ax.set_ylabel(' ')


def plot_yearly_change_in_bmi(sim_outcomes_control, sim_outcomes_bb):
    """ generates validation graphs: BMI differences by year """

    # plot
    f, axes = plt.subplots(1, 2, figsize=(5, 4), sharey=True)

    f.suptitle('Differences in Average BMI by Year')
    add_yearly_change_in_bmi_to_ax(ax=axes[0], sim_outcomes=sim_outcomes_control,
                                   intervention=I.Interventions.CONTROL)
    add_yearly_change_in_bmi_to_ax(ax=axes[1], sim_outcomes=sim_outcomes_bb,
                                   intervention=I.Interventions.BRIGHT_BODIES)

    f.subplots_adjust(hspace=2, wspace=2)
    f.tight_layout()

    # bbox_inches set to tight: cleans up figures
    plt.savefig("figures/yearlyBMIChange.png", dpi=300)
    plt.show()


def plot_bb_effect(sim_outcomes_BB, sim_outcomes_CC, maintenance_effect):
    """ plot differences in BMI by intervention
    and compare to RCT data """

    # find difference in yearly average BMI between interventions
    diff_yearly_ave_bmis = []
    for cohortID in range(len(sim_outcomes_CC.pathsOfCohortAveBMI)):
        bmis_cc = sim_outcomes_CC.pathsOfCohortAveBMI[cohortID].get_values()
        bmis_bb = sim_outcomes_BB.pathsOfCohortAveBMI[cohortID].get_values()
        diff_yearly_ave_bmis.append(numpy.array(bmis_cc) - numpy.array(bmis_bb))

    # to produce figure
    # rct data: treatment effect at 6 mo, year 1, and 2
    bb_ys = [3.0, 3.7, 2.8]
    lower_bounds = [1, 1.1, 1.2]
    upper_bounds = [1, 1.1, 1.2]

    f, ax = plt.subplots(figsize=(5, 4))

    # simulates trajectories
    for ys in diff_yearly_ave_bmis:
        ax.plot(range(len(ys)), ys, color='plum', alpha=0.5, label='Model', zorder=1)

    # bright bodies data
    ax.scatter([.5, 1, 2], bb_ys, color='purple', label='RCT', zorder=2)
    ax.errorbar([.5, 1, 2], bb_ys, yerr=[lower_bounds, upper_bounds],
                fmt='none', capsize=4, ecolor='purple', elinewidth=2, zorder=2)

    ax.set_title('Effectiveness of the Bright Bodies Intervention'
                 '\nAssuming Gradual Decay of Intervention Effect')
    ax.set_xlim((-0.5, 10.5))
    ax.set_xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    ax.set_yticks([0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0])
    ax.set_xlabel('Simulation Time (Years)')
    ax.set_ylabel('Reduction in BMI (kg/m'+r"$^2$"+')')

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1][:2], labels[::-1][:2], loc='upper right')

    if maintenance_effect == I.EffectMaintenance.FULL:
        plt.savefig("figures/bbEffFullMaint.png", dpi=300)
    elif maintenance_effect == I.EffectMaintenance.DEPREC:
        plt.savefig("figures/bbEffDeprecMaint.png", dpi=300)
    elif maintenance_effect == I.EffectMaintenance.NONE:
        plt.savefig("figures/bbEffNoMaint.png", dpi=300)
    plt.show()


def plot_sets_of_sample_paths(sets_of_sample_paths,
                              title=None, x_label=None, y_label=None,
                              x_range=None, y_range=None,
                              figure_size=None, output_type='show',
                              legends=None, transparency=1, color_codes=None, connect='step',
                              x_points=None, y_points_bb=None, y_points_cc=None,
                              ci_lower_values_bb=None, ci_upper_values_bb=None,
                              ci_lower_values_cc=None, ci_upper_values_cc=None):
    """ graphs multiple sample paths
    :param sets_of_sample_paths: (list) of list of sample paths
    :param title: (string) title of the figure
    :param x_label: (string) x-axis label
    :param y_label: (string) y-axis label
    :param x_range: (list) [x_min, x_max]
    :param y_range: (list) [y_min, y_max]
    :param figure_size: (tuple) figure size
    :param output_type: select from 'show', 'pdf' or 'png'
    :param legends: (list of strings) for legends
    :param transparency: float (0.0 transparent through 1.0 opaque)
    :param color_codes: (list of strings) color code of sample path sets
            e.g. 'b' blue 'g' green 'r' red 'c' cyan 'm' magenta 'y' yellow 'k' black
    :param connect: (string) set to 'step' to produce an step graph and to 'line' to produce a line graph
    """

    if len(sets_of_sample_paths) == 1:
        raise ValueError('Only one set of sample paths is provided. Use plot_sample_paths instead.')

    # FOR BMI GRAPH
    lines_bb = []
    lines_cc = []

    for i in range(len(x_points)):
        pairs_bb = [(x_points[i], ci_lower_values_bb[i]), (x_points[i], ci_upper_values_bb[i])]
        lines_bb.append(pairs_bb)
        pairs_cc = [(x_points[i], ci_lower_values_cc[i]), (x_points[i], ci_upper_values_cc[i])]
        lines_cc.append(pairs_cc)
    linecoll_bb = matcoll.LineCollection(lines_bb)
    linecoll_cc = matcoll.LineCollection(lines_cc)

    fig, ax = plt.subplots(figsize=figure_size)
    ax.set_title(title)  # title
    ax.set_xlabel(x_label)  # x-axis label
    ax.set_ylabel(y_label)  # y-axis label
    if x_range is not None:
        ax.set_xlim(x_range)
    if y_range is not None:
        ax.set_ylim(y_range)

    # cc: blue
    ax.scatter(x_points, y_points_cc, color='orange', marker="o", label='RCT: Clinical Control')
    ax.scatter(x_points, ci_lower_values_cc, color='orange', marker="_")
    ax.scatter(x_points, ci_upper_values_cc, color='orange', marker="_")

    # bb: green
    ax.scatter(x_points, y_points_bb, color='blue', marker="o", label='RCT: Bright Bodies')
    ax.scatter(x_points, ci_lower_values_bb, color='blue', marker="_")
    ax.scatter(x_points, ci_upper_values_bb, color='blue', marker="_")

    # generate lines
    ax.add_collection(linecoll_bb)
    ax.add_collection(linecoll_cc)
    ax.legend(loc='best')
    # add all sample paths
    Path.add_sets_of_sample_paths_to_ax(sets_of_sample_paths=sets_of_sample_paths,
                                        ax=ax,
                                        color_codes=color_codes,
                                        legends=legends,
                                        transparency=transparency,
                                        connect=connect)

    # set the minimum of y-axis to zero
    ax.set_ylim(bottom=0)  # the minimum has to be set after plotting the values
    # output figure
    if output_type == 'show':
        fig.show()
    else:
        Fig.output_figure(fig, output_type)


def plot_time_to_cost_savings(sim_outcomes_BB, sim_outcomes_CC):

    # list (array) of cost of BB each year for each cohort
    total_cost_by_year_bb = numpy.array(sim_outcomes_BB.costSavings)
    # average of each element over all the lists (ex. average first element of all lists, add to new list)
    average_cost_by_year_bb = (total_cost_by_year_bb.mean(axis=0))
    print(average_cost_by_year_bb)

    # list (array) of cost of BB each year for each cohort
    total_cost_by_year_cc = numpy.array(sim_outcomes_CC.costSavings)
    # average of each element over all the lists (ex. average first element of all lists, add to new list)
    average_cost_by_year_cc = (total_cost_by_year_cc.mean(axis=0))
    print(average_cost_by_year_cc)

    difference_average_cost_by_year = average_cost_by_year_bb - average_cost_by_year_cc
    print(difference_average_cost_by_year)

    # FIGURE: Years until BB Cost-Saving
    x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    y = difference_average_cost_by_year

    f, ax = plt.subplots()

    ax.plot(x, y, linewidth=6, color='fuchsia')
    ax.set_title('Average Time to Cost-Savings of BB Cohorts relative to CC Cohorts: \n'
                 'Difference in Cumulative Cost by Simulation Year')
    ax.set_xlabel('Simulation Years')
    ax.set_ylabel('Difference in Total Discounted Cost by Year ($)')

    ax.set_xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    single_cohort_difference_avg_cost_by_year = []
    for cohort in range(len(sim_outcomes_BB.costSavings)):
        cumulative_cost_bb = numpy.array(sim_outcomes_BB.costSavings[cohort])
        cumulative_cost_cc = numpy.array(sim_outcomes_CC.costSavings[cohort])
        difference_avg_cost_by_year = cumulative_cost_bb - cumulative_cost_cc
        single_cohort_difference_avg_cost_by_year.append(difference_avg_cost_by_year)
        plt.plot(x, single_cohort_difference_avg_cost_by_year[cohort], alpha=0.05, c='purple')

    ax.legend(['Average'])

    colors = ["fuchsia", "purple"]
    texts = ["Average", "Individual Cohorts"]
    patches = [mpatches.Patch(color=colors[i], label="{:s}".format(texts[i])) for i in range(len(texts))]
    plt.legend(handles=patches, loc='lower left', ncol=2)

    plt.axhline(color='black')
    plt.show()

    plt.savefig("figures/TimeToCostSavings.png", dpi=300)

