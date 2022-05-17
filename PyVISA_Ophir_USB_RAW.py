# -*- coding: utf-8 -*-
"""
******************************************************************************
Created on Thu Apr 29 15:53:25 2021
@author: David Pih
This program queries Ophir Power Sensor with Juno USB Interface.
******************************************************************************
Program starts as follows:
"""
print('File:', __file__)
print(__doc__)

# import module
import pyvisa
import re

# create Ophir command / query list
Ophir_Command_List = ['hi', 'ii', 'fe', 'wi 5', 'wl 2100', 'wn 1', 'pl 2', 
                      'ut 106', 'mm', 'aw', 'ar', 'pl', 'ut', 'se']

# Ophir's usb_control_out parameters
request_type = 0x40
request_id = 0x02
request_value = 0
index = 0

# Ophir's usb_control_in parameters
rReqType = 0xC0
rReq = 0x04
rLength = 0x78

# Ophir_Address = 'USB0::0x0BD3::0x0777::NI-VISA-10001::RAW'
OphirAddress = pyvisa.ResourceManager().list_resources('USB?::0x0BD3?*')[0]
print('Found Ophir Juno at ' + OphirAddress + '.')

# Open Ophir
Ophir = pyvisa.highlevel.ResourceManager().open_resource(OphirAddress)
print('Opened ' + OphirAddress + '.')
print('Query results:')

# query each command in Ophir command list
for command in Ophir_Command_List:
    # assemble Ophir command format starting with '$' and ending with '\n'
    commando = '$' + command + '\n'
    # USB Raw Write
    Ophir.visalib.usb_control_out(Ophir.session, request_type, request_id, 
                                  request_value, index, commando)
    #USB Raw Read
    read = Ophir.visalib.usb_control_in(Ophir.session, rReqType, rReq, 
                                         request_value, index, rLength)[0]
    # Get rid of '\n' in response
    read2 = re.sub(r'\n', '', read.decode('ascii'))
    # Get rid of '*' in response
    read3 = re.sub(r'\*', '', read2)
    # Get rid of space in the first of read string
    if read3 == '':
        read4 = read3
    elif read3[0] ==' ':
        read4 = re.sub(r' ', '', read3, 1)
    # print command and corresponding response from Juno USB Interface
    print(command + ': ' + read4)

# print('implementation_version:', Ophir.implementation_version)
# print('interface_number:', Ophir.interface_number)
# print('interface_type:', Ophir.interface_type)
# print('lock_state:', Ophir.lock_state)
# print('resource_class:', Ophir.resource_class)
print('resource_manufacturer_name:', Ophir.resource_manufacturer_name)
print('resource_name:', Ophir.resource_name)
print('session:', Ophir.session)
# print('spec_version:', Ophir.spec_version)
# print('timeout:', Ophir.timeout)
# print('visa_attributes_classes:', Ophir.get_visa_attribute('VI_ATTR_RSRC_NAME'))
# print('visalib:', Ophir.visalib)
# print('resource_info:', Ophir.resource_info)
# print('__dict__:', Ophir.__dict__)
# print('_session:', Ophir._session)

# Close Ophir
Ophir.close()
print('Closed ' + OphirAddress + '.')