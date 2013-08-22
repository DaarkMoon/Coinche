#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import interface
from locals import *

def main():
    GUI = interface.GUI(SCREN_RES,FPS)
    GUI.connect(SERVER)
    GUI.quit()
    
if __name__ == "__main__":
    main()

