import time
import VL53L0X

# Create a VL53L0X object
tof = VL53L0X.VL53L0X(i2c_bus=1,i2c_address=0x29) #right
tof1 = VL53L0X.VL53L0X(i2c_bus=1,i2c_address=0x29) #left

tof.open()
tof1.open()
# Start ranging

tof.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)
tof1.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)

def sensorR():
    distance = float(tof.get_distance())/10
    
    return distance
        
 
 
def sensorL():
    distance1 = float(tof1.get_distance())/10
  
    return float(distance1)

if __name__=='__main__':
    while True:
        print('sensor left: '+str(sensorL()))
        print('sensor right: '+str(sensorR()))
        time.sleep(1)
tof.stop_ranging()
tof.close()

