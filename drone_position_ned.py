#!/usr/bin/env python3

"""
Caveat when attempting to run the examples in non-gps environments:

`drone.offboard.stop()` will return a `COMMAND_DENIED` result because it
requires a mode switch to HOLD, something that is currently not supported in a
non-gps environment.
"""

import asyncio

from mavsdk import System
from mavsdk.offboard import (OffboardError, PositionNedYaw)


async def run():
    """ Does Offboard control using position NED coordinates. """

    
    drone = System()
    print("Connecting to vehicle using port 14550")
    await drone.connect(system_address="udp://:14550")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone!")
            break



    print("-- Arming")
    await drone.action.arm()

    max_speed = await drone.action.get_maximum_speed()

    
    print(f"Maximum speed: {max_speed} m/s")

    await drone.action.set_maximum_speed(0.5)
    await asyncio.sleep(4)

    max_speed = await drone.action.get_maximum_speed()

    await asyncio.sleep(5)

    print("-- Setting initial setpoint")
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, 0.0, 0.0))



    
    print("-- Starting offboard")
    try:
        await drone.offboard.start()
    except OffboardError as error:
        print(f"Starting offboard mode failed \
                with error code: {error._result.result}")
        print("-- Disarming")
        await drone.action.disarm()
        return

    await asyncio.sleep(5)

    print("-- Go 0m North, 0m East, -0.20m Down \
            within local coordinate system")
    await drone.offboard.set_position_ned(
            PositionNedYaw(0.0, 0.0, -0.20, 0.0))
    await asyncio.sleep(5)


    #print("-- Go 0m North, 0m East, -0.20m Down within local coordinate system")

    #print("-- Go 0m North, 0m East, 0m Down within local coordinate system")
    #await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, 0.0, 0.0)
    #await asyncio.sleep(5)

    print("-- Go 0.2m North, 0m East, -0.2m Down within local coordinate system, turn to face East")
    await drone.offboard.set_position_ned(PositionNedYaw(0.2, 0.0, -0.2, 90.0))
    await asyncio.sleep(4)

    print("-- Go 0.2m North, 0.2m East, -0.2m Down within local coordinate system")
    await drone.offboard.set_position_ned(PositionNedYaw(0.2, 0.2, -0.2, 90.0))
    await asyncio.sleep(4)

    print("-- Go 0m North, 0.2m East, -0.2m Down within local coordinate system, turn to face South")
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.2, -0.2, 180.0))
    await asyncio.sleep(4)


    print("Trying to land")
    try:
        await drone.action.land()
    except:
        print("Failed to land")

    await asyncio.sleep(8)

    print("-- Disarming")
    try:
        await drone.action.disarm()
    except:
        print("Disarming failed")



if __name__ == "__main__":
    # Run the asyncio loop
    asyncio.run(run())