import asyncio
from mavsdk import System
from mavsdk.action import ActionError

async def run():
    drone = System()
    await drone.connect(system_address="udp://:14550")  # Adjust the connection string as needed

    try:
        # Wait for the drone to connect
        print("Waiting for drone to connect...")
        async for state in drone.core.connection_state():
            if state.is_connected:
                print("Drone connected!")
                break

       

        # Arm the drone
        print("Arming drone...")
        await drone.action.arm()

        # Set takeoff altitude to 1 foot (approximately 0.3048 meters)
        takeoff_altitude = 0.3048
        await drone.action.set_takeoff_altitude(takeoff_altitude)

        await asyncio.sleep(5)
        # Take off
        print(f"Taking off to {takeoff_altitude} meters...")
        await drone.action.takeoff()

        # Wait for a few seconds to reach the altitude
        await asyncio.sleep(5)

        # Land the drone
        print("Landing drone...")
        await drone.action.land()

        # Wait for the drone to land
        async for in_air in drone.telemetry.in_air():
            if not in_air:
                print("Drone has landed")
                break

        # Disarm the drone
        print("Disarming drone...")
        await drone.action.disarm()

    except ActionError as error:
        print(f"An error occurred: {error}")
        print("Attempting to land and disarm the drone...")

        try:
            await drone.action.land()
            async for in_air in drone.telemetry.in_air():
                if not in_air:
                    print("Drone has landed")
                    break
            await drone.action.disarm()
            print("Drone disarmed successfully")
        except Exception as e:
            print(f"Failed to land and disarm the drone: {e}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(run())
