"""
ENGR 315 Final Project: Multivariable Gait Analysis with External Bracing

Team: GOMAD (Gait Observers for Multidimensional Analaysis of Dandering)

Authors: Aidan McPherson, Levi Lindauer, and Leonard Manwarren

This project will analyze the gait of a subject's hip, knee, and ankle joints while wearing
a brace on the right leg. The data was collected at the University of Illinois at Urbana-Champaign.

Link to data: https://archive.ics.uci.edu/dataset/760/multivariate+gait+data
"""

################################################################################
# This project aims to answer three questions
# Question 1: Which joint undergoes the most range of motion [ROM] while unbraced and
#             respective braced conditions?
#
# Question 2: Are there signs of accidental gait imbalances between the left and right 
#             legs in this test?
#
# Question 3: Which joint shows the greatest difference in range of motion [ROM] 
#             between braced and unbraced gait?
################################################################################

"""
This data has 180k data points with 7 columns/Variables. Listed in the order 
they appear in the data file, these variables are:

Column 1: Subject ID (1-10)
Column 2: Condition (1-3, where 1 = no brace, 2 = knee brace, 3 = ankle brace)
Column 3: Replication (1-10, where each subject performed 10 repetitions of the same condition)
Column 4: Leg (1-2, where 1 = left leg, 2 = right leg)
Column 5: Joint (1-3, where 1 = ankle, 2 = knee, 3 = hip)
Column 6: Time (0-100% of the gait cycle)                   <-- This will be a useful variable for plotting the ROM of each joint across the gait cycle.
Column 7: Angle (in degrees)

It may be helpful to create a directory of the data by subject, condition, leg, and 
joint for easier access and analysis. Replication may be averaged across for each subject
to simplify data organization.

As it stands, there will be 180 files if organized as defined.
"""

# Import necessary libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import norm
from scipy.stats import ttest_rel
from pathlib import Path
import shutil




# Create a function to see if I can read the relative path to the 'data' directory.
# This is important because other users may have different directory structures.
def test_datafile_path(path):
    try:
        data = pd.read_csv(path)
        #print("Data file loaded successfully!")
        return data
    except FileNotFoundError:
        #print("Data file not found. Please check the path and try again.")
        return None


# Load data from source CSV file located in the 'data' directory.
""" Create an if statement to check if the data file can be loaded successfully.
    If not, try to load the data file from a different path. """

path_to_datafile = -1               # This will change based on test_datafile_path function results.
path_indicator = -1                 #This is to help me keep track of which path is used for future reference.

if test_datafile_path("./data/multivariate+gait+data/gait.csv") is not None: # Check if the data file can be loaded from this path
    path_to_datafile = "./data/multivariate+gait+data/gait.csv"
    path_indicator = "./"                                        #This will help reduce nested if statements in the future

else:
    path_to_datafile = "../../data/multivariate+gait+data/gait_data.csv"  # If not, load the data file from this path.
    path_indicator = "../../"                                    #This will help reduce nested if statements in the future


data = pd.read_csv(path_to_datafile)                             # Data is we want to analyze


#################################################################################


"""WARNING YOUR CODE MAY MOVE TO A DIFFERENT DIRECTORY NAMED 'MULTIVARIABLE GAIT PROJECT' IN THE SAME PARENT DIRECTORY AS THIS FILE.
This is to help with organization and to ensure that all files related to this project are in the same directory."""
# Plus this is kinda funny :)
# Create the master directory for the project. This will be the parent directory for all other directories and files related to this project.
if not Path(path_indicator + "Multivariable Gait Project").exists():
    Path(path_indicator + "Multivariable Gait Project").mkdir(parents=True, exist_ok=True)
    shutil.move('ENGR315GaitAnalysis.py', path_indicator + "Multivariable Gait Project/") # Move the data file to the project directory for easier access and organization.


################################################################################


""" Make a nested directory to store the gait data
    This will be a nested directory organized by hierarchial order
    Gait Data -> Subject -> Condition -> Leg -> Joint """
# region Directory Creation
# Create main 'Gait Data' Directory
Path(path_indicator + "Multivariable Gait Project/Gait Data").mkdir(parents=True, exist_ok=True)

# Create second level of directory - Subjects (1-10)
for subject in range(1, 11):
    Path(path_indicator + f"Multivariable Gait Project/Gait Data/Subject{subject}").mkdir(parents=True, exist_ok=True)


# Create third level of directory - Conditions (1-3)
for subject in range(1, 11):
    for condition in range(1, 4):
        Path(path_indicator + f"Multivariable Gait Project/Gait Data/Subject{subject}/Condition{condition}").mkdir(parents=True, exist_ok=True)

# Create fourth level of directory - Legs (1-2)
for subject in range(1, 11):
    for condition in range(1, 4):
        for leg in range(1, 3):
            Path(path_indicator + f"Multivariable Gait Project/Gait Data/Subject{subject}/Condition{condition}/Leg{leg}").mkdir(parents=True, exist_ok=True)

# Create fifth level of directory - Joints (1-3)
for subject in range(1, 11):
    for condition in range(1, 4):
        for leg in range(1, 3):
            for joint in range(1, 4):
                Path(path_indicator + f"Multivariable Gait Project/Gait Data/Subject{subject}/Condition{condition}/Leg{leg}/Joint{joint}").mkdir(parents=True, exist_ok=True)

# Now that the directory is created, save the data for each subject, condition, leg, and joint
# in the appropriate directory. There will be 10 replications for each subject, condition, leg, and joint.

# I expect this to be a similar process to the directory creation, but instead of creating directories, I will be saving CSV files in the appropriate directories.
# The files will be named 'replication1.csv', 'replication2.csv', etc. for each replication.
for subject in range(1, 11):
    for condition in range(1, 4):
        for leg in range(1, 3):
            for joint in range(1, 4):
                for replication in range(1, 11): # Need this one to save each replication seperately
                    replication_data = data[(data['subject'] == subject) & (data['condition'] == condition) & (data['leg'] == leg) & (data['joint'] == joint) & (data['replication'] == replication)]
                    replication_data.to_csv(path_indicator + f"Multivariable Gait Project/Gait Data/Subject{subject}/Condition{condition}/Leg{leg}/Joint{joint}/replication{replication}.csv", index=False)
# endregion


########################################################################################
'Now that the data is organized, we can start analyzing it to answer the three questions.'
########################################################################################

"""
Question 1:
Which joint undergoes the most range of motion [ROM] while unbraced and respective braced
conditions?

The code is expected to answer the question and generate graphs showing the ROM
for each joint.
"""
# There is a region below this line. This helps collapses the code for organization
# region Question 1
print("-------Question 1-------")

# There are three joints to analyze: ankle, knee, and hip
# Additionally, there are three conditions to analyze: unbraced, knee brace, and ankle brace

# I want to find the joint with the average highest ROM and Lowest ROM
# Additionally it may be cool who got the true highest ROM for each joint and condition
# This will only consider the right leg (leg 2) since that is the leg with differing conditions.

################### Condition 1: Unbraced Gait [UNB] ###################
#### Hip Joint ROM
'Find the average ROM for the hip joint at each percent of the gait cycle'
'When iterating, keep the hip joint and right leg constant. Iterate through each subject and replication'
UNB_hip_all=[] #Read and store the all the data into this
for subject in range(1, 11):
    for replication in range(1, 11):
        # Read the data for the hip joint, right leg, unbraced condition for each subject and replication
        UNB_hip_data = pd.read_csv(path_indicator + f"Multivariable Gait Project/Gait Data/Subject{subject}/Condition1/Leg2/Joint3/replication{replication}.csv")
        UNB_hip_all.append(UNB_hip_data)

# Average the ROM for the hip joint at each percent of the gait cycle for each subject and replication
UNB_hip_avg_subject= pd.concat(UNB_hip_all).groupby(['subject', 'time'])['angle'].mean()

# Again except this is an average across all subjects
UNB_hip_avg_overall = pd.concat(UNB_hip_all).groupby('time')['angle'].mean()

# Find the ROM for the hip joint for each subject
UNB_hip_ROM_subject = pd.concat(UNB_hip_all).groupby('subject')['angle'].agg(lambda x: x.max() - x.min())

'Below are the variables to be used to compare later'
# Find the ROM for the hip joint overall
UNB_hip_ROM_overall = UNB_hip_avg_overall.max() - UNB_hip_avg_overall.min()

# Identify the subject with the highest ROM for the hip joint
UNB_hip_highest_ROM_subject = UNB_hip_ROM_subject.idxmax()
UNB_hip_highest_ROM_value = UNB_hip_ROM_subject.max()

#############################################
#### Knee Joint ROM
'Onto the knee joint, same dealio'
UNB_knee_all=[] #Read and store the all the data into this
for subject in range(1, 11):
    for replication in range(1, 11):
        # Read the data for the knee joint, right leg, unbraced condition for each subject and replication
        UNB_knee_data = pd.read_csv(path_indicator + f"Multivariable Gait Project/Gait Data/Subject{subject}/Condition1/Leg2/Joint2/replication{replication}.csv")
        UNB_knee_all.append(UNB_knee_data)

