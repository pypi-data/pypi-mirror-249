
"""THis is to install playwright at install-time"""
import subprocess

subprocess.run(['playwright', 'install'], check=True, shell=True)
