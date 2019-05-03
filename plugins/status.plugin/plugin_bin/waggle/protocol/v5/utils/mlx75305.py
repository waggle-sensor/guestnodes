# ANL:waggle-license
# This file is part of the Waggle Platform.  Please see the file
# LICENSE.waggle.txt for the legal details of the copyright and software
# license.  For more details on the Waggle project, visit:
#          http://www.wa8.gl
# ANL:waggle-license
#
# Conversion for MLX75305 light sense

def convert(value):
    raw_l = value['lightsense_mlx75305']

    # MCP output code transform factor 0.065 mV/(uW/cm^2): MCP mux
    value_voltage = raw_l * 0.0000625
    # voltage divider factor 5/2 to calc input voltage: voltage divider circuit
    value_voltage_divider = (value_voltage * 5.00) / 2.00

    converted_value = (value_voltage_divider - 0.09234) / 0.007   #with gain 1, the factor is 7mA/(uW/cm^2)

    converted_value_rounded = round(converted_value, 3)

    value['lightsense_mlx75305'] = (converted_value_rounded, 'uW/cm^2')
    # value['lightsense_mlx75305'] = (raw_l, 'raw')

    return value
