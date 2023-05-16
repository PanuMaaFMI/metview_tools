# metview_tools
Personally coded visualization tools, which use metviews python-interface.
Can be used by any of my colleagues, who wish to visualize grib files.

For further understanding of the programs, please read the program source code.
They are not coded to be used as scripts (so not input required), but rather to be modified from the code itself due to large number of parameters.
Still, one can modify them as they please. Just create a personal branch.

Before running any of the .py files, one should make sure to have metview's python-interface installed.
Official instructions can be founded from here: https://metview.readthedocs.io/en/latest/install.html

For Atos users, these are the commands I run before every session:

mkdir -p /home/$USER/metview
cd /home/$USER/metview
module load conda
conda activate myenv
conda install metview -c conda-forge
conda install metview-python -c conda-forge
pip install metview
mkdir -p /ec/res4/scratch/$USER/tmpdir/
export TMPDIR=/ec/res4/scratch/$USER/tmpdir/
python3 -m metview selfcheck
pip install display



I hope you find these programs usefull in your research,

Panu Maalampi
Research Assistant
Finnish Meteorological Institute

Metview licence terms:
# (C) Copyright 2017- ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
#
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
