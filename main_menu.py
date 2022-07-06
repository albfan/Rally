from ursina import *
from ursina import curve
from server import Server
import os

Text.default_resolution = 1080 * Text.size

class MainMenu(Entity):
    def __init__(self, car, ai_list, sand_track, grass_track, snow_track, forest_track, savannah_track):
        super().__init__(
            parent = camera.ui
        )

        # The different menus
        self.start_menu = Entity(parent = self, enabled = True)
        self.host_menu = Entity(parent = self, enabled = False)
        self.created_server_menu = Entity(parent = self, enabled = False)
        self.server_menu = Entity(parent = self, enabled = False)
        self.main_menu = Entity(parent = self, enabled = False)
        self.race_menu = Entity(parent = self, enabled = False)
        self.maps_menu = Entity(parent = self, enabled = False)
        self.settings_menu = Entity(parent = self, enabled = False)
        self.video_menu = Entity(parent = self, enabled = False)
        self.gameplay_menu = Entity(parent = self, enabled = False)
        self.controls_menu = Entity(parent = self, enabled = False)
        self.garage_menu = Entity(parent = self, enabled = False)
        self.pause_menu = Entity(parent = self, enabled = False)

        self.garage_page1 = Entity(parent = self.garage_menu)
        self.garage_page2 = Entity(parent = self.garage_menu)

        self.menus = [
            self.start_menu, self.host_menu, self.created_server_menu, self.server_menu,
            self.main_menu, self.race_menu, self.maps_menu, self.settings_menu, self.video_menu, self.gameplay_menu,
            self.controls_menu, self.garage_menu, self.pause_menu
        ]
        
        self.car = car
        self.sand_track = sand_track
        self.grass_track = grass_track
        self.snow_track = snow_track
        self.forest_track = forest_track
        self.savannah_track = savannah_track
        self.ai_list = ai_list

        self.tracks = [
            self.sand_track, self.grass_track, self.snow_track, self.forest_track, self.savannah_track
        ]

        # Animate the menu
        for menu in (self.start_menu, self.main_menu, self.race_menu, self.maps_menu, self.settings_menu, self.video_menu, self.gameplay_menu, self.controls_menu, self.pause_menu, self.garage_menu):
            def animate_in_menu(menu = menu):
                for i, e in enumerate(menu.children):
                    e.original_scale = e.scale
                    e.scale -= 0.01
                    e.animate_scale(e.original_scale, delay = i * 0.05, duration = 0.1, curve = curve.out_quad)

                    e.alpha = 0
                    e.animate("alpha", 0.7, delay = i * 0.05, duration = 0.1, curve = curve.out_quad)

                    if hasattr(e, "text_entity"):
                        e.text_entity.alpha = 0
                        e.text_entity.animate("alpha", 1, delay = i * 0.05, duration = 0.1)

            menu.on_enable = animate_in_menu

        # Start Menu

        self.car.position = (-80, -42, 18.8)
        self.car.rotation = (0, 90, 0)
        self.car.enable()
        self.grass_track.enable()

        def singleplayer():
            car.multiplayer = False
            self.start_menu.disable()
            self.main_menu.enable()
            grass_track.enable()
            self.car.position = (0, 0, 4)
            camera.rotation = (35, -20, 0)
            self.car.camera_follow.offset = self.car.camera_angle
            self.car.disable()
            for track in self.tracks:
                for i in track.track:
                    i.disable()
            for track in self.grass_track.track:
                track.enable()

        def multiplayer():
            self.start_menu.disable()
            self.host_menu.enable()
            self.car.enable()
            self.car.position = (-3, -44.5, 92)
            grass_track.disable()
            snow_track.enable()
            for track in self.tracks:
                for i in track.track:
                    i.disable()
            for track in self.snow_track.track:
                track.enable()

        def quit():
            application.quit()
            os._exit(0)

        start_title = Entity(model = "quad", scale = (0.5, 0.2, 0.2), texture = "rally-logo", parent = self.start_menu, y = 0.3)
        quit_button_start = Button(text = "X", color = color.hex("FF1414"), highlight_color = color.hex("FF4747"), scale_y = 0.058, scale_x = 0.06, y = 0.43, x = 0.85, parent = self.start_menu)

        if window.exit_button.enabled:
            quit_button_start.disable()

        singleplayer_button = Button(text = "Singleplayer", color = color.gray, highlight_color = color.light_gray, scale_y = 0.1, scale_x = 0.3, y = 0.05, parent = self.start_menu)
        multiplayer_button = Button(text = "Multiplayer", color = color.gray, highlight_color = color.light_gray, scale_y = 0.1, scale_x = 0.3, y = -0.08, parent = self.start_menu)
        
        singleplayer_button.on_click = Func(singleplayer)
        multiplayer_button.on_click = Func(multiplayer)
        quit_button_start.on_click = Func(quit)

        # Host Server Menu

        def create_server():
            if str(self.car.host_ip.text) != "IP" and str(self.car.host_port) != "PORT":
                self.car.server = Server(car.host_ip, car.host_port)
                self.car.server_running = True
                self.car.server.start_server = True
                self.host_menu.disable()
                self.created_server_menu.enable()
                self.car.enable()
                self.car.position = (-63, -40, -7)
                self.car.rotation = (0, 90, 0)
                snow_track.disable()
                sand_track.enable()
                back_button_server.disable()
                for track in self.tracks:
                    for i in track.track:
                        i.disable()
                for track in self.sand_track.track:
                    track.enable()

        def join_server_func():
            self.host_menu.disable()
            self.server_menu.enable()
            self.car.enable()
            self.car.position = (-105, -50, -59)
            snow_track.disable()
            sand_track.enable()
            for track in self.tracks:
                for i in track.track:
                    i.disable()
            for track in self.sand_track.track:
                track.enable()

        def back_host():
            self.host_menu.disable()
            self.start_menu.enable()
            self.car.position = (-80, -42, 18.8)
            self.car.rotation = (0, 90, 0)
            self.car.enable()
            self.grass_track.enable()
            self.snow_track.disable()
            for track in self.tracks:
                for i in track.track:
                    i.disable()
            for track in self.grass_track.track:
                track.enable()
        
        self.car.host_ip = InputField(default_value = "IP", limit_content_to = "0123456789.localhost", color = color.black, alpha = 100, y = 0.1, parent = self.host_menu)
        self.car.host_port = InputField(default_value = "PORT", limit_content_to = "0123456789", color = color.black, alpha = 100, y = 0.02, parent = self.host_menu)

        create_server_button = Button(text = "Create Server", color = color.hex("F58300"), highlight_color = color.gray, scale_y = 0.1, scale_x = 0.3, y = -0.1, parent = self.host_menu)
        join_server_button = Button(text = "Join Server", color = color.hex("0097F5"), highlight_color = color.gray, scale_y = 0.1, scale_x = 0.3, y = -0.22, parent = self.host_menu)
        back_button_host = Button(text = "<- Back", color = color.gray, scale_y = 0.05, scale_x = 0.2, y = 0.45, x = -0.65, parent = self.host_menu)

        create_server_button.on_click = Func(create_server)
        join_server_button.on_click = Func(join_server_func)
        back_button_host.on_click = Func(back_host)

        # Created Server

        def join_hosted_server_func():
            car.ip.text = car.host_ip.text
            car.port.text = car.host_port.text
            car.multiplayer = True
            self.created_server_menu.disable()
            self.main_menu.enable()
            self.car.position = (0, 0, 4)
            camera.rotation = (35, -20, 0)
            self.car.camera_follow.offset = self.car.camera_angle
            self.car.disable()
            self.sand_track.disable()
            self.grass_track.enable()
            for track in self.tracks:
                for i in track.track:
                    i.disable()
            for track in self.grass_track.track:
                track.enable()

        def stop_server():
            application.quit()
            os._exit(0)

        self.username_created_server = InputField(default_value = car.username_text, color = color.black, alpha = 100, y = 0.05, parent = self.created_server_menu)
        join_hosted_server = Button(text = "Join Server", color = color.hex("F58300"), highlight_color = color.gray, scale_y = 0.1, scale_x = 0.3, y = -0.1, parent = self.created_server_menu)
        running = Text(text = "Running server...", scale = 1.5, line_height = 2, x = 0, origin = 0, y = 0.2, parent = self.created_server_menu)
        stop_button = Button(text = "Stop", color = color.hex("D22828"), scale_y = 0.1, scale_x = 0.3, y = -0.22, parent = self.created_server_menu)

        join_hosted_server.on_click = Func(join_hosted_server_func)
        stop_button.on_click = Func(stop_server)

        # Server Menu

        def join_server():
            if str(self.car.ip.text) != "IP" and str(self.car.port.text) != "PORT":
                car.multiplayer = True
                self.server_menu.disable()
                self.main_menu.enable()
                grass_track.enable()
                sand_track.disable()
                self.car.position = (0, 0, 4)
                camera.rotation = (35, -20, 0)
                self.car.camera_follow.offset = self.car.camera_angle
                self.car.disable()
                self.car.connected = False
                for track in self.tracks.track:
                    track.disable()
                for track in self.grass_track.track:
                    track.enable()

        def back_server():
            self.host_menu.enable()
            self.server_menu.disable()
            self.car.enable()
            self.car.position = (-3, -44.5, 92)
            sand_track.disable()
            snow_track.enable()
            for track in self.tracks:
                for i in track.track:
                    i.disable()
            for track in self.snow_track.track:
                track.enable()

        car.username = InputField(default_value = car.username_text, color = color.black, alpha = 100, y = 0.18, parent = self.server_menu)
        car.ip = InputField(default_value = "IP", limit_content_to = "0123456789.localhost", color = color.black, alpha = 100, y = 0.1, parent = self.server_menu)
        car.port = InputField(default_value = "PORT", limit_content_to = "0123456789", color = color.black, alpha = 100, y = 0.02, parent = self.server_menu)
        join_button = Button(text = "Join Server", color = color.hex("F58300"), highlight_color = color.gray, scale_y = 0.1, scale_x = 0.3, y = -0.1, parent = self.server_menu)
        back_button_server = Button(text = "<- Back", color = color.gray, scale_y = 0.05, scale_x = 0.2, y = 0.45, x = -0.65, parent = self.server_menu)

        join_button.on_click = Func(join_server)
        back_button_server.on_click = Func(back_server)

        # Main Menu

        def back_singleplayer():
            self.car.position = (-80, -42, 18.8)
            self.car.rotation = (0, 90, 0)
            self.car.enable()
            self.grass_track.enable()
            self.start_menu.enable()
            self.main_menu.disable()
            if self.car.multiplayer_update:
                self.car.multiplayer_update = False
            for track in self.tracks:
                for i in track.track:
                    i.disable()
            for track in self.grass_track.track:
                track.enable()

        title = Entity(model = "quad", scale = (0.5, 0.2, 0.2), texture = "rally-logo", parent = self.main_menu, y = 0.3)

        back_button_singleplayer = Button(text = "Back", color = color.black, scale_y = 0.1, scale_x = 0.3, y = -0.34, parent = self.main_menu)
        back_button_singleplayer.on_click = Func(back_singleplayer)

        # Maps Menu

        def start():
            self.main_menu.disable()
            if self.car.multiplayer_update:
                ai_button.disable()
                self.ai_slider.disable()
                self.maps_menu.enable()
            else:
                self.race_menu.enable()

        def back():
            self.maps_menu.disable()
            if self.car.multiplayer_update:
                self.main_menu.enable()
            else:
                self.race_menu.enable()
                
            self.car.position = (0, 0, 4)
            unlocked_text.disable()
            for track in self.tracks:
                track.alpha = 255
                track.disable()
                for i in track.track:
                    i.disable()
            for track in self.grass_track.track:
                track.enable()
            grass_track.enable()

        def ai_func():
            self.car.ai = not self.car.ai
            if self.car.ai:
                ai_button.text = "AI: On"
                self.ai_slider.enable()
            elif self.car.ai == False:
                ai_button.text = "AI: Off"
                self.ai_slider.disable()

        def sand_track_func():
            if sand_track.unlocked:
                self.car.enable()
                mouse.locked = True
                self.maps_menu.disable()
                self.car.position = (-63, -30, -7)
                self.car.rotation = (0, 90, 0)
                self.car.reset_count_timer.enable()

                if self.car.multiplayer_update == False and self.car.ai:
                    for ai in ai_list:
                        if ai.set_enabled:
                            ai.enable()
                        ai.position = (-63, -40, -7) + (random.randint(-5, 5), random.randint(-3, 5), random.randint(-5, 5))
                        ai.rotation = (0, 65, 0)
                        ai.set_random_texture()
                        ai.next_path = ai.sap1
                        
                for track in self.tracks:
                    track.disable()
                    for i in track.track:
                        i.disable()

                sand_track.enable()
                sand_track.played = True

                for s in sand_track.track:
                    s.enable()
                    s.alpha = 255

                if self.car.time_trial == False:
                    self.car.highscore_count = float(self.car.sand_track_hs)
                else:
                    self.car.highscore_count = float(self.car.sand_track_laps)
            else:
                unlocked_text.shake()

        def grass_track_func():
            if grass_track.unlocked:
                self.car.enable()
                mouse.locked = True
                self.maps_menu.disable()
                self.car.position = (-80, -30, 15)
                self.car.rotation = (0, 90, 0)
                self.car.reset_count_timer.enable()

                if self.car.multiplayer_update == False and self.car.ai:
                    for ai in ai_list:
                        if ai.set_enabled:
                            ai.enable()
                        ai.position = (-80, -35, 15) + (random.randint(-5, 5), random.randint(-3, 5), random.randint(-5, 5))
                        ai.rotation = (0, 90, 0)
                        ai.set_random_texture()
                        ai.next_path = ai.gp1

                for track in self.tracks:
                    track.disable()
                    for i in track.track:
                        i.disable()

                grass_track.enable()
                grass_track.played = True

                for g in grass_track.track:
                    g.enable()
                    g.alpha = 255

                if self.car.time_trial == False:
                    self.car.highscore_count = float(self.car.grass_track_hs)
                else:
                    self.car.highscore_count = float(self.car.grass_track_laps)
            else:
                unlocked_text.shake()

        def snow_track_func():
            if snow_track.unlocked:
                self.car.enable()
                mouse.locked = True
                self.maps_menu.disable()
                self.car.position = (-5, -35, 90)
                self.car.rotation = (0, 90, 0)
                self.car.reset_count_timer.enable()

                if self.car.multiplayer_update == False and self.car.ai:
                    for ai in ai_list:
                        if ai.set_enabled:
                            ai.enable()
                        ai.position = (-5, -40, 90) + (random.randint(-5, 5), random.randint(-3, 5), random.randint(-5, 5))
                        ai.rotation = (0, 90, 0)
                        ai.set_random_texture()
                        ai.next_path = ai.snp1
                        
                for track in self.tracks:
                    track.disable()
                    for i in track.track:
                        i.disable()

                snow_track.enable()
                snow_track.played = True

                for s in snow_track.track:
                    s.enable()
                    s.alpha = 255

                if self.car.time_trial == False:
                    self.car.highscore_count = float(self.car.snow_track_hs)
                else:
                    self.car.highscore_count = float(self.car.snow_track_laps)
            else:
                unlocked_text.shake()

        def forest_track_func():
            if forest_track.unlocked:
                self.car.enable()
                mouse.locked = True
                self.maps_menu.disable()
                self.car.position = (12, -35, 73)
                self.car.rotation = (0, 90, 0)
                self.car.reset_count_timer.enable()

                if self.car.multiplayer_update == False and self.car.ai:
                    for ai in ai_list:
                        if ai.set_enabled:
                            ai.enable()
                        ai.position = (12, -40, 73) + (random.randint(-5, 5), random.randint(-3, 5), random.randint(-5, 5))
                        ai.rotation = (0, 90, 0)
                        ai.set_random_texture()
                        ai.next_path = ai.fp1

                for track in self.tracks:
                    track.disable()
                    for i in track.track:
                        i.disable()

                forest_track.enable()
                forest_track.played = True
                
                for f in forest_track.track:
                    f.enable()
                    f.alpha = 255

                if self.car.time_trial == False:
                    self.car.highscore_count = float(self.car.forest_track_hs)
                else:
                    self.car.highscore_count = float(self.car.forest_track_laps)
            else:
                unlocked_text.shake()

        def savannah_track_func():
            if savannah_track.unlocked:
                self.car.enable()
                mouse.locked = True
                self.maps_menu.disable()
                self.car.position = (-12, -35, 40)
                self.car.rotation = (0, 90, 0)
                self.car.reset_count_timer.enable()

                if self.car.multiplayer_update == False and self.car.ai:
                    for ai in ai_list:
                        if ai.set_enabled:
                            ai.enable()
                        ai.position = (-12, -35, 40) + (random.randint(-5, 5), random.randint(-3, 5), random.randint(-5, 5))
                        ai.rotation = (0, 90, 0)
                        ai.set_random_texture()
                        ai.next_path = ai.svp1

                for track in self.tracks:
                    track.disable()
                    for i in track.track:
                        i.disable()

                savannah_track.enable()
                savannah_track.played = True

                for s in savannah_track.track:
                    s.enable()
                    s.alpha = 255

                if self.car.time_trial == False:
                    self.car.highscore_count = float(self.car.savannah_track_hs)
                else:
                    self.car.highscore_count = float(self.car.savannah_track_laps)
            else:
                unlocked_text.shake()

        def sand_track_hover():
            for track in self.tracks:
                track.disable()
                for i in track.track:
                    if track != sand_track:
                        i.disable()
                    else:
                        i.enable()
            sand_track.enable()
            self.car.position = (-40, 30, -175)
            unlocked_text.disable()
            if not self.car.time_trial:
                highscore_text.enable()
                highscore_text.text = "Highscore: " + str(round(self.car.sand_track_hs, 2)) + "\n Mandaw: 14.49"

        def grass_track_hover():
            for track in self.tracks:
                track.disable()
                for i in track.track:
                    if track != grass_track:
                        i.disable()
                    else:
                        i.enable()
            grass_track.enable()
            self.car.position = (20, 30, -100)
            if grass_track.unlocked == False:
                grass_track.alpha = 200
                unlocked_text.enable()
                unlocked_text.text = "Get Less Than 17 seconds on Sand Track"
                highscore_text.disable()
                for track in grass_track.track:
                    i.alpha = 200
            else:
                if not self.car.time_trial:
                    highscore_text.enable()
                    highscore_text.text = "Highscore: " + str(round(self.car.grass_track_hs, 2)) + "\n Mandaw: 17.76"
                unlocked_text.disable()
                grass_track.alpha = 255

        def snow_track_hover():
            for track in self.tracks:
                track.disable()
                for i in track.track:
                    if track != snow_track:
                        i.disable()
                    else:
                        i.enable()
            snow_track.enable()
            self.car.position = (20, 30, -80)
            if snow_track.unlocked == False:
                snow_track.alpha = 200
                unlocked_text.enable()
                unlocked_text.text = "Get Less Than 19 seconds on Grass Track"
                highscore_text.disable()
                for track in snow_track.track:
                    i.alpha = 200
            else:
                if not self.car.time_trial:
                    highscore_text.enable()
                    highscore_text.text = "Highscore: " + str(round(self.car.snow_track_hs, 2)) + "\n Mandaw: 31.45"
                unlocked_text.disable()
                snow_track.alpha = 255
        
        def forest_track_hover():
            for track in self.tracks:
                track.disable()
                for i in track.track:
                    if track != forest_track:
                        i.disable()
                    else:
                        i.enable()
            forest_track.enable()
            self.car.position = (50, 30, -100)
            if forest_track.unlocked == False:
                forest_track.alpha = 200
                unlocked_text.enable()
                unlocked_text.text = "Get Less Than 33 seconds on Snow Track"
                highscore_text.disable()
                for track in forest_track.track:
                    i.alpha = 200
            else:
                if not self.car.time_trial:
                    highscore_text.enable()
                    highscore_text.text = "Highscore: " + str(round(self.car.forest_track_hs, 2)) + "\n Mandaw: 24.28"
                unlocked_text.disable()
                forest_track.alpha = 255

        def savannah_track_hover():
            for track in self.tracks:
                track.disable()
                for i in track.track:
                    if track != savannah_track:
                        i.disable()
                    else:
                        i.enable()
            savannah_track.enable()
            self.car.position = (25, 30, -130)
            if savannah_track.unlocked == False:
                savannah_track.alpha = 200
                unlocked_text.enable()
                unlocked_text.text = "Get Less Than 26 seconds on Forest Track"
                highscore_text.disable()
                for track in savannah_track.track:
                    i.alpha = 200
            else:
                if not self.car.time_trial:
                    highscore_text.enable()
                    highscore_text.text = "Highscore: " + str(round(self.car.savannah_track_hs, 2)) + "\n Mandaw: 14.13"
                unlocked_text.disable()
                savannah_track.alpha = 255

        start_button = Button(text = "Start Game", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.02, parent = self.main_menu)
        sand_track_button = Button(text = "Sand Track", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.3, x = -0.5, parent = self.maps_menu)
        grass_track_button = Button(text = "Grass Track", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.3, x = 0, parent = self.maps_menu)
        snow_track_button = Button(text = "Snow Track", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.3, x = 0.5, parent = self.maps_menu)
        forest_track_button = Button(text = "Forest Track", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.1, x = -0.5, parent = self.maps_menu)
        savannah_track_button = Button(text = "Savannah Track", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.1, x = 0, parent = self.maps_menu)
        back_button = Button(text = "<- Back", color = color.gray, scale_y = 0.05, scale_x = 0.2, y = 0.45, x = -0.65, parent = self.maps_menu)
        
        unlocked_text = Text("Get Less Than 16 seconds on Sand Track to Unlock Grass Track", scale = 1.5, color = color.orange, line_height = 2, origin = 0, y = -0.1, parent = self.maps_menu)
        unlocked_text.disable()

        highscore_text = Text("", scale = 1.2, color = color.white, line_height = 2, origin = 0, y = -0.07, parent = self.maps_menu)
        highscore_text.disable()

        ai_button = Button(text = "AI: Off", color = color.light_gray, scale_y = 0.1, scale_x = 0.3, y = -0.28, x = 0, parent = self.maps_menu)
        self.ai_slider = Slider(min = 1, max = 3, default = 1, text = "AI", y = -0.4, x = -0.3, scale = 1.3, parent = self.maps_menu, dynamic = True)
        self.ai_slider.step = 1
        self.ai_slider.disable()

        self.leaderboard_background = Entity(model = "quad", color = color.hex("0099ff"), alpha = 100, scale = (0.4, 0.42), position = Vec2(0.6, 0.25), parent = camera.ui)
        self.leaderboard_title = Text("Leaderboard", color = color.gold, scale = 5, line_height = 2, origin = 0, y = 0.4, parent = self.leaderboard_background)
        
        self.leaderboard_01 = Text(text = "", color = color.hex("#CCCCCC"), scale = 3, line_height = 2, x = 0, origin = 0, y = 0.2, parent = self.leaderboard_background)
        self.leaderboard_02 = Text(text = "", color = color.hex("#CCCCCC"), scale = 3, line_height = 2, x = 0, origin = 0, y = 0.1, parent = self.leaderboard_background)
        self.leaderboard_03 = Text(text = "", color = color.hex("#CCCCCC"), scale = 3, line_height = 2, x = 0, origin = 0, y = 0, parent = self.leaderboard_background)
        self.leaderboard_04 = Text(text = "", color = color.hex("#CCCCCC"), scale = 3, line_height = 2, x = 0, origin = 0, y = -0.1, parent = self.leaderboard_background)
        self.leaderboard_05 = Text(text = "", color = color.hex("#CCCCCC"), scale = 3, line_height = 2, x = 0, origin = 0, y = -0.2, parent = self.leaderboard_background)
        
        self.leaderboard_texts = [self.leaderboard_background, self.leaderboard_title, self.leaderboard_01, self.leaderboard_02, self.leaderboard_03, self.leaderboard_04, self.leaderboard_05]

        self.leaderboard_background.disable()
        self.leaderboard_title.disable()

        sand_track_button.on_mouse_enter = Func(sand_track_hover)
        grass_track_button.on_mouse_enter = Func(grass_track_hover)
        snow_track_button.on_mouse_enter = Func(snow_track_hover)
        forest_track_button.on_mouse_enter = Func(forest_track_hover)
        savannah_track_button.on_mouse_enter = Func(savannah_track_hover)

        start_button.on_click = Func(start)
        sand_track_button.on_click = Func(sand_track_func)
        grass_track_button.on_click = Func(grass_track_func)
        snow_track_button.on_click = Func(snow_track_func)
        forest_track_button.on_click = Func(forest_track_func)
        savannah_track_button.on_click = Func(savannah_track_func)
        ai_button.on_click = Func(ai_func)
        back_button.on_click = Func(back)

        # Race Menu

        def race_button_func():
            self.race_menu.disable()
            self.maps_menu.enable()
            ai_button.enable()
            self.car.time_trial = False
            self.car.count = 0.0
            self.car.reset_count = 0.0

        def time_trial_func():
            self.race_menu.disable()
            self.maps_menu.enable()
            ai_button.disable()
            self.ai_slider.disable()
            self.car.time_trial = True
            self.car.count = 100.0
            self.car.reset_count = 100.0
            self.car.ai = False

        def back_race():
            self.race_menu.disable()
            self.main_menu.enable()

        race_button = Button(text = "Race", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.06, parent = self.race_menu)
        time_trial_button = Button(text = "Time Trial", color = color.black, scale_y = 0.1, scale_x = 0.3, y = -0.06, parent = self.race_menu)
        back_button_race = Button(text = "<- Back", color = color.gray, scale_y = 0.05, scale_x = 0.2, y = 0.45, x = -0.65, parent = self.race_menu)

        race_button.on_click = Func(race_button_func)
        time_trial_button.on_click = Func(time_trial_func)
        back_button_race.on_click = Func(back_race)

        # Settings

        def settings():
            self.main_menu.disable()
            self.settings_menu.enable()

        def video():
            self.settings_menu.disable()
            self.video_menu.enable()

        def gameplay():
            self.settings_menu.disable()
            self.gameplay_menu.enable()

        def controls():
            self.settings_menu.disable()
            self.controls_menu.enable()

        def back_settings():
            self.settings_menu.disable()
            self.main_menu.enable()

        settings_button = Button(text = "Settings", color = color.black, scale_y = 0.1, scale_x = 0.3, y = -0.22, parent = self.main_menu)
        
        video_button = Button(text = "Video", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.18, parent = self.settings_menu)
        gameplay_button = Button(text = "Gameplay", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.06, parent = self.settings_menu)
        controls_button = Button(text = "Controls", color = color.black, scale_y = 0.1, scale_x = 0.3, y = -0.06, parent = self.settings_menu)

        back_button_settings = Button(text = "Back", color = color.black, scale_y = 0.1, scale_x = 0.3, y = -0.18, parent = self.settings_menu)

        settings_button.on_click = Func(settings) 
        video_button.on_click = Func(video)
        gameplay_button.on_click = Func(gameplay)
        controls_button.on_click = Func(controls)
        back_button_settings.on_click = Func(back_settings)

        # Gameplay Menu

        def camera_shake():
            self.car.camera_shake_option = not self.car.camera_shake_option
            if self.car.camera_shake_option:
                camera_shake_button.text = "Camera Shake: On"
            elif self.car.camera_shake_option == False:
                camera_shake_button.text = "Camera Shake: Off"

        def back_gameplay():
            self.gameplay_menu.disable()
            self.settings_menu.enable()

        camera_shake_button = Button("Camera Shake: On", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.12, parent = self.gameplay_menu)
        reset_highsore_button = Button(text = "Reset Highscore", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0, parent = self.gameplay_menu)
        back_button_gameplay = Button(text = "Back", color = color.black, scale_y = 0.1, scale_x = 0.3, y = -0.12, parent = self.gameplay_menu)

        camera_shake_button.on_click = Func(camera_shake)
        reset_highsore_button.on_click = Func(self.car.reset_highscore)
        back_button_gameplay.on_click = Func(back_gameplay)

        # Video Menu

        def fullscreen():
            window.fullscreen = not window.fullscreen
            if window.fullscreen:
                fullscreen_button.text = "Fullscreen: On"
            elif window.fullscreen == False:
                fullscreen_button.text = "Fullscreen: Off"

        def borderless():
            window.borderless = not window.borderless
            if window.borderless:
                borderless_button.text = "Borderless: On"
            elif window.borderless == False:
                borderless_button.text = "Borderless: Off"
            window.exit_button.enable()

        def fps():
            window.fps_counter.enabled = not window.fps_counter.enabled
            if window.fps_counter.enabled:
                fps_button.text = "FPS: On"
            elif window.fps_counter.enabled == False:
                fps_button.text = "FPS: Off"

        def exit_button_func():
            window.exit_button.enabled = not window.exit_button.enabled
            if window.exit_button.enabled:
                exit_button.text = "Exit Button: On"
            elif window.exit_button.enabled == False:
                exit_button.text = "Exit Button: Off"

        def back_video():
            self.video_menu.disable()
            self.settings_menu.enable()

        fullscreen_button = Button("Fullscreen: On", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.24, parent = self.video_menu)
        borderless_button = Button("Borderless: On", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.12, parent = self.video_menu)
        fps_button = Button("FPS: Off", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0, parent = self.video_menu)
        exit_button = Button("Exit Button: Off", color = color.black, scale_y = 0.1, scale_x = 0.3, y = -0.12, parent = self.video_menu)
        back_button_video = Button(text = "Back", color = color.black, scale_y = 0.1, scale_x = 0.3, y = -0.24, parent = self.video_menu)

        fullscreen_button.on_click = Func(fullscreen)
        borderless_button.on_click = Func(borderless)
        fps_button.on_click = Func(fps)
        exit_button.on_click = Func(exit_button_func)
        back_button_video.on_click = Func(back_video)

        # Controls

        def back_controls():
            self.controls_menu.disable()
            self.settings_menu.enable()

        def controls_settings():
            if self.car.controls == "wasd":
                self.car.controls = "zqsd"
                controls_settings_button.text = "Controls: ZQSD"
            elif self.car.controls == "zqsd":
                self.car.controls = "wasd"
                controls_settings_button.text = "Controls: WASD"

        controls_settings_button = Button("Controls: WASD", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.06, parent = self.controls_menu)
        back_button_controls = Button(text = "Back", color = color.black, scale_y = 0.1, scale_x = 0.3, y = -0.06, parent = self.controls_menu)

        back_button_controls.on_click = Func(back_controls)
        controls_settings_button.on_click = Func(controls_settings)

        # Pause Menu

        def resume():
            mouse.locked = True
            self.pause_menu.disable()

        def respawn():
            if sand_track.enabled:
                self.car.position = (-63, -40, -7)
                self.car.rotation = (0, 90, 0)
                if self.car.multiplayer_update == False and self.car.ai:
                    for ai in ai_list:
                        ai.disable()
                        if ai.set_enabled:
                            ai.enable()
                        ai.position = (-63, -45, -7) + (random.randint(-5, 5), random.randint(-3, 5), random.randint(-5, 5))
                        ai.rotation = (0, 90, 0)
                        ai.set_random_texture()
                        ai.next_path = ai.sap1
                        ai.speed = 0
                        ai.velocity_y = 0
            elif grass_track.enabled:
                self.car.position = (-80, -30, 15)
                self.car.rotation = (0, 90, 0)
                if self.car.multiplayer_update == False and self.car.ai:
                    for ai in ai_list:
                        ai.disable()
                        if ai.set_enabled:
                            ai.enable()
                        ai.position = (-80, -35, 15) + (random.randint(-5, 5), random.randint(-3, 5), random.randint(-5, 5))
                        ai.rotation = (0, 90, 0)
                        ai.set_random_texture()
                        ai.next_path = ai.gp1
                        ai.speed = 0
                        ai.velocity_y = 0
            elif snow_track.enabled:
                self.car.position = (-5, -35, 90)
                self.car.rotation = (0, 90, 0)
                if self.car.multiplayer_update == False and self.car.ai:
                    for ai in ai_list:
                        ai.disable()
                        if ai.set_enabled:
                            ai.enable()
                        ai.position = (-5, -40, 90) + (random.randint(-5, 5), random.randint(-3, 5), random.randint(-5, 5))
                        ai.rotation = (0, 90, 0)
                        ai.set_random_texture()
                        ai.next_path = ai.snp1
                        ai.speed = 0
                        ai.velocity_y = 0
            elif forest_track.enabled:
                self.car.position = (12, -35, 73)
                self.car.rotation = (0, 90, 0)
                if self.car.multiplayer_update == False and self.car.ai:
                    for ai in ai_list:
                        ai.disable()
                        if ai.set_enabled:
                            ai.enable()
                        ai.position = (12, -40, 73) + (random.randint(-5, 5), random.randint(-3, 5), random.randint(-5, 5))
                        ai.rotation = (0, 90, 0)
                        ai.set_random_texture()
                        ai.next_path = ai.fp1
                        ai.speed = 0
                        ai.velocity_y = 0
            elif savannah_track.enabled:
                self.car.position = (-12, -35, 40)
                self.car.rotation = (0, 90, 0)
                if self.car.multiplayer_update == False and self.car.ai:
                    for ai in ai_list:
                        ai.disable()
                        if ai.set_enabled:
                            ai.enable()
                        ai.position = (-12, -35, 40) + (random.randint(-5, 5), random.randint(-3, 5), random.randint(-5, 5))
                        ai.rotation = (0, 90, 0)
                        ai.set_random_texture()
                        ai.next_path = ai.svp1
                        ai.speed = 0
                        ai.velocity_y = 0
            self.car.speed = 0
            self.car.anti_cheat = 1
            self.car.velocity_y = 0
            if self.car.time_trial == False:
                self.car.count = 0.0
                self.car.reset_count = 0.0
                self.car.timer_running = False
            elif self.car.time_trial:
                self.count = 100.0
                self.reset_count = 100.0
                self.laps = 0
                self.timer_running = False
                self.start_time = False

        def main_menu():
            self.car.position = (0, 0, 4)
            self.car.disable()
            self.car.rotation = (0, 65, 0)
            self.car.speed = 0
            self.car.velocity_y = 0
            self.car.count = 0.0
            self.car.last_count = 0.0
            self.car.reset_count = 0.0
            self.car.laps = 0
            self.car.time_trial = False
            self.car.start_time = False
            self.car.reset_count_timer.disable()
            self.car.timer_running = False
            self.car.anti_cheat = 1
            self.main_menu.enable()
            self.pause_menu.disable()
            for track in self.tracks:
                track.disable()
                track.alpha = 255
                for i in track.track:
                    i.disable()
            grass_track.enable()

            if self.car.multiplayer_update == False and self.car.ai:
                for ai in ai_list:
                    ai.disable()
                    ai.speed = 0
                    ai.velocity_y = 0
                
        p_resume_button = Button(text = "Resume", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.11, parent = self.pause_menu)
        p_respawn_button = Button(text = "Respawn", color = color.black, scale_y = 0.1, scale_x = 0.3, y = -0.01, parent = self.pause_menu)
        p_mainmenu_button = Button(text = "Main Menu", color = color.black, scale_y = 0.1, scale_x = 0.3, y = -0.13, parent = self.pause_menu)
        p_mainmenu_button.on_click = Func(main_menu)
        p_respawn_button.on_click = Func(respawn)
        p_resume_button.on_click = Func(resume)

        # Garage

        def back_garage():
            self.garage_menu.disable()
            self.main_menu.enable()
            self.car.position = (0, 0, 4)
            camera.rotation = (35, -20, 0)
            self.car.camera_follow.offset = self.car.camera_angle
            self.car.disable()
            grass_track.enable()
            sand_track.disable()
            for track in self.tracks:
                for i in track.track:
                    i.disable()
            for track in self.grass_track.track:
                track.enable()

            self.car.highscore_count = float(self.car.grass_track_hs)

        def garage_button_func():
            self.garage_menu.enable()
            self.main_menu.disable()
            self.car.enable()
            self.car.position = (-105, -50, -59)
            grass_track.disable()
            sand_track.enable()
            for track in self.tracks:
                for i in track.track:
                    i.disable()
            for track in self.sand_track.track:
                track.enable()

        def left():
            self.garage_page1.enable()
            self.garage_page2.disable()

        def right():
            self.garage_page1.disable()
            self.garage_page2.enable()

        def change_colour(colour):
            """
            Changes the car color to the selected color after a small animation.
            """
            if colour == "red":
                car.texture = "car-red.png"
                car.animate_rotation_y(car.rotation_y + 360, duration = 0.4, curve = curve.in_out_quad)
            if colour == "blue":
                car.texture = "car-blue.png"
                car.animate_rotation_y(car.rotation_y + 360, duration = 0.4, curve = curve.in_out_quad)
            if colour == "green":
                if car.green_unlocked:
                    car.texture = "car-green.png"
                    car.animate_rotation_y(car.rotation_y + 360, duration = 0.4, curve = curve.in_out_quad)
                else:
                    self.garage_locked_text("Get Less Than 19s on Grass Track")
            if colour == "orange":
                if car.orange_unlocked:
                    car.texture = "car-orange.png"
                    car.animate_rotation_y(car.rotation_y + 360, duration = 0.4, curve = curve.in_out_quad)
                else:
                    self.garage_locked_text("Get Less Than 16s on Sand Track")
            if colour == "black":
                if car.black_unlocked:
                    car.texture = "car-black.png"
                    car.animate_rotation_y(car.rotation_y + 360, duration = 0.4, curve = curve.in_out_quad)
                else:
                    self.garage_locked_text("Get Less Than 16s on Savannah Track")
            if colour == "white":
                if car.white_unlocked:
                    car.texture = "car-white.png"
                    car.animate_rotation_y(car.rotation_y + 360, duration = 0.4, curve = curve.in_out_quad)
                else:
                    self.garage_locked_text("Get Less Than 33s on Snow Track")

        def viking_helmet():
            if self.car.viking_helmet_unlocked:
                car.animate_rotation_y(car.rotation_y + 360, duration = 0.4, curve = curve.in_out_quad)
                car.viking_helmet.enabled = not car.viking_helmet.enabled
                car.duck.disable()
                car.banana.disable()
                car.surfinbird.disable()
            else:
                self.garage_locked_text("Get Less Than 15s on Sand Track")

        def duck():
            if self.car.duck_unlocked:
                car.animate_rotation_y(car.rotation_y + 360, duration = 0.4, curve = curve.in_out_quad)
                car.duck.enabled = not car.duck.enabled
                car.viking_helmet.disable()
                car.banana.disable()
                car.surfinbird.disable()
            else:
                self.garage_locked_text("Get Less Than 25s on Forest Track")

        def banana():
            if self.car.banana_unlocked:
                car.animate_rotation_y(car.rotation_y + 360, duration = 0.4, curve = curve.in_out_quad)
                car.banana.enabled = not car.banana.enabled
                car.duck.disable()
                car.viking_helmet.disable()
                car.surfinbird.disable()
            else:
                self.garage_locked_text("Beat Mandaw on Grass Track")

        def surfinbird():
            if self.car.surfinbird_unlocked:
                car.animate_rotation_y(car.rotation_y + 360, duration = 0.4, curve = curve.in_out_quad)
                car.surfinbird.enabled = not car.surfinbird.enabled
                car.viking_helmet.disable()
                car.duck.disable()
                car.banana.disable()
            else:
                self.garage_locked_text("Beat Mandaw in Every Track")

        def viking_hover():
            self.garage_name_text.enable()
            self.garage_name_text.text = "Viking Helmet"

        def duck_hover():
            self.garage_name_text.enable()
            self.garage_name_text.text = "Duck"
        
        def banana_hover():
            self.garage_name_text.enable()
            self.garage_name_text.text = "Banana"

        def banana_hover():
            self.garage_name_text.enable()
            self.garage_name_text.text = "Banana"
        
        def surfinbird_hover():
            self.garage_name_text.enable()
            self.garage_name_text.text = "Surfin Bird"

        self.start_spin = True

        garage_button = Button(text = "Garage", color = color.black, scale_y = 0.1, scale_x = 0.3, y = -0.1, parent = self.main_menu)
        self.garage_page2.disable()

        back_button_garage = Button(text = "<- Back", color = color.gray, scale_y = 0.05, scale_x = 0.2, y = 0.45, x = -0.65, parent = self.garage_menu)
        left_arrow = Button(text = "<-", color = color.gray, scale_y = 0.05, scale_x = 0.1, y = -0.3, x = -0.6, parent = self.garage_menu)
        right_arrow = Button(text = "->", color = color.gray, scale_y = 0.05, scale_x = 0.1, y = -0.3, x = -0.4, parent = self.garage_menu)

        red_button = Button(color = color.red, scale_y = 0.1, scale_x = 0.15, y = 0.1, x = -0.7, parent = self.garage_page1)
        blue_button = Button(color = color.cyan, scale_y = 0.1, scale_x = 0.15, y = 0.1, x = -0.5, parent = self.garage_page1)
        green_button = Button(color = color.lime, scale_y = 0.1, scale_x = 0.15, y = 0.1, x = -0.3, parent = self.garage_page1)
        orange_button = Button(color = color.orange, scale_y = 0.1, scale_x = 0.15, y = -0.1, x = -0.7, parent = self.garage_page1)
        black_button = Button(color = color.black, scale_y = 0.1, scale_x = 0.15, y = -0.1, x = -0.5, parent = self.garage_page1)
        white_button = Button(color = color.white, scale_y = 0.1, scale_x = 0.15, y = -0.1, x = -0.3, parent = self.garage_page1)

        viking_helmet_button = Button(texture = "viking_helmet-icon.png", color = color.white, scale = (0.16, 0.1), y = 0.1, x = -0.7, alpha = 255, parent = self.garage_page2)
        duck_button = Button(texture = "duck-icon.png", color = color.white, scale = (0.16, 0.1), y = 0.1, x = -0.5, alpha = 255, parent = self.garage_page2)
        banana_button = Button(texture = "banana-icon.png", color = color.white, scale = (0.16, 0.1), y = 0.1, x = -0.3, alpha = 255, parent = self.garage_page2)
        surfinbird_button = Button(texture = "surfinbird-icon.png", color = color.white, scale = (0.16, 0.1), y = -0.1, x = -0.7, alpha = 255, parent = self.garage_page2)

        self.garage_name_text = Text("Surfin Bird", scale = 1.5, color = color.white, line_height = 2, origin = 0, x = -0.5, y = -0.4, parent = self.garage_menu)
        self.garage_name_text.disable()

        self.garage_unlocked_text = Text("Beat Mandaw in Every Track", scale = 1.5, color = color.orange, line_height = 2, origin = 0, y = 0.3, parent = self.garage_menu)
        self.garage_unlocked_text.disable()

        garage_button.on_click = Func(garage_button_func)
        back_button_garage.on_click = Func(back_garage)
        left_arrow.on_click = Func(left)
        right_arrow.on_click = Func(right)
        red_button.on_click = Func(change_colour, "red")
        blue_button.on_click = Func(change_colour, "blue")
        green_button.on_click = Func(change_colour, "green")
        orange_button.on_click = Func(change_colour, "orange")
        black_button.on_click = Func(change_colour, "black")
        white_button.on_click = Func(change_colour, "white")

        viking_helmet_button.on_click = Func(viking_helmet)
        duck_button.on_click = Func(duck)
        banana_button.on_click = Func(banana)
        surfinbird_button.on_click = Func(surfinbird)

        viking_helmet_button.on_mouse_enter = Func(viking_hover)
        viking_helmet_button.on_mouse_exit = Func(self.garage_name_text.disable)
        duck_button.on_mouse_enter = Func(duck_hover)
        duck_button.on_mouse_exit = Func(self.garage_name_text.disable)
        banana_button.on_mouse_enter = Func(banana_hover)
        banana_button.on_mouse_exit = Func(self.garage_name_text.disable)
        surfinbird_button.on_mouse_enter = Func(surfinbird_hover)
        surfinbird_button.on_mouse_exit = Func(self.garage_name_text.disable)

        # Server Error Log
        self.connected = Text(text = "Connected to server!", scale = 1.5, color = color.hex("4dff4d"), line_height = 2, x = -0.55, origin = 0, y = 0.45, parent = camera.ui)
        self.not_connected = Text(text = "Not connected to server...", scale = 1.5, color = color.hex("FF2E2E"), line_height = 2, x = -0.55, origin = 0, y = 0.45, parent = camera.ui)
        self.connected.disable()
        self.not_connected.disable()

    def garage_locked_text(self, warning):
        self.garage_unlocked_text.enable()
        self.garage_unlocked_text.text = warning
        self.garage_unlocked_text.shake()
        invoke(self.garage_unlocked_text.disable, delay = 1)

    def update(self):
        # AI Slider
        if self.car.multiplayer_update == False:
            if self.ai_slider.value == 0: 
                for ai in self.ai_list:
                    ai.set_enabled = False
            elif self.ai_slider.value == 1:
                self.ai_list[0].set_enabled = True
                self.ai_list[1].set_enabled = False
                self.ai_list[2].set_enabled = False
            elif self.ai_slider.value == 2:
                self.ai_list[0].set_enabled = True
                self.ai_list[1].set_enabled = True
                self.ai_list[2].set_enabled = False
            elif self.ai_slider.value == 3:
                self.ai_list[0].set_enabled = True
                self.ai_list[1].set_enabled = True
                self.ai_list[2].set_enabled = True

        # Set the camera's position and make the car rotate
        if self.start_menu.enabled or self.host_menu.enabled or self.garage_menu.enabled or self.server_menu.enabled:
            if not held_keys["right mouse"]:
                if self.start_spin:
                    self.car.rotation_y += 15 * time.dt
            else:
                self.car.rotation_y = mouse.x * 200

            if self.start_menu.enabled:
                self.car.camera_follow.offset = (-25, 4, 0)
                camera.rotation = (5, 90, 0)
            elif self.host_menu.enabled:
                self.car.camera_follow.offset = (-25, 8, 0)
                camera.rotation = (14, 90, 0)
            else:
                self.car.camera_follow.offset = (-25, 6, 5)
                camera.rotation = (10, 90, 0)

        # If the host menu or server menu is enabled, save username
        if self.host_menu.enabled or self.server_menu.enabled or self.created_server_menu.enabled:
            with open(self.car.username_path, "w") as user:
                if self.created_server_menu.enabled:
                    user.write(self.username_created_server.text)
                else:
                    user.write(self.car.username.text)

        # If multiplayer, start leaderboard
        if self.car.multiplayer_update:
            for menu in self.menus:
                if menu.enabled == False:
                    if self.sand_track.enabled or self.grass_track.enabled or self.snow_track.enabled or self.forest_track.enabled or self.savannah_track.enabled:
                        invoke(self.start_leaderboard, delay = 0.1)
                else:
                    for l in self.leaderboard_texts:
                        l.disable()
        else:
            for l in self.leaderboard_texts:
                l.disable()
            
    def start_leaderboard(self):
        for l in self.leaderboard_texts:
            l.enable()

        self.leaderboard_01.text = str(self.car.leaderboard_01)
        self.leaderboard_02.text = str(self.car.leaderboard_02)
        self.leaderboard_03.text = str(self.car.leaderboard_03)
        self.leaderboard_04.text = str(self.car.leaderboard_04)
        self.leaderboard_05.text = str(self.car.leaderboard_05)
    
    def input(self, key):
        # Pause menu
        if not self.start_menu.enabled and not self.main_menu.enabled and not self.server_menu.enabled and not self.settings_menu.enabled and not self.race_menu.enabled and not self.maps_menu.enabled and not self.settings_menu.enabled and not self.garage_menu.enabled and not self.controls_menu.enabled and not self.host_menu.enabled and not self.created_server_menu.enabled and not self.video_menu.enabled and not self.gameplay_menu.enabled:
            if key == "escape":
                self.pause_menu.enabled = not self.pause_menu.enabled
                mouse.locked = not mouse.locked

            if self.car.reset_count_timer.enabled == False:
                self.car.timer.enable()
            else:
                self.car.timer.disable()
             
            self.car.highscore.enable()
        
        else:
            self.car.timer.disable()
            self.car.reset_count_timer.disable()
            self.car.highscore.disable()
            self.car.laps_text.disable()

        if self.start_spin:
            self.car.copy_normals = False
        else:
            self.car.copy_normals = True

        if key == "w":
            self.start_spin = False
        elif key == "w up":
            self.start_spin = True