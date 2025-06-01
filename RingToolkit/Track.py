import subprocess

def track(file_name: str, core_number: int = 4):
    subprocess.run(f"mpiexec -n {core_number} Pelegant {file_name}")