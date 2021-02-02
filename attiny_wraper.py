import attiny
from smbus2 import SMBus
from warnings import warn

i2cbus = SMBus(1)

i2caddress = attiny.TWI_SLAVE_ADDRESS

def readFlags():
    return i2cbus.read_byte_data(i2caddress, attiny.FLAGS)

# 1 means answer is True, 0 means False
def isButtonPressed():
    return i2cbus.read_byte_data(i2caddress, attiny.FLAGS) >> (attiny.FLAGS_BUTTON) & 0x01

def isBatteryCharging():
    return ~ (i2cbus.read_byte_data(i2caddress, attiny.FLAGS) >> (attiny.FLAGS_CHG) & 0x01)

def isBoostRunning():
    return ~ (i2cbus.read_byte_data(i2caddress, attiny.FLAGS) >> (attiny.FLAGS_BOOST) & 0x01)

def isInputVoltagePresent():
    return ~ (i2cbus.read_byte_data(i2caddress, attiny.FLAGS) >> (attiny.FLAGS_AOK) & 0x01)

def isChargeActive():
    return (i2cbus.read_byte_data(i2caddress, attiny.FLAGS) >> (attiny.FLAGS_CHARGE_OFF) & 0x01)

def isBoostActive():
    return (i2cbus.read_byte_data(i2caddress, attiny.FLAGS) >> (attiny.FLAGS_BOOST_OFF) & 0x01)

def readTime():
    time = i2cbus.read_i2c_block_data(i2caddress,attiny.UNIX_TIME,attiny.UNIX_TIME_LENGTH) 
    return time[0]+(time[1]<<8)+(time[2]<<16)+(time[3]<<24)

def writeTime():
    import time
    t = int(time.time())
    print(t)
    i2cbus.write_byte_data(i2caddress, attiny.UNIX_TIME, t)
    i2cbus.write_byte_data(i2caddress, attiny.UNIX_TIME+1, t>>8)
    i2cbus.write_byte_data(i2caddress, attiny.UNIX_TIME+2, t>>16)
    i2cbus.write_byte_data(i2caddress, attiny.UNIX_TIME+3, t>>24)

def readVbat():
    Vbat = i2cbus.read_i2c_block_data(i2caddress,attiny.ADC_VBATT,attiny.ADC_VBATT_LENGTH) 
    return (Vbat[0]+(Vbat[1]<<8))

def readIB():
    ib = i2cbus.read_i2c_block_data(i2caddress,attiny.ADC_IB,attiny.ADC_IB_LENGTH) 
    return (ib[0]+(ib[1]<<8))

def readVin():
    VIN = i2cbus.read_i2c_block_data(i2caddress,attiny.ADC_VIN,attiny.ADC_VIN_LENGTH) 
    return (VIN[0]+(VIN[1]<<8))

def readFanSpeed():
    return i2cbus.read_byte_data(i2caddress,attiny.FAN_SPEED) 
    
def writeFanSpeed(speed):
    #fan speed in %
    try:
        i2cbus.write_byte_data(i2caddress,attiny.FAN_SPEED, speed) 
    except:
        warn("Fan speed probably made, but confirm with a read.")

print(readFlags())
print(readTime())
writeTime()
print(readTime())
print(readVbat())
print(readIB())
print(readVin())
print(readFanSpeed())
writeFanSpeed(50)
print(readFanSpeed())

print("Is button pressed")
print(isButtonPressed())
print("Is battery charging")
print(isBatteryCharging())
print("Is Boost running")
print(isBoostRunning())
print("Is Input voltage present")
print(isInputVoltagePresent())
print("Is Charge Active")
print(isChargeActive())
print("Is Boost Active")
print(isBoostActive())
