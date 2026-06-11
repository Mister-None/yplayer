import subprocess, re, sys, requests, os
from dotenv import load_dotenv
from colorama import Fore, init

load_dotenv(dotenv_path=os.getenv('DOTENV_FILE_PATH'))
init(autoreset=True)


youtube_key = os.getenv('YPLAYER_KEY')
base_url = os.getenv('BASE_URL')

next_page_token = []
prev_page_token = []

if len(sys.argv) < 2:
    sys.argv.append('a')

if sys.argv[1] in ['h']:
    print('a >>> audio\nv >>> video\nc >>> channel\np >>> playlist\nb >>> blacklist\nf >>> favourite\nw >>> watched'), exit()

elif sys.argv[1] in ['a', 'v']:
    content_type = 'video'
elif sys.argv[1] == 'c':
    content_type = 'channel'
elif sys.argv[1] == 'p':
    print('Under development!!!'), exit()
    content_type = 'playlist'

def youtube_search(n):
    global lst1, lst0, blacklist, bl_path, favourite, fv_path, search_params, raw_query, wt_path, watched, min_number, max_number, old_max_number 
    lst1 = []

    bl_path = os.getenv('BL_PATH')
    fv_path = os.getenv('FV_PATH')
    wt_path = os.getenv('WT_PATH')

    with open(bl_path, 'r') as f:
        blacklist = [i for i in f.read().split('\n') if i]
    with open(fv_path, 'r') as f:
        favourite = [i for i in f.read().split('\n') if i]
    with open(wt_path, 'r') as f:
        watched = [i for i in f.read().split('\n') if i]

    if sys.argv[1] not in ['f', 'b', 'w']:
        if n  in ['next', 'prev']:
            query_0 = old_query.split('--')

        else:
            raw_query = input(Fore.LIGHTCYAN_EX + f'> ').strip()
            query_0 = raw_query.split('--')

        query = query_0[0]

        search_params = {
            'key': youtube_key,
            'q': query,  
            'maxResults': 50, 
            'type': content_type, 
            'safeSearch': 'none',
        }
        if len(query_0) > 1:
            if query_0[-1] == 'l':
                query_duration = 'long'
            elif query_0[-1] == 'm':
                query_duration = 'medium'
            elif query_0[-1] == 's':
                query_duration = 'short'

        else:
            query_duration = 'any'

        if sys.argv[1] in ['v', 'a'] and not n:
            results = requests.get(f"{base_url}search?videoDuration={query_duration}", params=search_params).json()
            try:next_page_token.append(results['nextPageToken'])
            except KeyError: print(Fore.RED + "There is no more results for that query!!!")

        elif not n:
            results = requests.get(f"{base_url}search?", params=search_params).json()
            next_page_token.append(results['nextPageToken'])

        if n == 'next':  
            search_params['pageToken'] = next_page_token[0]
            results = requests.get(f"{base_url}search?videoDuration={query_duration}", params=search_params).json()
            next_page_token.pop()
            try:next_page_token.append(results['nextPageToken'])
            except KeyError: 
                print('No more results')
                exit()
            try: prev_page_token.pop()
            except: pass
            prev_page_token.append(results['prevPageToken'])
        elif n == 'prev':
            try: search_params['pageToken'] = prev_page_token[0]
            except IndexError: print('This is the first page!!!'), exit()
            results = requests.get(f"{base_url}search?videoDuration={query_duration}", params=search_params).json()
            prev_page_token.pop()
            try: prev_page_token.append(results['prevPageToken'])
            except KeyError: pass
        lst0 = [i['id'][f'{content_type}Id'] for i in results['items'] if content_type in i['id']['kind'] and  not (i['id'][f'{content_type}Id'] in blacklist or i['id'][f'{content_type}Id'] in favourite or i['id'][f'{content_type}Id'] in watched)]
    if sys.argv[1] in ['f', 'b', 'w']:
        if sys.argv[1] == 'b':
            desired_list = blacklist       
        elif sys.argv[1] == 'f':
            desired_list = favourite       
        elif sys.argv[1] == 'w':
            desired_list = watched       
        if not n:
            min_number = 0
            max_number = 50
        elif n == 'next':
            min_number = max_number
            max_number += 50
            if len(desired_list) < max_number:
                old_max_number = max_number
                max_number = len(desired_list) + 1
        elif n == 'prev':
            min_number -= 50 
            if len(desired_list) < max_number:
                max_number = old_max_number - 50
            else:    
                max_number -= 50
        lst0 = [i for i in desired_list[min_number:max_number] if i]     
    elif sys.argv[1] == 'c':
        channel_params = {
            'key': youtube_key,
            'id': ','.join(lst0),
            'part': 'statistics,snippet,contentDetails'
            }
        channels = requests.get(f"{base_url}channels", params=channel_params).json()
        playlist_lst0 = [[i['contentDetails']['relatedPlaylists']['uploads'], i['snippet']['title'], i['statistics']['subscriberCount']] for i in channels['items']]
        playlist_lst1 = sorted(playlist_lst0, key=lambda x: int(x[2]))
        playlist_lst2 = []          
        for id, i in enumerate(playlist_lst1):
            print(f"{id} ==> {i[1]} ==> {i[2]}")
            playlist_lst2.append(i[0])
        chan_n = int(input('>>> '))
        playlist_params = { 
            'key': youtube_key,
            'playlistId': playlist_lst2[chan_n],
            'part': 'snippet',
            'maxResults': 50
            }
        videos_itemes = requests.get(f"{base_url}playlistItems", params=playlist_params).json()
        lst0 = []
        for id, i in enumerate(videos_itemes['items']):
            if i['snippet']['resourceId']['videoId'] not in blacklist and i['snippet']['resourceId']['videoId'] not in favourite and i['snippet']['resourceId']['videoId'] not in watched: 
                lst0.append(i['snippet']['resourceId']['videoId'])
    video_params = {
        'key': youtube_key,
        'part': 'contentDetails,snippet,statistics',
        'id': ','.join(lst0)
    }
    videos = requests.get(f"{base_url}videos", params=video_params).json()
    if sys.argv[1] == 'c':
        video_base = reversed(videos['items'])
    elif sys.argv[1] in ['v']:
        video_base = sorted(videos['items'], reverse=True, key=lambda x: int(x['statistics']['viewCount']))
    elif sys.argv[1] in ['a']:
        video_base = sorted(videos['items'], key=lambda x: int(x['statistics']['viewCount']))
    elif sys.argv[1] in ['f', 'w', 'b']:
        video_base = videos['items']
        #video_base = sorted(videos['items'], key=lambda x: x['snippet']['title'])
    for id, i in enumerate(video_base):
        title = i['snippet']['title']
        views = i['statistics']['viewCount']
        pub_date = i['snippet']['publishedAt'].split('T')[0]
        try: duration = i['contentDetails']['duration']
        except KeyError: duration = 'unkown'
        try:seconds = re.search(r'\d+S', duration).group(0)[:-1].zfill(2)
        except AttributeError: seconds = '00'
        try:minutes = re.search(r'\d+M', duration).group(0)[:-1].zfill(2)
        except AttributeError: minutes = '00'            
        try: hours = re.search(r'\d+H', duration).group(0)[:-1].zfill(2)
        except AttributeError: hours = '00'
        duration = hours+':'+minutes+':'+seconds
        if sys.argv[1] in ['b', 'f', 'w']:
            offset_id = min_number + id 
            print(f"{Fore.LIGHTYELLOW_EX}{offset_id}{Fore.LIGHTWHITE_EX} ==> {Fore.LIGHTMAGENTA_EX}{title} {Fore.LIGHTWHITE_EX}==> {Fore.LIGHTCYAN_EX}{duration} {Fore.LIGHTWHITE_EX}==> {Fore.LIGHTBLUE_EX}{pub_date} {Fore.LIGHTWHITE_EX}==> {Fore.YELLOW}{views}")

        else:
            if int(minutes) >= 2: 
                print(f"{Fore.LIGHTYELLOW_EX}{id}{Fore.LIGHTWHITE_EX}==> {Fore.LIGHTMAGENTA_EX}{title} {Fore.LIGHTWHITE_EX}==> {Fore.LIGHTCYAN_EX}{duration} {Fore.LIGHTWHITE_EX}==> {Fore.LIGHTBLUE_EX}{pub_date} {Fore.LIGHTWHITE_EX}==> {Fore.YELLOW}{views}")

        lst1.append('https://youtu.be/'+i['id'])
