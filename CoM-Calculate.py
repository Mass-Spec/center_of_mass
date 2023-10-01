#test Tkinter plus CoM

#tkinter_app for com calc
import tkinter as tk
from tkinter import filedialog, Text
import os
# Start by importing urlopen
import urllib.request
CoM_x = ("")

PC_CID = str(702)

download_link = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/CID/' + PC_CID + '/record/SDF/?record_type=3d&response_type=save&response_basename=Conformer3D_CID_' + PC_CID

root = tk.Tk()

text_answer = tk.Label(root, text = str("CoM is:" + str(PC_CID)),font=("Arial", 17))
text_answer.place(relx=.33, rely=.2)

# Define the atomic masses of atoms and combine lists into a dictionary

atomic_masses = [1.008, 12, 14.003, 15.998, 34.969, 79.918]
elements = ['H', 'C', 'N', 'O', 'Cl', 'Br']
mapper = dict(zip(elements, atomic_masses))

#set up empty mass list
mass_list = []
mass_list2 = []

def remove(url_string):
    return url_string.replace(" ", "")


canvas = tk.Canvas(root, height=700, width=1100, bg ="#CC9900")
canvas.pack()

frame = tk.Frame(root, bg="white")
frame.place(relwidth=0.9, relheight=0.9, relx=.05, rely=.05)

text_prompt = tk.Label(root, text = 'Please input the CID # from PubChem (no spaces):',font=("Arial", 17))
text_prompt.place(relx=.33, rely=.5)

CID_Input = tk.Text(frame, height = 1.5, width = 30, bg='lightgrey', font=("Arial", 24))

CID_Input.place(rely=.6, relx=.3)



############################################################################
#beginning of Com_calc
#!/usr/bin/env python3
# PC_CID = (input("Please enter your CID # from pubchem (no spaces):"))

def CoM_calcy():

    #redefine CID input to take only the first line of input
    PC_CID_raw = str(CID_Input.get("1.0", 'end'))
    PC_CID = PC_CID_raw.splitlines()[0]

    #remove spaces from input and define url with CID number
    url_string = ('https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/CID/' + PC_CID + '/record/SDF/?record_type=3d&response_type=save&response_basename=Conformer3D_CID_' + PC_CID)
    download_link = (remove(url_string))
    # Download coordinates of CID
    with urllib.request.urlopen(download_link) as f:
        coord = f.read().decode(encoding = 'unicode_escape')

    #find title and define it
    title_link = "https://pubchem.ncbi.nlm.nih.gov/compound/" + remove(PC_CID)
    with urllib.request.urlopen(title_link) as f:
        title_html = f.read().decode(encoding = 'unicode_escape')

    title_index = title_html.find("<title>")
    start_index = title_index + len("<title>")
    end_index = title_html.find("PubChem</title>")
    title = title_html[start_index:end_index]
    print(title)


    # Extract and define the number of atoms

    num_atoms = (coord.splitlines()[3]).split()[0]
    # print(num_atoms)
    int_atoms = int(num_atoms) + 4


    # Create xyz coord from coord
    fin_coord = []

    # Only take the lines containing xyz info

    for n in range(4, int_atoms):
        new_line = ((coord.splitlines()[n]))
        fin_coord.append(new_line)

    # only take the first four items in each string

    fin_coord = [line_n.split()[:4] for line_n in fin_coord]

    #    if then statement to convert string numbers to integers
    for i in range(0, len(fin_coord)):
        fin_coord[i][0] = float(fin_coord[i][0])
        fin_coord[i][1] = float(fin_coord[i][1])
        fin_coord[i][2] = float(fin_coord[i][2])

        # Also convert elements to atomic mass

        fin_coord[i][3] = mapper[fin_coord[i][3]]


    for i in range(0, len(fin_coord)):
        mass_list.append(fin_coord[i][3])

    Sum_M = sum(mass_list)

    # Output the atomic mass
    print("The atomic mass is calculated to be " + str(Sum_M))

    # Now the coordinates will be weighted with their masses
    x_weighted = []
    y_weighted = []
    z_weighted = []

    for i in range(0, len(fin_coord)):
        x_weighted.append((fin_coord[i][0]) * fin_coord[i][3])
        y_weighted.append((fin_coord[i][1]) * fin_coord[i][3])
        z_weighted.append((fin_coord[i][2]) * fin_coord[i][3])

    # Now sum each weighted list

    sum_x = sum(x_weighted)
    sum_y = sum(y_weighted)
    sum_z = sum(z_weighted)


    # Divide by Sum_M to find center of mass

    CoM_x = sum_x / Sum_M
    CoM_y = sum_y / Sum_M
    CoM_z = sum_z / Sum_M

    text_answer = tk.Label(root, text = "The center of mass of " + title + "is calculated to be:\n" + "\n x = " + str(CoM_x) + " Å" +'\n y = ' + str(CoM_y) + " Å" + '\n z = ' + str(CoM_z) + " Å",font=("Arial", 17))
    text_answer.place(relx=.3, rely=.2)

    plot_button = tk.Button(root, height = 2, width = 20, bg = "darkgrey", text ="Plot", font=("Arial", 24), command=(plot))
    plot_button.place(rely=.83, relx=.385)
    return fin_coord

    # Now we need to plot the 3D coordinates and the COM

    # import 3d plotting and matplotlib ; attempt to remove redundant things in plot