# Average the ROM for the knee joint at each percent of the gait cycle for each subject and replication
UNB_knee_avg_subject= pd.concat(UNB_knee_all).groupby(['subject', 'time'])['angle'].mean()

# Again except this is an average across all subjects
UNB_knee_avg_overall = pd.concat(UNB_knee_all).groupby('time')['angle'].mean()

# Find the ROM for the knee joint for each subject
UNB_knee_ROM_subject = pd.concat(UNB_knee_all).groupby('subject')['angle'].agg(lambda x: x.max() - x.min())

'Below are the variables to be used to compare later'
# Find the ROM for the knee joint overall
UNB_knee_ROM_overall = UNB_knee_avg_overall.max() - UNB_knee_avg_overall.min()

# Identify the subject with the highest ROM for the knee joint
UNB_knee_highest_ROM_subject = UNB_knee_ROM_subject.idxmax()
UNB_knee_highest_ROM_value = UNB_knee_ROM_subject.max()


##############################################
#### Ankle Joint ROM
'Onto the ankle joint, same dealio again'
UNB_ankle_all=[] #Read and store the all the data into this
for subject in range(1, 11):
    for replication in range(1, 11):
        # Read the data for the ankle joint, right leg, unbraced condition for each subject and replication
        UNB_ankle_data = pd.read_csv(path_indicator + f"Multivariable Gait Project/Gait Data/Subject{subject}/Condition1/Leg2/Joint1/replication{replication}.csv")
        UNB_ankle_all.append(UNB_ankle_data)

# Average the ROM for the ankle joint at each percent of the gait cycle for each subject and replication
UNB_ankle_avg_subject= pd.concat(UNB_ankle_all).groupby(['subject', 'time'])['angle'].mean()

# Again except this is an average across all subjects
UNB_ankle_avg_overall = pd.concat(UNB_ankle_all).groupby('time')['angle'].mean()

# Find the ROM for the ankle joint for each subject
UNB_ankle_ROM_subject = pd.concat(UNB_ankle_all).groupby('subject')['angle'].agg(lambda x: x.max() - x.min())

'Below are the variables to be used to compare later'
# Find the ROM for the ankle joint overall
UNB_ankle_ROM_overall = UNB_ankle_avg_overall.max() - UNB_ankle_avg_overall.min()

# Identify the subject with the highest ROM for the ankle joint
UNB_ankle_highest_ROM_subject = UNB_ankle_ROM_subject.idxmax()
UNB_ankle_highest_ROM_value = UNB_ankle_ROM_subject.max()


##################################################
#### Compare the ROM of the three joints to see which one has the highest and lowest ROM
# Set dummy variables to be used for comparison later
UNB_ROM_MAX_JOINT = -1
UNB_ROM_MAX_JOINT_VALUE = -1
if UNB_hip_ROM_overall > UNB_knee_ROM_overall and UNB_hip_ROM_overall > UNB_ankle_ROM_overall:
    UNB_ROM_MAX_JOINT = "Hip"
    UNB_ROM_MAX_JOINT_VALUE = UNB_hip_ROM_overall

elif UNB_knee_ROM_overall > UNB_hip_ROM_overall and UNB_knee_ROM_overall > UNB_ankle_ROM_overall:
    UNB_ROM_MAX_JOINT = "Knee"
    UNB_ROM_MAX_JOINT_VALUE = UNB_knee_ROM_overall

elif UNB_ankle_ROM_overall > UNB_hip_ROM_overall and UNB_ankle_ROM_overall > UNB_knee_ROM_overall:
    UNB_ROM_MAX_JOINT = "Ankle"
    UNB_ROM_MAX_JOINT_VALUE = UNB_ankle_ROM_overall

# Check for the lowest ROM joint as well
UNB_ROM_MIN_JOINT = -1
UNB_ROM_MIN_JOINT_VALUE = -1
if UNB_hip_ROM_overall < UNB_knee_ROM_overall and UNB_hip_ROM_overall < UNB_ankle_ROM_overall:
    UNB_ROM_MIN_JOINT = "Hip"
    UNB_ROM_MIN_JOINT_VALUE = UNB_hip_ROM_overall
elif UNB_knee_ROM_overall < UNB_hip_ROM_overall and UNB_knee_ROM_overall < UNB_ankle_ROM_overall:
    UNB_ROM_MIN_JOINT = "Knee"
    UNB_ROM_MIN_JOINT_VALUE = UNB_knee_ROM_overall
elif UNB_ankle_ROM_overall < UNB_hip_ROM_overall and UNB_ankle_ROM_overall < UNB_knee_ROM_overall:
    UNB_ROM_MIN_JOINT = "Ankle"
    UNB_ROM_MIN_JOINT_VALUE = UNB_ankle_ROM_overall


#################### THIS WILL ALL BE COMMENTED OUT FOR NOW ################

# Print the results for the unbraced condition
print("             UNBRACED CONDITION RESULTS                 ")
print(f"The joint with the highest ROM is the {UNB_ROM_MAX_JOINT} with an average ROM of {UNB_ROM_MAX_JOINT_VALUE:.3f} degrees.")
print()
print(f"The joint with the lowest ROM is the {UNB_ROM_MIN_JOINT} with an average ROM of {UNB_ROM_MIN_JOINT_VALUE:.3f} degrees.")
print()
print(f"The subject with the highest ROM for the hip joint is Subject {UNB_hip_highest_ROM_subject} with an average ROM of {UNB_hip_highest_ROM_value:.3f} degrees.")
print()
print(f"The subject with the highest ROM for the knee joint is Subject {UNB_knee_highest_ROM_subject} with an average ROM of {UNB_knee_highest_ROM_value:.3f} degrees.")
print()
print(f"The subject with the highest ROM for the ankle joint is Subject {UNB_ankle_highest_ROM_subject} with an average ROM of {UNB_ankle_highest_ROM_value:.3f} degrees.")
print("_______________________________")

# Plot the ROM for each joint across the gait cycle for the unbraced condition
plt.figure(figsize=(10, 6))
plt.plot(UNB_hip_avg_overall.index, UNB_hip_avg_overall.values, label='Hip Joint ROM', color='blue')
plt.plot(UNB_knee_avg_overall.index, UNB_knee_avg_overall.values, label='Knee Joint ROM', color='orange')
plt.plot(UNB_ankle_avg_overall.index, UNB_ankle_avg_overall.values, label='Ankle Joint ROM', color='green')
plt.title('Average ROM for Each Joint Across the Gait Cycle (Unbraced Condition)')
plt.xlabel('Percent of Gait Cycle')
plt.ylabel('Range of Motion (degrees)')
plt.xlim(0, 100)
plt.legend()
plt.show()

# Plot the Highest ROM Subjects for each joint across the gait cycle for the unbraced condition
# Starting with the hip joint, then knee, then ankle. Each will be a different color and labeled accordingly. This will be a line graph with time on the x-axis and ROM on the y-axis. The title will indicate that this is the ROM for each joint across the gait cycle for the subjects with the highest ROM in the unbraced condition.
# Hip Joint
plt.figure(figsize=(10, 6))
plt.plot(UNB_hip_avg_subject.loc[UNB_hip_highest_ROM_subject].index, UNB_hip_avg_subject.loc[UNB_hip_highest_ROM_subject].values, label=f'Subject {UNB_hip_highest_ROM_subject} Hip Joint ROM', color='blue')
plt.plot(UNB_hip_avg_overall.index, UNB_hip_avg_overall.values, label='Average Hip Joint ROM', color='red', linestyle='--')
plt.title('ROM for Hip Joint Across the Gait Cycle for the Subjects with the Highest ROM (Unbraced Condition)')
plt.xlabel('Percent of Gait Cycle')
plt.ylabel('Range of Motion (degrees)')
plt.xlim(0, 100)
plt.legend()
plt.show()

# Knee Joint
plt.figure(figsize=(10, 6))
plt.plot(UNB_knee_avg_subject.loc[UNB_knee_highest_ROM_subject].index, UNB_knee_avg_subject.loc[UNB_knee_highest_ROM_subject].values, label=f'Subject {UNB_knee_highest_ROM_subject} Knee Joint ROM', color='orange')
plt.plot(UNB_knee_avg_overall.index, UNB_knee_avg_overall.values, label='Average Knee Joint ROM', color='red', linestyle='--')
plt.title('ROM for Knee Joint Across the Gait Cycle for the Subjects with the Highest ROM (Unbraced Condition)')
plt.xlabel('Percent of Gait Cycle')
plt.ylabel('Range of Motion (degrees)')
plt.xlim(0, 100)
plt.legend()
plt.show()