youtube_search(None)

while True:
    n = input(Fore.LIGHTGREEN_EX + '>>> ')
    if n in ['q', 'й', ' ']: break
    elif n in ['r', 'к']: youtube_search(None)
    elif n  in ['next', 'prev'] and sys.argv[1] in ['b', 'f', 'w']: youtube_search(n)
    elif n  in ['next', 'prev']:
        old_query = raw_query
        youtube_search(n)
    else:
        for id1, i in enumerate(lst1):
            if n.endswith('d'):
                selected_id = int(re.search(r'\d+',  n).group(0))
                if id1 == selected_id:
                    subprocess.run(['sudo', 'yt-dlp', lst1[id1], '-x', '-q'])

            elif '-' in n:
                min_id = int(n.split('-')[0])
                max_id = int(n.split('-')[-1])
                if min_id <= id1 <= max_id:
                    print(lst1[id1])
                    with open(wt_path, 'a') as f: f.write(lst1[id1][17:]+'\n')
                    subprocess.run(['mpv', lst1[id1], '--no-video'])
            elif ',' in n:
                selected_ids = n.split(',')
                if id1 in [int(i) for i in selected_ids]:
                    print(id1, '>>>', lst1[id1])
                    with open(wt_path, 'a') as f: f.write(lst1[id1][17:]+'\n')
                    subprocess.run(['mpv', lst1[id1], '--no-video'])
            elif '<=' in n:
                min_id = int(n.split('<=')[0])
                if id1 >= min_id:
                    print(id1, '>>>', lst1[id1])
                    with open(wt_path, 'a') as f: f.write(lst1[id1][17:]+'\n')
                    subprocess.run(['mpv', lst1[id1], '--no-video'])
            elif '>=' in n:
                max_id = int(n.split('>=')[0])
                if id1 <= max_id:
                    print(id1, '>>>', lst1[id1])
                    with open(wt_path, 'a') as f: f.write(lst1[id1][17:]+'\n')
                    subprocess.run(['mpv', lst1[id1], '--no-video',])
            elif 'bl' in n:
                selected_id = int(n.split('bl')[0])
                bl_video_id = lst1[id1].split('.be/')[-1]
                if bl_video_id not in blacklist and id1==selected_id:
                    with open(bl_path, 'a') as f:
                        f.write(bl_video_id+'\n')
                        continue
            elif n.endswith('f'):
                selected_id = int(re.search(r'\d+',  n).group(0))
                fv_video_id = lst1[id1].split('.be/')[-1]
                if fv_video_id not in favourite and id1==selected_id:
                    with open(fv_path, 'a') as f:
                        f.write('https://youtu.be/'+fv_video_id+'\n')
                        continue
            elif sys.argv[1] in ['c', 'v', 'p'] and id1 == int(n):
                print(id1, '>>>', lst1[id1])
                with open(wt_path, 'a') as f: f.write(lst1[id1][17:]+'\n')
                subprocess.run(['sudo', 'mpv', lst1[int(n)],])
            elif id1 == int(n):
                with open(wt_path, 'a') as f: f.write(lst1[id1][17:]+'\n')
                print(lst1[int(n)])
                subprocess.run(['mpv', lst1[int(n)], '--no-video'])
