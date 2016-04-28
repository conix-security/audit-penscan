#!/usr/bin/env python
import sys

import penScan.core as core
import penScan.core_sploit as core_sploit

def run():
    if len(sys.argv) > 1:	
    	if sys.argv[1] == 'sploit':
    		core_sploit.main()
    else:
    	core.main()

if __name__ == "__main__":
    run()
