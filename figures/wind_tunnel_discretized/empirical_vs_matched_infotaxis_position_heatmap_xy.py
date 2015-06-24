"""
Plot the position heatmaps projected onto the xy-plane for the discretized empirical trajectories.
"""
from __future__ import print_function, division

FIG_SIZE = (16, 6)

import matplotlib.pyplot as plt

from db_api import models
from db_api.connect import session

from config import *
from config.empirical_position_heatmap import *

row_labels = ('0.3 m/s', '0.4 m/s', '0.6 m/s')
col_labels = ('on', 'none', 'afterodor')

for sim_id_template in (SIMULATION_ID_EMPIRICAL, SIMULATION_ID_INFOTAXIS):
    fig, axs = plt.subplots(3, 3, facecolor='white', figsize=FIG_SIZE, tight_layout=True)

    for e_ctr, expt in enumerate(EXPERIMENTS):
        for o_ctr, odor_state in enumerate(ODOR_STATES):

            sim_id = sim_id_template.format(expt, odor_state)
            sim = session.query(models.Simulation).get(sim_id)

            sim.analysis_position_histogram.fetch_data(session)
            heatmap_xy = sim.analysis_position_histogram.xy

            print(heatmap_xy.sum())

            ax = axs[e_ctr, o_ctr]
            ax.matshow(heatmap_xy.T, origin='lower', extent=sim.env.extentxy)

            # labels
            if e_ctr == 2:
                ax.set_xlabel('x')

            if o_ctr == 0:
                ax.set_ylabel('y')

            ax.set_title('{} {}'.format(row_labels[e_ctr], col_labels[o_ctr]))

    if sim_id_template == SIMULATION_ID_EMPIRICAL:
        fig.suptitle('empirical')
    elif sim_id_template == SIMULATION_ID_INFOTAXIS:
        fig.suptitle('infotaxis')

plt.show(block=True)