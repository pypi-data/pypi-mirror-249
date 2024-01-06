
"""THis is to install playwright at install-time"""


def main():
    import subprocess
    result = subprocess.run('playwright install', check=True,
                            shell=True, capture_output=True, text=True)
    print("Installation completed successfully.")
