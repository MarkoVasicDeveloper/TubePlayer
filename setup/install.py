import pkg_resources
import subprocess
import sys

def check_requirements(requirements_file):
    with open(requirements_file, 'r') as f:
        requirements = f.readlines()

    installed_packages = {pkg.key for pkg in pkg_resources.working_set}
    missing_packages = []

    for req in requirements:
        package = req.split('==')[0].strip()
        if package and package not in installed_packages:
            missing_packages.append(req.strip())

    install_packages(missing_packages)

def install_packages(packages):
    if packages:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + packages)

check_requirements('requirements.txt')