# Ankle Joint
plt.figure(figsize=(10, 6))
plt.plot(UNB_ankle_avg_subject.loc[UNB_ankle_highest_ROM_subject].index, UNB_ankle_avg_subject.loc[UNB_ankle_highest_ROM_subject].values, label=f'Subject {UNB_ankle_highest_ROM_subject} Ankle Joint ROM', color='green')
plt.plot(UNB_ankle_avg_overall.index, UNB_ankle_avg_overall.values, label='Average Ankle Joint ROM', color='red', linestyle='--')
plt.title('ROM for Ankle Joint Across the Gait Cycle for the Subjects with the Highest ROM (Unbraced Condition)')
plt.xlabel('Percent of Gait Cycle')
plt.ylabel('Range of Motion (degrees)')
plt.xlim(0, 100)
plt.legend()
plt.show()


'--------------------------------------------------------------------------------------------'
################### Condition 2: Knee Brace Gait [KBR] ###################
'Same process as before, now for the knee brace condition'
#### Hip Joint ROM
'Find the average ROM for the hip joint at each percent of the gait cycle'
'When iterating, keep the hip joint and right leg constant. Iterate through each subject and replication'
KBR_hip_all=[] #Read and store the all the data into this
for subject in range(1, 11):
    for replication in range(1, 11):
        # Read the data for the hip joint, right leg, knee brace condition for each subject and replication
        KBR_hip_data = pd.read_csv(path_indicator + f"Multivariable Gait Project/Gait Data/Subject{subject}/Condition2/Leg2/Joint3/replication{replication}.csv")
        KBR_hip_all.append(KBR_hip_data)

# Average the ROM for the hip joint at each percent of the gait cycle for each subject and replication
KBR_hip_avg_subject= pd.concat(KBR_hip_all).groupby(['subject', 'time'])['angle'].mean()

# Again except this is an average across all subjects
KBR_hip_avg_overall = pd.concat(KBR_hip_all).groupby('time')['angle'].mean()

# Find the ROM for the hip joint for each subject
KBR_hip_ROM_subject = pd.concat(KBR_hip_all).groupby('subject')['angle'].agg(lambda x: x.max() - x.min())

'Below are the variables to be used to compare later'
# Find the ROM for the hip joint overall
KBR_hip_ROM_overall = KBR_hip_avg_overall.max() - KBR_hip_avg_overall.min()

# Identify the subject with the highest ROM for the hip joint
KBR_hip_highest_ROM_subject = KBR_hip_ROM_subject.idxmax()
KBR_hip_highest_ROM_value = KBR_hip_ROM_subject.max()

##################################
#### Knee Joint ROM

KBR_knee_all=[] #Read and store the all the data into this
for subject in range(1, 11):
    for replication in range(1, 11):
        # Read the data for the knee joint, right leg, knee brace condition for each subject and replication
        KBR_knee_data = pd.read_csv(path_indicator + f"Multivariable Gait Project/Gait Data/Subject{subject}/Condition2/Leg2/Joint2/replication{replication}.csv")
        KBR_knee_all.append(KBR_knee_data)

# Average the ROM for the knee joint at each percent of the gait cycle for each subject and replication
KBR_knee_avg_subject= pd.concat(KBR_knee_all).groupby(['subject', 'time'])['angle'].mean()

# Again except this is an average across all subjects
KBR_knee_avg_overall = pd.concat(KBR_knee_all).groupby('time')['angle'].mean()

# Find the ROM for the knee joint for each subject
KBR_knee_ROM_subject = pd.concat(KBR_knee_all).groupby('subject')['angle'].agg(lambda x: x.max() - x.min())

'Below are the variables to be used to compare later'
# Find the ROM for the knee joint overall
KBR_knee_ROM_overall = KBR_knee_avg_overall.max() - KBR_knee_avg_overall.min()

# Identify the subject with the highest ROM for the knee joint
KBR_knee_highest_ROM_subject = KBR_knee_ROM_subject.idxmax()
KBR_knee_highest_ROM_value = KBR_knee_ROM_subject.max()

#################################
#### Ankle Joint ROM

KBR_ankle_all=[] #Read and store the all the data into this
for subject in range(1, 11):
    for replication in range(1, 11):
        # Read the data for the ankle joint, right leg, ankle brace condition for each subject and replication
        KBR_ankle_data = pd.read_csv(path_indicator + f"Multivariable Gait Project/Gait Data/Subject{subject}/Condition2/Leg2/Joint1/replication{replication}.csv")
        KBR_ankle_all.append(KBR_ankle_data)

# Average the ROM for the ankle joint at each percent of the gait cycle for each subject and replication
KBR_ankle_avg_subject= pd.concat(KBR_ankle_all).groupby(['subject', 'time'])['angle'].mean()

# Again except this is an average across all subjects
KBR_ankle_avg_overall = pd.concat(KBR_ankle_all).groupby('time')['angle'].mean()

# Find the ROM for the ankle joint for each subject
KBR_ankle_ROM_subject = pd.concat(KBR_ankle_all).groupby('subject')['angle'].agg(lambda x: x.max() - x.min())

'Below are the variables to be used to compare later'
# Find the ROM for the ankle joint overall
KBR_ankle_ROM_overall = KBR_ankle_avg_overall.max() - KBR_ankle_avg_overall.min()

# Identify the subject with the highest ROM for the ankle joint
KBR_ankle_highest_ROM_subject = KBR_ankle_ROM_subject.idxmax()
KBR_ankle_highest_ROM_value = KBR_ankle_ROM_subject.max()


#############################
#### Compare the ROM of the three joints to see which one has the highest and lowest ROM

# Set dummy variables to be used for comparison later
KBR_ROM_MAX_JOINT = -1
KBR_ROM_MAX_JOINT_VALUE = -1
if KBR_hip_ROM_overall > KBR_knee_ROM_overall and KBR_hip_ROM_overall > KBR_ankle_ROM_overall:
    KBR_ROM_MAX_JOINT = "Hip"
    KBR_ROM_MAX_JOINT_VALUE = KBR_hip_ROM_overall

elif KBR_knee_ROM_overall > KBR_hip_ROM_overall and KBR_knee_ROM_overall > KBR_ankle_ROM_overall:
    KBR_ROM_MAX_JOINT = "Knee"
    KBR_ROM_MAX_JOINT_VALUE = KBR_knee_ROM_overall

elif KBR_ankle_ROM_overall > KBR_hip_ROM_overall and KBR_ankle_ROM_overall > KBR_knee_ROM_overall:
    KBR_ROM_MAX_JOINT = "Ankle"
    KBR_ROM_MAX_JOINT_VALUE = KBR_ankle_ROM_overall

# Check for the lowest ROM joint as well
KBR_ROM_MIN_JOINT = -1
KBR_ROM_MIN_JOINT_VALUE = -1
if KBR_hip_ROM_overall < KBR_knee_ROM_overall and KBR_hip_ROM_overall < KBR_ankle_ROM_overall:
    KBR_ROM_MIN_JOINT = "Hip"
    KBR_ROM_MIN_JOINT_VALUE = KBR_hip_ROM_overall
elif KBR_knee_ROM_overall < KBR_hip_ROM_overall and KBR_knee_ROM_overall < KBR_ankle_ROM_overall:
    KBR_ROM_MIN_JOINT = "Knee"
    KBR_ROM_MIN_JOINT_VALUE = KBR_knee_ROM_overall
elif KBR_ankle_ROM_overall < KBR_hip_ROM_overall and KBR_ankle_ROM_overall < KBR_knee_ROM_overall:
    KBR_ROM_MIN_JOINT = "Ankle"
    KBR_ROM_MIN_JOINT_VALUE = KBR_ankle_ROM_overall


#################### THIS WILL ALL BE COMMENTED OUT FOR NOW ################

# Print the results for the knee brace condition
print("             KNEE BRACE CONDITION RESULTS                 ")
print(f"The joint with the highest ROM is the {KBR_ROM_MAX_JOINT} with an average ROM of {KBR_ROM_MAX_JOINT_VALUE:.3f} degrees.")
print()
print(f"The joint with the lowest ROM is the {KBR_ROM_MIN_JOINT} with an average ROM of {KBR_ROM_MIN_JOINT_VALUE:.3f} degrees.")
print()
print(f"The subject with the highest ROM for the hip joint is Subject {KBR_hip_highest_ROM_subject} with an average ROM of {KBR_hip_highest_ROM_value:.3f} degrees.")
print()
print(f"The subject with the highest ROM for the knee joint is Subject {KBR_knee_highest_ROM_subject} with an average ROM of {KBR_knee_highest_ROM_value:.3f} degrees.")
print()
print(f"The subject with the highest ROM for the ankle joint is Subject {KBR_ankle_highest_ROM_subject} with an average ROM of {KBR_ankle_highest_ROM_value:.3f} degrees.")
print("_______________________________")

# Plot the ROM for each joint across the gait cycle for the knee brace condition
plt.figure(figsize=(10, 6))
plt.plot(KBR_hip_avg_overall.index, KBR_hip_avg_overall.values, label='Hip Joint ROM', color='blue')
plt.plot(KBR_knee_avg_overall.index, KBR_knee_avg_overall.values, label='Knee Joint ROM', color='orange')
plt.plot(KBR_ankle_avg_overall.index, KBR_ankle_avg_overall.values, label='Ankle Joint ROM', color='green')
plt.title('Average ROM for Each Joint Across the Gait Cycle (Knee Brace Condition)')
plt.xlabel('Percent of Gait Cycle')
plt.ylabel('Range of Motion (degrees)')
plt.xlim(0, 100)
plt.legend()
plt.show()

