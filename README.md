# First and Follow Finder

This repository contains a tool for analyzing context-free grammars, specifically for finding FIRST and FOLLOW sets. It includes functionality for:

- Taking user input for grammar rules
- Validating the grammar
- Removing left recursion (direct and indirect)
- Calculating FIRST and FOLLOW sets

## Files

- `input.txt`: Contains the input grammar
- `Grammar_FF.py`: Main script for finding FIRST and FOLLOW sets
- `Grammar_LR.py`: Script for removing left recursion
- `FIRST_FOLLOW.py`: Implementation of FIRST and FOLLOW algorithms
- `utils.py`: Utility functions for grammar processing

## Usage

- Sample input provided in `input.txt`
 ![INPUT](https://github.com/user-attachments/assets/70c1199b-3f12-4eca-843b-d4073d3454b1)
- Run `FIRST_FOLLOW.py`
- ![FF LR](https://github.com/user-attachments/assets/345d0247-ccc6-4360-b4e9-3d0bc48fa770)



## Features

- Handles both direct and indirect left recursion
- Validates input grammar for correctness
- Provides detailed output of FIRST and FOLLOW sets

For more information on how to use this tool, please refer to the individual script files.
