from numpy import vstack,array
from numoy.random import rand
import numpy as np
from scipy.cluster.vq import kmeans,vq
import pandas as pd 
import pandas_datareader as dr 
from match import sqrt
from sklearn.cluster import KMeans 
from mathplotlib import pyplot as plt 
import openpyxl
import os
import time
from pandas import ExcelWriter
from pandas import ExcelFile

import matplotlib as matplotlibfrom mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
import statmodels.formula.pi as smf
import re
#import plotly.plotly as py

##setups