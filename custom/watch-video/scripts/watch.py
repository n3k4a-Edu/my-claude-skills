"""watch.py <video> [--every SECONDS] [--start S --end S] [--out DIR] [--lang ar|en|...] [--no-audio]

Turns a video into what Claude can read:
  - <out>/sheet_NNN.jpg : 4x4 frames per sheet, time-ordered, each frame stamped with its time
  - <out>/transcript.txt : timestamped speech (faster-whisper, GPU if available)
  - <out>/summary.txt    : duration, time range of each sheet, loudness per 10 s
"""
import argparse
import os
import subprocess

import numpy as np

_LOCAL_FF = os.path.expanduser(os.path.join("~", "bin", "ffmpeg.exe"))
FF = _LOCAL_FF if os.path.exists(_LOCAL_FF) else "ffmpeg"


def duration(path):
    r = subprocess.run([FF, "-hide_banner", "-i", path], capture_output=True, text=True, encoding="utf-8", errors="ignore")
    for line in r.stderr.splitlines():
        if "Duration:" in line:
            h, m, s = line.split("Duration:")[1].split(",")[0].strip().split(":")
            return int(h) * 3600 + int(m) * 60 + float(s)
    return 0.0


def sheets(v, out, start, span, every):
    stamp = r"drawtext=text='%{pts\:hms\:" + str(start) + r"}':x=6:y=6:fontsize=22:fontcolor=yellow:box=1:boxcolor=black@0.6,"
    base = [FF, "-hide_banner", "-loglevel", "error", "-y", "-ss", str(start), "-t", str(span), "-i", v, "-vf"]
    target = os.path.join(out, "sheet_%03d.jpg")
    r = subprocess.run(base + [f"fps=1/{every},scale=480:-1," + stamp + "tile=4x4", target], capture_output=True)
    if r.returncode:  # no drawtext in this ffmpeg build: sheets without the time stamp
        subprocess.run(base + [f"fps=1/{every},scale=480:-1,tile=4x4", target], capture_output=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--every", type=float, default=0, help="seconds between frames (default: about 16 sheets)")
    ap.add_argument("--start", type=float, default=0)
    ap.add_argument("--end", type=float, default=0)
    ap.add_argument("--out", default=None)
    ap.add_argument("--lang", default=None)
    ap.add_argument("--no-audio", action="store_true")
    a = ap.parse_args()

    v = os.path.abspath(a.video)
    out = a.out or os.path.splitext(v)[0] + "_watch"
    os.makedirs(out, exist_ok=True)
    dur = duration(v)
    start = a.start
    end = a.end or dur
    span = max(1.0, end - start)
    every = a.every or max(1.0, span / (16 * 16))

    for f in os.listdir(out):
        if f.startswith("sheet_"):
            os.remove(os.path.join(out, f))
    sheets(v, out, start, span, every)
    names = sorted(f for f in os.listdir(out) if f.startswith("sheet_"))
    lines = [f"video: {v}",
             f"duration: {dur:.1f} s, frames every {every:.2f} s, {len(names)} sheets (16 frames each)"]
    for i, n in enumerate(names):
        t0 = start + i * 16 * every
        lines.append(f"  {n}: {t0:.0f}s - {min(end, t0 + 16 * every):.0f}s")

    # audio once: 16 kHz mono float32 from ffmpeg, used for loudness and speech
    r = subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-ss", str(start), "-t", str(span), "-i", v, "-vn",
                        "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True)
    audio = np.frombuffer(r.stdout, dtype=np.float32).copy() if r.returncode == 0 and r.stdout else None
    if audio is not None and len(audio):
        step = 16000 * 10
        db = []
        for k in range(0, len(audio), step):
            seg = audio[k:k + step]
            rms = float(np.sqrt(np.mean(seg * seg)))
            db.append("-" if rms <= 1e-6 else f"{20 * np.log10(rms):.0f}")
        lines.append(f"loudness (dB RMS) per 10 s from {start:.0f}s: " + " ".join(db))
    else:
        lines.append("no audio track")
    with open(os.path.join(out, "summary.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    if not a.no_audio and audio is not None and len(audio):
        try:
            from faster_whisper import WhisperModel
            try:
                model = WhisperModel("small", device="cuda", compute_type="float16")
                segs, info = model.transcribe(audio, language=a.lang, vad_filter=True)
                segs = list(segs)
            except Exception:
                model = WhisperModel("small", device="cpu", compute_type="int8")
                segs, info = model.transcribe(audio, language=a.lang, vad_filter=True)
                segs = list(segs)
            with open(os.path.join(out, "transcript.txt"), "w", encoding="utf-8") as f:
                f.write(f"language: {info.language} ({info.language_probability:.2f})\n")
                for sg in segs:
                    f.write(f"[{start + sg.start:7.1f}-{start + sg.end:7.1f}] {sg.text.strip()}\n")
        except Exception as e:
            with open(os.path.join(out, "transcript.txt"), "w", encoding="utf-8") as f:
                f.write(f"transcription failed: {e}\n")

    print(out)
    print("\n".join(lines[:2]))


if __name__ == "__main__":
    main()
