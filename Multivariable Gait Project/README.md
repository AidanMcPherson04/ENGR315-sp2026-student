Multivariable Gait Data Analysis - README

------------------------------------------------------------
OVERVIEW
------------------------------------------------------------
This project analyzes human gait data using the Multivariate Gait Dataset from the UCI Machine Learning Repository. The goal is to investigate biomechanical relationships in walking patterns by comparing joint motion across different conditions.

The analysis focuses on three primary questions:
1. Which joint exhibits the greatest range of motion (ROM)?
2. Are there measurable asymmetries between the left and right legs?
3. How does bracing (knee or ankle) affect joint motion?

------------------------------------------------------------
DATASET
------------------------------------------------------------
Source: Multivariate Gait Data (UCI Repository)

Description:
The dataset contains joint angle measurements (hip, knee, ankle) collected from multiple subjects under different walking conditions:
- Unbraced (normal walking)
- Knee brace applied
- Ankle brace applied

Structure:
- Organized by subject, condition, and trial
- Measurements recorded over a normalized gait cycle (0–100%)

------------------------------------------------------------
FEATURES USED
------------------------------------------------------------
- Joint angles (degrees):
  Hip, Knee, Ankle
- Left and right leg measurements
- Gait cycle percentage

------------------------------------------------------------
METHODS
------------------------------------------------------------

1. Range of Motion (ROM)
ROM = max(angle) - min(angle)
Calculated for each joint and averaged across subjects.

2. Symmetry Analysis
- Compares left vs right joint angles
- Uses paired t-test
- Significance level: alpha = 0.05

3. Braced vs Unbraced Comparison
- Uses squared difference:
  (theta_braced - theta_unbraced)^2
- Used instead of percent difference to avoid instability near zero values

------------------------------------------------------------
TOOLS AND LIBRARIES
------------------------------------------------------------
- Python 3.x
- numpy
- pandas
- matplotlib
- scipy.stats

------------------------------------------------------------
OUTPUTS
------------------------------------------------------------

Command Line Output:
- Joint with highest and lowest ROM
- Subject-level ROM comparisons
- Statistical test results (symmetry)
- Summary of differences between conditions

Plots Generated:
- Joint angle vs gait cycle
- Left vs right comparisons
- Difference plots (braced vs unbraced)

All plots include labeled axes, titles, and units.

------------------------------------------------------------
KEY FINDINGS
------------------------------------------------------------
- The knee joint exhibits the largest range of motion
- Human gait is not perfectly symmetrical
- Bracing primarily affects the targeted joint
- Largest differences occur during heel strike and toe-off

------------------------------------------------------------
HOW TO RUN
------------------------------------------------------------
1. Install required libraries:
   pip install numpy pandas matplotlib scipy

2. Place dataset files in the correct directory

3. Run the script:
   python main.py

4. View results:
   - Metrics printed in terminal
   - Plots displayed in windows

------------------------------------------------------------
NOTES AND LIMITATIONS
------------------------------------------------------------
- Averaging across subjects may hide individual variability
- Left/right phase differences not explicitly corrected
- Squared difference used instead of percent difference
- Additional normalization could improve results

------------------------------------------------------------
AUTHOR
------------------------------------------------------------
Leonard Manwarren
Levi Lindauer
Aidan McPherson

------------------------------------------------------------
ACKNOWLEDGMENTS
------------------------------------------------------------
- UCI Machine Learning Repository
- Course instruction and materials from ENGR 315: Computational Methods taught at James Madison University by Dr. Morgul