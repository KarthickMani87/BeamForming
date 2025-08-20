Beamforming with Multiprocessing, UDP Data Handling, and Visualization

This project implements a real-time beamforming system in Python using multiprocessing for parallel FFT computations, UDP for network-based data streaming, and PyQtGraph/Matplotlib for visualization.
The system simulates/receives multi-channel array data, applies beamforming with adjustable parameters (angles, array spacing, sound velocity), and displays results in real-time.

Features

📡 UDP Receive: Stream array sensor data over UDP.
🔀 Multiprocessing: Parallel FFT-based power calculation for beamforming.
🎛 Beamforming: Delay-and-sum approach with configurable array spacing, sampling rate, and scanning angles.
📊 Visualization: Real-time GUI plotting via pyqtgraph and matplotlib.
⚡ High performance: Uses multiprocessing.Queue to distribute computation across CPU cores.

📂 Project Structure
.
├── BeamFormFFT.py            # Core beamforming functions (FFT, power calculations)
├── FFTMultiProcess.py        # Multiprocessing-based FFT routines
├── MainFun.py                # Main entry function (launches UDP recv, beamforming, GUI)
├── PlotExampleCanvas.py      # Example canvas for PyQt plotting
├── PlotSpectrum.py           # Spectrum plotting utilities
├── PyQtExampes.py            # Example PyQt GUI snippets
├── PyQtGradientDisplay.py    # Gradient display widget for beamforming results
├── ShipSignal.wav            # Example input signal (for testing beamforming)
├── UdpRecv.py                # UDP data receiver, manages ArrayData buffer
├── UdpSend.py                # UDP data sender (for simulation/testing)
├── UpdateGUI.py              # Real-time GUI process for visualization
├── README.md                 # Documentation (this file)

🔑 Key Modules

MainFun.py
Orchestrates the workflow: starts UDP receiver, GUI process, and calls the beamforming loop.

BeamFormFFT.py / FFTMultiProcess.py
Contain the core signal processing: FFT, delay-and-sum beamforming, power computation across angles, and multiprocessing helpers.

UdpRecv.py & UdpSend.py

UdpRecv.py: Receives array data packets and buffers them into ArrayData.

UdpSend.py: Test utility to simulate array data over UDP.

UpdateGUI.py
Handles PyQt-based visualization of beamforming results in real-time.

Plotting Utilities (PlotSpectrum.py, PlotExampleCanvas.py, PyQtExampes.py, PyQtGradientDisplay.py)
Provide different spectrum and energy plotting GUIs, as well as PyQt examples for display.

ShipSignal.wav
Sample dataset for testing beamforming without real-time UDP input.


Configuration

Modify the following parameters in main.py as needed:

UDP_IP     = "127.0.0.1"   # IP for UDP data stream
UDP_PORT   = 5015          # UDP port

Dist       = 0.09          # Array element spacing (meters)
cSound     = 1500          # Speed of sound (m/s)
NumArr     = 16            # Number of array elements

MinAngle   = 0             # Beamforming scan start angle
MaxAngle   = 180           # Beamforming scan end angle
AngleJump  = 5             # Angular resolution

LISTSIZE   = 205           # Buffer size per array element
SamplingRate = 16000       # Sampling rate (Hz)


Running

Start the system with:

python main.py


This will:

Start a UDP receiver thread (Recv_Data) to collect array input data.
Launch the GUI process (GUIProcess) to visualize results.
Run the beamforming loop (ReadArrayDataAndProcess) to process input data and compute beam power across scan angles.


Data Flow

UDP Receiver (UdpRecv.py)
Collects incoming multi-channel data into ArrayData.

Beamforming Process (ReadArrayDataAndProcess)

Buffers array data into inpData.

Applies Hann windowing.

Distributes tasks across worker processes (Calc_Power_From_NetworkMP).

Computes delay-and-sum power for each steering angle.

Visualization (UpdateGUI.py)

Plots energy distribution vs. angle.

Displays strongest beam direction in real-time.


Notes

The UDP sender (data generator) is not included; you must stream raw array data into the specified UDP_IP and UDP_PORT.
The visualization process is designed to run in parallel; make sure GUI libraries are installed correctly.
Performance scales with CPU cores thanks to multiprocessing.

Future Work

Add record & playback mode for offline testing.
Implement GPU acceleration (e.g., with CuPy).
Extend visualization with 2D/3D beam pattern plots.
