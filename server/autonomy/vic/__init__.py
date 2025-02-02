try:
    import smbus2
    class VehicleInterfaceController:
        address = 0x32
        
        def __call__(self, package):
            print("p:", package)
            mappedSteering = int(10*(-package['steering'] + 40)/80)
            mappedForward = package['forward']
            mappedReverse = package['reverse']
            
            output = f'{str(mappedSteering)},{str(mappedForward)},{str(mappedReverse)}'
            print("o:", output)
            self.send(output)
            
        def send(self, package):
            with smbus2.SMBus(1) as bus:
                message = smbus2.i2c_msg.write(self.address, package)
                bus.i2c_rdwr(message)
    
except ImportError as e:
    class VehicleInterfaceController:
        def __call__(self, package):
            pass
            

                
