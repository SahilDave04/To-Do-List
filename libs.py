import sys
import subprocess

lbs = ['PyQT5','mysql-connector-python','pywin32']
print("Checking if all needed libraries are installed")
reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
installed_packages = set([r.decode().split('==')[0] for r in reqs.split()])
if set(lbs).issubset(installed_packages):
    print("All the needed libraries are present.")
else:
    print("Libraries missing")
    print("Beginning download...")
    for i in lbs:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install',i ])
        print(f"Installed library : {i}")
