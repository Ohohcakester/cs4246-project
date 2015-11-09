import os
# Create the queries and outputs directories if they do not exist
try: os.mkdir('queries')
except: pass
try: os.mkdir('outputs')
except: pass

import sys
sys.path.append('..')
import bayes

