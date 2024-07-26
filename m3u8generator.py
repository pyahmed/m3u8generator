#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
An extremely simple script to generate an m3u8 playlist with byte-ranges 
in order to serve it via HLS. Script requires ffprobe to be in PATH.
(c)2024 - Yasar L. Ahmed
'''

import subprocess
import json
import time
import os
import sys
import datetime

def generate_m3u8(inp_filename, output_path=False, save_results=False):
    proc_sta_time = time.time()
    fnam, fext = os.path.splitext(inp_filename)
    auto_output_fnam = f'{fnam}.m3u8'
    
    print('Input: ', inp_filename)
    
    def type_conversion(inp):
        if 'start_time' in inp:
            return {'start_time': float(inp['start_time'])}
        
        if 'pkt_pos' in inp:
            inp_pts_time = float(inp['pts_time'])
            inp_pkt_pos  = int(inp['pkt_pos'])
        
            inp_conv = {'pts_time': inp_pts_time, 'pkt_pos': inp_pkt_pos}
            return inp_conv

        return inp

    fnam, fext = os.path.splitext(inp_filename)
    basename = os.path.basename(inp_filename)

    ffprobe_cmd = f'ffprobe -select_streams v:0 -show_entries format=start_time -show_entries frame=pts_time,pkt_pos -skip_frame nokey -print_format json "{inp_filename}"'

    ffprobe_proc = subprocess.run(ffprobe_cmd, capture_output=True)
    ffprobe_outp = ffprobe_proc.stdout.decode()

    ffprobe_data = json.loads(ffprobe_outp, object_hook=type_conversion)
    
    ts = datetime.datetime.now().time().isoformat().split('.')[0].replace(':','')
    output_fnam = f'{fnam}_{ts}.json'
    if save_results:
        fh = open(output_fnam, 'wt')
        json.dump(ffprobe_data, fh)
        fh.close()
       
    last_pkt_pos = 0
    durations = []
    segments = []
    
    for current_frame in ffprobe_data['frames']:
        try:
            next_frame = ffprobe_data['frames'][ffprobe_data['frames'].index(current_frame) + 1]
        except Exception as e:
            next_frame = False
        
        pkt_pos = current_frame['pkt_pos']
        pts_time = current_frame['pts_time'] - ffprobe_data['format']['start_time']
        
        pkt_range = pkt_pos - last_pkt_pos
        if next_frame:
            next_pts_time = next_frame['pts_time'] - ffprobe_data['format']['start_time']
            next_pkt_pos  = next_frame['pkt_pos']
        
            current_frame_duration = round(next_pts_time - pts_time, 6)
            current_range = next_pkt_pos - pkt_pos
            segment_str = f'''#EXTINF:{current_frame_duration},\n#EXT-X-BYTERANGE:{current_range}@{pkt_pos}\n{basename}\n'''
            segments.append(segment_str)
            durations.append(current_frame_duration)
        
            # print(segment_str)
    
    m3u8_segments = ''.join(segments)
    
    max_duration = max(durations)
    
    FINAL_m3u8 = f"#EXTM3U\n#EXT-X-VERSION:4\n#EXT-X-TARGETDURATION:{max(durations)}\n#EXT-X-MEDIA-SEQUENCE:0\n{m3u8_segments}#EXT-X-ENDLIST"
    
    if not output_path:
        output_path = auto_output_fnam
    fh = open(output_path, 'wt')
    fh.write(FINAL_m3u8)
    fh.close()
    proc_end_time = time.time()
    proc_time = round(proc_end_time - proc_sta_time, 2)
    print('Output:', output_path)
    print('Time:  ', proc_time, 's')

FILENAME = sys.argv[1]

generate_m3u8(FILENAME)
