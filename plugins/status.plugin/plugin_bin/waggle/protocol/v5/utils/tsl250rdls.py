# ANL:waggle-license
# This file is part of the Waggle Platform.  Please see the file
# LICENSE.waggle.txt for the legal details of the copyright and software
# license.  For more details on the Waggle project, visit:
#          http://www.wa8.gl
# ANL:waggle-license
# Conversion for TSL250RD in Lightsense

def convert(value):
    raw_l = value['lightsense_tsl250_light']

    # MCP output code transform factor 0.065 mV/(uW/cm^2): MCP mux
    value_voltage = raw_l * 0.0000625
    # voltage divider factor 5/2 to calc input voltage: voltage divider circuit
    value_voltage_divider = (value_voltage * 5.00) / 2.00

    # a = (math.log10(0.04)-math.log10(0.6))/(math.log10(0.6)-1)
    # b = math.log10(3)/(a*math.log10(50))
    # irrad = 10**((math.log10(input) - b)/a)

    irrad = (value_voltage_divider - 0.005781) / 0.064

    irrad_rounded = round(irrad, 3)
    value['lightsense_tsl250_light'] = (irrad_rounded, 'uW/cm^2')
    # value['lightsense_tsl250_light'] = (raw_l, 'raw')

    return value
