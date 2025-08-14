import asyncio
from mavsdk import System


#async def monitor_mode(drone):
#    """ Continuously prints the current mode of the drone. """
#    async for flight_mode in drone.telemetry.flight_mode():
#        print(f"Current drone mode: {flight_mode}")
#        await asyncio.sleep(1) 

async def run():

    drone = System()
    await drone.connect(system_address="udp://:14550")


    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"Drone discovered with UUID: {state}")
            break


 #   asyncio.create_task(monitor_mode(drone))

    print("Waiting for drone to have a global position estimate...")
    print(drone.__dict__)
    print("-----------------")

   
    async for health in drone.telemetry.health():
        print(health)
        if health.is_global_position_ok:
            print("Global position estimate ok")
        break

    print("-- Arming")
    await drone.action.arm()

    await asyncio.sleep(4)

    #print("-- Taking off")
    
    #await drone.action.takeoff()



    await asyncio.sleep(4)

    #print("-- Landing")

    #await drone.action.land()
    
    await asyncio.sleep(5)

   # 
   # await drone.action.land()
    print("-- DisArming")
    await drone.action.disarm()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
