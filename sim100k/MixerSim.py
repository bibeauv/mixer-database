from jinja2 import Template
import os
import numpy as np
import sys
import math
from subprocess import Popen, PIPE
import warnings
warnings.filterwarnings("error")

# ----------------------------------------------------------------------------
# Fonctions python permettant le lancement des simulations des mélangeurs
# - generate_data_folders
# - launch_gmsh
# - launch_job
# - get_torque_and_write_data
# ______________
# Valérie Bibeau, Polytechnique Montréal, 2020

def generate_data_folders(TD, HT, TC, DW, WHub, E, theta, Re, start, stop, enable):
    """
    Generate the folders of the geometries

    Args:
        TD (list): min, max, len (geometric ratio)
        HT (list): min, max, len (geometric ratio)
        TC (list): min, max, len (geometric ratio)
        DW (list): min, max, len (geometric ratio)
        WHub (list): min, max, len (pourcentage of W for the Hub)
        E (list): min, max, len (pourcentage of W for the thickness of the blades)
        theta (list): min, max, len
        Re (list): min, max, len
        start (int): Start of the fregmentation
        stop (int): End of the fregmentation
        enable (bool): If true, the folders are generated
    """

    if enable == True:
        # Create arrays for every ratios of the mixer's geometry
        array_ratioTD = np.linspace(TD[0],TD[1],TD[2])
        array_ratioHT = np.linspace(HT[0],HT[1],HT[2])
        array_ratioTC = np.linspace(TC[0],TC[1],TC[2])
        array_ratioDW = np.linspace(DW[0],DW[1],DW[2])
        array_WHub = np.linspace(WHub[0],WHub[1],WHub[2])
        array_E = np.linspace(E[0],E[1],E[2])
        array_theta = np.linspace(theta[0],theta[1],theta[2])

        # Create array for the impeller velocity (omega)
        Reynolds = np.logspace(Re[0],Re[1],Re[2])

        # First geometry parameter of the loop
        first = len(array_ratioTD)
        if start > first:
            return print('Error: Start > First... Length of the first adimensional geometry is %d' % first)

        # Get current path
        path = os.getcwd()
        
        # Total of geometries' folders possible
        total = (len(array_ratioTD)*
                len(array_ratioHT)*
                len(array_ratioTC)*
                len(array_ratioDW)*
                len(array_WHub)*
                len(array_E)*
                len(array_theta))

        # Start and stop segment for fragmentation
        print ("Total of possible geometries folders to generate: ", total)
        print ("Number of geometries folders generated:           ", int((stop-start+1)*total/first))

        start_number = (start-1)*total/first+1
        stop_number = stop*total/first

        number = start_number
        for rTD in array_ratioTD[start-1:stop]:
            for rHT in array_ratioHT:
                for rTC in array_ratioTC:
                    for rDW in array_ratioDW:
                        for pWHub in array_WHub:  
                            for p_thick in array_E:
                                for t in array_theta:
                                    # Open the geometry file
                                    fic_geo = open("mixer.geo","r")
                                    cte_geo = fic_geo.read()
                                    # Insert the geometry
                                    template = Template(cte_geo)
                                    geometries = template.render(ratioTD = rTD,
                                                                ratioHT = rHT,
                                                                ratioTC = rTC,
                                                                ratioDW = rDW,
                                                                ratioDW_Hub = pWHub*rDW,
                                                                p_thick = p_thick,
                                                                theta = t,
                                                                min_mesh_length = "{{min_mesh_length}}",
                                                                max_mesh_length = "{{max_mesh_length}}")
                                    fic_geo.close()

                                    # Create the folder of the geometry
                                    newPath = path + '/mixer_' + str(int(number))
                                    os.mkdir(newPath)

                                    # Copy the file we need
                                    os.system('cp mixer.prm ' + newPath)
                                    os.system('cp launch_lethe.py ' + newPath)
                                    os.system('cp launch.sh ' + newPath)

                                    # Go into the geometry folder
                                    os.chdir(newPath)

                                    # Write the geometry file
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
                                        parameters = template_prm.render(viscosity = (1/rTD)**2/Re)
                                        fic_prm.close()

                                        # Create the folder for the viscosity
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
                                        fic_tag.write("D/W_Hub\t%f\t" % pWHub)
                                        fic_tag.write("E\t%f\t" % p_thick)
                                        fic_tag.write("theta\t%f\t" % t)
                                        fic_tag.write("Re\t%f\t" % Re)
                                        fic_tag.close()

                                        i = i + 1

                                        os.chdir("../")

                                    os.chdir("../")

                                    if number == stop_number:
                                        break
                                    else:
                                        number = number+1

