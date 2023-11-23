import time
import os,sys
import shutil
sys.dont_write_bytecode = True

def ChromeReset():
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    # Import the configurations module
    import configurations
    # Check if CHROME_DATA_PATH exists
    if not os.path.exists(configurations.CHROME_DATA_PATH):
        # Check if CHROME_BACKUP_PATH exists
        if os.path.exists(configurations.CHROME_BACKUP_PATH):
            # Copy CHROME_BACKUP_PATH to CHROME_DATA_PATH
            shutil.copytree(configurations.CHROME_BACKUP_PATH, configurations.CHROME_DATA_PATH)
    else:
        # Delete CHROME_DATA_PATH
        shutil.rmtree(configurations.CHROME_DATA_PATH)

        # Check if CHROME_BACKUP_PATH exists
        if os.path.exists(configurations.CHROME_BACKUP_PATH):
            # Copy CHROME_BACKUP_PATH to CHROME_DATA_PATH
            shutil.copytree(configurations.CHROME_BACKUP_PATH, configurations.CHROME_DATA_PATH)

def fileReset(file_path):
    try:
        shutil.rmtree(file_path, ignore_errors=True)
        time.sleep(5)
        os.makedirs(file_path)
    except:
        os.makedirs(file_path)

def updateVideoID(file_path, vidnum):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    if os.path.exists(file_path):
        f = open(file_path, "r")
        newuploadID = int(f.read())
        f.close()
    else:
        newuploadID = vidnum

    f = open(file_path, 'w+')
    f.write(str(newuploadID + 1))
    f.close()

    return newuploadID + 1

def getID(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    f = open(file_path,'a+')
    f.close()

    #Finding the lastID
    if os.stat(file_path).st_size == 0:
        f2=open(file_path,'w+')
        newuploadID=1
        f2.write(str(newuploadID))
        f2.close()
        #updating +1 so from 0 it will change to 1
        #newuploadID=updateVideoID(file_path)
    else:
        f  = open(file_path, "r")
        newuploadID=f.read()
        newuploadID=str(newuploadID)
        f.close()
    return newuploadID

def initializing_logs(file_path):
    dir_name = os.path.dirname(file_path)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    if not os.path.exists(file_path):
        open(file_path, 'w').close()




def manualCheckNUM(file_path, num):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    f = open(file_path, 'a+')
    f.close()

    # Finding the lastID
    if os.stat(file_path).st_size == 0:
        return False
    else:
        with open(file_path, 'r') as f:
            file_contents = f.read().strip()
            print(file_contents)
            if ',' in file_contents:
                file_contents = file_contents.replace(',', '')
            numbers_list = file_contents.split()
            if num in list(map(int, numbers_list)):
                return True  # number exists in the file, possible video has been uploaded
                
            else:
                return False  # doesn't exist


def manualUploadIDsaver(file_path, num):
    num = int(num)
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Read the current contents of the file
    with open(file_path, 'r') as f:
        contents = f.read().strip()

    # If the file is empty, start with an empty list
    if not contents:
        id_list = []
    else:
        # Otherwise, split the contents into a list of IDs
        id_list = []
        for id_str in contents.split(','):
            if id_str:
                id_list.append(int(id_str))

    # Add the new ID to the list and sort it in ascending order
    id_list.append(num)
    id_list.sort()

    # Write the sorted IDs back to the file separated by commas
    with open(file_path, 'w') as f:
        f.write(','.join(map(str, id_list)))