import os, subprocess, time
name_simulation = 'simulation_tutorial'

yml_path = os.path.join('schema', f'{name_simulation}.yml') # YML path

# yml_path = f'{name_simulation}.yml'

command = "soil"
start = time.time()

output = subprocess.check_output([command, yml_path])