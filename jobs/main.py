import json
import os
import random
import time
import uuid
from datetime import datetime, timedelta

from confluent_kafka import SerializingProducer

# Coordinates for the starting point (Visakhapatnam) and destination (Hyderabad)
VISAKHAPATNAM_COORDINATES = {"latitude": 17.686815, "longitude": 83.218483}
HYDERABAD_COORDINATES = {"latitude": 17.4065, "longitude": 78.4772}

# Calculate the increments for latitude and longitude for simulating movement
LATITUDE_INCREMENT = (HYDERABAD_COORDINATES['latitude'] - VISAKHAPATNAM_COORDINATES['latitude']) / 100
LONGITUDE_INCREMENT = (HYDERABAD_COORDINATES['longitude'] - VISAKHAPATNAM_COORDINATES['longitude']) / 100

# Environment variables for Kafka configuration (topics and bootstrap servers)
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
VEHICLE_TOPIC = os.getenv('VEHICLE_TOPIC', 'vehicle_data')
GPS_TOPIC = os.getenv('GPS_TOPIC', 'gps_data')
TRAFFIC_TOPIC = os.getenv('TRAFFIC_TOPIC', 'traffic_data')
WEATHER_TOPIC = os.getenv('WEATHER_TOPIC', 'weather_data')
EMERGENCY_TOPIC = os.getenv('EMERGENCY_TOPIC', 'emergency_data')

# Initial time and location setup
start_time = datetime.now()
start_location = VISAKHAPATNAM_COORDINATES.copy()

def get_next_time():
    """
    Returns the current time in the format YYYY-MM-DDTHH:MM:SS
    The time is updated every 30 to 60 seconds to simulate real-time data flow.
    """
    global start_time
    start_time += timedelta(seconds=random.randint(30, 60))  # update frequency
    return start_time

def generate_weather_data(vehicle_id, timestamp, location):
    """
    Generates mock weather data for a vehicle at a specific location and time.
    Returns a dictionary containing weather information.
    """
    return {
        'id': uuid.uuid4(),
        'vehicle_id': vehicle_id,
        'location': location,
        'timestamp': timestamp,
        'temperature': random.uniform(-5, 26),
        'weatherCondition': random.choice(['Sunny', 'Cloudy', 'Rain', 'Snow']),
        'precipitation': random.uniform(0, 25),
        'windSpeed': random.uniform(0, 100),
        'humidity': random.randint(0, 100),  # percentage
        'airQualityIndex': random.uniform(0, 500)  # AQL Value
    }

def generate_emergency_incident_data(vehicle_id, timestamp, location):
    """
    Generates emergency incident data (such as accidents, fires, etc.)
    Returns a dictionary containing the incident data.
    """
    return {
        'id': uuid.uuid4(),
        'vehicle_id': vehicle_id,
        'incidentId': uuid.uuid4(),
        'type': random.choice(['Accident', 'Fire', 'Medical', 'Police', 'None']),
        'timestamp': timestamp,
        'location': location,
        'status': random.choice(['Active', 'Resolved']),
        'description': 'Description of the incident'
    }

def generate_gps_data(vehicle_id, timestamp, vehicle_type='private'):
    """
    Generates GPS data for the vehicle including speed, direction, and vehicle type.
    Returns a dictionary containing GPS data.
    """
    return {
        'id': uuid.uuid4(),
        'vehicle_id': vehicle_id,
        'timestamp': timestamp,
        'speed': random.uniform(0, 40),  # speed in km/h
        'direction': 'North-East',
        'vehicleType': vehicle_type
    }

def generate_traffic_camera_data(vehicle_id, timestamp, location, camera_id):
    """
    Generates data from traffic cameras, including a snapshot (represented here as a string).
    Returns a dictionary with traffic camera data.
    """
    return{
        'id': uuid.uuid4(),
        'vehicle_id': vehicle_id,
        'camera_id': camera_id,
        'location': location,
        'timestamp': timestamp,
        'snapshot': 'Base64EncodedString'  # Placeholder for the actual image data
    }