# Plot the Highest ROM Subjects for each joint across the gait cycle for the knee brace condition
# Starting with the hip joint, then knee, then ankle. Each will be a different color and labeled accordingly. This will be a line graph with time on the x-axis and ROM on the y-axis. The title will indicate that this is the ROM for each joint across the gait cycle for the subjects with the highest ROM in the unbraced condition.
# Hip Joint
plt.figure(figsize=(10, 6))
plt.plot(KBR_hip_avg_subject.loc[KBR_hip_highest_ROM_subject].index, KBR_hip_avg_subject.loc[KBR_hip_highest_ROM_subject].values, label=f'Subject {KBR_hip_highest_ROM_subject} Hip Joint ROM', color='blue')
plt.plot(KBR_hip_avg_overall.index, KBR_hip_avg_overall.values, label='Average Hip Joint ROM', color='red', linestyle='--')
plt.title('ROM for Hip Joint Across the Gait Cycle for the Subjects with the Highest ROM (Knee Brace Condition)')
plt.xlabel('Percent of Gait Cycle')
plt.ylabel('Range of Motion (degrees)')
plt.xlim(0, 100)
plt.legend()
plt.show()

# Knee Joint
plt.figure(figsize=(10, 6))
plt.plot(KBR_knee_avg_subject.loc[KBR_knee_highest_ROM_subject].index, KBR_knee_avg_subject.loc[KBR_knee_highest_ROM_subject].values, label=f'Subject {KBR_knee_highest_ROM_subject} Knee Joint ROM', color='orange')
plt.plot(KBR_knee_avg_overall.index, KBR_knee_avg_overall.values, label='Average Knee Joint ROM', color='red', linestyle='--')
plt.title('ROM for Knee Joint Across the Gait Cycle for the Subjects with the Highest ROM (Knee Brace Condition)')
plt.xlabel('Percent of Gait Cycle')
plt.ylabel('Range of Motion (degrees)')
plt.xlim(0, 100)
plt.legend()
plt.show()

# Ankle Joint
plt.figure(figsize=(10, 6))
plt.plot(KBR_ankle_avg_subject.loc[KBR_ankle_highest_ROM_subject].index, KBR_ankle_avg_subject.loc[KBR_ankle_highest_ROM_subject].values, label=f'Subject {KBR_ankle_highest_ROM_subject} Ankle Joint ROM', color='green')
plt.plot(KBR_ankle_avg_overall.index, KBR_ankle_avg_overall.values, label='Average Ankle Joint ROM', color='red', linestyle='--')
plt.title('ROM for Ankle Joint Across the Gait Cycle for the Subjects with the Highest ROM (Knee Brace Condition)')
plt.xlabel('Percent of Gait Cycle')
plt.ylabel('Range of Motion (degrees)')
plt.xlim(0, 100)
plt.legend()
plt.show()



'--------------------------------------------------------------------------------------------'
################### Condition 3: Ankle Brace Gait [ABR] ###################
'Same process as before, now for the ankle brace condition'
#### Hip Joint ROM
'Find the average ROM for the hip joint at each percent of the gait cycle'
'When iterating, keep the hip joint and right leg constant. Iterate through each subject and replication'
ABR_hip_all=[] #Read and store the all the data into this
for subject in range(1, 11):
    for replication in range(1, 11):
        # Read the data for the hip joint, right leg, ankle brace condition for each subject and replication
        ABR_hip_data = pd.read_csv(path_indicator + f"Multivariable Gait Project/Gait Data/Subject{subject}/Condition3/Leg2/Joint3/replication{replication}.csv")
        ABR_hip_all.append(ABR_hip_data)

# Average the ROM for the hip joint at each percent of the gait cycle for each subject and replication
ABR_hip_avg_subject= pd.concat(ABR_hip_all).groupby(['subject', 'time'])['angle'].mean()

# Again except this is an average across all subjects
ABR_hip_avg_overall = pd.concat(ABR_hip_all).groupby('time')['angle'].mean()

# Find the ROM for the hip joint for each subject
ABR_hip_ROM_subject = pd.concat(ABR_hip_all).groupby('subject')['angle'].agg(lambda x: x.max() - x.min())

'Below are the variables to be used to compare later'
# Find the ROM for the hip joint overall
ABR_hip_ROM_overall = ABR_hip_avg_overall.max() - ABR_hip_avg_overall.min()

# Identify the subject with the highest ROM for the hip joint
ABR_hip_highest_ROM_subject = ABR_hip_ROM_subject.idxmax()
ABR_hip_highest_ROM_value = ABR_hip_ROM_subject.max()

#####################################
#### Knee Joint ROM
ABR_knee_all=[] #Read and store the all the data into this
for subject in range(1, 11):
    for replication in range(1, 11):
        # Read the data for the knee joint, right leg, ankle brace condition for each subject and replication
        ABR_knee_data = pd.read_csv(path_indicator + f"Multivariable Gait Project/Gait Data/Subject{subject}/Condition3/Leg2/Joint2/replication{replication}.csv")
        ABR_knee_all.append(ABR_knee_data)

# Average the ROM for the knee joint at each percent of the gait cycle for each subject and replication
ABR_knee_avg_subject= pd.concat(ABR_knee_all).groupby(['subject', 'time'])['angle'].mean()

# Again except this is an average across all subjects
ABR_knee_avg_overall = pd.concat(ABR_knee_all).groupby('time')['angle'].mean()

# Find the ROM for the knee joint for each subject
ABR_knee_ROM_subject = pd.concat(ABR_knee_all).groupby('subject')['angle'].agg(lambda x: x.max() - x.min())

'Below are the variables to be used to compare later'
# Find the ROM for the knee joint overall
ABR_knee_ROM_overall = ABR_knee_avg_overall.max() - ABR_knee_avg_overall.min()

# Identify the subject with the highest ROM for the knee joint
ABR_knee_highest_ROM_subject = ABR_knee_ROM_subject.idxmax()
ABR_knee_highest_ROM_value = ABR_knee_ROM_subject.max()

#####################################
#### Ankle Joint ROM
ABR_ankle_all=[] #Read and store the all the data into this
for subject in range(1, 11):
    for replication in range(1, 11):
        # Read the data for the ankle joint, right leg, ankle brace condition for each subject and replication
        ABR_ankle_data = pd.read_csv(path_indicator + f"Multivariable Gait Project/Gait Data/Subject{subject}/Condition3/Leg2/Joint1/replication{replication}.csv")
        ABR_ankle_all.append(ABR_ankle_data)

# Average the ROM for the ankle joint at each percent of the gait cycle for each subject and replication
ABR_ankle_avg_subject= pd.concat(ABR_ankle_all).groupby(['subject', 'time'])['angle'].mean()

# Again except this is an average across all subjects
ABR_ankle_avg_overall = pd.concat(ABR_ankle_all).groupby('time')['angle'].mean()

# Find the ROM for the ankle joint for each subject
ABR_ankle_ROM_subject = pd.concat(ABR_ankle_all).groupby('subject')['angle'].agg(lambda x: x.max() - x.min())

'Below are the variables to be used to compare later'
# Find the ROM for the ankle joint overall
ABR_ankle_ROM_overall = ABR_ankle_avg_overall.max() - ABR_ankle_avg_overall.min()

# Identify the subject with the highest ROM for the ankle joint
ABR_ankle_highest_ROM_subject = ABR_ankle_ROM_subject.idxmax()
ABR_ankle_highest_ROM_value = ABR_ankle_ROM_subject.max()

#####################################
#### Compare the ROM of the three joints to see which one has the highest and lowest ROM

# Set dummy variables to be used for comparison later
ABR_ROM_MAX_JOINT = -1
ABR_ROM_MAX_JOINT_VALUE = -1
if ABR_hip_ROM_overall > ABR_knee_ROM_overall and ABR_hip_ROM_overall > ABR_ankle_ROM_overall:
    ABR_ROM_MAX_JOINT = "Hip"
    ABR_ROM_MAX_JOINT_VALUE = ABR_hip_ROM_overall

elif ABR_knee_ROM_overall > ABR_hip_ROM_overall and ABR_knee_ROM_overall > ABR_ankle_ROM_overall:
    ABR_ROM_MAX_JOINT = "Knee"
    ABR_ROM_MAX_JOINT_VALUE = ABR_knee_ROM_overall

elif ABR_ankle_ROM_overall > ABR_hip_ROM_overall and ABR_ankle_ROM_overall > ABR_knee_ROM_overall:
    ABR_ROM_MAX_JOINT = "Ankle"
    ABR_ROM_MAX_JOINT_VALUE = ABR_ankle_ROM_overall

