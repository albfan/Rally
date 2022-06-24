from ursina import *
from ursina import curve
from particles import ParticleSystem
import json

sign = lambda x: -1 if x < 0 else (1 if x > 0 else 0)
Text.default_resolution = 1080 * Text.size

class Car(Entity):
    def __init__(self, position = (0, 0, 4), rotation = (0, 0, 0), topspeed = 30, acceleration = 0.35, braking_strength = 15, friction = 0.6, camera_speed = 8, drift_speed = 35):
        super().__init__(
            model = "car.obj",
            collider = "box",
            position = position,
            rotation = rotation,
            visible = False,
        )

        # Model + Texture
        self.graphics_parent = Entity()
        self.graphics = Entity(model = "car.obj", texture = "car-red.png")
        
        # Camera's position
        camera.position = self.position + (20, 40, -50)
        camera.rotation = (35, -20, 0)

        # Controls
        self.controls = "wasd"

        # Car's values
        self.speed = 0
        self.velocity_y = 0
        self.rotation_speed = 0
        self.max_rotation_speed = 2.6
        self.topspeed = topspeed
        self.braking_strenth = braking_strength
        self.camera_speed = camera_speed
        self.acceleration = acceleration
        self.friction = friction
        self.drift_speed = drift_speed
        self.pivot_rotation_distance = 1

        # Pivot for drifting
        self.pivot = Entity()
        self.pivot.position = self.position
        self.pivot.rotation = self.rotation

        # Particles
        self.number_of_particles = 0.05
        self.particle_pivot = Entity()
        self.particle_pivot.parent = self
        self.particle_pivot.position = self.position - (0, 1, 5)

        self.copy_normals = False

        # Making tracks accessible in update
        self.sand_track = None
        self.grass_track = None
        self.snow_track = None
        self.plains_track = None

        # Stopwatch/Timer
        self.timer_running = False
        self.count = 0.0
        self.highscore_count = None
        self.last_count = self.count
        self.reset_count = 0.0
        self.timer = Text(text = "", origin = (0, 0), size = 0.05, scale = (1, 1), position = (-0.7, 0.43))
        self.highscore = Text(text = "", origin = (0, 0), size = 0.05, scale = (0.6, 0.6), position = (-0.7, 0.38))
        self.laps_text = Text(text = "", origin = (0, 0), size = 0.05, scale = (1.1, 1.1), position = (0, 0.43))
        self.reset_count_timer = Text(text = str(round(self.reset_count, 1)), origin = (0, 0), size = 0.05, scale = (1, 1), position = (-0.7, 0.43))
        
        self.timer.disable()
        self.highscore.disable()
        self.laps_text.disable()
        self.reset_count_timer.disable()

        self.time_trial = False
        self.start_time = False
        self.laps = 0
        self.laps_hs = 0

        self.anti_cheat = 1
        self.ai = False
        self.ai_list = []

        # Multiplayer
        self.multiplayer = False
        self.multiplayer_update = False
        self.server_running = False

        # Shows whether you are connected to a server or not
        self.connected_text = True
        self.disconnected_text = True
        
        # Smoothfollow
        self.camera_angle = (20, 40, -50)
        self.camera_follow = SmoothFollow(target = self, offset = self.camera_angle, speed = self.camera_speed)
        camera.add_script(self.camera_follow)

        # Camera shake
        self.original_camera_position = camera.position
        self.shake_duration = 2.0
        self.shake_amount = 0.1
        self.can_shake = False
        self.camera_shake_option = True

        # Get highscore from json file
        path = os.path.dirname(os.path.abspath(__file__))
        self.highscore_path = os.path.join(path, "./highscore/highscore.json")
        
        try:
            with open(self.highscore_path, "r") as hs:
                self.highscores = json.load(hs)
        except FileNotFoundError:
            with open(self.highscore_path, "w+") as hs:
                self.reset_highscore()
                self.highscores = json.load(hs)

        self.sand_track_hs = self.highscores["highscore"]["sand_track"]
        self.grass_track_hs = self.highscores["highscore"]["grass_track"]
        self.snow_track_hs = self.highscores["highscore"]["snow_track"]
        self.plains_track_hs = self.highscores["highscore"]["plains_track"]

        self.sand_track_laps = self.highscores["time_trial"]["sand_track"]
        self.grass_track_laps = self.highscores["time_trial"]["grass_track"]
        self.snow_track_laps = self.highscores["time_trial"]["snow_track"]
        self.plains_track_laps = self.highscores["time_trial"]["plains_track"]

        self.highscore_count = self.sand_track_hs
        self.highscore_count = float(self.highscore_count)

        self.username_path = os.path.join(path, "./highscore/username.txt")
        with open(self.username_path, "r") as username:
            self.username_text = username.read()

    def update(self):
        # Stopwatch/Timer
        if self.time_trial == False:
            self.highscore.text = str(round(self.highscore_count, 1))
            self.laps_text.disable()
            if self.timer_running:
                self.count += time.dt
                self.reset_count += time.dt
        elif self.time_trial:
            self.highscore.text = str(self.laps_hs)
            self.laps_text.text = str(self.laps)
            self.laps_text.enable()
            if self.timer_running:
                self.count -= time.dt
                self.reset_count -= time.dt
                if self.count <= 0.0:
                    self.count = 100.0
                    self.reset_count = 100.0
                    self.timer_running = False

                    if self.laps >= self.laps_hs:
                        self.laps_hs = self.laps

                    self.laps = 0

                    if self.sand_track.enabled:
                        self.sand_track_laps = self.laps_hs
                    elif self.grass_track.enabled:
                        self.grass_track_laps = self.laps_hs
                    elif self.snow_track.enabled:
                        self.snow_track_laps = self.laps_hs
                    elif self.plains_track.enabled:
                        self.plains_track_laps = self.laps_hs

                    self.start_time = False

                    self.save_highscore()
                    self.reset_car()

        self.timer.text = str(round(self.count, 1))
        self.reset_count_timer.text = str(round(self.reset_count, 1))

        # Read the username
        with open(self.username_path, "r") as username:
            self.username_text = username.read()

        self.pivot.position = self.position

        camera.rotation = (35, -20, 0)
        self.camera_follow.offset = self.camera_angle

        # The y rotation distance between the car and the pivot
        self.pivot_rotation_distance = (self.rotation_y - self.pivot.rotation_y)

        # Drifting
        if self.pivot.rotation_y != self.rotation_y:
            if self.pivot.rotation_y > self.rotation_y:
                self.pivot.rotation_y -= (self.drift_speed * ((self.pivot.rotation_y - self.rotation_y) / 40)) * time.dt
                self.speed += self.pivot_rotation_distance / 4.5 * time.dt
                self.rotation_speed -= 1 * time.dt
            if self.pivot.rotation_y < self.rotation_y:
                self.pivot.rotation_y += (self.drift_speed * ((self.rotation_y - self.pivot.rotation_y) / 40)) * time.dt
                self.speed -= self.pivot_rotation_distance / 4.5 * time.dt
                self.rotation_speed += 1 * time.dt

        # Change number of particles depending on the rotation of the car
        if self.pivot.rotation_y - self.rotation_y < -20 or self.pivot.rotation_y - self.rotation_y > 20:
            self.number_of_particles += 1 * time.dt
            self.shake_amount += 1 * self.speed * time.dt
        else:
            self.number_of_particles -= 2 * time.dt
            self.shake_amount -= 0.2 * time.dt

        # Check if the car is hitting the ground
        ground_check = raycast(origin = self.position, direction = self.down, distance = 5, ignore = [self, self.sand_track.finish_line, self.sand_track.wall_trigger, self.grass_track.finish_line, self.grass_track.wall_trigger, self.grass_track.wall_trigger_ramp, self.snow_track.finish_line, self.snow_track.wall_trigger, self.snow_track.wall_trigger_end, self.plains_track.finish_line, self.plains_track.wall_trigger])

        if ground_check.hit:
            # Driving
            if held_keys[self.controls[0]] or held_keys["up arrow"]:
                self.speed += self.acceleration * 50 * time.dt
                self.speed += -self.velocity_y * 2 * time.dt

                # Particles + set particle colour depending on the track
                self.particles = ParticleSystem(position = self.particle_pivot.world_position, rotation_y = random.random() * 360, number_of_particles = self.number_of_particles)
                if self.sand_track.enabled == True:
                    self.particles.texture = "particle_sand_track.png"
                elif self.grass_track.enabled == True:
                    self.particles.texture = "particle_grass_track.png"
                elif self.snow_track.enabled == True:
                    self.particles.texture = "particle_snow_track.png"
                elif self.plains_track.enabled == True:
                    self.particles.texture = "particle_plains_track.png"
                else:
                    self.particles.texture = "particle_sand_track.png"
                self.particles.fade_out(duration = 0.2, delay = 1 - 0.2, curve = curve.linear)
                invoke(self.particles.disable, delay = 1)
            else:
                self.speed -= self.friction * 5 * time.dt

            # Braking
            if held_keys[self.controls[2] or held_keys["down arrow"]]:
                self.speed -= self.braking_strenth * time.dt

            # Hand Braking
            if held_keys["space"]:
                if self.rotation_speed < 0:
                    self.rotation_speed -= 3 * time.dt
                elif self.rotation_speed > 0:
                    self.rotation_speed += 3 * time.dt
                self.drift_speed -= 20 * time.dt
                self.speed -= 20 * time.dt
                self.max_rotation_speed = 3
            else:
                self.max_rotation_speed = 2.6

        # Rotation
        self.graphics_parent.position = self.position
        self.graphics.position = self.position

        self.graphics.quaternion = slerp(self.graphics.quaternion, self.graphics_parent.quaternion, 20 * time.dt)

        # Raycast for getting the ground's normals
        rotation_ray = raycast(origin = self.position, direction = (0, -1, 0), ignore = [self, self.sand_track.finish_line, self.sand_track.wall_trigger, self.grass_track.finish_line, self.grass_track.wall_trigger, self.grass_track.wall_trigger_ramp, self.snow_track.finish_line, self.snow_track.wall_trigger, self.snow_track.wall_trigger_end, self.plains_track.finish_line, self.plains_track.wall_trigger, ])

        if self.copy_normals:
            self.ground_normal = self.position + rotation_ray.world_normal
        else:
            self.ground_normal = self.position + (0, 180, 0)

        if rotation_ray.distance <= 4:
            self.graphics_parent.look_at(self.ground_normal, axis = "up")
            self.graphics_parent.rotate((0, self.rotation_y + 180, 0))
        else:
            self.graphics_parent.rotation_y = self.rotation_y

        # Steering
        self.rotation_y += self.rotation_speed * 50 * time.dt

        if self.rotation_speed > 0:
            self.rotation_speed -= self.speed / 6 * time.dt
        elif self.rotation_speed < 0:
            self.rotation_speed += self.speed / 6 * time.dt

        if self.speed != 0:
            if held_keys[self.controls[1]] or held_keys["left arrow"]:
                self.rotation_speed -= 8 * time.dt
                self.drift_speed -= 10 * time.dt
            elif held_keys[self.controls[3]] or held_keys["right arrow"]:
                self.rotation_speed += 8 * time.dt
                self.drift_speed -= 10 * time.dt
            else:
                self.drift_speed += 0.01 * time.dt
                if self.rotation_speed > 0:
                    self.rotation_speed -= 5 * time.dt
                elif self.rotation_speed < 0:
                    self.rotation_speed += 5 * time.dt

        # Cap the speed
        if self.speed >= self.topspeed:
            self.speed = self.topspeed
        if self.speed <= 0.1:
            self.speed = 0.1
            self.pivot.rotation = self.rotation

        # Cap the drifting
        if self.drift_speed <= 20:
            self.drift_speed = 20
        if self.drift_speed >= 40:
            self.drift_speed = 40

        # Cap the steering
        if self.rotation_speed >= self.max_rotation_speed:
            self.rotation_speed = self.max_rotation_speed
        if self.rotation_speed <= -self.max_rotation_speed:
            self.rotation_speed = -self.max_rotation_speed

        # Camera Shake
        if self.speed >= 1:
            self.can_shake = True
            self.shake_amount += self.speed / 5000 * time.dt

        # Cap the camera shake amount
        if self.shake_amount <= 0:
            self.shake_amount = 0
        if self.shake_amount >= 0.03:
            self.shake_amount = 0.03

        # Respawn
        if held_keys["g"]:
            self.reset_car()

        # If the camera can shake and camera shake is on, then shake the camera
        if self.can_shake and self.camera_shake_option:
            self.shake_camera()

        # Reset the car's position if y value is less than -100
        if self.y <= -100:
            self.reset_car()

        # Reset the car's position if y value is greater than 300
        if self.y >= 300:
            self.reset_car()

        # Gravity
        movementY = self.velocity_y * time.dt
        direction = (0, sign(movementY), 0)

        # Main raycast for collision
        y_ray = boxcast(origin = self.world_position, direction = self.down, distance = self.scale_y * 1.7 + abs(movementY), ignore = [self, self.sand_track.finish_line, self.sand_track.wall_trigger, self.grass_track.finish_line, self.grass_track.wall_trigger, self.grass_track.wall_trigger_ramp, self.snow_track.finish_line, self.snow_track.wall_trigger, self.snow_track.wall_trigger_end, self.plains_track.finish_line, self.plains_track.wall_trigger, ])

        if y_ray.hit:
            self.velocity_y = 0
            # Check if hitting a wall or steep slope
            if y_ray.world_normal.y > 0.7 and y_ray.world_point.y - self.world_y < 0.5:
                # Set the y value to the ground's y value
                self.y = y_ray.world_point.y + 1.4
        else:
            self.y += movementY * 50 * time.dt
            self.velocity_y -= 50 * time.dt

        # Movement
        movementX = self.pivot.forward[0] * self.speed * time.dt
        movementZ = self.pivot.forward[2] * self.speed * time.dt

        # Collision Detection
        if movementX != 0:
            direction = (sign(movementX), 0, 0)
            x_ray = boxcast(origin = self.world_position, direction = direction, distance = self.scale_x / 2 + abs(movementX), ignore = [self, self.sand_track.finish_line, self.sand_track.wall_trigger, self.grass_track.finish_line, self.grass_track.wall_trigger, self.grass_track.wall_trigger_ramp, self.snow_track.finish_line, self.snow_track.wall_trigger, self.snow_track.wall_trigger_end, self.plains_track.finish_line, self.plains_track.wall_trigger, ], thickness = (1, 1))

            if not x_ray.hit:
                self.x += movementX

        if movementZ != 0:
            direction = (0, 0, sign(movementZ))
            z_ray = boxcast(origin = self.world_position, direction = direction, distance = self.scale_z / 2 + abs(movementZ), ignore = [self, self.sand_track.finish_line, self.sand_track.wall_trigger, self.grass_track.finish_line, self.grass_track.wall_trigger, self.grass_track.wall_trigger_ramp, self.snow_track.finish_line, self.snow_track.wall_trigger, self.snow_track.wall_trigger_end, self.plains_track.finish_line, self.plains_track.wall_trigger, ], thickness = (1, 1))

            if not z_ray.hit:
                self.z += movementZ

    def reset_car(self):
        if self.grass_track.enabled:
            self.position = (-80, -30, 15)
            self.rotation = (0, 90, 0)
        elif self.sand_track.enabled:
            self.position = (-63, -40, -7)
            self.rotation = (0, 90, 0)
        elif self.snow_track.enabled:
            self.position = (-5, -35, 90)
            self.rotation = (0, 90, 0)
        elif self.plains_track.enabled:
            self.position = (12, -40, 73)
            self.rotation = (0, 90, 0)
        self.speed = 0
        self.velocity_y = 0
        self.anti_cheat = 1
        if self.time_trial == False:
            self.timer_running = False
            self.count = 0.0
            self.reset_count = 0.0
        elif self.time_trial:
            self.count = 100.0
            self.reset_count = 100.0
            self.laps = 0
            self.timer_running = False
            self.start_time = False

    def save_highscore(self):
        self.highscore_dict = {
            "highscore": {
                "sand_track": self.sand_track_hs,
                "grass_track": self.grass_track_hs,
                "snow_track": self.snow_track_hs,
                "plains_track": self.plains_track_hs
            },
            
            "time_trial": {
                "sand_track": self.sand_track_laps,
                "grass_track": self.grass_track_laps, 
                "snow_track": self.snow_track_laps, 
                "plains_track": self.plains_track_laps
            }
        }

        with open(self.highscore_path, "w") as hs:
            json.dump(self.highscore_dict, hs, indent = 4)

    def reset_highscore(self):
        self.highscore_dict = {
            "highscore": {
                "sand_track": 0.0,
                "grass_track": 0.0,
                "snow_track": 0.0,
                "plains_track": 0.0
            },

            "time_trial": {
                "sand_track": 0,
                "grass_track": 0, 
                "snow_track": 0, 
                "plains_track": 0
            }
        }

        with open(self.highscore_path, "w") as hs:
            json.dump(self.highscore_dict, hs, indent = 4)
    
    def reset_timer(self):
        self.count = self.reset_count
        self.timer.enable()
        self.reset_count_timer.disable()

    def update_camera_pos(self):
        self.original_camera_position = camera.position

    def shake_camera(self):
        camera.x += random.randint(-1, 1) * self.shake_amount
        camera.y += random.randint(-1, 1) * self.shake_amount
        camera.z += random.randint(-1, 1) * self.shake_amount

# Class for copying the car's position, rotation for multiplayer
class CarRepresentation(Entity):
    def __init__(self, car, position = (0, 0, 0), rotation = (0, 65, 0)):
        super().__init__(
            parent = scene,
            model = "car.obj",
            texture = "car-red.png",
            position = position,
            rotation = rotation,
            scale = (1, 1, 1)
        )

        self.text_object = None
        self.highscore = 0.0

# Username shown above the car
class CarUsername(Text):
    def __init__(self, car):
        super().__init__(
            parent = car,
            text = "Guest",
            y = 3,
            scale = 30,
            color = color.white
        )
    
        self.username_text = "Guest"

    def update(self):
        self.text = self.username_text