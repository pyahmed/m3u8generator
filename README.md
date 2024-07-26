# m3u8generator
Generate an m3u8 playlist with byteranges for serving a single TS file via HLS

This script runs ffprobe to obtain data (pkt_pos and pts_time) for I-frames in a given MPEG-TS file. It then creates an m3u8 playlist that contains those positions and the durations of those "segments". This allows serving large TS-files via HLS without requiring splitting or repackaging with just a simple web server.

# Requirements
ffprobe needs to be in PATH. Either run it from an appropriate environment or modify the code to include the correct directory like so:
```os.environ["PATH"] += os.pathsep + 'c:/programs/ffmpeg/bin'```

# Notes
The script has been only tested on Windows 10 / Python 3.10. It should work without modifications on Linux and Mac, but is not tested.
