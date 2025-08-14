import asyncio
from mavsdk import System
from mavsdk import telemetry



# Method to create a route plan
async def route_planner():
    
    # cretae drone object
    drone = System()
    await drone.connect(system_address="udp://:14550")
   

    # check for connections

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"Drone discovered with UUID: {state}")
            break

    # check for telemerty health 
    print("Waiting for drone to have a heartbeat...")
    async for health in drone.telemetry.health():
        if health.is_armable :
            break

    async 



    # check for the drone state

    # check for the drone mode // change to manual mode if it is different

    # check for armable

    # arm the drone

    # create a localposition as 0,0,0,0 (use this as reference frame for indoor navigation and gps denied navigation)

    # takeoff

    # Drone movement (can be any relative frame of reference for now)

        # contineously run for GPS spoffing attacks and check for deviation of path 

            # if yes check for deviation and got to initial location and block mavlink packets from the attacker ip

    # Drone location reached ? drone.action.land, drone.action.disarm



#calling the method
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(route_planner())