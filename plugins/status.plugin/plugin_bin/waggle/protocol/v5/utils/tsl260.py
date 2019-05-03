# ANL:waggle-license
# This file is part of the Waggle Platform.  Please see the file
# LICENSE.waggle.txt for the legal details of the copyright and software
# license.  For more details on the Waggle project, visit:
#          http://www.wa8.gl
# ANL:waggle-license
# Conversion for TSL260 light sensor

def convert(value):
    raw_l = value['lightsense_tsl260_light']

    # MCP output code transform factor 0.065 mV/(uW/cm^2): MCP mux
    value_voltage = raw_l * 0.0000625
    # voltage divider factor 5/2 to calc input voltage: voltage divider circuit
    value_voltage_divider = (value_voltage * 5.00) / 2.00

    # input unit: V, irrad unit: uW/cm^2
    irrad = (value_voltage_divider - 0.006250) / 0.058

    irrad_rounded = round(irrad, 3)
    value['lightsense_tsl260_light'] = (irrad_rounded, 'uW/cm^2')
    # value['lightsense_tsl260_light'] = (raw_l, 'raw')

    return value
