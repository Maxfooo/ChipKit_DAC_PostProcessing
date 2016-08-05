'''
Created on Jul 28, 2016

@author: maxr
'''


specialCaseText = """
For some reason I am getting half values out of the ADC, but I came to the conclusion that, that isn't anything to worry about. Now, instead of 24 bits of precision, we are working with 23 by eliminating the MSB, which was stuck at 1, even when the input was 0. So when the special case button is pressed it takes the 24 bit results and chops off the MSB, then re-scales everything to seem as if the results were 23 bits of precision.
"""

breakIfErrorText = """
If you do NOT select 'break if error', then the script will try to process the file and put any detected errors into the 'ErrorLog.txt'. If you DO select 'break if error, then if the following errors are detected in the file, the script will stop running and tell you. \n\nPossible errors include:\n+Too many samples\n+Too few samples\n+Repeat Code\n+Out of order code 
"""
