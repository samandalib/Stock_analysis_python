# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 13:00:42 2020

@author: hesam
"""

class DeltaObject:
    def __init__(self, delta_change, percent_change, dates):
        self.change = delta_change
        self.percent = percent_change
        self.dates = dates
    def __repr__(self):
        return f'{self.change},{self.percent},{self.dates}'