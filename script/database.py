# ------------------------------------------------------------------------
# Script python permettant de générer une base de données :
# La base de données contient les maillages de différentes géométries et les
# paramètres physiques d'un mélangeur muni d'une turbine pitch blade.
# ______________
# Valérie Bibeau, Polytechnique Montréal, 2020

from jinja2 import Template
import os
import numpy as np

# Create arrays for every ratios of the mixer's geometry
array_ratioTD = np.linspace(2,5,10)
array_ratioHT = np.linspace(1,1.5,10)
array_ratioTC = np.linspace(2,5,10)
array_ratioDW = np.linspace(3,6,10)
array_ratioDW_Hub = np.linspace(3,6,10)

path = "/home/bibeauv/soft/lethe/database"

i = 1

for rTD in array_ratioTD :
    for rHT in array_ratioHT :
        for rTC in array_ratioTC :
            for rDW in array_ratioDW :
                for rDW_Hub in array_ratioDW_Hub :
                    if rDW_Hub <= rDW :
                        # Open the geometry file
                        fic_geo = open("mixer.geo","r")
                        cte_geo = fic_geo.read()
                        # Insert the geometry
                        template = Template(cte_geo)
                        geometries = template.render(ratioTD = rTD,
                                                     ratioHT = rHT,
                                                     ratioTC = rTC,
                                                     ratioDW = rDW,
                                                     ratioDW_Hub = rDW_Hub,
                                                     theta = 0.785398163,
                                                     p_thick = 0.1)
                        fic_geo.close()

                        # Open the parameter file
                        fic_prm = open("mixer.prm","r")
                        cte_prm = fic_prm.read()
                        # Insert the parameters
                        template_prm = Template(cte_prm)
                        parameters = template.render(omega = 6.283185307)
                        fic_prm.close()

                        # Create the folder where the simulation will launch
                        path_number = str(i)
                        newPath = path + "/mixer_" + path_number
                        os.mkdir(newPath)
                        os.chdir(newPath)
                        # Write the geometry file and the parameter file
                        wr_geo = open("mixer.geo","w")
                        geo_file = wr_geo.write(geometries)
                        wr_geo.close()

                        wr_prm = open("mixer.prm","w")
                        prm_file = wr_prm.write(parameters)
                        wr_prm.close()

                        # Generate the mesh
                        os.system('gmsh -3 mixer.geo')
                        # Launch of Lethe
                        # os.system('../../build/applications/gls_navier_stokes_3d/gls_navier_stokes_3d mixer.prm')

                        os.chdir("../")
                        i = i+1
