"""
utilities for parallel computing
"""

import os
import json
import sys
import re
import argparse
import codecs

def split_list(target,num_of_runs,run_id,debug=False):
    size = len(target)
    gap = size/num_of_runs
    if gap==0:
        raise RuntimeError("The gap becomes zero: %d/%d" %(size,gap))
    else:
        

        #debug purpose
        if debug:
            print "size: %d, gap: %d"
            print "process %d - %d" %(gap*(run_id-1)-1,min(gap*run_id,size-1)-1)

        if run_id == num_of_runs:
            return target[gap*(run_id-1):]
        else:
            return target[gap*(run_id-1):gap*run_id]