# Check for the lowest ROM joint as well
ABR_ROM_MIN_JOINT = -1
ABR_ROM_MIN_JOINT_VALUE = -1
if ABR_hip_ROM_overall < ABR_knee_ROM_overall and ABR_hip_ROM_overall < ABR_ankle_ROM_overall:
    ABR_ROM_MIN_JOINT = "Hip"
    ABR_ROM_MIN_JOINT_VALUE = ABR_hip_ROM_overall
elif ABR_knee_ROM_overall < ABR_hip_ROM_overall and ABR_knee_ROM_overall < ABR_ankle_ROM_overall:
    ABR_ROM_MIN_JOINT = "Knee"
    ABR_ROM_MIN_JOINT_VALUE = ABR_knee_ROM_overall
elif ABR_ankle_ROM_overall < ABR_hip_ROM_overall and ABR_ankle_ROM_overall < ABR_knee_ROM_overall:
    ABR_ROM_MIN_JOINT = "Ankle"
    ABR_ROM_MIN_JOINT_VALUE = ABR_ankle_ROM_overall


#################### THIS WILL ALL BE COMMENTED OUT FOR NOW ################

# Print the results for the ankle brace condition
print("             ANKLE BRACE CONDITION RESULTS                 ")
print(f"The joint with the highest ROM is the {ABR_ROM_MAX_JOINT} with an average ROM of {ABR_ROM_MAX_JOINT_VALUE:.3f} degrees.")
print()
print(f"The joint with the lowest ROM is the {ABR_ROM_MIN_JOINT} with an average ROM of {ABR_ROM_MIN_JOINT_VALUE:.3f} degrees.")
print()
print(f"The subject with the highest ROM for the hip joint is Subject {ABR_hip_highest_ROM_subject} with an average ROM of {ABR_hip_highest_ROM_value:.3f} degrees.")
print()
print(f"The subject with the highest ROM for the knee joint is Subject {ABR_knee_highest_ROM_subject} with an average ROM of {ABR_knee_highest_ROM_value:.3f} degrees.")
print()
print(f"The subject with the highest ROM for the ankle joint is Subject {ABR_ankle_highest_ROM_subject} with an average ROM of {ABR_ankle_highest_ROM_value:.3f} degrees.")
print("_______________________________")

# Plot the ROM for each joint across the gait cycle for the ankle brace condition
plt.figure(figsize=(10, 6))
plt.plot(ABR_hip_avg_overall.index, ABR_hip_avg_overall.values, label='Hip Joint ROM', color='blue')
plt.plot(ABR_knee_avg_overall.index, ABR_knee_avg_overall.values, label='Knee Joint ROM', color='orange')
plt.plot(ABR_ankle_avg_overall.index, ABR_ankle_avg_overall.values, label='Ankle Joint ROM', color='green')
plt.title('Average ROM for Each Joint Across the Gait Cycle (Ankle Brace Condition)')
plt.xlabel('Percent of Gait Cycle')
plt.ylabel('Range of Motion (degrees)')
plt.xlim(0, 100)
plt.legend()
plt.show()

# Plot the Highest ROM Subjects for each joint across the gait cycle for the unbraced condition
# Starting with the hip joint, then knee, then ankle. Each will be a different color and labeled accordingly. This will be a line graph with time on the x-axis and ROM on the y-axis. The title will indicate that this is the ROM for each joint across the gait cycle for the subjects with the highest ROM in the unbraced condition.
# Hip Joint
plt.figure(figsize=(10, 6))
plt.plot(ABR_hip_avg_subject.loc[ABR_hip_highest_ROM_subject].index, ABR_hip_avg_subject.loc[ABR_hip_highest_ROM_subject].values, label=f'Subject {ABR_hip_highest_ROM_subject} Hip Joint ROM', color='blue')
plt.plot(ABR_hip_avg_overall.index, ABR_hip_avg_overall.values, label='Average Hip Joint ROM', color='red', linestyle='--')
plt.title('ROM for Hip Joint Across the Gait Cycle for the Subjects with the Highest ROM (Ankle Brace Condition)')
plt.xlabel('Percent of Gait Cycle')
plt.ylabel('Range of Motion (degrees)')
plt.xlim(0, 100)
plt.legend()
plt.show()

# Knee Joint
plt.figure(figsize=(10, 6))
plt.plot(ABR_knee_avg_subject.loc[ABR_knee_highest_ROM_subject].index, ABR_knee_avg_subject.loc[ABR_knee_highest_ROM_subject].values, label=f'Subject {ABR_knee_highest_ROM_subject} Knee Joint ROM', color='orange')
plt.plot(ABR_knee_avg_overall.index, ABR_knee_avg_overall.values, label='Average Knee Joint ROM', color='red', linestyle='--')
plt.title('ROM for Knee Joint Across the Gait Cycle for the Subjects with the Highest ROM (Ankle Brace Condition)')
plt.xlabel('Percent of Gait Cycle')
plt.ylabel('Range of Motion (degrees)')
plt.xlim(0, 100)
plt.legend()
plt.show()

# Ankle Joint
plt.figure(figsize=(10, 6))
plt.plot(ABR_ankle_avg_subject.loc[ABR_ankle_highest_ROM_subject].index, ABR_ankle_avg_subject.loc[ABR_ankle_highest_ROM_subject].values, label=f'Subject {ABR_ankle_highest_ROM_subject} Ankle Joint ROM', color='green')
plt.plot(ABR_ankle_avg_overall.index, ABR_ankle_avg_overall.values, label='Average Ankle Joint ROM', color='red', linestyle='--')
plt.title('ROM for Ankle Joint Across the Gait Cycle for the Subjects with the Highest ROM (Ankle Brace Condition)')
plt.xlabel('Percent of Gait Cycle')
plt.ylabel('Range of Motion (degrees)')
plt.xlim(0, 100)
plt.legend()
plt.show()

# endregion

############################################################################################

############################################################################################
"""
Question 2:
Are there signs of accidental gait imbalances between the left and right legs in this test?

This code will only analyze the unbraced condition of each subject to see if there are any
imbalances between the left and right legs. Graphs will be generated to compare the ROM of 
the left and right legs for each joint.

Subjects will be represented by their averaged replications.

Consider doing a t-test to compare the ROM of the left and right legs for each joint
to see if there are any significant differences.
"""
print("-------Question 2-------")

# region Question 2

# This will compare the ROM of the left and right legs for each joint in the unbraced condition to see if there are any imbalances.
# We will calculate the average ROM for each joint for both legs and then perform a t-test to see if there are any significant differences between the two legs.

""" NOTE: The left leg (Leg1) will be out of phase by 180 degrees compared to the right leg (Leg2) since they are opposite legs.
        This means that when the right leg is in the stance phase, the left leg will be in the swing phase, and vice versa.
        Therefore, we will need to account for this phase difference when comparing the ROM of the two legs. """

# Find the left leg ROM for each joint in the unbraced condition

############################
# Hip Joint ROM for Left Leg
UNB_hip_left_all=[] #Read and store the all the data into this
for subject in range(1, 11):
    for replication in range(1, 11):
        # Read the data for the hip joint, left leg, unbraced condition for each subject and replication
        UNB_hip_left_data = pd.read_csv(path_indicator + f"Multivariable Gait Project/Gait Data/Subject{subject}/Condition1/Leg1/Joint3/replication{replication}.csv")
        UNB_hip_left_all.append(UNB_hip_left_data)

# Group the data by subject and time to get the average ROM for the hip joint for the left leg in the unbraced condition
# Additionally multiply angle by -1 to account for the phase difference between the left and right legs
UNB_hip_left_avg_subject= pd.concat(UNB_hip_left_all).groupby(['subject', 'time'])['angle'].mean()

#############################
# Knee Joint ROM for Left Leg
UNB_knee_left_all=[] #Read and store the all the data into this
for subject in range(1, 11):
    for replication in range(1, 11):
        # Read the data for the knee joint, left leg, unbraced condition for each subject and replication
        UNB_knee_left_data = pd.read_csv(path_indicator + f"Multivariable Gait Project/Gait Data/Subject{subject}/Condition1/Leg1/Joint2/replication{replication}.csv")
        UNB_knee_left_all.append(UNB_knee_left_data)

# Group the data
UNB_knee_left_avg_subject= pd.concat(UNB_knee_left_all).groupby(['subject', 'time'])['angle'].mean()

##############################
# Ankle Joint ROM for Left Leg
UNB_ankle_left_all=[] #Read and store the all the data into this
for subject in range(1, 11):
    for replication in range(1, 11):
        # Read the data for the ankle joint, left leg, unbraced condition for each subject and replication
        UNB_ankle_left_data = pd.read_csv(path_indicator + f"Multivariable Gait Project/Gait Data/Subject{subject}/Condition1/Leg1/Joint1/replication{replication}.csv")
        UNB_ankle_left_all.append(UNB_ankle_left_data)

# Group the data
UNB_ankle_left_avg_subject= pd.concat(UNB_ankle_left_all).groupby(['subject', 'time'])['angle'].mean()

'---------------------------------------------------------------------------------------------'

