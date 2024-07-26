# m3u8generator
Generate an m3u8 playlist with byteranges for serving a single TS file via HLS

This script runs ffprobe to obtain data (pkt_pos and pts_time) for I-frames in a given MPEG-TS file. It then creates an m3u8 playlist that contains those positions and the durations of those "segments". This allows serving large TS-files via HLS without requiring splitting or repackaging with just a simple web server. The script was put together using information from here:
- https://stackoverflow.com/questions/63167587/ffmpeg-pkt-pos-vs-hls-byterange-differs
- https://stackoverflow.com/questions/23497782/how-to-create-byte-range-m3u8-playlist-for-hls
- https://github.com/pbs/iframe-playlist-generator,
- https://stackoverflow.com/questions/18178374/how-can-html5-videos-byte-range-requests-pseudo-streaming-work

I couldn't get the ruby/python scripts to work, so I wrote this.


# Requirements
ffprobe needs to be in PATH. Either run it from an appropriate environment or modify the code to include the correct directory like so:
```os.environ["PATH"] += os.pathsep + 'c:/programs/ffmpeg/bin'```

# Notes
The script has been only tested on Windows 10 / Python 3.10. It should work without modifications on Linux and Mac, but is not tested.
