import subprocess

def ele_track(file_name: str, core_number: int = 24):
    subprocess.run(f"mpiexec -n {core_number} Pelegant {file_name}")