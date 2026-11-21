import numpy as np
import soundfile as sf
import os

sfx_dir = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\oracle_cloud_reel\sfx"
os.makedirs(sfx_dir, exist_ok=True)
sr = 44100

def gen_pop(fname):
    # Quick bubble/card pop (120ms, pitch drop 800Hz -> 200Hz)
    t = np.linspace(0, 0.12, int(0.12 * sr), False)
    freq = np.linspace(800, 200, len(t))
    env = np.exp(-t * 35)
    wave = np.sin(2 * np.pi * freq * t) * env * 0.4
    sf.write(os.path.join(sfx_dir, fname), wave, sr)

def gen_chime(fname):
    # Pleasant bell/chime (600ms, two harmonic tones 1046Hz + 1318Hz)
    t = np.linspace(0, 0.6, int(0.6 * sr), False)
    env = np.exp(-t * 6)
    wave = (0.5 * np.sin(2 * np.pi * 1046 * t) + 0.3 * np.sin(2 * np.pi * 1318 * t)) * env * 0.35
    sf.write(os.path.join(sfx_dir, fname), wave, sr)

def gen_alarm(fname):
    # Digital alert beep (300ms, pulsing 880Hz)
    t = np.linspace(0, 0.35, int(0.35 * sr), False)
    env = np.ones_like(t)
    env[int(len(t)*0.8):] = np.linspace(1, 0, len(t) - int(len(t)*0.8))
    wave = np.sin(2 * np.pi * 880 * t) * env * 0.3
    sf.write(os.path.join(sfx_dir, fname), wave, sr)

def gen_whoosh(fname):
    # White noise sweep (200ms)
    t = np.linspace(0, 0.22, int(0.22 * sr), False)
    noise = np.random.uniform(-1, 1, len(t))
    env = np.sin(np.pi * t / 0.22) ** 2
    wave = noise * env * 0.25
    sf.write(os.path.join(sfx_dir, fname), wave, sr)

gen_pop("pop.wav")
gen_chime("chime.wav")
gen_alarm("alarm.wav")
gen_whoosh("whoosh.wav")
print("Generated broadcast SFX successfully!")
