import asyncio
from mavsdk import System
from mavsdk.offboard import (OffboardError, PositionNedYaw)
import math
from collections import deque

# Flask-SocketIO for real-time logs
from flask_socketio import SocketIO
import sys

# Initialize a dummy SocketIO object, to be set by Flask when integrated
socketio = None

def set_socketio(instance):
    """Set the Flask-SocketIO instance."""
    global socketio
    socketio = instance

# Custom log function to emit logs to the web and console
def log(message):
    """Custom logging function to emit messages to the front end and console."""
    print(message)  # Print to terminal
    if socketio:
        socketio.emit("log", {"message": message}, broadcast=True)
    sys.stdout.flush()

DEVIATION_THRESHOLD = 0.2 #this is the threshold for the deviation

distance_history = deque(maxlen=5)

#defining as global veriables so required functions can access this 
prev_checkpoint = []

next_checkpoint = []

async def run():
    """
        This function we will create simultanious tasks to monitor different telemetry of the drone

        we run these task in a thread using asyncio.ensure_future and we create another method to 
        monitor and stop the threads

    """

    #Create connection to drone
    print(2)
    log("system")
    log("checking 123")
    drone = System()
    await drone.connect(system_address="udp://:14550")

    log("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            log(f"Drone discovered with UUID: {state}")
            break

    # not checking for globaa telemetry as i was doing indoor gps denied navigation


    #initialize the checkpoint(north, east, down)
    #also using the global variables so that it updates the global variable whenever we change those values
    global prev_checkpoint
    global next_checkpoint
    global distance_history
    prev_checkpoint = [0.0, 0.0, 0.0]

    next_checkpoint = [0.0, 0.0, 0.0]

    """ 
    create threads
    """

    #print mode thread
    print_mode_task = asyncio.ensure_future(print_mode(drone))

    #print telemetry thread

    print_telemetry_armed_task = asyncio.ensure_future(print_telemetry_armed(drone))
    
    # check for position and do deviation calculation
    print_telemetry_position_task = asyncio.ensure_future(print_telemetry_position(drone))
    
    running_tasks = [print_mode_task, print_telemetry_armed_task, print_telemetry_position_task]


    #check for termination task
    termination_task = asyncio.ensure_future(check_disarmed(drone, running_tasks))



    """
        Drone Manuvers
    """

    
    # Execute the Drone movement
    log("-- Arming")
    await drone.action.arm()

    max_speed = await drone.action.get_maximum_speed()

    
    log(f"Maximum speed: {max_speed} m/s")

    await drone.action.set_maximum_speed(0.5)
    await asyncio.sleep(4)

    max_speed = await drone.action.get_maximum_speed()

    await asyncio.sleep(5)

    
    
    #check for previous 5 distances

    log("-- Setting initial setpoint")
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, 0.0, 0.0))



    
    log("-- Starting offboard")
    try:
        await drone.offboard.start()
    except OffboardError as error:
        log(f"Starting offboard mode failed \
                with error code: {error._result.result}")
        log("-- Disarming")
        await drone.action.disarm()
        return

    await asyncio.sleep(5)

    prev_checkpoint = next_checkpoint
    next_checkpoint = [0.0, 0.0, -0.20]
    distance_history = deque(maxlen=5)
    
    log("-- Go 0m North, 0m East, -0.20m Down \
            within local coordinate system")
    await drone.offboard.set_position_ned(
            PositionNedYaw(next_checkpoint[0], next_checkpoint[1], next_checkpoint[2], 0.0))
    await asyncio.sleep(5)


    #log("-- Go 0m North, 0m East, 0m Down within local coordinate system")
    #await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, 0.0, 0.0)
    #await asyncio.sleep(5)

    log("-- Go 0.2m North, 0m East, -0.2m Down within local coordinate system, turn to face East")
    prev_checkpoint = next_checkpoint
    next_checkpoint = [0.2, 0.0, -0.20]
    distance_history = deque(maxlen=5)
    await drone.offboard.set_position_ned(PositionNedYaw(next_checkpoint[0], next_checkpoint[1], next_checkpoint[2], 0.0))
    await asyncio.sleep(8)

    log("-- Go 0.2m North, 0.2m East, -0.2m Down within local coordinate system")
    prev_checkpoint = next_checkpoint
    next_checkpoint = [0.2, 0.2, -0.20]
    distance_history = deque(maxlen=5)
    await drone.offboard.set_position_ned(PositionNedYaw(next_checkpoint[0], next_checkpoint[1], next_checkpoint[2], 0.0))
    await asyncio.sleep(4)

    log("----- Initiaing GPS Spoofing Attack -----")

    log("Sending GPS spoof to move to different location ")
    next_checkpoint = [0.0, 0.2, -0.20]

    await drone.offboard.set_position_ned(PositionNedYaw(0.5, 0.2, -0.2, 0.0))
    await asyncio.sleep(4)


   #print("-- Go 0m North, 0.2m East, -0.2m Down within local coordinate system, turn to face South")
    prev_checkpoint = next_checkpoint
    next_checkpoint = [0.0, 0.2, -0.20]
    distance_history = deque(maxlen=5)
    await drone.offboard.set_position_ned(PositionNedYaw(next_checkpoint[0], next_checkpoint[1], next_checkpoint[2], 0.0))
    await asyncio.sleep(4)


    log("Trying to land")
    try:
        await drone.action.land()
    except:
        log("Failed to land")

    await asyncio.sleep(8)

    log("-- Disarming")
    try:
        await drone.action.disarm()
    except:
        log("Disarming failed")

    # Wait until the drone is disarmed (instead of exiting after 'disarm' is sent)
    await termination_task


