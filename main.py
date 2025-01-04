import pyaudio
import numpy as np
import soundfile as sf
import webrtcvad  # Voice Activity Detection (VAD)
import noisereduce as nr  # For noise reduction
import time
from collections import deque

# Audio parameters
RATE = 16000  # Audio sample rate (16kHz is common)
CHUNK_SIZE = 320  # Size of audio chunks (20 ms at 16kHz = 320 samples)
FORMAT = pyaudio.paInt16  # Audio format (16-bit PCM)
CHANNELS = 1  # Mono audio
OUTPUT_FILENAME = 'processed_audio.wav'  # Output file name

# Initialize PyAudio and WebRTC VAD
p = pyaudio.PyAudio()
vad = webrtcvad.Vad(3)  # Initialize WebRTC VAD (aggressive mode)

# Open audio stream for real-time capture
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=False,  # Disable direct playback to prevent echo
                frames_per_buffer=CHUNK_SIZE)

# Function for Voice Activity Detection (VAD)
def is_speech(input_chunk):
    """Check if the given audio chunk contains speech."""
    try:
        return vad.is_speech(input_chunk, RATE)
    except Exception as e:
        print(f"VAD Error: {e}")
        return False

# Function to measure and return latency
def measure_latency_and_clean(audio_chunk):
    """Measure latency and clean the audio chunk."""
    start_time = time.time()

    # Apply noise reduction
    cleaned_chunk = nr.reduce_noise(y=audio_chunk.astype(np.float32), sr=RATE).astype(np.int16)

    end_time = time.time()
    latency = (end_time - start_time) * 1000  # Convert to milliseconds
    print(f"Latency: {latency:.2f} ms")

    return cleaned_chunk

# Function to apply short-term energy threshold for smoothing
def apply_energy_threshold(audio_chunk, threshold=0.01):
    """Apply short-term energy threshold to reduce breaking out."""
    energy = np.sum(audio_chunk.astype(np.float32) ** 2) / len(audio_chunk)
    if energy < threshold:
        return np.zeros_like(audio_chunk)
    return audio_chunk

# Function to process audio for single speaker scenario
def process_single_speaker(audio_chunk):
    """Process audio to isolate and enhance the primary speaker."""
    # Apply noise reduction and latency measurement
    cleaned_chunk = measure_latency_and_clean(audio_chunk)
    # Apply energy threshold to smooth the audio
    smoothed_chunk = apply_energy_threshold(cleaned_chunk)
    return smoothed_chunk

# Function to process audio for multiple speakers scenario
def process_multiple_speakers(audio_chunk):
    """Process audio to preserve multiple speaker voices while filtering noise."""
    # Apply noise reduction and latency measurement
    cleaned_chunk = measure_latency_and_clean(audio_chunk)
    return cleaned_chunk

# Select the scenario to process
SCENARIO = 'single'  # Change to 'multiple' for multiple speakers scenario

# Create a file to save the processed audio
with sf.SoundFile(OUTPUT_FILENAME, 'w', samplerate=RATE, channels=CHANNELS) as file:
    print("Processing audio in real-time...")

    try:
        while True:
            # Read audio chunk from the microphone
            audio_chunk = np.frombuffer(stream.read(CHUNK_SIZE, exception_on_overflow=False), dtype=np.int16)
            if audio_chunk.size == 0:
                print("Empty chunk, skipping...")
                continue  # Skip empty chunks

            # Process the audio chunk based on the selected scenario
            if SCENARIO == 'single':
                processed_chunk = process_single_speaker(audio_chunk)
            elif SCENARIO == 'multiple':
                processed_chunk = process_multiple_speakers(audio_chunk)
            else:
                raise ValueError("Invalid scenario selected. Choose 'single' or 'multiple'.")

            # Ensure the processed chunk is of the correct length before VAD
            if len(processed_chunk) != CHUNK_SIZE:
                print("Processed chunk length mismatch. Skipping this chunk.")
                continue

            # If speech is detected, write to file
            if is_speech(processed_chunk.tobytes()):
                print("Speech detected, writing to file.")
                file.write(processed_chunk)
            else:
                # Write silence for non-speech
                print("No speech detected, writing silence.")
                file.write(np.zeros_like(processed_chunk))

    except KeyboardInterrupt:
        print("\nReal-time processing stopped by user.")
    finally:
        # Stop and close the stream gracefully
        stream.stop_stream()
        stream.close()
        p.terminate()
        print("Stream closed.")
