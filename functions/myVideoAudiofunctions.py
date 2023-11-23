import subprocess
import time
import os,sys
from pydub import AudioSegment
from pydub.utils import mediainfo
sys.dont_write_bytecode = True


def is_video_mobile_compatible(url):
    cmd = ['ffprobe', '-v', 'error', '-select_streams', 'v:0',
		   '-show_entries', 'stream=width,height', '-of', 'csv=s=x:p=0', url]
    output = subprocess.getoutput(" ".join(cmd))
    if output.endswith('x\n'):
        output = output[:-2]
    width, height = map(int, output.strip().split('x'))
	#print(width / height,9 / 16)
    return height >= width and width / height <= 1 / 1


def is_video_bigger_than_16_9_accurate(url):
    cmd = ['ffprobe', '-v', 'error', '-select_streams', 'v:0',
		   '-show_entries', 'stream=width,height', '-of', 'csv=s=x:p=0', url]
    output = subprocess.getoutput(" ".join(cmd))
    width, height = map(int, output.strip().split('x'))
    aspect_ratio = round(width / height, 2)
    return aspect_ratio > round(16 / 9, 2)

def is_video_bigger_than_16_9(url):

    cmd = ['ffprobe', '-v', 'error', '-select_streams', 'v:0',
           '-show_entries', 'stream=width,height', '-of', 'csv=s=x:p=0', url]
    try:
        output = subprocess.getoutput(" ".join(cmd))
        if output.endswith('x\n'):
            output = output[:-2]
        width, height = map(int, output.strip().split('x'))
        return (width / height) > 16 / 9
    except ValueError as e:
        print(f"Error: {e} for URL: {url}")
         


def getVideoLength(url,audio):

    link=url+audio
    #x=subprocess.check_output('ffprobe -i '+link+' -show_entries format=duration -v quiet -of csv="p=0"',shell=True)
    #print("THIS ->",url)
    x=subprocess.getoutput('ffprobe -i '+link+' -show_entries format=duration -v quiet -of csv="p=0"')
    #x=x.decode("utf-8")
    
    length=x.split(".", 1)[0]
    #print(length)
    return (length)


def check_last_5_seconds_0db(video_path):
    # Get the duration of the video in milliseconds
    time.sleep(3)
    video_info = mediainfo(video_path)
    time.sleep(3)
    #print ("test"+str(video_info)+"test")
    video_duration_ms = round(float(video_info['duration']) * 1000)

    # Extract the last 5 seconds of the video as an AudioSegment object
    audio = AudioSegment.from_file(video_path, 'mp4')[video_duration_ms - 3000:]

    # Compute the mean and maximum volume in dBFS
    mean_vol_dBFS = audio.dBFS
    #maybe for futrue usage
    max_vol_dBFS = audio.max_dBFS

    # Print the results
    if str(mean_vol_dBFS)!="-inf":
        return True
    else:
        return False

def is_mp4_encoding_complete(video_path):
    command = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', video_path]
    try:
        result = subprocess.check_output(command, stderr=subprocess.STDOUT)
        duration = float(result)
        if duration > 0:
            return True
    except subprocess.CalledProcessError as e:
        return False
    return False