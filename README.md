# yplayer
Search and play youtube videos using terminal and mpv player

TODO
1. Create youtube-data-api key using cloud.google;
2. Create .env file and put there your key,  should be YPLAYER_KEY=your_key;
3. Add in your .env three path:
    3.1 BL_PATH=blacklist videos
    3.2 FV_PATH=favourite videos
    3.3 WT_PATH=watched videos
4. For help use option h;
5. By default yplayer in audio mode, if you want to watch video use option v;
6. For selecting duration use options in "Query" prompt; 
    Examples:
        "jazz night --l" (shows only videos that are more than 20 minutes)
        "phonk music --m" (shows only videos that are more or equal than 4 minutes but less or equal than 20 minutes)
        "funny videos --s" (shows only videos that are less than 4 minutes)
7. For quiting enter 'q' in "Query" prompt;
8. For showing next list of results enter "next" in "Query" prompt;
9. For selecting previous list of results enter "prev" in "Query" prompt;
10. For selecting video:
    Examples:
        1. video1
        2. video2
        3. video3
        4. video4
        ...
        50. video50
        >>> 1 # play video1
        >>> 3<= # play from 3 to the end of list
        >>> 2,3,45 # play video2, video3, video45
        >>> 30>= # play from video30 to the first item of list
        >>> 3bl # add video to blacklist
        >>> 3fv # add video to favourite list
        # enter 'q' for exiting playing

11. Listened/watched videos automatically add to watched list, so you wont see them again in a search results, if you wanna see list use option b, f, w (blacklist, favourite, watched respectfully)
     Examples:   
        "python yplayer.py f" # show favourite videos
        "python yplayer.py b" # show blacklisted videos
12. Enjoy minimalistic reprasantion of youtube.
    
