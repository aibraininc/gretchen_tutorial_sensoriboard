#!/usr/bin/python

from src.sensorimotor import Sensorimotor
from time import sleep

def print_position(data):
    print(''.join('{0: .2f} '.format(k) for k in data))

def main():
    motors = Sensorimotor(number_of_motors=2, verbose=False)

    try:
        # Check for motors
        N = motors.ping()
        print("Found {0} motors.".format(N))
        sleep(1.0)

        #voltage limit for supply voltage and desired max. motor speed
        motors.set_voltage_limit([0.16, 0.16])
        # Start motors
        motors.start()

        #TODO: set this parameters according to your desired motor positon control behaviour
        motors.set_pos_ctrl_params(0, Kp = 0, Ki = 0, Kd = 0, deadband = 0, pulse_threshold = 0)
        motors.set_pos_ctrl_params(1, Kp = 0, Ki = 0, Kd = 0, deadband = 0, pulse_threshold = 0)

        motors.set_position([0.3, 0.3])
        sleep(1.5)

		# Print the current position
        print_position(motors.get_position())

        motors.set_position([-0.3, -0.3])
        sleep(1.5)

		# Print the current position
        print_position(motors.get_position())

        motors.stop()

    except (KeyboardInterrupt, SystemExit):
        # Stop motors
        print("\rAborted, stopping motors")
        motors.stop()

    except:
        # Script crashed?
        print("\rException thrown, stopping motors")
        motors.stop()

    print("____\nDONE.")

if __name__ == "__main__":
    main()
