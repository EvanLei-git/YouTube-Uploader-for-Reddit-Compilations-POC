import sqlite3,sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the configurations module
import configurations
from credentials import credentials
from functions import myDBfunctions
from functions import myFilefunctions
from functions import myRedditWebfuntions
from functions import myTimefunctions
from functions import myVideoAudiofunctions

def reset_upload_ids(upload_ids):
    database_path = configurations.DATABASE_PATH  # Replace with the actual path to your database
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    for upload_id in upload_ids:
        cursor.execute(f"UPDATE {configurations.DATABASE_TABLE_NAME} SET usedvideo = 0, uploadID = 0 WHERE uploadID = ?", (upload_id,))
        connection.commit()

    cursor.close()
    connection.close()

# Example usage
upload_ids = []
#example  upload_ids = ["16","17"]
reset_upload_ids(upload_ids)