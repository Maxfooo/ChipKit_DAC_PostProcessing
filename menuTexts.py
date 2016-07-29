'''
Created on Jul 28, 2016

@author: maxr
'''


specialCaseText = \
"""
For some reason I am getting half values out of the ADC, but I came to the conclusion that, that isn't anything to worry about. Now, instead of 24 bits of precision, we are working with 23 by eliminating the MSB, which was stuck at 1, even when the input was 0.

So when the special case button is pressed it takes the 24 bit results and chops off the MSB, then re-scales everything to seem as if the results were 23 bits of precision.
"""
