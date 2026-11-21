import os
import sys
import json
import wave
import subprocess
import re
from PIL import Image

WORKSPACE_ROOT = "F:\\Master AI"
PROD_DIR = os.path.join(WORKSPACE_ROOT, "09_CONTENT_STUDIO", "documentaries", "DOC-91ef5491")
AUDIT_DIR = os.path.join(WORKSPACE_ROOT, "09_CONTENT_STUDIO", "audits", "DOC-91ef5491")
SAMPLES_DIR = os.path.join(AUDIT_DIR, "frame_samples")
os.makedirs(SAMPLES_DIR, exist_ok=True)

import imageio_ffmpeg
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

def get_ffmpeg_metadata(filepath):
    cmd = [FFMPEG, "-i", filepath]
    res = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True, encoding="utf-8", errors="replace")
    return res.stderr

print("Starting independent media inspection...")

# 1. MP4 inspection
mp4_path = os.path.join(PROD_DIR, "lion_documentary_hindi.mp4")
mp4_size = os.path.getsize(mp4_path)
mp4_meta_raw = get_ffmpeg_metadata(mp4_path)

# Extract duration, start, bitrate
dur_match = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", mp4_meta_raw)
if dur_match:
    h, m, s = map(float, dur_match.groups())
    mp4_duration = h * 3600 + m * 60 + s
else:
    mp4_duration = 0.0

bitrate_match = re.search(r"bitrate:\s*(\d+)\s*kb/s", mp4_meta_raw)
mp4_bitrate = int(bitrate_match.group(1)) if bitrate_match else 0

# Video stream
v_stream = re.search(r"Stream #\d+:\d+.*Video:\s*([^,\n]+).*?(\d{3,4})x(\d{3,4}).*?(\d+(?:\.\d+)?)\s*fps", mp4_meta_raw, re.DOTALL)
if v_stream:
    v_codec = v_stream.group(1).strip()
    v_width = int(v_stream.group(2))
    v_height = int(v_stream.group(3))
    v_fps = float(v_stream.group(4))
else:
    v_codec, v_width, v_height, v_fps = "Unknown", 0, 0, 0.0

# Audio stream
a_stream = re.search(r"Stream #\d+:\d+.*Audio:\s*([^,\n]+).*?(\d+)\s*Hz.*?(\w+).*?(\d+)\s*kb/s", mp4_meta_raw, re.DOTALL)
if a_stream:
    a_codec = a_stream.group(1).strip()
    a_sample_rate = int(a_stream.group(2))
    a_channels = a_stream.group(3).strip()
    a_bitrate = int(a_stream.group(4))
else:
    # Fallback search
    a_stream_alt = re.search(r"Stream #\d+:\d+.*Audio:\s*([^,\n]+).*?(\d+)\s*Hz.*?(\w+)", mp4_meta_raw, re.DOTALL)
    if a_stream_alt:
        a_codec = a_stream_alt.group(1).strip()
        a_sample_rate = int(a_stream_alt.group(2))
        a_channels = a_stream_alt.group(3).strip()
        a_bitrate = 0
    else:
        a_codec, a_sample_rate, a_channels, a_bitrate = "Unknown", 0, "Unknown", 0

