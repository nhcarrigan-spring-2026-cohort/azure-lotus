import subprocess


def run():
    subprocess.run(["isort", "."], check=True)
    subprocess.run(["black", "."], check=True)
