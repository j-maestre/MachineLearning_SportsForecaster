import os
import subprocess
import platform
import importlib.util
import subprocess



def CheckPythonPackages(name):
  if importlib.util.find_spec(name) is None:
    permission_garanted = False
    while not permission_garanted:
      reply = str(input("Would you like to install Python packages '{0:s}'? [Y/N]: ".format(name))).lower().strip()[:1]
      if reply == 'n':
        return False
      permission_garanted = (reply == 'y')

    print(f"Installing {name} module...")
    subprocess.call(['python', '-m', 'pip', 'install', name])
    return CheckPythonPackages(name)
  return True

packages_needed = ['requests', 'Flask', 'tensorflow']


for name in packages_needed:
  if not CheckPythonPackages(name):
    print("Can't install the packages needed for the setup.")
    exit()