def simulate_vehicle_movement():
    """
    Simulates the movement of a vehicle towards Hyderabad.
    Updates latitude and longitude based on pre-calculated increments and adds randomness
    to simulate real-world road travel.
    """
    global start_location

    # Move towards Hyderabad by incrementing latitude and longitude
    start_location['latitude'] += LATITUDE_INCREMENT
    start_location['longitude'] += LONGITUDE_INCREMENT

    # Add small random changes to simulate road travel
    start_location['latitude'] += random.uniform(-0.0005, 0.0005)
    start_location['longitude'] += random.uniform(-0.0005, 0.0005)

    return start_location

def generate_vehicle_data(vehicle_id):
    """
    Generates complete vehicle data, including location, speed, make, and model.
    The vehicle’s location is simulated and updated as it moves towards the destination.
    """
    location = simulate_vehicle_movement()
    return {
        'id': uuid.uuid4(),
        'vehicle_id': vehicle_id,
        'timestamp': get_next_time().isoformat(),
        'location': (location['latitude'], location['longitude']),
        'speed': random.uniform(10, 40),  # speed in km/h
        'direction': 'North-East',
        'make': 'Jeep',
        'model': 'Wrangler',
        'year': 2023,
        'fuelType': 'Gasoline'
    }

def json_serializer(obj):
    """
    Custom serializer for non-serializable objects (like UUID).
    This function ensures that UUIDs are converted to strings before serialization.
    """
    if isinstance(obj, uuid.UUID):
        return str(obj)
    raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')

def delivery_report(err, msg):
    """
    Callback function for Kafka producer to handle success or failure of message delivery.
    Prints the status of the message delivery to the console.
    """
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

def produce_data_to_kafka(producer, topic, data):
    """
    Sends the generated data to Kafka.
    It serializes the data and produces it to the specified Kafka topic.
    """
    producer.produce(
        topic,
        key=str(data['id']),
        value=json.dumps(data, default=json_serializer).encode('utf-8'),
        on_delivery=delivery_report
    )

    # Ensure all messages are delivered
    producer.flush()

def simulate_journey(producer, vehicle_id):
    """
    Simulates the vehicle's journey by continuously generating and sending vehicle,
    GPS, weather, traffic, and emergency incident data to Kafka topics.
    Stops when the vehicle reaches the destination (Hyderabad).
    """
    while True:
        vehicle_data = generate_vehicle_data(vehicle_id)
        gps_data = generate_gps_data(vehicle_id, vehicle_data['timestamp'])
        traffic_camera_data = generate_traffic_camera_data(vehicle_id, vehicle_data['timestamp'], vehicle_data['location'], 'Camera-001')
        weather_data = generate_weather_data(vehicle_id, vehicle_data['timestamp'], vehicle_data['location'])
        emergency_incident_data = generate_emergency_incident_data(vehicle_id, vehicle_data['timestamp'], vehicle_data['location'])

        # Log the current location
        print(f"Current Location: {vehicle_data['location']}")

        EPSILON = 0.01  # Tolerance for latitude and longitude
        # Check if the vehicle is near Hyderabad
        if (abs(vehicle_data['location'][0] - HYDERABAD_COORDINATES['latitude']) <= EPSILON
                and abs(vehicle_data['location'][1] - HYDERABAD_COORDINATES['longitude']) <= EPSILON):
            print('Vehicle has reached Hyderabad. Simulation ending...')
            break

        produce_data_to_kafka(producer, VEHICLE_TOPIC, vehicle_data)
        produce_data_to_kafka(producer, GPS_TOPIC, gps_data)
        produce_data_to_kafka(producer, TRAFFIC_TOPIC, traffic_camera_data)
        produce_data_to_kafka(producer, WEATHER_TOPIC, weather_data)
        produce_data_to_kafka(producer, EMERGENCY_TOPIC, emergency_incident_data)

        time.sleep(5)


if __name__ == '__main__':
    # Kafka producer configuration
    producer_config = {
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'error_cb': lambda err: print(f'Kafka Error: {err}')
    }

    # Initialize the Kafka producer
    producer = SerializingProducer(producer_config)

    try:
        # Start simulating the journey for a specific vehicle
        simulate_journey(producer, 'AP35Q7926')

    except KeyboardInterrupt:
        print('Simulation ended by the user.')
    except Exception as e:
        print(f'An unexpected error occurred: {e}')
