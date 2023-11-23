

import multiprocessing

def run_script(script_path):
    subprocess.Popen(['python', script_path])

script_paths = ['utilities/VideoCreator.py', 'utilities/RedditJSONscrapper.py']

processes = []
for path in script_paths:
    process = multiprocessing.Process(target=run_script, args=(path,))
    processes.append(process)
    process.start()

# Wait for all processes to finish
for process in processes:
    process.join()