"""A simple implementation for controlling the SynthHD by windfreak.

  Typical usage example:

  SynthHDDevice('synth',com_port='COM4')

  Rabi_pulse = str.encode(str(float(Rabi_freq)))
  Pulse_amp = str.encode(str(Rabi_amp))
  synth.add_start_command(b'C0') #selects the channel to output RF
  synth.add_start_command(b'c0') #don't sweep continuous
  synth.add_start_command(b'W'+Pulse_amp)
  synth.add_start_command(b'f'+Rabi_pulse)
"""

import sys

if sys.version_info < (3, 6):
    raise RuntimeError("SynthHD strongly prefers Python 3.6+")
