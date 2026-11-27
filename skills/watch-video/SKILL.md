---
name: watch-video
description: Watch and listen to a local video file (mp4/mkv/webm/avi/mov...). Use whenever the user asks to watch, review, analyse, compare or "read" a video, or asks what is said/shown in it. Produces time-stamped contact sheets you read as images plus a timestamped speech transcript (faster-whisper on the GPU) and a loudness timeline.
---
# Watch a video

1. Run: `python "<this skill's base directory>/scripts/watch.py" "<video path>" [--every SECONDS] [--start S --end S] [--lang ar|en] [--no-audio]`
   - default spacing gives about 16 sheets; long videos: first pass with a large `--every`, then zoom into the
     interesting part with `--start/--end` and a small `--every` (e.g. 0.5).
   - output folder `<video>_watch/` (or `--out DIR`): `sheet_NNN.jpg` (4x4 frames, time burned into each frame),
     `transcript.txt` (`[start-end] text`), `summary.txt` (sheet time ranges + loudness per 10 s).
2. Read `summary.txt` and `transcript.txt` first, then Read the sheets (images). Many sheets: hand batches of
   ~12 sheets to subagents so the image limit per context is not hit.
3. Report with timestamps (mm:ss) so the user can check the moment.

Bink2 (.bk2, game videos): convert first with RAD Video Tools:
`radvideo64.exe binkconv "<in.bk2>" "<out.avi>" /O /#` (C:\Program Files (x86)\RADVideo), then run watch.py on the avi
and delete the avi (it is uncompressed, GBs).
