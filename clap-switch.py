#!/usr/bin/env python3

# Clap Switcher script for VM-CLAP1 hand clap sensor and LIFX bulb.
# It's able to detect a clap sequence to avoid false clap-like sounds.

import logging
import tenacity as t

from gpiozero import Button
from lifxlan import LifxLAN
from lifxlan.errors import WorkflowException
from os import getenv
from socket import error as SocketError
from time import sleep, time

# Settings
GPIO_BUTTON = getenv('CLAP_SWITCH_GPIO_BUTTON', 2)
LIGHT_NAME = getenv('CLAP_SWITCH_LIGHT_NAME', 'Main')
LIGHT_BRIGHT = getenv('CLAP_SWITCH_LIGHT_BRIGHT', 65535)  # 100%
LIGHT_TEMP = getenv('CLAP_SWITCH_LIGHT_TEMP', 4000)  # Kelvin
# Count of sequential claps to toggle
CLAP_COUNT = int(getenv('CLAP_SWITCH_CLAP_COUNT', 2))
# Time interval in seconds to fit clap sequence
SEQ_ALLOWANCE = float(getenv('CLAP_SWITCH_SEQ_ALLOWANCE', 3.0))
# Should we wait for acknowledge from the bulb
RAPID = bool(getenv('CLAP_SWITCH_RAPID', False))
LOG_LEVEL = getenv('CLAP_SWITCH_LOG_LEVEL', 'INFO').upper()
# Number of retries if error occured
RETRY_COUNT = getenv('CLAP_SWITCH_RETRY_COUNT', 2)

LOG_FORMAT = '%(asctime)s - [%(levelname)s] - %(message)s'

# VM-CLAP1 output pin goes low for 40ms.
SCRIPT_SLOWINESS = 0.04


startup_msg_tpl = 'LIFX LAMP CLAP SWITCHER ' + \
                  'for {} light, on {} claps in {} seconds'

logging.basicConfig(format=LOG_FORMAT,
                    level=LOG_LEVEL)

log = logging.getLogger(__name__)


@t.retry(reraise=True, stop=t.stop_after_attempt(RETRY_COUNT),
         before=t.before_log(log, logging.DEBUG),
         retry=t.retry_if_exception_type(WorkflowException))
def toggle_lights(device):
    try:
        if device.get_power() == 0:
            log.info('Turning ON...')
            device.set_power(1, rapid=RAPID)
            sleep(0.5)
            device.set_brightness(LIGHT_BRIGHT, rapid=RAPID)
            device.set_colortemp(LIGHT_TEMP, rapid=RAPID)
        else:
            log.info('Turning OFF...')
            device.set_power(0, rapid=RAPID)
    except (WorkflowException, SocketError) as err:
        log.exception('Boom!')


def main():
    lifxlan = LifxLAN()
    clap = Button(GPIO_BUTTON)

    log.info(startup_msg_tpl.format(LIGHT_NAME,
                                    CLAP_COUNT,
                                    SEQ_ALLOWANCE))
    r = t.Retrying(reraise=True,
                   stop=t.stop_after_attempt(RETRY_COUNT),
                   retry=t.retry_if_exception_type(WorkflowException))

    group = r.call(lifxlan.get_devices_by_name, LIGHT_NAME)
    device = group.devices[0]
    log.info('Ready for input...')

    while True:
        # sleep is to slow the script down, so it consumes less CPU
        sleep(SCRIPT_SLOWINESS)
        counter = 0
        if clap.is_active:
            first_clap = time()
            while time()-first_clap < SEQ_ALLOWANCE:
                # VM-CLAP1 button should be still active at this point,
                # so we count our first clap
                if clap.is_active:
                    counter += 1
                    log.debug('COUNTER: {}/{}'.format(counter, CLAP_COUNT))
                if counter == CLAP_COUNT:
                    toggle_lights(device)
                    break
                sleep(SCRIPT_SLOWINESS)


if __name__ == '__main__':
    main()
