import os
import subprocess

def main():
    command = 'npx cypress run | tee cypress-log.txt'
    subprocess.call(command, shell=True)

    current_dir = os.path.dirname(os.path.realpath(__file__))
    calculate_similarity_script = os.path.join(current_dir, 'calculate-similarity.py')

    subprocess.run(f'python {calculate_similarity_script}', shell=True)