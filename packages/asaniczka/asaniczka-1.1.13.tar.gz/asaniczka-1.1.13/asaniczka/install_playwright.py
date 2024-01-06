
"""THis is to install playwright at install-time"""


def main():
    import subprocess
    try:
        result = subprocess.run('playwright install', check=True,
                                shell=True, capture_output=True, text=True)
        print("Installation completed successfully.")
    except subprocess.CalledProcessError as e:
        print("Installation failed with the following error:")
        print(e.stderr)


# main()
