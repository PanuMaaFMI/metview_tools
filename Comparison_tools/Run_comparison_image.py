# (C) Copyright 2017- ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
#
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#
# Contributors:
# 2023-05-16 Panu Maalampi
#

import metview as mv

#-------------------------------------------------------------------

#CHECK THE FOLLOWING CONFIGURATIONS

# Read the input from the following two grib files

# Give the model run in format YYYYMMDDHH+0HH
select_run="2022032200+012"

#First file
folder_a = "/perm/fibf/hm_home/Gradu/46h1ron_sumuet2/"
file_a   = "fc" + select_run + "grib"

# Don't touch
path_a   = folder_a + file_a

# Second file
folder_b = "/perm/fibf/hm_home/Gradu/46h1ron_mcsumuen/"
file_b   = "fc" + select_run + "grib2_fp"

# Don't touch
path_b   = folder_b + file_b

# Don't touch
if mv.exist(path_a):
    a = mv.read(source=path_a)
else:
    print("Could not find file " + file_a)
    exit()

# Don't touch
if mv.exist(path_b):
    b = mv.read(source=path_b)
else:
    print("Could not find file " + file_b)
    exit()

# Select corners for the figure (degrees).
# It should be same size or bigger than the previous one.
# [S, W, N, E]
view_area = [50, 5, 70, 50]

# Selecting variables: One should either use variable names, as they appear in the output of grib_ls,
# or variable id, as they appear in parameter database! URL: https://codes.ecmwf.int/grib/param-db/
# It is important that the method, which is not used, should be commented out from the var_x=x.select(...) part!
# Note that when comparing different grib files, with different versions,
# they might have different level types (model or pressure), which causes errors in definitions.
# Best way to circle this is to make different elements for different files
# e.g. variable_a=xxx and variable_b=yyy etc.

# Select variable by name
variable_name = "clwc"

# Select variable by id
variable_id   = 246

# Select the level from which the variable will be found.
level=[65]

# Choose proper level type as they appear in output of grib_ls
# "hybrid"/"heightAboveGround"/"heightAboveSea"/"nominalTop"/"entireAtmosphere"
level_type = "hybrid"

# Time step
step=[12]

# Remember to comment out unused parameters
var_a=a.select(#paramId=variable_id,
               shortName=variable_name,
               #typeOfLevel=level_type,
               levelist=level,
               step=step)

var_b=b.select(#paramId=variable_id,
               shortName=variable_name,
               #typeOfLevel=level_type,
               levelist=level,
               step=step)

# Determine folder where the figure will be stored.
# In addition name the file and choose a format (pdf or png)
folder_output = "/home/fibf/visualization/"
file_output   = variable_name + "_" + str(level[0]) + "_" +  select_run
path_output   = folder_output + file_output

# Select output format ("png" or "pdf").
output_format = "pdf"

#Give title to the figures (A=left and B=right).
a_name = "Cy46h1-dev with tegen"
b_name = "Cy46h1-dev with n.r.t."

# Determine contouring for the figures. 
# Removing comments from contour_level_selection and contour_level_list
# allows you to manually determine the intervals. Otherwise it is automatic.
var_shade = mv.mcont(
    legend="on",
    #contour level type is either "count", "interval" or "level_list"
    contour_level_selection_type="level_list",
    #contour_level_list=[-5e6,-2.5e6,-1e6,-7.5e5,-5e5,-2.5e5,-1e5,0,1e5,2.5e5,5e5,7.5e5],
    #contour_level_list=[1e-6,1e-5,1e-4,1e-3,1e-2],
    #contour_level_list=[-150,-125,-100,-75,-50,-25,0,25,50],
    contour_shade="ON",
    contour_shade_method="AREA_FILL",
    contour_shade_colour_method="CALCULATE",
    contour_shade_colour_direction="CLOCKWISE",
    contour_shade_max_level_colour="RED",
    contour_shade_min_level_colour="BLUE",
    contour_line_colour="GREY",
    contour_line_thickness=2,
    contour_highlight="OFF",
    contour_label="OFF",
)

# Everything should be ready! Run with python3 (assuming one has metview installed).
# More info about the installation can be found from metview_tools/README.md
#--------------------------------------------------------------------

unit_a = mv.grib_get_string(var_a[0], "units")
unit_b = mv.grib_get_string(var_b[0], "units")

legend_a = mv.mlegend(
    legend_automatic_position="right",
    legend_text_font_size=0.5,
    legend_title="on",
    legend_title_text=unit_a,
    legend_title_position="top"
)

legend_b = mv.mlegend(
    legend_automatic_position="right",
    legend_text_font_size=0.5,
    legend_title="on",
    legend_title_text=unit_b,
    legend_title_position="top"
)

# define coastlines
coast = mv.mcoast(
    map_coastline_resolution="medium",
    map_coastline_land_shade="on",
    map_coastline_land_shade_colour="RGB(0.9448,0.8819,0.765)",
    map_boundaries="on",
    map_boundaries_colour="charcoal",
    map_grid_line_style="dash",
    map_grid_latitude_increment=5,
    map_grid_longitude_increment=10
)

# define geographical view
view = mv.geoview(map_projection="lambert",
                  map_area_definition="corners",
                  area=view_area,
                  coastlines=coast)
pages = mv.mvl_regular_layout(view, 2, 1, 1, 1, [20, 100, 0, 100])

title_view = mv.annotationview()
title_page = mv.plot_page(top=0, bottom=100, left=0, right=100, view=title_view)
pages.append(title_page)

# width of and A4 landscape page in cm
pw = 29.7

bdate = mv.base_date(var_a[0])
step  = mv.grib_get_long(var_a[0], "step")
shared_title = mv.mtext(
    text_lines=[
        "Comparison of parameter '" + variable_name + "' (level=" + str(level[0]) + ") in two model versions",
        "{} (+{}h)".format(bdate.strftime('%Y-%m-%d %H UTC'), int(step)),
    ],
    text_font_size=0.8,
    text_mode="positional",
    text_box_x_position=pw / 2 - 20 / 2,
    text_box_y_position=19,
    text_box_x_length=20,
    text_box_y_length=2
)

# define titles
title_left  = mv.mtext(text_lines=[a_name, ""], text_font_size=0.8)
title_right = mv.mtext(text_lines=[b_name, ""], text_font_size=0.8)

# define layout
dw = mv.plot_superpage(page=pages)

# define the output plot filename, format and outputlocation
if output_format=="png":
    mv.setoutput(mv.png_output(output_name=path_output))
elif output_format=="pdf":
    mv.setoutput(mv.pdf_output(output_name=path_output))
else:
    "Figure format not supported. Choose between png and pdf."
    exit()

# generate plot
d=[[dw[0], var_a, var_shade, legend_a, title_left],
   [dw[1], var_b, var_shade, legend_b, title_right],
   [dw[2], shared_title]]
mv.plot(d)