def plot():

    #redefine CID input to take only the first line of input
    PC_CID_raw = str(CID_Input.get("1.0", 'end'))
    PC_CID = PC_CID_raw.splitlines()[0]

    #remove spaces from input and define url with CID number
    url_string = ('https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/CID/' + PC_CID + '/record/SDF/?record_type=3d&response_type=save&response_basename=Conformer3D_CID_' + PC_CID)
    download_link = (remove(url_string))
    # Download coordinates of CID
    with urllib.request.urlopen(download_link) as f:
        coord2 = f.read().decode(encoding = 'unicode_escape')


    # Extract and define the number of atoms

    num_atoms2 = (coord2.splitlines()[3]).split()[0]
    # print(num_atoms)
    int_atoms2 = int(num_atoms2) + 4


    # Create xyz coord from coord
    fin_coord2 = []

    # Only take the lines containing xyz info

    for n in range(4, int_atoms2):
        new_line2 = ((coord2.splitlines()[n]))
        fin_coord2.append(new_line2)

    # only take the first four items in each string

    fin_coord2 = [line_n2.split()[:4] for line_n2 in fin_coord2]

    #    if then statement to convert string numbers to integers
    for i in range(0, len(fin_coord2)):
        fin_coord2[i][0] = float(fin_coord2[i][0])
        fin_coord2[i][1] = float(fin_coord2[i][1])
        fin_coord2[i][2] = float(fin_coord2[i][2])

        # Also convert elements to atomic mass

        fin_coord2[i][3] = mapper[fin_coord2[i][3]]


    for i in range(0, len(fin_coord2)):
        mass_list2.append(fin_coord2[i][3])

    Sum_M2 = sum(mass_list2)


    # Now the coordinates will be weighted with their masses
    x_weighted2 = []
    y_weighted2 = []
    z_weighted2 = []

    for i in range(0, len(fin_coord2)):
        x_weighted2.append((fin_coord2[i][0]) * fin_coord2[i][3])
        y_weighted2.append((fin_coord2[i][1]) * fin_coord2[i][3])
        z_weighted2.append((fin_coord2[i][2]) * fin_coord2[i][3])

    # Now sum each weighted list

    sum_x2 = sum(x_weighted2)
    sum_y2 = sum(y_weighted2)
    sum_z2 = sum(z_weighted2)

    # Divide by Sum_M to find center of mass

    CoM_x = sum_x2 / Sum_M2
    CoM_y = sum_y2 / Sum_M2
    CoM_z = sum_z2 / Sum_M2





    import matplotlib.pyplot as plt

    from mpl_toolkits import mplot3d

    import numpy as np

    # Setting up 3d axis

    fig = plt.figure()

    ax = plt.axes(projection='3d')


    x_data = []
    y_data = []
    z_data = []


    for i in range(0, len(fin_coord2)):
        x_data.append((fin_coord2[i][0]))
        y_data.append((fin_coord2[i][1]))
        z_data.append((fin_coord2[i][2]))





    col = []

    for i in range(0, len(fin_coord2)):
        if mass_list2[i] == 1.008:
            col.append('gold')
        if mass_list2[i] == 12:
            col.append('black')
        if mass_list2[i] == 14.003:
            col.append('blue')
        if mass_list2[i] == 15.998:
            col.append('red')
        if mass_list2[i] == 34.969:
            col.append('green')
        if mass_list2[i] == 79.918:
            col.append('brown')
    range_z = ((min(z_data))-(max(z_data)))
    if range_z <= 1:
        print("Z-axis deviations are small, look only at x and y axis")

    ax.set_xlabel("x (Å)")
    ax.set_ylabel("y (Å)")
    ax.set_zlabel("z (Å)")

    ax.scatter3D(x_data, y_data, z_data, s= 200, c=col)
    ax.scatter3D(CoM_x, CoM_y, CoM_z, s= 400, c='purple', marker = 'x')

    plt.show()




    ############################################################################


go_button = tk.Button(root, height = 2, width = 20, bg = "darkgrey", text ="Calculate Center of Mass", font=("Arial", 24), command=(CoM_calcy))
go_button.place(rely=.73, relx=.385)




root.mainloop()
