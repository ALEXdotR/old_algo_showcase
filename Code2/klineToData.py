#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 00:27:16 2022

@author: alex
"""

import pandas as pd
import os
import math
import numpy as np

class tradeWrangling():
    
    def __init__(self, _df):
        self.df = _df
    
    def klineToData(self):
        _df = self.df.drop(columns=['ignore'])
        
        return _df