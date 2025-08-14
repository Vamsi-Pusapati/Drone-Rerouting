import asyncio
from mavsdk import System

async def run():
    drone = System()
    await drone.connect(system_address="udp://:14550")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"Drone discovered with UUID: {state}")
            break

    #print("Waiting for drone to have a global position estimate...")
    #async for health in drone.telemetry.health():
    #    print(f"Drone health: {health}")
    #    if health.is_global_position_ok:
    #        print("Global position estimate ok")
    #        break

    # Fetch and print takeoff altitude

    #print(drone.telemetry.__dict__)
    #async for position in drone.telemetry.position():
    #    takeoff_altitude = position.relative_altitude_m
    #    print(f"Takeoff altitude: {takeoff_altitude} meters")
    #    break  # Remove if continuous altitude monitoring is needed

    # Fetch and print maximum speed

    take_off_height = await drone.action.get_takeoff_altitude()
    print(f"Take off Height : {take_off_height} m from takeoff location")
    
    max_speed = await drone.action.get_maximum_speed()

    
    print(f"Maximum speed: {max_speed} m/s")

    await drone.action.set_maximum_speed(0.5)
    await asyncio.sleep(4)

    max_speed = await drone.action.get_maximum_speed()

    print(f"Maximum speed: {max_speed} m/s")

    print("-- Arming")
    await drone.action.arm()

    await asyncio.sleep(4)

    # Uncomment these lines to take off and land
    #print("-- Taking off")
    #await drone.action.takeoff()
    #await asyncio.sleep(4)
    print("-- Landing")
    #await drone.action.land()
    #await asyncio.sleep(10)

    print("-- Disarming")
    await drone.action.disarm()


    await drone.action.disarm()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
