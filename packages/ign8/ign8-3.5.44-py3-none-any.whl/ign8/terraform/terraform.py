import subprocess
import os

from ign8 import runme





def init():
    """Initialize terraform"""
    pass

def plan():
    """Run terraform plan"""
    pass

def pluging_install():
    # we need to have go installed
    # execute go version to check if go is installed
    # if go is not installed, install go
    gotest = runme("go version")
    print(gotest.returncode)


  


    # we need to have terraform installed


def apply():
    """Run terraform apply"""
    pass



