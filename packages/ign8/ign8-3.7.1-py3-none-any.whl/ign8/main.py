from .common import prettyllog
import os
import subprocess

def main():
    prettyllog("main", "check", "main", "all", "200", "Success")
    return True

def serve():
    prettyllog("main", "check", "main", "all", "200", "Success")
    os.system("pip install --uprade ign8")
    os.chdir("/usr/local/lib/python3.9/site-packages/ign8/ui/project/ignite/")
    gunicorn = subprocess.Popen(["gunicorn", "ignite.wsgi", "-c", "gunicorn.conf"])
    prettyllog("main", "check", "main", "all", "200", "Success", "info")
    gunicorn.wait()



#    os.command("gunicorn ignite.wsgi -c gunicorn.conf")
    # change working directory to the root of the project




    return True
