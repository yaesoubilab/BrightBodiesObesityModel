import matplotlib.pyplot as plt
import numpy

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
        ax.set_title('\nControl')
        ax.text(-0.05, 1.025, 'A)', transform=ax.transAxes, size=11, weight='bold')

    # adding RCT data
    ax.scatter([1, 2], ys, color='orange', label="RCT Average Difference in BMI")
    # adding error bars
    ax.errorbar([1, 2], ys, yerr=(lbs, ubs), fmt='none', capsize=4, ecolor='orange')

    # adding simulation outcomes
    for this_y in year_one_vs_zero:
        ax.scatter(1, this_y, color='blue', marker='_', s=200, alpha=0.25)
    for this_y in year_two_vs_one:
        ax.scatter(2, this_y, color='blue', marker='_', s=200, alpha=0.25)

    ax.axhline(y=0, color='k', ls='--', linewidth=0.5)

    ax.set_xlim((0.5, 2.5))
    ax.set_xticks([1, 2])
    ax.set_xticklabels(['Year 1 to 0', 'Year 2 to 1'])
    ax.set_ylim((-3.5, 3.5))
    if intervention == I.Interventions.CONTROL:
        ax.set_ylabel('Difference in BMI (kg/m^2)')
    else:
        ax.set_ylabel(' ')

    ax.legend(['RCT', 'Model'], loc='upper right')


def plot_validation(sim_outcomes_control, sim_outcomes_bb):
    """ generates validation graphs: BMI differences by year """

    # plot
    f, axes = plt.subplots(1, 2, figsize=(7, 4), sharey=True)

    f.suptitle('Differences in Average BMI by Year')
    add_yearly_change_in_bmi_to_ax(ax=axes[0], sim_outcomes=sim_outcomes_control,
                                   intervention=I.Interventions.CONTROL)
    add_yearly_change_in_bmi_to_ax(ax=axes[1], sim_outcomes=sim_outcomes_bb,
                                   intervention=I.Interventions.BRIGHT_BODIES)

    f.subplots_adjust(hspace=2, wspace=2)
    # f.tight_layout()

    # bbox_inches set to tight: cleans up figures
    plt.savefig("figures/RCT_validation.png", dpi=300)
    plt.show()


def plot_diff_in_mean_bmi(sim_outcomes_BB, sim_outcomes_CC, maintenance_effect):
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

    f, ax = plt.subplots()

    # simulates trajectories
    for ys in diff_yearly_ave_bmis:
        ax.plot(range(len(ys)), ys, color='blue', alpha=0.2, label='Model')

    # bright bodies data
    ax.scatter([.5, 1, 2], bb_ys, color='orange', label='Bright Bodies RCT')
    ax.errorbar([.5, 1, 2], bb_ys, yerr=[lower_bounds, upper_bounds],
                fmt='none', capsize=4, ecolor='orange', elinewidth=2)

    ax.set_title('Treatment Effect: Difference in Average BMI')
    ax.set_xlim((0.0, 10.5))
    ax.set_xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    ax.set_yticks([0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0])
    ax.set_xlabel('Simulation Time (Years)')
    ax.set_ylabel('Difference in BMI (kg/m^2)')

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1][:2], labels[::-1][:2], loc='upper right')

    if maintenance_effect == I.EffectMaintenance.FULL:
        plt.savefig("figures/Avg_BMI_Full_Maintenance.png", dpi=300)
    elif maintenance_effect == I.EffectMaintenance.DEPREC:
        plt.savefig("figures/Avg_BMI_Deprec_Maintenance.png", dpi=300)
    elif maintenance_effect == I.EffectMaintenance.NONE:
        plt.savefig("figures/Avg_BMI_No_Maintenance.png", dpi=300)
    plt.show()
