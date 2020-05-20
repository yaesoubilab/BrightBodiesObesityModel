import matplotlib.pyplot as plt
import numpy as np
from SimPy.SamplePathClasses import *
import SimPy.Plots.FigSupport as Fig
from matplotlib import collections as matcoll


def plot_sample_path(sample_path,
                     title=None, x_label=None, y_label=None,
                     figure_size=None, output_type='show',
                     legend=None, color_code=None, connect='step'):
    """
    plot a sample path
    :param sample_path: a sample path
    :param title: (string) title of the figure
    :param x_label: (string) x-axis label
    :param y_label: (string) y-axis label
    :param figure_size: (tuple) figure size
    :param output_type: select from 'show', 'pdf' or 'png'
    :param legend: (string) the legend
    :param color_code: (string) for example: 'b' blue 'g' green 'r' red 'c' cyan 'm' magenta 'y' yellow 'k' black
    :param connect: (string) set to 'step' to produce an step graph and to 'line' to produce a line graph
    """

    if not (isinstance(sample_path, IncidenceSamplePath) or isinstance(sample_path, PrevalenceSamplePath)):
        raise ValueError(
            'sample_path should be an instance of PrevalenceSamplePath or PrevalencePathBatchUpdate.')

    fig, ax = plt.subplots(figsize=figure_size)
    ax.set_title(title)  # title
    ax.set_xlabel(x_label)  # x-axis label
    ax.set_ylabel(y_label)  # y-axis label

    # add a sample path to this ax
    add_sample_path_to_ax(sample_path=sample_path,
                          ax=ax,
                          color_code=color_code,
                          legend=legend,
                          connect=connect)
    ax.set_ylim(bottom=0)  # the minimum has to be set after plotting the values

    if isinstance(sample_path, PrevalenceSamplePath):
        ax.set_xlim(left=0)
    elif isinstance(sample_path, IncidenceSamplePath):
        ax.set_xlim(left=0.5)

    # output figure
    Fig.output_figure(fig, output_type, title)


def plot_sample_paths(sample_paths,
                      title=None, x_label=None, y_label=None,
                      x_range=None, y_range=None,
                      figure_size=None, output_type='show',
                      legends=None, transparency=1, common_color_code=None, connect='step'):
    """ graphs multiple sample paths
    :param sample_paths: a list of sample paths
    :param title: (string) title of the figure
    :param x_label: (string) x-axis label
    :param y_label: (string) y-axis label
    :param x_range: (list) [x_min, x_max]
    :param y_range: (list) [y_min, y_max]
    :param figure_size: (tuple) figure size
    :param output_type: select from 'show', 'pdf' or 'png'
    :param legends: (list) of strings for legend
    :param transparency: (float) 0.0 transparent through 1.0 opaque
    :param common_color_code: (string) color code if all sample paths should have the same color
        'b'	blue 'g' green 'r' red 'c' cyan 'm' magenta 'y' yellow 'k' black
    :param connect: (string) set to 'step' to produce an step graph and to 'line' to produce a line graph
    """

    if len(sample_paths) == 1:
        raise ValueError('Only one sample path is provided. Use graph_sample_path instead.')

    fig, ax = plt.subplots(figsize=figure_size)
    ax.set_title(title)  # title
    ax.set_xlabel(x_label)  # x-axis label
    ax.set_ylabel(y_label)  # y-axis label
    if x_range is not None:
        ax.set_xlim(x_range)
    if y_range is not None:
        ax.set_ylim(y_range)

    # add all sample paths
    add_sample_paths_to_ax(sample_paths=sample_paths,
                           ax=ax,
                           common_color_code=common_color_code,
                           transparency=transparency,
                           connect=connect)

    # add legend if provided
    if legends is not None:
        if common_color_code is None:
            ax.legend(legends)
        else:
            ax.legend([legends])

    # set the minimum of y-axis to zero
    ax.set_ylim(bottom=0)  # the minimum has to be set after plotting the values
    # output figure
    Fig.output_figure(fig, output_type, title)


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
        raise ValueError('Only one set of sample paths is provided. Use graph_sample_paths instead.')

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
    add_sets_of_sample_paths_to_ax(sets_of_sample_paths=sets_of_sample_paths,
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


def add_sample_path_to_ax(sample_path, ax, color_code=None, legend=None, transparency=1, connect='step'):

    # x and y values
    if isinstance(sample_path, PrevalenceSamplePath):
        x_values = sample_path.get_times()
    elif isinstance(sample_path, IncidenceSamplePath):
        x_values = sample_path.get_period_numbers()

    y_values = sample_path.get_values()

    # plot the sample path
    if connect == 'step':
        ax.step(x=x_values, y=y_values, where='post', color=color_code, label=legend, alpha=transparency)
    else:
        ax.plot(x_values, y_values, color=color_code, label=legend, alpha=transparency)

    # add legend if provided
    if legend is not None:
        ax.legend()


def add_sample_paths_to_ax(sample_paths, ax, common_color_code, transparency, connect):

    # add every path
    for path in sample_paths:
        add_sample_path_to_ax(sample_path=path,
                              ax=ax,
                              color_code=common_color_code,
                              transparency=transparency,
                              connect=connect)


def add_sets_of_sample_paths_to_ax(sets_of_sample_paths, ax, color_codes, legends, transparency, connect):

    # add every path
    for i, sample_paths in enumerate(sets_of_sample_paths):
        for j, path in enumerate(sample_paths):
            if j == 0:
                legend = legends[i]
            else:
                legend = None
            add_sample_path_to_ax(sample_path=path,
                                  ax=ax,
                                  color_code=color_codes[i],
                                  legend=legend,
                                  transparency=transparency,
                                  connect=connect)

