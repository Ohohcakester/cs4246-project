import pandas as pd
import subprocess
import os
import time
import ast

how_do_you_run_python = 'py'

targetDir = 'bayes_ext_temp_folder/'

try: os.mkdir(targetDir)
except: pass

def predictGP(df, testTimes):
    fileName = targetDir + str(int(time.time()*1000))

    df.to_csv(fileName+'_A.csv')
    testTimes.to_csv(fileName+'_B.csv')
    returnCode = subprocess.call(how_do_you_run_python + ' bayes.py '+fileName, shell=True)
    while returnCode == 1:
        print 'GP Crashed! Try again!'
        returnCode = subprocess.call(how_do_you_run_python + ' bayes.py '+fileName, shell=True)
    
    result_df = pd.read_csv(fileName+'_OUT.csv', converters={"MU": ast.literal_eval, "VAR": ast.literal_eval})

    #cleanup code
    os.remove(fileName+'_A.csv')
    os.remove(fileName+'_B.csv')
    os.remove(fileName+'_OUT.csv')

    return result_df