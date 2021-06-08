import extract
import pandas
import sys
import os

nameToId = {
	'text_neck':0,
	'poor_sitting_posture':1,
	'correct_standing_posture':2,
	'correct_sitting_posture':3
}


#checks, whether time entry has a format 'mm:ss'
def check_time(start_time, end_time):
	start_sec = start_time
	end_sec = end_time

	if start_time.find(":")>0:

		start_split = start_time.split(':')
		start_split = [ x.replace('0','',1) if (x.startswith('0') and len(x) > 1) \
						 else x for x in start_split]
		start_sec = int(start_split[0])*60 + int(start_split[1])

	
	if end_time.find(":")>0:
		end_split = end_time.split(':')
		end_split = [ x.replace('0','',1) if (x.startswith('0') and len(x) > 1)\
						 else x for x in end_split]
		end_sec = int(end_split[0])*60 + int(end_split[1])

	return int(start_sec), int(end_sec)


def calc_duration(start_time, end_time):
	start_sec = start_time
	end_sec = end_time

	if start_time.find(":")>0:

		start_split = start_time.split(':')
		start_split = [ x.replace('0','',1) if (x.startswith('0') and len(x) > 1) \
						 else x for x in start_split]
		start_sec = int(start_split[0])*60 + int(start_split[1])

	
	if end_time.find(":")>0:
		end_split = end_time.split(':')
		end_split = [ x.replace('0','',1) if (x.startswith('0') and len(x) > 1)\
						 else x for x in end_split]
		end_sec = int(end_split[0])*60 + int(end_split[1])

	return int(end_sec) - int(start_sec)



def download_videos(yt_data, target_dir):
	urls = set()
	for row in data.iterrows():
		urls.add(row[1].url)
	for url in urls:
		extract.download_and_read_video(url, target_dir, only_download=True)




if __name__ == '__main__': 

    csv_filename = sys.argv[1] 
    video_folder = sys.argv[2]


	#check if there is an additional argument for separation of csv items
    if len(sys.argv) == 3:
    	csv_separator = ";"
    else:
    	csv_separator = sys.argv[3]

    data = pandas.read_csv(csv_filename,sep=csv_separator)
    #download_videos(data, video_folder)
    #cmd = "ffmpeg -ss 00:08:00 -i Video.mp4 -ss 00:01:00 -t 00:01:00 -c copy "
	#ffmpeg -ss 00:02:02 -i videos/cVd76HsjzVs.mp4 -to 00:00:02 -c copy clips/output.mp4
    overall_duration = 0

    for row in data.iterrows():
		#check for ':' in start_time and end_time
	    start_time = row[1].start_sec
	    end_time = row[1].end_sec
	    class_name = row[1].class_id
	    class_id = nameToId[class_name]
	    duration  = calc_duration(start_time, end_time)
	    overall_duration += duration
	    s,t =check_time(start_time, end_time)
	    video_id = extract.get_youtube_video_id_from_url(row[1].url)
	    video_filename = "%s/%s.mp4"%(video_folder + '/videos', video_id)
	    print(video_filename)
	    clip_filename = "%s/%s_%s_%s.mp4"%(video_folder + '/clips', video_id , str(s) + '_' + str(t), str(class_id))
	    print(clip_filename)
	    cmd = "ffmpeg -ss 00:%s -i %s  -to 00:00:%s -c copy %s"%(start_time,video_filename,duration,clip_filename)
	    print(cmd)
	    os.system(cmd)

    print('overall_duration = ', overall_duration)