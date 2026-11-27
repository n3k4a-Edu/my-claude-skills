# Watching videos, making videos and demos

Open a skill with `skills/<name>/INSTRUCTIONS.md` (relative to this folder).

- **watch** — Watch a video (URL or local path). Downloads with yt-dlp, extracts auto-scaled frames with ffmpeg, pulls the transcript from captions (or local WhisperX / cloud Whisper fallback), and hands the result to the agent so… _(needs: yt-dlp and ffmpeg)_
- **watch-video** — Watch and listen to a local video file (mp4/mkv/webm/avi/mov...). Use whenever the user asks to watch, review, analyse, compare or "read" a video, or asks what is said/shown in it. Produces time-stamped contact sheets… _(needs: ffmpeg)_
- **video-editing** — AI-assisted video editing workflows for cutting, structuring, and augmenting real footage. Covers the full pipeline from raw capture through FFmpeg, Remotion, ElevenLabs, fal.ai, and final polish in Descript or CapCut.…
- **remotion-video-creation** — Best practices for Remotion - Video creation in React. 29 domain-specific rules covering 3D, animations, audio, captions, charts, transitions, and more. Use when building video in React with Remotion — animations,… _(needs: Node.js + Remotion)_
- **manim-video** — Build reusable Manim explainers for technical concepts, graphs, system diagrams, and product walkthroughs, then hand off to the wider ECC video stack if needed. Use when the user wants a clean animated explainer rather… _(needs: Python + manim)_
- **ui-demo** — Record polished UI demo videos using Playwright. Use when the user asks to create a demo, walkthrough, screen recording, or tutorial video of a web application. Produces WebM videos with visible cursor, natural pacing,… _(needs: Playwright)_