# We already have the right leg ROM for each joint in the unbraced condition from Question 1
# Rename the variables for clarity
UNB_hip_right_avg_subject = UNB_hip_avg_subject
UNB_knee_right_avg_subject = UNB_knee_avg_subject
UNB_ankle_right_avg_subject = UNB_ankle_avg_subject

'---------------------------------------------------------------------------------------------'
# Time for the t-test to compare the ROM of the left and right legs for each joint in the unbraced condition
# Create empty lists to store the p-values for each joint
hip_p_values = []
knee_p_values = []
ankle_p_values = []

# Iterate through each subject and perform a t-test for each joint
for subject in range(1, 11):
    # Hip Joint
    hip_t_stat, hip_p_value = ttest_rel(UNB_hip_left_avg_subject.loc[subject].values, UNB_hip_right_avg_subject.loc[subject].values)
    hip_p_values.append(hip_p_value)
    # Knee Joint
    knee_t_stat, knee_p_value = ttest_rel(UNB_knee_left_avg_subject.loc[subject].values, UNB_knee_right_avg_subject.loc[subject].values)
    knee_p_values.append(knee_p_value)
    # Ankle Joint
    ankle_t_stat, ankle_p_value = ttest_rel(UNB_ankle_left_avg_subject.loc[subject].values, UNB_ankle_right_avg_subject.loc[subject].values)
    ankle_p_values.append(ankle_p_value)


# Compare the p-value to a significance level of 0.05 to determine if there are any significant differences between the left and right legs for each joint
# If p-value is less than 0.05, we can reject the null hypothesis and conclude that there is a significant difference between the left and right legs for that joint. If p-value is greater than or equal to 0.05, we fail to reject the null hypothesis and conclude that there is no significant difference between the left and right legs for that joint.
# Set to 0.05 because this is a common significance level used
alpha = 0.05
# Generate lists to store the results of the t-tests for each joint
hip_significant_list = []
hip_not_significant_list = []
knee_significant_list = []
knee_not_significant_list = []
ankle_significant_list = []
ankle_not_significant_list = []

# Iterate through the p-values for each joint and determine if they are significant or not
for subject, hip_p, knee_p, ankle_p in zip(range(1, 11), hip_p_values, knee_p_values, ankle_p_values):
    # Hip Joint
    if hip_p < alpha:
        # Append the results to a list to be printed later
        hip_significant_list.append('Subject'+str(subject))
    else:
        hip_not_significant_list.append('Subject'+str(subject))

    # Knee Joint
    if knee_p < alpha:
        knee_significant_list.append('Subject'+str(subject))
    else:
        knee_not_significant_list.append('Subject'+str(subject))

    # Ankle Joint
    if ankle_p < alpha:
        ankle_significant_list.append('Subject'+str(subject))
    else:
        ankle_not_significant_list.append('Subject'+str(subject))

# Check if a user has [non]significant differences in all three joints
subject_all_significant = []
subject_all_not_significant = []
subject_mixed = []

for subject in range(1, 11):
    # Boolean condition to check if the subject has significant differences in all three joints
    if 'Subject'+str(subject) in hip_significant_list and 'Subject'+str(subject) in knee_significant_list and 'Subject'+str(subject) in ankle_significant_list:
        #print(f"Subject {subject} has significant differences between the left and right legs for all three joints.")
        subject_all_significant.append('Subject'+str(subject))
    elif 'Subject'+str(subject) in hip_not_significant_list and 'Subject'+str(subject) in knee_not_significant_list and 'Subject'+str(subject) in ankle_not_significant_list:
        #print(f"Subject {subject} has no significant differences between the left and right legs for all three joints.")
        subject_all_not_significant.append('Subject'+str(subject))
    else:
        #print(f"Subject {subject} has a mix of significant and non-significant differences between the left and right legs for the three joints.")
        subject_mixed.append('Subject'+str(subject))

# Print the number of subjects with significant differences in all three joints, no significant differences in all three joints, and a mix of significant and non-significant differences
# Significant differences in all three joints
print(f"There are {len(subject_all_significant)} subjects with significant differences between the left and right legs for all three joints.")
if len(subject_all_significant) > 0:
    print(f"The subjects with significant differences in all three joints are: {', '.join(subject_all_significant)}")
print('\n')
# Non-significant differences in all three joints
print(f"There are {len(subject_all_not_significant)} subjects with no significant differences between the left and right legs for all three joints.")
if len(subject_all_not_significant) > 0:
    print(f"The subjects with no significant differences in all three joints are: {', '.join(subject_all_not_significant)}")
print('\n')
# Mixed significant and non-significant differences
print(f"There are {len(subject_mixed)} subjects with a mix of significant and non-significant differences between the left and right legs for the three joints.")
if len(subject_mixed) > 0:
    print(f"The subjects with mixed significant and non-significant differences are: {', '.join(subject_mixed)}")
print('\n')

############ THIS IS COMMENTED OUT FOR NOW ############

# Plot the of the "significant subject's" ROM for the left and right legs for each joint 
# Define a color for each subject
subject_left_colors = ['blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']
subject_right_colors = ['lightblue', 'lightcoral', 'lightgreen', 'lightpink', 'violet', 'tan', 'peachpuff', 'lightgray', 'olivedrab', 'lightcyan']
# Starting with the hip joint
plt.figure(figsize=(10, 6))
for subject in range(1, 11):
    if 'Subject'+str(subject) in subject_all_significant:
        plt.plot(UNB_hip_left_avg_subject.loc[subject].index, UNB_hip_left_avg_subject.loc[subject].values, label=f'Subject {subject} Left Leg Hip Joint ROM', color=subject_left_colors[subject-1])
        plt.plot(UNB_hip_right_avg_subject.loc[subject].index, UNB_hip_right_avg_subject.loc[subject].values, label=f'Subject {subject} Right Leg Hip Joint ROM', color=subject_right_colors[subject-1])
plt.title('Subjects with Significant Differences Between Left and Right Legs (Hip Joint)')
plt.xlabel('Percent of Gait Cycle')
plt.ylabel('Range of Motion (degrees)')
plt.xlim(0, 100)
plt.legend()
plt.show()

# Knee Joint
plt.figure(figsize=(10, 6))
for subject in range(1, 11):
    if 'Subject'+str(subject) in subject_all_significant:
        plt.plot(UNB_knee_left_avg_subject.loc[subject].index, UNB_knee_left_avg_subject.loc[subject].values, label=f'Subject {subject} Left Leg Knee Joint ROM', color=subject_left_colors[subject-1])
        plt.plot(UNB_knee_right_avg_subject.loc[subject].index, UNB_knee_right_avg_subject.loc[subject].values, label=f'Subject {subject} Right Leg Knee Joint ROM', color=subject_right_colors[subject-1])
plt.title('Subjects with Significant Differences Between Left and Right Legs (Knee Joint)')
plt.xlabel('Percent of Gait Cycle')
plt.ylabel('Range of Motion (degrees)')
plt.xlim(0, 100)
plt.legend()
plt.show()

# Ankle Joint
plt.figure(figsize=(10, 6))
for subject in range(1, 11):
    if 'Subject'+str(subject) in subject_all_significant:
        plt.plot(UNB_ankle_left_avg_subject.loc[subject].index, UNB_ankle_left_avg_subject.loc[subject].values, label=f'Subject {subject} Left Leg Ankle Joint ROM', color=subject_left_colors[subject-1])
        plt.plot(UNB_ankle_right_avg_subject.loc[subject].index, UNB_ankle_right_avg_subject.loc[subject].values, label=f'Subject {subject} Right Leg Ankle Joint ROM', color=subject_right_colors[subject-1])
plt.title('Subjects with Significant Differences Between Left and Right Legs (Ankle Joint)')
plt.xlabel('Percent of Gait Cycle')
plt.ylabel('Range of Motion (degrees)')
plt.xlim(0, 100)
plt.legend()
plt.show()

# Plot one of the significant subject
if len(subject_all_significant) > 0:
    plt.figure(figsize=(10, 6))
    subject = int(subject_all_significant[0].split('Subject')[1]) # Using the first since they all have significant differences in all three joints
    plt.plot(UNB_hip_left_avg_subject.loc[subject].index, UNB_hip_left_avg_subject.loc[subject].values, label=f'{subject} Left Leg Hip Joint ROM', color='blue')
    plt.plot(UNB_hip_right_avg_subject.loc[subject].index, UNB_hip_right_avg_subject.loc[subject].values, label=f'{subject} Right Leg Hip Joint ROM', color='lightblue')
    plt.plot(UNB_knee_left_avg_subject.loc[subject].index, UNB_knee_left_avg_subject.loc[subject].values, label=f'{subject} Left Leg Knee Joint ROM', color='orange')
    plt.plot(UNB_knee_right_avg_subject.loc[subject].index, UNB_knee_right_avg_subject.loc[subject].values, label=f'{subject} Right Leg Knee Joint ROM', color='lightcoral')
    plt.plot(UNB_ankle_left_avg_subject.loc[subject].index, UNB_ankle_left_avg_subject.loc[subject].values, label=f'{subject} Left Leg Ankle Joint ROM', color='green')
    plt.plot(UNB_ankle_right_avg_subject.loc[subject].index, UNB_ankle_right_avg_subject.loc[subject].values, label=f'{subject} Right Leg Ankle Joint ROM', color='lightgreen')
    plt.title(f'Subject {subject}\'s Left and Right Leg ROM for All Joints (All Significant)')
    plt.xlabel('Percent of Gait Cycle')
    plt.ylabel('Range of Motion (degrees)')
    plt.xlim(0, 100)
    plt.legend()
    plt.show()

