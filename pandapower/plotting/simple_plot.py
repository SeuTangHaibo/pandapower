# -*- coding: utf-8 -*-

# Copyright (c) 2016 by University of Kassel and Fraunhofer Institute for Wind Energy and Energy
# System Technology (IWES), Kassel. All rights reserved. Use of this source code is governed by a 
# BSD-style license that can be found in the LICENSE file.

import matplotlib.pyplot as plt
from pandapower.plotting.collections import create_bus_collection, create_line_collection, \
                                            create_trafo_collection, draw_collections
from pandapower.plotting.generic_geodata import create_generic_coordinates
try:
    import pplog as logging
except:
    import logging

try:
    import seaborn
    colors = seaborn.color_palette()
except:
    colors = ["b", "g", "r", "c", "y"]

logger = logging.getLogger(__name__)


def simple_plot(net=None, respect_switches=False, line_width=1.0, bus_size=1.0, ext_grid_size=1.0,
                bus_color=colors[0], line_color='grey', trafo_color='g', ext_grid_color='y'):
    """
        Plots a pandapower network as simple as possible. If no geodata is available, artificial geodata is generated. For advanced plotting see the tutorial

        INPUT:
            **net** - The pandapower format network. If none is provided, mv_oberrhein() will be plotted as an example

        Optional:

            **respect_switches** (bool, False) - Respect switches when artificial geodata is created

            **line_width** (float, 1.0) - width of lines

            **bus_size** (float, 1.0) - Relative size of buses to plot.

                The value bus_size is multiplied with mean_distance_between_buses, which equals the distance between
                the max geoocord and the min divided by 200.
                mean_distance_between_buses = sum((net['bus_geodata'].max() - net['bus_geodata'].min()) / 200)

            **ext_grid_size** (float, 1.0) - Relative size of ext_grids to plot.

                See bus sizes for details. Note: ext_grids are plottet as rectangles

            **bus_color** (String, colors[0]) - Bus Color. Init as first value of color palette. Usually colors[0] = "b".

            **line_color** (String, 'grey') - Line Color. Init is grey

            **trafo_color** (String, 'g') - Trafo Color. Init is green

            **ext_grid_color** (String, 'y') - External Grid Color. Init is yellow

        """
    if net is None:
        import pandapower.networks as nw
        logger.warning("No Pandapower network provided -> Plotting mv_oberrhein")
        net = nw.mv_oberrhein()

    # create geocoord if none are available
    if len(net.line_geodata) == 0 and len(net.bus_geodata) == 0:
        logger.warning("No or insufficient geodata available --> Creating artificial coordinates." +
                       " This may take some time")
        create_generic_coordinates(net, respect_switches=respect_switches)

    if bus_size or ext_grid_size is None:
        # if either bus_size or ext_grid size is None -> calc size from distance between min and
        # max geocoord
        mean_distance_between_buses = sum((net['bus_geodata'].max() - net[
            'bus_geodata'].min()) / 200)
        # set the bus / ext_grid sizes accordingly
        # Comment: This is implemented because if you would choose a fixed values
        # (e.g. bus_size = 0.2), the size
        # could be to small for large networks and vice versa
        bus_size *= mean_distance_between_buses
        ext_grid_size *= mean_distance_between_buses * 1.5

    # if bus geodata is available, but no line geodata
    use_line_geodata = False if len(net.line_geodata) == 0 else True

    # create bus collections ti plot
    bc = create_bus_collection(net, net.bus.index, size=bus_size, color=bus_color, zorder=10)
    lc = create_line_collection(net, net.line.index, color=line_color, linewidths=line_width,
                                     use_line_geodata=use_line_geodata)
    sc = create_bus_collection(net, net.ext_grid.bus.values, patch_type="rect",
                                    size=ext_grid_size, color=ext_grid_color, zorder=11)
    # create trafo collection if trafo is available
    tc = create_trafo_collection(net, net.trafo.index, color=trafo_color) if len(net.trafo) else None

    draw_collections([lc, bc, tc, sc])
    plt.show()

if __name__ == "__main__":
    simple_plot()
