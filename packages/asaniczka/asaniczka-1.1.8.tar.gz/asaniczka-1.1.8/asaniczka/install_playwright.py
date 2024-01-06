
"""THis is to install playwright at install-time"""


def main():
    import subprocess

    subprocess.call(['playwright', 'install'], check=True, shell=True)
