# AnsysConvergencePlotter

Ever find yourself wondering about the progress of your Ansys simulation when you're away from your computer? With this script, you can conveniently receive updates on your simulation status directly to your phone via your Outlook email account, no matter where you are. Stay connected and informed, even when you're on the go.


## Installing / Getting started


To use AnsysConvergencePlotter, you need to install the following Python libraries:

- [pywin32](https://pypi.org/project/pywin32/): Provides access to the Windows API, required for interacting with Outlook.
- [numpy](https://numpy.org/): Fundamental package for scientific computing with Python.

```bash
python -m pip install pywin32
pip install numpy
```

The script takes the following arguments. See a brief description of each:

```python
# Directory where your .wbpj is saved
main_folder = r"C:\..."

# Solver Files Directory - You can find the directory in Mechanical under: 
# Analysis Settings -> Analysis Data Management
analysis_folder = [r"C:\..."]

# Define the time interval for sending the plot to your e-mail 
# minutes * seconds = 60 * 60 = 1 hour
timerInterval = 60*60 

# Outlook e-mail adress
email = 'abc@abc.com'
```

In case you want to track more than one simulation, add all Solver Files Directories to the list 
'analysis_folder'.

## Usage

Here's a simple example of how to use the Ansys Convergence Plotter:

```python
# Import the AnsysConvergencePlotter module
from AnsysConvergencePlotter import AnsysConvergencePlotter

# Initialize the ConvergencePlotter object with your parameters
plotter = AnsysConvergencePlotter(main_folder, analysis_folder, timerInterval, email)

# Run the plotter
plotter.run()
```

Example of plot:
![Alt text](https://github.com/fAzeOl/AnsysConvergencePlotter/blob/main/Picture/PlotConvForce.png)

## Troubleshooting

If you encounter any issues during installation or usage, please check the following:

* Ensure that you have installed all required libraries listed in the Installing section.
* Double-check the directory paths specified in the script to ensure they point to the correct locations.
* Verify your Outlook email and make sure you have Outlook installed and running while the script is excecuting.