# Plot one of the non-significant subjects (highest p-value)
if len(subject_all_not_significant) > 0:
    plt.figure(figsize=(10, 6))
    subject = int(subject_all_not_significant[0].split('Subject')[1]) # Using the first since they all have non-significant differences in all three joints
    plt.plot(UNB_hip_left_avg_subject.loc[subject].index, UNB_hip_left_avg_subject.loc[subject].values, label=f'{subject} Left Leg Hip Joint ROM', color='blue')
    plt.plot(UNB_hip_right_avg_subject.loc[subject].index, UNB_hip_right_avg_subject.loc[subject].values, label=f'{subject} Right Leg Hip Joint ROM', color='lightblue')
    plt.plot(UNB_knee_left_avg_subject.loc[subject].index, UNB_knee_left_avg_subject.loc[subject].index, label=f'{subject} Left Leg Knee Joint ROM', color='orange')
    plt.plot(UNB_knee_right_avg_subject.loc[subject].index, UNB_knee_right_avg_subject.loc[subject].index, label=f'{subject} Right Leg Knee Joint ROM', color='lightcoral')
    plt.plot(UNB_ankle_left_avg_subject.loc[subject].index, UNB_ankle_left_avg_subject.loc[subject].index, label=f'{subject} Left Leg Ankle Joint ROM', color='green')
    plt.plot(UNB_ankle_right_avg_subject.loc[subject].index, UNB_ankle_right_avg_subject.loc[subject].index, label=f'{subject} Right Leg Ankle Joint ROM', color='lightgreen')
    plt.title(f'Subject {subject}\'s Left and Right Leg ROM for All Joints (All Non-Significant)')
    plt.xlabel('Percent of Gait Cycle')
    plt.ylabel('Range of Motion (degrees)')
    plt.xlim(0, 100)
    plt.legend()
    plt.show()


# Plot a mixed subject
if len(subject_mixed) > 0:
    plt.figure(figsize=(10, 6))
    subject = int(subject_mixed[0].split('Subject')[1]) # Using the first since they have a mix of significant and non-significant differences in the three joints
    plt.plot(UNB_hip_left_avg_subject.loc[subject].index, UNB_hip_left_avg_subject.loc[subject].values, label=f'{subject} Left Leg Hip Joint ROM', color='blue')
    plt.plot(UNB_hip_right_avg_subject.loc[subject].index, UNB_hip_right_avg_subject.loc[subject].values, label=f'{subject} Right Leg Hip Joint ROM', color='lightblue')
    plt.plot(UNB_knee_left_avg_subject.loc[subject].index, UNB_knee_left_avg_subject.loc[subject].values, label=f'{subject} Left Leg Knee Joint ROM', color='orange')
    plt.plot(UNB_knee_right_avg_subject.loc[subject].index, UNB_knee_right_avg_subject.loc[subject].values, label=f'{subject} Right Leg Knee Joint ROM', color='lightcoral')
    plt.plot(UNB_ankle_left_avg_subject.loc[subject].index, UNB_ankle_left_avg_subject.loc[subject].values, label=f'{subject} Left Leg Ankle Joint ROM', color='green')
    plt.plot(UNB_ankle_right_avg_subject.loc[subject].index, UNB_ankle_right_avg_subject.loc[subject].values, label=f'{subject} Right Leg Ankle Joint ROM', color='lightgreen')
    plt.title(f'Subject {subject}\'s Left and Right Leg ROM for All Joints (Mixed Significant and Non-Significant)')
    plt.xlabel('Percent of Gait Cycle')
    plt.ylabel('Range of Motion (degrees)')
    plt.xlim(0, 100)
    plt.legend()
    plt.show()

# endregion
############################################################################################ 

############################################################################################

"""
Question 3:
Which joint shows the greatest difference in range of motion [ROM] between braced and
unbraced gait?

The code is expected to answer the question and generate graphs showing 
the difference of ROM for each joint. 

The percent difference will be the differnece of the brace ROM compared to the
 unbraced ROM, divided by the unbraced ROM, and multiplied
by 100 to get a percentage. 
"""


print("-------Question 3-------")
# region Question 3
"""
# Luckily, we already have the ROM for each joint for the unbraced condition and the two braced conditions. 
# We just need to calculate the root mean square error (RSME) for each joint and then compare them to see which one has the greatest difference.

Calculate the Square Difference [Sq Diff] for each joint for both individual subjects and overall
# Do the Square Difference because some values near 0, blowing up the percent error. Resulting in 8000% which is extreme"""
################################# KNEE BRACE CONDITION [KBR] #################################
# RSME for the hip joint
KBR_hip_RSME_subject = ((KBR_hip_avg_subject - UNB_hip_avg_subject) ** 2)
KBR_hip_RSME_overall = ((KBR_hip_avg_overall - UNB_hip_avg_overall) ** 2)

# RSME for the knee joint
KBR_knee_RSME_subject = ((KBR_knee_avg_subject - UNB_knee_avg_subject) ** 2)
KBR_knee_RSME_overall = ((KBR_knee_avg_overall - UNB_knee_avg_overall) ** 2)

# RSME for the ankle joint
KBR_ankle_RSME_subject = ((KBR_ankle_avg_subject - UNB_ankle_avg_subject) ** 2)
KBR_ankle_RSME_overall = ((KBR_ankle_avg_overall - UNB_ankle_avg_overall) ** 2)


################################# Ankle BRACE CONDITION [ABR] #################################
# RSME for the hip joint
ABR_hip_RSME_subject = ((ABR_hip_avg_subject - UNB_hip_avg_subject) ** 2)
ABR_hip_RSME_overall = ((ABR_hip_avg_overall - UNB_hip_avg_overall) ** 2)

# RSME for the knee joint
ABR_knee_RSME_subject = ((ABR_knee_avg_subject - UNB_knee_avg_subject) ** 2)
ABR_knee_RSME_overall = ((ABR_knee_avg_overall - UNB_knee_avg_overall) ** 2)

# RSME for the ankle joint
ABR_ankle_RSME_subject = ((ABR_ankle_avg_subject-UNB_ankle_avg_subject) ** 2)
ABR_ankle_RSME_overall = ((ABR_ankle_avg_overall - UNB_ankle_avg_overall) ** 2)

#####################################################################
### Compare the results to see which joint has the greatest difference in ROM between the braced and unbraced conditions

# Identify the joint with the greatest Sq Diff in ROM for the knee brace condition
KBR_ROM_MAX_JOINT = -1
KBR_ROM_MAX_JOINT_VALUE = -1
if KBR_hip_RSME_overall.abs().max() > KBR_knee_RSME_overall.abs().max() and KBR_hip_RSME_overall.abs().max() > KBR_ankle_RSME_overall.abs().max():
    KBR_ROM_MAX_JOINT = "Hip"
    KBR_ROM_MAX_JOINT_VALUE = KBR_hip_RSME_overall.abs().max()
elif KBR_knee_RSME_overall.abs().max() > KBR_hip_RSME_overall.abs().max() and KBR_knee_RSME_overall.abs().max() > KBR_ankle_RSME_overall.abs().max():
    KBR_ROM_MAX_JOINT = "Knee"
    KBR_ROM_MAX_JOINT_VALUE = KBR_knee_RSME_overall.abs().max()
elif KBR_ankle_RSME_overall.abs().max() > KBR_hip_RSME_overall.abs().max() and KBR_ankle_RSME_overall.abs().max() > KBR_knee_RSME_overall.abs().max():
    KBR_ROM_MAX_JOINT = "Ankle"
    KBR_ROM_MAX_JOINT_VALUE = KBR_ankle_RSME_overall.abs().max()

# Now lowest percent difference joint for the knee brace condition
KBR_ROM_MIN_JOINT = -1
KBR_ROM_MIN_JOINT_VALUE = -1
if KBR_hip_RSME_overall.abs().max() < KBR_knee_RSME_overall.abs().max() and KBR_hip_RSME_overall.abs().max() < KBR_ankle_RSME_overall.abs().max():
    KBR_ROM_MIN_JOINT = "Hip"
    KBR_ROM_MIN_JOINT_VALUE = KBR_hip_RSME_overall.abs().max()
elif KBR_knee_RSME_overall.abs().max() < KBR_hip_RSME_overall.abs().max() and KBR_knee_RSME_overall.abs().max() < KBR_ankle_RSME_overall.abs().max():
    KBR_ROM_MIN_JOINT = "Knee"
    KBR_ROM_MIN_JOINT_VALUE = KBR_knee_RSME_overall.abs().max()
