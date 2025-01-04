# Real-Time Noise Cancellation System

## Overview

This project implements a real-time noise cancellation system that processes live audio streams from a microphone input. The system is designed to handle two scenarios:
1. **Single Speaker Scenario**: Isolates and enhances the audio of one primary speaker while treating all other voices and background noises as interference to be minimized or eliminated.
2. **Multiple Speaker Scenario**: Preserves multiple speaker voices and simultaneously filters out environmental noise (e.g., white noise, workplace background noise, or vehicle noise).

The processed audio is saved as a `.wav` file.

## Requirements

- Python 3.x
- `pyaudio` for audio input
- `numpy` for numerical operations
- `soundfile` for audio file operations
- `webrtcvad` for voice activity detection
- `noisereduce` for noise reduction

## Installation

1. **Install Python and Pip**: Ensure you have Python 3 and pip installed.

2. **Install Required Packages**:
    ```bash
    pip install pyaudio numpy soundfile webrtcvad noisereduce
    ```

## Usage

1. **Run the Script**:
    - Ensure that your microphone is connected and working.
    - Set the `SCENARIO` variable to either `'single'` or `'multiple'` depending on the scenario you want to test.
    - Run the script:
      ```bash
      python noise_cancellation.py
      ```

2. **Process Audio**:
    - The script will process audio in real-time. It reads from the microphone, applies noise reduction, and saves the output to a `.wav` file.

## How It Works

### Key Functions:

- **Voice Activity Detection (VAD)**: Checks if a given audio chunk contains speech.
- **Noise Reduction and Latency Measurement**: Measures latency and cleans the audio chunk by applying noise reduction.
- **Energy Threshold Smoothing**: Applies a short-term energy threshold to reduce breaking out.
- **Single Speaker Processing**: Isolates and enhances the primary speaker's audio.
- **Multiple Speaker Processing**: Preserves multiple speakers' voices while filtering noise.

### Script Execution:

1. The script reads audio chunks from the microphone.
2. Based on the selected scenario (`single` or `multiple`), it processes the audio chunk.
3. The processed audio chunk is checked for speech activity.
4. If speech is detected, the chunk is written to the output file. Otherwise, silence is written.

## Testing

1. **Single Speaker Scenario**:
    - Set `SCENARIO = 'single'`.
    - Run the script and speak into the microphone with background noise.
    - Check `processed_audio.wav` to ensure the primary speaker's voice is clear and background noise is reduced.

2. **Multiple Speaker Scenario**:
    - Set `SCENARIO = 'multiple'`.
    - Run the script with multiple people speaking and some background noise.
    - Check `processed_audio.wav` to ensure all speakers' voices are preserved and background noise is reduced.

## Conclusion

This real-time noise cancellation system helps in isolating and enhancing speech while reducing background noise. It can be used in various scenarios such as meetings, interviews, or any situation requiring clear audio capture.

Feel free to contribute or suggest improvements!
