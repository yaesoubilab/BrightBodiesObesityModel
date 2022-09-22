import bright_bodies_support.CEA as CEA
import bright_bodies_support.Inputs as I
import bright_bodies_support.Plots as P
import deampy.plots.sample_paths as Path
from bright_bodies_support.ParameterGenerator import ParamGenerator
from yom import MultiCohortClasses as MultiCls

# SIMULATE BOTH INTERVENTIONS AND PRINT COMPARATIVE OUTCOMES

# *** Alter maintenance scenarios via MAINTENANCE_EFFECT.
RUN_IN_PARALLEL = True

# color codes
COLOR_CC = 'coral'
COLOR_BB = 'royalblue'
COLOR_MODEL = 'plum'
COLOR_DATA = 'purple'


# this line is needed to avoid errors that occur on Windows computers when running the model in parallel
def compare(scenario):
    """
    :param scenario: effect maintenance scenario
    """

    # change the working directory to the root directory
    # os.chdir('../')

    # create an instance of the model inputs
    inputs = I.ModelInputs()

    # for MultiCohort BRIGHT BODIES
    multiCohortBB = MultiCls.MultiCohort(
        ids=range(inputs.nCohorts),
        parameter_generator=ParamGenerator(
            intervention=I.Interventions.BRIGHT_BODIES,
            maintenance_scenario=scenario,
            model_inputs=inputs)
    )
    # simulate these cohorts (BB)
    multiCohortBB.simulate(sim_duration=inputs.simDuration,
                           if_run_in_parallel=RUN_IN_PARALLEL)

    # for MultiCohort CLINICAL CONTROL
    multiCohortCC = MultiCls.MultiCohort(
        ids=range(inputs.nCohorts),
        parameter_generator=ParamGenerator(
            intervention=I.Interventions.CONTROL,
            maintenance_scenario=scenario,
            model_inputs=inputs)
    )
    # simulate these cohorts (CC)
    multiCohortCC.simulate(sim_duration=inputs.simDuration,
                           if_run_in_parallel=RUN_IN_PARALLEL)

    # -------- FIGURES  ----------

    Path.plot_sets_of_sample_paths(
        sets_of_sample_paths=[multiCohortCC.multiSimOutputs.pathsOfCohortAveBMI,
                              multiCohortBB.multiSimOutputs.pathsOfCohortAveBMI],
        title='Average BMIs of Simulated Cohorts'
              '\nAssuming Gradual Decay of Intervention Effect',
        y_range=[0, 40],
        x_label='Simulation Time (Year)',
        y_label='Average BMI (kg/m'+r"$^2$"+') per Person-Year',
        legends=['Clinical Control', 'Bright Bodies'],
        connect='line',
        color_codes=[COLOR_CC, COLOR_BB],
        transparency=0.5,
        figure_size=(5.5, 4.5),
        file_name='outputs/figs/bmiTrajectories-{}.png'.format(scenario.name)
    )

    P.plot_bb_effect(sim_outcomes_BB=multiCohortBB.multiSimOutputs,
                     sim_outcomes_CC=multiCohortCC.multiSimOutputs,
                     maintenance_effect=scenario,
                     color_model=COLOR_MODEL,
                     color_data=COLOR_DATA)

    P.plot_yearly_change_in_bmi(sim_outcomes_control=multiCohortCC.multiSimOutputs,
                                sim_outcomes_bb=multiCohortBB.multiSimOutputs,
                                maintenance_effect=scenario,
                                color_model=COLOR_MODEL,
                                color_data=COLOR_DATA
                                )

    # report cost-effectiveness bright_bodies_analysis
    CEA.report_CEA(sim_outcomes_BB=multiCohortBB.multiSimOutputs,
                   sim_outcomes_CC=multiCohortCC.multiSimOutputs,
                   maintenance_effect=scenario,
                   color_bb=COLOR_BB, color_cc=COLOR_CC)

    # COMPARATIVE: average BMIs over 10 years
    P.plot_sets_of_sample_paths(
        sets_of_sample_paths=[multiCohortCC.multiSimOutputs.pathsOfCohortAveBMI,
                              multiCohortBB.multiSimOutputs.pathsOfCohortAveBMI],
        title='Cohort Average BMIs over 10 Years',
        y_range=[0, 40],
        x_label='Simulation Year',
        y_label='Average BMI (kg/m'+r"$^2$"+')',
        legends=['Model: Clinical Control', 'Model: Bright Bodies'],
        connect='line',
        color_codes=[COLOR_CC, COLOR_BB],
        transparency=0.5,
        x_points=[0.0, 0.5, 1, 2],
        y_points_bb=[35.7, 33.6, 33.9, 34.8],
        y_points_cc=[36.2, 37.1, 38.1, 38.1],
        ci_lower_values_bb=[0, 33, 33.3, 34],
        ci_upper_values_bb=[0, 34.2, 34.6, 35.6],
        ci_lower_values_cc=[0, 36.3, 37.3, 37.1],
        ci_upper_values_cc=[0, 37.9, 39, 39.1],
        file_name='outputs/figs/bmiTrajectoriesUnadjusted-{}.png'.format(scenario)
    )

    # -------- OUTCOMES  ----------

    CEA.report_HC_savings(sim_outcomes_BB=multiCohortBB.multiSimOutputs,
                          sim_outcomes_CC=multiCohortCC.multiSimOutputs,
                          pop_size=inputs.popSize,
                          maintenance_effect=scenario,)

    CEA.report_incremental_cost_effect_savings(sim_outcomes_BB=multiCohortBB.multiSimOutputs,
                                               sim_outcomes_CC=multiCohortCC.multiSimOutputs,
                                               maintenance_effect=scenario,)

    P.plot_time_to_cost_savings(sim_outcomes_BB=multiCohortBB.multiSimOutputs,
                                sim_outcomes_CC=multiCohortCC.multiSimOutputs,
                                maintenance_effect=scenario,
                                color=COLOR_DATA,
                                figure_size=(6, 5))

    CEA.report_time_to_cost_savings(sim_outcomes_BB=multiCohortBB.multiSimOutputs,
                                    sim_outcomes_CC=multiCohortCC.multiSimOutputs,
                                    maintenance_effect=scenario,)


if __name__ == '__main__':

    compare(scenario=I.EffectMaintenance.DEPREC)
    compare(scenario=I.EffectMaintenance.NONE)
    compare(scenario=I.EffectMaintenance.FULL)