elif KBR_ankle_RSME_overall.abs().max() < KBR_hip_RSME_overall.abs().max() and KBR_ankle_RSME_overall.abs().max() < KBR_knee_RSME_overall.abs().max():
    KBR_ROM_MIN_JOINT = "Ankle"
    KBR_ROM_MIN_JOINT_VALUE = KBR_ankle_RSME_overall.abs().max()

# Individual subjects for the knee brace condition
KBR_ROM_MAX_HIP_SUBJECT = -1
KBR_ROM_MAX_HIP_SUBJECT_VALUE = -1

KBR_ROM_MAX_KNEE_SUBJECT = -1
KBR_ROM_MAX_KNEE_SUBJECT_VALUE = -1

KBR_ROM_MAX_ANKLE_SUBJECT = -1
KBR_ROM_MAX_ANKLE_SUBJECT_VALUE = -1

# Go through each subject and compare the Sq Diff for each joint.
# If subject has greater amount of percent Sq Diff, replace current value and subject for that joint.
for subject in range(1, 11):
    hip_diff = KBR_hip_RSME_subject.loc[subject].abs().max()
    knee_diff = KBR_knee_RSME_subject.loc[subject].abs().max()
    ankle_diff = KBR_ankle_RSME_subject.loc[subject].abs().max()
    if hip_diff > knee_diff and hip_diff > ankle_diff:
        if hip_diff > KBR_ROM_MAX_HIP_SUBJECT_VALUE:
            KBR_ROM_MAX_HIP_SUBJECT = "Subject"+str(subject)+" Hip"
            KBR_ROM_MAX_HIP_SUBJECT_VALUE = hip_diff
    elif knee_diff > hip_diff and knee_diff > ankle_diff:
        if knee_diff > KBR_ROM_MAX_KNEE_SUBJECT_VALUE:
            KBR_ROM_MAX_KNEE_SUBJECT = "Subject"+str(subject)+" Knee"
            KBR_ROM_MAX_KNEE_SUBJECT_VALUE = knee_diff
    elif ankle_diff > hip_diff and ankle_diff > knee_diff:
        if ankle_diff > KBR_ROM_MAX_ANKLE_SUBJECT_VALUE:
            KBR_ROM_MAX_ANKLE_SUBJECT = "Subject"+str(subject)+" Ankle"
            KBR_ROM_MAX_ANKLE_SUBJECT_VALUE = ankle_diff

# Identify the joint with the greatest Sq Diff in ROM for the ankle brace condition
ABR_ROM_MAX_JOINT = -1
ABR_ROM_MAX_JOINT_VALUE = -1
if ABR_hip_RSME_overall.abs().max() > ABR_knee_RSME_overall.abs().max() and ABR_hip_RSME_overall.abs().max() > ABR_ankle_RSME_overall.abs().max():
    ABR_ROM_MAX_JOINT = "Hip"
    ABR_ROM_MAX_JOINT_VALUE = ABR_hip_RSME_overall.abs().max()
elif ABR_knee_RSME_overall.abs().max() > ABR_hip_RSME_overall.abs().max() and ABR_knee_RSME_overall.abs().max() > ABR_ankle_RSME_overall.abs().max():
    ABR_ROM_MAX_JOINT = "Knee"
    ABR_ROM_MAX_JOINT_VALUE = ABR_knee_RSME_overall.abs().max()
elif ABR_ankle_RSME_overall.abs().max() > ABR_hip_RSME_overall.abs().max() and ABR_ankle_RSME_overall.abs().max() > ABR_knee_RSME_overall.abs().max():
    ABR_ROM_MAX_JOINT = "Ankle"
    ABR_ROM_MAX_JOINT_VALUE = ABR_ankle_RSME_overall.abs().max()

# Now lowest percent difference joint for the ankle brace condition
ABR_ROM_MIN_JOINT = -1
ABR_ROM_MIN_JOINT_VALUE = -1
if ABR_hip_RSME_overall.abs().max() < ABR_knee_RSME_overall.abs().max() and ABR_hip_RSME_overall.abs().max() < ABR_ankle_RSME_overall.abs().max():
    ABR_ROM_MIN_JOINT = "Hip"
    ABR_ROM_MIN_JOINT_VALUE = ABR_hip_RSME_overall.abs().max()
elif ABR_knee_RSME_overall.abs().max() < ABR_hip_RSME_overall.abs().max() and ABR_knee_RSME_overall.abs().max() < ABR_ankle_RSME_overall.abs().max():
    ABR_ROM_MIN_JOINT = "Knee"
    ABR_ROM_MIN_JOINT_VALUE = ABR_knee_RSME_overall.abs().max()
elif ABR_ankle_RSME_overall.abs().max() < ABR_hip_RSME_overall.abs().max() and ABR_ankle_RSME_overall.abs().max() < ABR_knee_RSME_overall.abs().max():
    ABR_ROM_MIN_JOINT = "Ankle"
    ABR_ROM_MIN_JOINT_VALUE = ABR_ankle_RSME_overall.abs().max()

# Individual subjects for the ankle brace condition
ABR_ROM_MAX_HIP_SUBJECT = -1
ABR_ROM_MAX_HIP_SUBJECT_VALUE = -1

ABR_ROM_MAX_KNEE_SUBJECT = -1
ABR_ROM_MAX_KNEE_SUBJECT_VALUE = -1

ABR_ROM_MAX_ANKLE_SUBJECT = -1
ABR_ROM_MAX_ANKLE_SUBJECT_VALUE = -1

for subject in range(1, 11):
    hip_diff = ABR_hip_RSME_subject.loc[subject].abs().max()
    knee_diff = ABR_knee_RSME_subject.loc[subject].abs().max()
    ankle_diff = ABR_ankle_RSME_subject.loc[subject].abs().max()
    if hip_diff > knee_diff and hip_diff > ankle_diff:
        if hip_diff > ABR_ROM_MAX_HIP_SUBJECT_VALUE:
            ABR_ROM_MAX_HIP_SUBJECT = "Subject"+str(subject)+" Hip"
            ABR_ROM_MAX_HIP_SUBJECT_VALUE = hip_diff
    elif knee_diff > hip_diff and knee_diff > ankle_diff:
        if knee_diff > ABR_ROM_MAX_KNEE_SUBJECT_VALUE:
            ABR_ROM_MAX_KNEE_SUBJECT = "Subject"+str(subject)+" Knee"
            ABR_ROM_MAX_KNEE_SUBJECT_VALUE = knee_diff
    elif ankle_diff > hip_diff and ankle_diff > knee_diff:
        if ankle_diff > ABR_ROM_MAX_ANKLE_SUBJECT_VALUE:
            ABR_ROM_MAX_ANKLE_SUBJECT = "Subject"+str(subject)+" Ankle"
            ABR_ROM_MAX_ANKLE_SUBJECT_VALUE = ankle_diff

# Print Results 
# Knee Brace Condition
print("              KNEE BRACE CONDITION       ")
print("The joint that experienced the greatest difference in ROM is", KBR_ROM_MAX_JOINT)
print("While the minimum difference is", KBR_ROM_MIN_JOINT)
print()
print("              ANKLE BRACE CONDITION       ")
print("The joint that experienced the greatest difference in ROM is", ABR_ROM_MAX_JOINT)
print("While the minimum difference is", ABR_ROM_MIN_JOINT)

# Plot the Sq Diff for each joint for the knee brace condition
plt.figure(figsize=(10, 6))
plt.plot(KBR_hip_RSME_overall.index, KBR_hip_RSME_overall.values, label='Hip Joint Percent Difference', color='blue')
plt.plot(KBR_knee_RSME_overall.index, KBR_knee_RSME_overall.values, label='Knee Joint Percent Difference', color='orange')
plt.plot(KBR_ankle_RSME_overall.index, KBR_ankle_RSME_overall.values, label='Ankle Joint Percent Difference', color='green')
plt.title('ROM for Each Joint Across the Gait Cycle (Knee Brace Condition)')
plt.xlabel('Percent of Gait Cycle')
plt.ylabel('Square Difference Error')
plt.legend()
plt.xlim(0, 100)
plt.show()

# Plot the Sq Diff for each joint for the ankle brace condition
plt.figure(figsize=(10, 6))
plt.plot(ABR_hip_RSME_overall.index, ABR_hip_RSME_overall.values, label='Hip Joint Percent Difference', color='blue')
plt.plot(ABR_knee_RSME_overall.index, ABR_knee_RSME_overall.values, label='Knee Joint Percent Difference', color='orange')
plt.plot(ABR_ankle_RSME_overall.index, ABR_ankle_RSME_overall.values, label='Ankle Joint Percent Difference', color='green')
plt.title('ROM for Each Joint Across the Gait Cycle (Ankle Brace Condition)')
plt.xlabel('Percent of Gait Cycle')
plt.ylabel('Square Difference Error')
plt.legend()
plt.xlim(0, 100)
plt.show()

# endregion 
