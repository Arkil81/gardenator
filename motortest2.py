from time import sleep
import pigpio

DIR = 2     # Direction GPIO Pin
STEP = 3    # Step GPIO Pin

# Connect to pigpiod daemon
pi = pigpio.pi()

# Set up pins as an output
pi.set_mode(DIR, pigpio.OUTPUT)
pi.set_mode(STEP, pigpio.OUTPUT)

def generate_ramp(ramp):
    """Generate ramp wave forms.
    ramp:  List of [Frequency, Steps]
    """
    pi.wave_clear()     # clear existing waves
    length = len(ramp)  # number of ramp levels
    wid = [-1] * length

    # Generate a wave per ramp level
    for i in range(length):
        frequency = ramp[i][0]
        micros = int(500000 / frequency)
        wf = []
        wf.append(pigpio.pulse(1 << STEP, 0, micros))  # pulse on
        wf.append(pigpio.pulse(0, 1 << STEP, micros))  # pulse off
        pi.wave_add_generic(wf)
        wid[i] = pi.wave_create()

    # Generate a chain of waves
    chain = []
    for i in range(length):
        steps = ramp[i][1]
        x = steps & 255
        y = steps >> 8
        chain += [255, 0, wid[i], 255, 1, x, y]

    pi.wave_chain(chain)  # Transmit chain.


# Ramp forwards until end, then switch direction and ramp backwards

pi.write(DIR, 0)  # Set direction

# Ramp forwards
generate_ramp([[320, 50],
	[500, 100],
	[800, 200],
	[1000, 4600],
	[800, 200],
	[500, 100],
	[320, 50]
])

while pi.wave_tx_busy():
    print("Sleeping...")
    sleep(0.1)


pi.stop()
