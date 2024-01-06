
"""THis is to install playwright at install-time"""


def main():
    import subprocess

    subprocess.run(['playwright', 'install'], check=True, shell=True)


if __name__ == '__main__':
    main()
