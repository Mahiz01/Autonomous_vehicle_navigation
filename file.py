import random
class AdvancedNavigationEnvironment:
    def __init__(self, map_data):
        self.map_data = map_data
        self.reset()

    def reset(self):
        self.traffic_conditions = self.randomize_traffic_conditions()
        self.vehicle_state = self.initialize_vehicle_state()
        self.environmental_factors = self.get_environmental_factors()
        self.current_map_info = self.get_map_info()
        return self.get_state()

    def randomize_traffic_conditions(self):
        return {
            'traffic_lights': random.choice([0, 1, 2]),  # 0: Red, 1: Yellow, 2: Green
            'congestion': random.choice(['low', 'medium', 'high'])
        }

    def initialize_vehicle_state(self):
        return {
            'position': 0,
            'speed': 0,
            'lane': 0
        }

    def get_environmental_factors(self):
        return {
            'weather': random.choice(['clear', 'rainy', 'foggy'])
        }

    def get_map_info(self):
        return {
            'road_network': self.map_data['roads'],
            'points_of_interest': self.map_data['poi']
        }

    def get_state(self):
        return (self.traffic_conditions, self.vehicle_state, self.environmental_factors, self.current_map_info)

    def step(self, action):
        # Action effects
        if action == 0:  # Accelerate
            self.vehicle_state['speed'] += 1
            self.vehicle_state['position'] += self.vehicle_state['speed']
        elif action == 1:  # Brake
            self.vehicle_state['speed'] = max(0, self.vehicle_state['speed'] - 1)
            self.vehicle_state['position'] += self.vehicle_state['speed']
        elif action == 2:  # Change Lane
            self.vehicle_state['lane'] = (self.vehicle_state['lane'] + 1) % 3

        done = self.vehicle_state['position'] >= 100
        reward = 0

        if done:
            reward = 10 if self.traffic_conditions['traffic_lights'] == 2 else -10

        return self.get_state(), reward, done
    
    
    
    
# Example map data
map_data = {
    'roads': [
        {'id': 1, 'name': 'Main St', 'type': 'urban', 'length': 1000, 'lanes': 3, 'speed_limit': 50},
        {'id': 2, 'name': 'Second Ave', 'type': 'residential', 'length': 500, 'lanes': 2, 'speed_limit': 30},
        {'id': 3, 'name': 'Third Blvd', 'type': 'highway', 'length': 2000, 'lanes': 4, 'speed_limit': 80}
    ],
    'intersections': [
        {'id': 1, 'name': 'Main St / Second Ave', 'type': 'crossroad', 'traffic_lights': True},
        {'id': 2, 'name': 'Main St / Third Blvd', 'type': 'T-junction', 'traffic_lights': True}
    ],
    'poi': [
        {'type': 'gas_station', 'name': 'Shell Station', 'location': (37.7749, -122.4194), 'address': '123 Main St'},
        {'type': 'restaurant', 'name': 'Joe\'s Diner', 'location': (37.7750, -122.4183), 'address': '456 Second Ave'},
        {'type': 'parking_lot', 'name': 'City Parking Garage', 'location': (37.7745, -122.4189), 'address': '789 Third Blvd'}
    ]
}




# Create the environment
env = AdvancedNavigationEnvironment(map_data)

# Reseting environment to initial state
state = env.reset()
print(f"Initial State: {state}")

#loop
done = False
while not done:
    action = 0  # Accelerate
    new_state, reward, done = env.step(action)
    print(f"New State: {new_state}, Reward: {reward}, Done: {done}")

# done is true 
    if done:
        if reward > 0:
            print("The vehicle received a positive reward for a successful trip with green traffic light.")
        else:
            print("The vehicle received a negative reward due to the traffic light being red or yellow.")