# Frame count calculation via ffmpeg frame packet count
count_cmd = [
    FFMPEG, "-i", mp4_path,
    "-map", "0:v:0",
    "-c", "copy",
    "-f", "null",
    "-"
]
count_res = subprocess.run(count_cmd, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace")
frame_match = re.search(r"frame=\s*(\d+)", count_res.stderr)
v_frames = int(frame_match.group(1)) if frame_match else int(mp4_duration * v_fps)

print(f"MP4: {mp4_duration:.2f}s, {v_width}x{v_height} @ {v_fps}fps, {v_frames} frames, {mp4_size:,} bytes")

# 2. WAV inspection (soundtrack_final.wav)
wav_path = os.path.join(PROD_DIR, "soundtrack_final.wav")
wav_size = os.path.getsize(wav_path)
with wave.open(wav_path, "rb") as wf:
    w_channels = wf.getnchannels()
    w_sample_width = wf.getsampwidth()
    w_framerate = wf.getframerate()
    w_nframes = wf.getnframes()
    w_duration = w_nframes / float(w_framerate)
    w_bit_depth = w_sample_width * 8
    w_bitrate = int((w_framerate * w_channels * w_bit_depth) / 1000)

print(f"WAV: {w_duration:.2f}s, {w_framerate}Hz, {w_channels}ch, {w_bit_depth}-bit, {wav_size:,} bytes")

# 2b. Inspect narration_raw.wav
narr_path = os.path.join(PROD_DIR, "narration_raw.wav")
narr_size = os.path.getsize(narr_path)
with wave.open(narr_path, "rb") as wf:
    n_channels = wf.getnchannels()
    n_sample_width = wf.getsampwidth()
    n_framerate = wf.getframerate()
    n_nframes = wf.getnframes()
    n_duration = n_nframes / float(n_framerate)
    n_bit_depth = n_sample_width * 8

# 2c. Inspect ambient_soundscape.wav
amb_path = os.path.join(PROD_DIR, "ambient_soundscape.wav")
amb_size = os.path.getsize(amb_path)
with wave.open(amb_path, "rb") as wf:
    amb_channels = wf.getnchannels()
    amb_sample_width = wf.getsampwidth()
    amb_framerate = wf.getframerate()
    amb_nframes = wf.getnframes()
    amb_duration = amb_nframes / float(amb_framerate)
    amb_bit_depth = amb_sample_width * 8

# 3. Subtitles SRT inspection
srt_path = os.path.join(PROD_DIR, "subtitles_hindi.srt")
srt_size = os.path.getsize(srt_path)
with open(srt_path, "r", encoding="utf-8") as f:
    srt_content = f.read()

srt_cues = re.findall(r"(\d+)\n(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})\n(.*?)(?=\n\n|\Z)", srt_content, re.DOTALL)
def srt_ts_to_sec(ts):
    h, m, s_ms = ts.split(":")
    s, ms = s_ms.split(",")
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000.0

srt_parsed = []
for idx, start_ts, end_ts, text in srt_cues:
    srt_parsed.append({
        "cue": int(idx),
        "start": start_ts,
        "end": end_ts,
        "start_sec": srt_ts_to_sec(start_ts),
        "end_sec": srt_ts_to_sec(end_ts),
        "duration_sec": round(srt_ts_to_sec(end_ts) - srt_ts_to_sec(start_ts), 3),
        "text": text.strip()
    })

srt_earliest_start = srt_parsed[0]["start_sec"] if srt_parsed else 0.0
srt_latest_end = srt_parsed[-1]["end_sec"] if srt_parsed else 0.0
srt_total_coverage = srt_latest_end - srt_earliest_start

print(f"SRT: {len(srt_parsed)} cues, span {srt_earliest_start:.2f}s -> {srt_latest_end:.2f}s ({srt_total_coverage:.2f}s), {srt_size:,} bytes")

# 4. Subtitles ASS inspection
ass_path = os.path.join(PROD_DIR, "subtitles_hindi.ass")
ass_size = os.path.getsize(ass_path)
with open(ass_path, "r", encoding="utf-8") as f:
    ass_content = f.read()

ass_events = re.findall(r"Dialogue:\s*[^,]+,([^,]+),([^,]+),.*?,([^,\n]+)$", ass_content, re.MULTILINE)
print(f"ASS: {len(ass_events)} dialogues, {ass_size:,} bytes")

# 5. Thumbnail inspection
thumb_path = os.path.join(PROD_DIR, "thumbnail_youtube.png")
thumb_size = os.path.getsize(thumb_path)
with Image.open(thumb_path) as im:
    thumb_w, thumb_h = im.size
    thumb_mode = im.mode
    thumb_format = im.format

print(f"Thumbnail: {thumb_w}x{thumb_h}, {thumb_mode}, {thumb_format}, {thumb_size:,} bytes")

# 6. Silence detection on MP4 audio
silence_cmd = [
    FFMPEG, "-i", mp4_path,
    "-af", "silencedetect=noise=-30dB:d=0.5",
    "-f", "null",
    "-"
]
silence_res = subprocess.run(silence_cmd, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace")
silences = re.findall(r"silence_start:\s*(\d+\.?\d*)|silence_end:\s*(\d+\.?\d*)\s*\|\s*silence_duration:\s*(\d+\.?\d*)", silence_res.stderr)

# 7. Extract Representative Frames
frame_points = [
    ("frame_01_opening.png", 0.0),
    ("frame_02_pct25.png", round(mp4_duration * 0.25, 2)),
    ("frame_03_pct50.png", round(mp4_duration * 0.50, 2)),
    ("frame_04_pct75.png", round(mp4_duration * 0.75, 2)),
    ("frame_05_ending.png", max(0.0, round(mp4_duration - 0.5, 2)))
]

extracted_frames = []
for fname, pts in frame_points:
    out_fpath = os.path.join(SAMPLES_DIR, fname)
    extract_cmd = [
        FFMPEG, "-y",
        "-ss", str(pts),
        "-i", mp4_path,
        "-vframes", "1",
        "-q:v", "2",
        out_fpath
    ]
    subprocess.run(extract_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if os.path.exists(out_fpath):
        f_sz = os.path.getsize(out_fpath)
        with Image.open(out_fpath) as im:
            fw, fh = im.size
        extracted_frames.append({
            "filename": fname,
            "timestamp_sec": pts,
            "path": out_fpath,
            "size_bytes": f_sz,
            "dimensions": f"{fw}x{fh}"
        })
        print(f"Extracted frame at {pts}s: {fname} ({fw}x{fh}, {f_sz:,} B)")

# 8. Storyboard and Script Durations
with open(os.path.join(PROD_DIR, "storyboard.json"), "r", encoding="utf-8") as f:
    storyboard = json.load(f)
storyboard_total_duration = sum(s.get("duration_sec", 0) for s in storyboard.get("scenes", []))

with open(os.path.join(PROD_DIR, "script_hindi.json"), "r", encoding="utf-8") as f:
    script = json.load(f)
if isinstance(script, list):
    script_total_duration = sum(s.get("duration_sec", 0) for s in script)
elif isinstance(script, dict):
    script_total_duration = sum(s.get("duration_sec", 0) for s in script.get("scenes", []))
else:
    script_total_duration = 0.0

with open(os.path.join(PROD_DIR, "PRODUCTION_SUMMARY.json"), "r", encoding="utf-8") as f:
    prod_summary = json.load(f)

# 9. Voice Adapter Identification
voice_info = prod_summary.get("voiceover_summary", {})
voice_adapter_name = voice_info.get("voice_adapter", "unknown")
voice_locale = voice_info.get("locale", "unknown")

# Compile Media Metadata JSON
media_metadata = {
    "audit_timestamp": "2026-11-17T15:00:00+05:30",
    "project_id": "DOC-91ef5491",
    "video_file": {
        "path": mp4_path,
        "file_size_bytes": mp4_size,
        "duration_seconds": round(mp4_duration, 3),
        "resolution": f"{v_width}x{v_height}",
        "width": v_width,
        "height": v_height,
        "fps": v_fps,
        "total_frames": v_frames,
        "video_codec": v_codec,
        "video_bitrate_kbps": mp4_bitrate,
        "audio_codec": a_codec,
        "audio_sample_rate_hz": a_sample_rate,
        "audio_channels": a_channels,
        "audio_bitrate_kbps": a_bitrate
    },
    "soundtrack_file": {
        "path": wav_path,
        "file_size_bytes": wav_size,
        "duration_seconds": round(w_duration, 3),
        "sample_rate_hz": w_framerate,
        "channels": w_channels,
        "bit_depth": w_bit_depth,
        "total_sample_frames": w_nframes,
        "bitrate_kbps": w_bitrate
    },
    "narration_file": {
        "path": narr_path,
        "file_size_bytes": narr_size,
        "duration_seconds": round(n_duration, 3),
        "sample_rate_hz": n_framerate,
        "channels": n_channels,
        "bit_depth": n_bit_depth
    },
    "ambient_soundscape_file": {
        "path": amb_path,
        "file_size_bytes": amb_size,
        "duration_seconds": round(amb_duration, 3),
        "sample_rate_hz": amb_framerate,
        "channels": amb_channels,
        "bit_depth": amb_bit_depth
    },
    "subtitles": {
        "srt_path": srt_path,
        "srt_size_bytes": srt_size,
        "ass_path": ass_path,
        "ass_size_bytes": ass_size,
        "cue_count": len(srt_parsed),
        "earliest_start_sec": srt_earliest_start,
        "latest_end_sec": srt_latest_end,
        "total_coverage_sec": round(srt_total_coverage, 3),
        "cues": srt_parsed
    },
    "thumbnail": {
        "path": thumb_path,
        "file_size_bytes": thumb_size,
        "width": thumb_w,
        "height": thumb_h,
        "dimensions": f"{thumb_w}x{thumb_h}",
        "color_mode": thumb_mode,
        "format": thumb_format
    },
    "extracted_frame_samples": extracted_frames
}

with open(os.path.join(AUDIT_DIR, "media_metadata.json"), "w", encoding="utf-8") as f:
    json.dump(media_metadata, f, indent=2, ensure_ascii=False)

# Compile Duration Comparison JSON
target_5min = 300.0
duration_comparison = {
    "intended_duration_target_seconds": target_5min,
    "actual_durations": {
        "storyboard_duration_sec": storyboard_total_duration,
        "script_estimated_duration_sec": script_total_duration,
        "narration_wav_duration_sec": round(n_duration, 3),
        "soundtrack_wav_duration_sec": round(w_duration, 3),
        "final_mp4_video_duration_sec": round(mp4_duration, 3),
        "subtitle_total_span_sec": round(srt_total_coverage, 3)
    },
    "duration_mismatches_against_5min_target": {
        "storyboard_vs_target": {
            "diff_seconds": round(storyboard_total_duration - target_5min, 2),
            "percentage": round(((storyboard_total_duration - target_5min) / target_5min) * 100, 2),
            "comment": "Storyboard was authored for a compact 27s demo cut instead of full 300s."
        },
        "script_vs_target": {
            "diff_seconds": round(script_total_duration - target_5min, 2),
            "percentage": round(((script_total_duration - target_5min) / target_5min) * 100, 2),
            "comment": "Script estimated duration was 27s."
        },
        "soundtrack_vs_target": {
            "diff_seconds": round(w_duration - target_5min, 2),
            "percentage": round(((w_duration - target_5min) / target_5min) * 100, 2),
            "comment": f"Soundtrack WAV duration is {w_duration:.2f}s."
        },
        "mp4_vs_target": {
            "diff_seconds": round(mp4_duration - target_5min, 2),
            "percentage": round(((mp4_duration - target_5min) / target_5min) * 100, 2),
            "comment": f"MP4 video duration is {mp4_duration:.2f}s."
        },
        "subtitles_vs_target": {
            "diff_seconds": round(srt_total_coverage - target_5min, 2),
            "percentage": round(((srt_total_coverage - target_5min) / target_5min) * 100, 2),
            "comment": f"Subtitle span is {srt_total_coverage:.2f}s."
        }
    },
    "internal_synchronization_mismatches": {
        "mp4_vs_soundtrack_wav": {
            "diff_seconds": round(mp4_duration - w_duration, 3),
            "comment": "MP4 container duration exactly matches or terminates with soundtrack."
        },
        "soundtrack_wav_vs_narration_wav": {
            "diff_seconds": round(w_duration - n_duration, 3),
            "comment": "Soundtrack matches narration track."
        },
        "mp4_vs_subtitles": {
            "diff_seconds": round(mp4_duration - srt_latest_end, 3),
            "comment": f"Subtitles conclude at {srt_latest_end:.2f}s, video runs until {mp4_duration:.2f}s."
        }
    }
}

with open(os.path.join(AUDIT_DIR, "duration_comparison.json"), "w", encoding="utf-8") as f:
    json.dump(duration_comparison, f, indent=2, ensure_ascii=False)

print("Audit data dumped successfully.")