def launch_gmsh(gmsh, first_mixer, last_mixer, max_mesh_length, min_max, decrease, enable):
    """
    Launch gmsh

    Args:
        first_mixer (int): First mixer to mesh
        last_mixer (int): Last mixer to mesh
        max_mesh_length (float): Maximum mesh length
        min_max (float): Fraction of maximum mesh length to set minimum mesh length
        enable (bool): If true, gmsh will be launched
    """
    if enable == True:
        this_path = os.getcwd()
        for mixer in np.linspace(first_mixer, last_mixer, (last_mixer-first_mixer)+1, dtype=int):
            os.chdir(this_path + '/mixer_' + str(mixer))
            
            ok = False
            mesh_length = max_mesh_length
            while ok == False and max_mesh_length > 0:
                os.system('cp mixer.geo mixer_copy.geo')
                
                fic_geo = open("mixer_copy.geo","r")
                cte_geo = fic_geo.read()
                template = Template(cte_geo)
                mesh = template.render(min_mesh_length = mesh_length*min_max,
                                       max_mesh_length = mesh_length)
                fic_geo.close()

                wr_geo = open("mixer_copy.geo","w")
                wr_geo.write(mesh)
                wr_geo.close()

                p = Popen([gmsh + ' -3 mixer_copy.geo -o mixer.msh'], stdout=PIPE, stderr=PIPE, shell=True)
                stdout, stderr = p.communicate()

                if stderr != b'':
                    mesh_length = mesh_length - decrease
                    os.system('rm mixer_copy.geo')
                    print("*Mesh has been refined*")
                else:
                    ok = True
                    print('---------- Generating mesh of mixer_' + str(mixer) + ' is complete ----------')
                
        os.chdir('../')

def launch_job(first_mixer, last_mixer, enable):
    """
    Launch jobs

    Args:
        first_mixer (int): First mixer to launch
        last_mixer (int): Last mixer to launch
        enable (bool): If true, the jobs will launch
    """
    if enable == True:
        this_path = os.getcwd()
        for mixer in np.linspace(first_mixer, last_mixer, (last_mixer-first_mixer)+1, dtype=int):
            geo_path = this_path + '/mixer_' + str(mixer)
            os.chdir(geo_path)

            os.system('sbatch -J ' + 'mixer_' + str(mixer) + ' launch.sh')
        
        os.chdir('../')

def launch_local(lethe, first_mixer, last_mixer, enable):
    """
    Launch locally Lethe

    Args:
        lethe (string): Directory to Lethe
        first_mixer (int): First mixer to simulate
        last_mixer (int): Last mixer to simulate
        enable (bool): If true, launch locally Lethe
    """
    if enable == True:
        this_path = os.getcwd()
        for mixer in np.linspace(first_mixer, last_mixer, (last_mixer-first_mixer)+1, dtype=int):
            geo_path = this_path + '/mixer_' + str(mixer)
            os.chdir(geo_path)

            path, dirs, files = next(os.walk(geo_path))
            for d in np.linspace(1, len(dirs), len(dirs), dtype=int):
                os.chdir(geo_path + '/mixer_' + str(d))
                print('---------- Launching Lethe for mixer_' + str(mixer) + '-' + str(d) + ' ----------')
                os.system(lethe + ' mixer.prm')

def get_torque_and_write_data(first_mixer, last_mixer, enable):
    """
    Get torque from simulation and write the data set

    Args:
        first_mixer (int): First mixer to get data
        last_mixer (int): Last mixer to get data
        enable (bool): If true, writing the data will be done
    """
    if enable == True:
        this_path = os.getcwd()
        
        database_name = 'mixer_database_' + str(int(first_mixer)) + '-' + str(int(last_mixer))

        progress = 1

        open(database_name + ".txt", "w").close()
        fic_data = open(database_name + ".txt", "a")
        for mixer in np.linspace(first_mixer, last_mixer, (last_mixer-first_mixer)+1, dtype=int):
            geo_path = this_path + '/mixer_' + str(mixer)
            os.chdir(geo_path)

            path, dirs, files = next(os.walk(geo_path))
            for d in np.linspace(1, len(dirs), len(dirs), dtype=int):
                os.chdir(geo_path + '/mixer_' + str(d))
                fic_data.write('mixer_' + str(mixer) + '-' + str(d) + '\t')

                fic_tag = open("mixer.txt","r")
                geo_info = fic_tag.read()
                fic_data.write(geo_info)
                geo_info = geo_info.split("\t")
                D = geo_info[1] # Impeller diameter
                fic_tag.close()

                try:
                    with open("torque.00.dat","r") as fic_torque:
                        lines = fic_torque.readlines()
                    fic_torque.close()
                
                    get_torque = lines[-1]
                    get_torque = get_torque.split(" ")
                    torque = get_torque[3]

                    # Calculate power number
                    D = 1/float(D)
                    torque = float(torque)
                    Np = 2*math.pi*torque/D/D/D/D/D

                    fic_data.write("Np\t%f\n" % Np)

                except:
                    fic_data.write("!SIMULATION FAILED!\n")
                
                pourcentage = progress/(((last_mixer-first_mixer)+1)*len(dirs))
                sys.stdout.write("\rProgress: " + "{:.2%}".format(pourcentage))
                sys.stdout.flush()
                progress += 1

        os.chdir('../../')

        fic_data.close()
        sys.stdout.write("\n")
