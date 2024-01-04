from .common import prettyllog
import os
import subprocess

def main():
    prettyllog("main", "check", "main", "all", "200", "Success")
    return True

def serve():
    prettyllog("main", "check", "main", "all", "200", "Success")
    os.system("pip install --upgrade ign8 >/dev/null 2>&1")
    os.chdir("/usr/local/lib/python3.9/site-packages/ign8/ui/project/ignite/")
    os.system("ansible-playbook -i inventory playbook.yml")
    #p = Popen(['espeak', '-b', '1'], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    gunicorn = subprocess.Popen(["gunicorn", "ignite.wsgi", "-c", "gunicorn.conf"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    prettyllog("main", "check", "main", "all", "200", "Success", "info")
    gunicorn.wait()



#    os.command("gunicorn ignite.wsgi -c gunicorn.conf")
    # change working directory to the root of the project




    return True
