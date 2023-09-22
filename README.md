# Roughness-Analysis-by-Electron-Microscopy
Roughness analysis approach by electron microscopy for spherical microparticles

The python script in this repository accompanies the following publication:

Hülagü, D., Tobias, C., Climent, E., Gojani, A., Rurack, K., Hodoroaba, V.-D., Generalized analysis approach of the profile roughness by electron microscopy with the example of hierarchically grown polystyrene-iron oxide silica core-shell-shell particles. Advanced Engineering Materials, 2022.
DOI: 10.1002/adem.202101344

If you use the code in your own work, please cite the above article.

# How to use the code:
• Download PyCharm (PyCharm Community Edition 2020.2 x64) software on your computer.

• Download the python script from the GitHub repository.

• Copy the EM images that you want to evaluate into the folder where you downloaded the python script as “xxxx.tif”.

• In the python script, enter the name of the EM image file. The script detects itself whether it is an SEM, TEM, or TSEM image.

• In the python script, enter the resolution of the EM image. 

• Press the run button. 

• The python script will output 5 files per each evaluated EM image:

    - Threshold image: “xxxx_IsoData_threshold.tif”
    
    - Border detected: “xxxx_border.png” and optimized center: “xxxx_optimized_center.png”
    
    - Distribution of distances as histogram: “xxxx_distance_distribution.png”
    
    - Distribution of distances as a function of angles: “xxxx_angles_and_distance.png”
    
    - Distribution of distances as a function of angles in a csv file: “xxxx_angles_and_distance.csv”
    
•	The final outcome of the python script is provide in the Terminal section of the PyCharm software.

•	Roughness value of the single particle is provided as “Roughness is XX.XX” in nm.
