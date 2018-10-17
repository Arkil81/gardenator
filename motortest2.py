from time import sleep
import pigpio

DIR = 2     # Direction GPIO Pin
STEP = 3    # Step GPIO Pin
#SWITCH = 16  # GPIO pin of switch

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


# Set up input switch
#pi.set_mode(SWITCH, pigpio.INPUT)
#pi.set_pull_up_down(SWITCH, pigpio.PUD_UP)

#MODE = (14, 15, 18)   # Microstep Resolution GPIO Pins
#RESOLUTION = {'Full': (0, 0, 0),
#              'Half': (1, 0, 0),
#              '1/4': (0, 1, 0),
#              '1/8': (1, 1, 0),
#              '1/16': (0, 0, 1),
#              '1/32': (1, 0, 1)}
#for i in range(3):
#    pi.write(MODE[i], RESOLUTION['Full'][i])

# Set duty cycle and frequency
#pi.set_PWM_dutycycle(STEP, 128)  # PWM 1/2 On 1/2 Off
#pi.set_PWM_frequency(STEP, 500)  # 500 pulses per second

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

#sleep(1)

#pi.write(DIR, 1)  # Set direction

# Ramp backwards
#generate_ramp([[320, 50],
#	[500, 100],
#	[800, 200],
#	[1000, 4600],
#	[800, 200],
#	[500, 100],
#	[320, 50]
#])

pi.set_PWM_dutycycle(STEP, 0)  # PWM off
pi.stop()
