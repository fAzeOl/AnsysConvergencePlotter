"""
Author: Filipe Azevedo
Title: Convergence Plot
Version: v1 
Created: 2024/02

Ansys version: 2021R2

Description:
Builds Convergence and Timestep plot from Ansys analysis and send it to an e-mail in an specific time interval.

"""

#----------------------------------------------------------------------------------------------------#

# Directory where your .wbpj is saved
main_folder = r"C:\..."

# Solver Files Directory - You can find the directory in Mechanical under Analysis Settings -> Analysis Data Management
analysis_folder = [r"C:\..."]

# Define the time interval for sending the plot to your e-mail
timerInterval = 60*60

# Outlook e-mail adress
email = 'abc@abc.com'

#----------------------------------------------------------------------------------------------------#

# Import the AnsysConvergencePlotter module
from AnsysConvergencePlotter import AnsysConvergencePlotter

# Initialize the ConvergencePlotter object with your parameters
plotter = AnsysConvergencePlotter(main_folder, analysis_folder, timerInterval, email)

# Run the plotter
plotter.run()