async def check_distance_to_next_checkpoint(current_location, checkpoint_location):
    # Calculate the distance between the current location and the next checkpoint

    if(current_location and checkpoint_location):
        north = current_location[0]-checkpoint_location[0]
        east = current_location[1]-checkpoint_location[1]
        down = current_location[2]-checkpoint_location[2]
        distance = math.sqrt(north**2 + east**2 + down**2)
        return distance
    return 0
    
async def check_for_deviation(current_distance, previous_5_distance):
    # Check if the drone has deviated from the path

    if len(previous_5_distance) >=3:
        avg_dist = sum(previous_5_distance)/len(previous_5_distance)
        deviation = current_distance - avg_dist
        log(f"found deviation - {deviation}m")

        if deviation > DEVIATION_THRESHOLD:
            log("Detected deviation in the drone path")
            log("Turning to Offboard Mode")
            log("Updating the Policies")
            log("Redirecting to the Next Checkpoint")
            
            await drone.offboard.set_position_ned(PositionNedYaw(next_checkpoint[0], next_checkpoint[1], next_checkpoint[2], 0.0))
            await asyncio.sleep(4)

    
    



async def print_mode(drone):
    "print mode of the drone"

    previous_flight_mode = None

    async for flight_mode in drone.telemetry.flight_mode():
        if flight_mode != previous_flight_mode:
            previous_flight_mode = flight_mode
            log(f"Flight mode: {flight_mode}")


async def print_telemetry_armed(drone):
    was_armed = False

    counter =1
    async for is_armed in drone.telemetry.armed():
        
        log("Is_armed: " + str(is_armed) + " - " + str(counter))
        counter += 1


    


async def print_telemetry_position(drone):

    #print(drone.telemetry.__dict__)

    
    async for position_velocity_ned in drone.telemetry.position_velocity_ned():
        north = position_velocity_ned.position.north_m
        east = position_velocity_ned.position.east_m
        down = position_velocity_ned.position.down_m

        current_location = [north, east, down]


        distance_to_checkpoint = await check_distance_to_next_checkpoint(current_location, next_checkpoint)

        deviation = await check_for_deviation(distance_to_checkpoint, distance_history)
        distance_history.append(distance_to_checkpoint)


        log(f"NED Position -> North: {north} m, East: {east} m, Down: {down} m, Distance to Checkpoint: {distance_to_checkpoint}m")



    



async def check_disarmed(drone, running_tasks):

    was_armed = False

    async for is_armed in drone.telemetry.armed():
        if is_armed:
            was_armed = is_armed
        
        if was_armed and not is_armed:
            for task in running_tasks:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
            await asyncio.get_event_loop().shutdown_asyncgens()
            return

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())