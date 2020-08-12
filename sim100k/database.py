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
array_ratioTD = np.linspace(2,5,2)
array_ratioHT = np.linspace(1,1.5,2)
array_ratioTC = np.linspace(2,5,2)
array_ratioDW = np.linspace(3,6,2)

# Create array for the impeller velocity (omega)
Reynolds = np.logspace(0,2,2)

# Constants
theta = 0.785398163
p_thick = 0.1

# First geometry parameter of the loop
first = len(array_ratioTD)                                      # Fragmentation

path = os.getcwd()

total = (len(array_ratioTD)*
         len(array_ratioHT)*
         len(array_ratioTC)*
         len(array_ratioDW)* 1)                                 # Hub

# Start and stop segment for fragmentation
print ("First adimensional geometry is TD")                     # Fragmentation
print ("Size of the first adimensional geometry =", first)
print ("Total of possible folders =", total)
print ("Set the start segment :")
start = int(input())
print ("Set the stop segment :")
stop = int(input())
print ("Number of folders =", (stop-start+1)*total/first)

start_number = (start-1)*total/first+1
stop_number = stop*total/first

number = start_number
for rTD in array_ratioTD[start-1:stop]:                         # Fragmentation
    for rTC in array_ratioTC:
        for rDW in array_ratioDW:
            rDW_Hub = 0.75*rDW                                  # Hub
            for rHT in array_ratioHT:
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
                                                theta = theta,
                                                p_thick = p_thick,
                                                mesh_length = "{{mesh_length}}")
                fic_geo.close()

                # Create the folder of the geometry
                path_number = str(int(number))
                newPath = path + "/mixer_" + path_number
                os.mkdir(newPath)
                os.system('cp mixer.prm ' + newPath)
                os.chdir(newPath)

                # Write the geometry file and the parameter file
                wr_geo = open("mixer.geo","w")
                wr_geo.write(geometries)
                wr_geo.close()

                i = 1
                for Re in Reynolds:
                    # Open the parameter file
                    fic_prm = open("mixer.prm","r")
                    cte_prm = fic_prm.read()
                    # Insert the parameters
                    template_prm = Template(cte_prm)
                    if i == 1:
                        parameters = template_prm.render(restart = False,
                                                         restart_filename = "restart",
                                                         viscosity = (1/rTD)**2/Re)
                    else:
                        parameters = template_prm.render(restart = True,
                                                         restart_filename = "restart",
                                                         viscosity = (1/rTD)**2/Re)
                    fic_prm.close()

                    # Create the folder of the viscosity
                    newPath_Re = newPath + "/mixer_" + str(int(i))
                    os.mkdir(newPath_Re)
                    os.chdir(newPath_Re)

                    # Write the prm file
                    wr_prm = open("mixer.prm","w")
                    wr_prm.write(parameters)
                    wr_prm.close()

                    # Write the tag file
                    fic_tag = open("mixer.txt","w")
                    fic_tag.write("T/D\t%f\t" % rTD)
                    fic_tag.write("H/T\t%f\t" % rHT)
                    fic_tag.write("T/C\t%f\t" % rTC)
                    fic_tag.write("D/W\t%f\t" % rDW)
                    fic_tag.write("D/W_Hub\t%f\t" % rDW_Hub)
                    fic_tag.write("E\t%f\t" % p_thick)
                    fic_tag.write("theta\t%f\t" % theta)
                    fic_tag.write("Re\t%f\t" % Re)

                    i = i + 1

                    os.chdir("../")

                os.chdir("../")

                if number == stop_number:
                    break
                else:
                    number = number+1