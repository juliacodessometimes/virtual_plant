class Plant:
    
    config = {
        "time_per_frame": {
            "dead": [150, 150, 150, 150],
            "shrivel": [150, 150, 150, 150],
            "droop":  [250, 250, 250, 250],
            "limp": [500, 500, 500, 500],
            "perk": [250, 250, 250, 250],
            "idle": [500, 500, 500, 500],
            "happy": [250, 250, 250, 250],
            "grow": [250, 250, 250]
        },
        "number_of_frames": {
            "dead": [],
            "shrivel": [],
            "droop":  [],
            "limp": [],
            "perk": [],
            "idle": [],
            "happy": [],
            "grow": []
        }
    }


    def __init__(self):
        # These are variables for keeping track of plant states.
        self.water_level = 150
        self.drying_speed = 1 # Unit per delta.
        self.growth_stage = 0
        self.mood = "idle"
        self.new_mood = "idle"
        self.age = 0 # Plant age at the current stage

        # Thresholds for moods
        self.age_threshold = 200

        self.happy_threshold = 200
        self.droop_threshold = 80
        self.dead_threshold = 0

        # Variables for keeping track of rendering states.
        self.current_index = 0
        self.time_per_frame = self.config["time_per_frame"][self.mood][self.growth_stage]
        self.number_of_frames = self.config["number_of_frames"][self.mood][self.growth_stage]
        self.time_elapsed = 0

    def add_water(self, amount):
        # Adds water to plant if plant is not dead
        if self.mood != "dead":
            self.water_level += amount
    
    def update(self, delta):
        if self.mood != "limp" and self.mood != "dead" and self.mood != "shrivel":
            self.age += 1

        self.check_mood()
        self.update_animation_frame(delta)

        if self.mood != "grow":
            self.update_water_level(delta)

    def check_mood(self):
        # Check if we need to switch to a new mood/animation list when the current animation loop is finished.
        # If we do need to change, change new_mood to the next mood, and wait to update in the animation frame update.

        # "grow", "droop", "shrivel", and "perk" are transition states since they are suppose to play only once.
        # All other states are meant to loop their animation until a change is triggered

        # Changing moods decided by water_level
        if self.water_level >= self.happy_threshold and self.new_mood != "grow":
            self.new_mood = "happy"
        elif self.water_level < self.happy_threshold and self.water_level > self.droop_threshold:
            if self.mood == "limp":
                self.new_mood = "perk"
            else:
                self.new_mood = "idle"
        elif self.water_level <= self.droop_threshold and self.water_level > self.dead_threshold:
            if self.mood == "idle" and self.new_mood != "limp":
                self.new_mood = "droop"
        elif self.water_level <= self.dead_threshold and self.new_mood != "dead":
            self.new_mood = "shrivel"

        
        # Changing between static states and transition states
        if self.age > self.age_threshold and self.mood == "happy" and self.growth_stage != 3:
            self.new_mood = "grow"

        if self.mood == "grow":
            self.new_mood = "idle"
        elif self.mood == "droop":
            self.new_mood = "limp"
        elif self.mood == "perk":
            self.new_mood = "idle"
        elif self.mood == "shrivel":
            self.new_mood = "dead"


    def update_water_level(self, delta):
        # Decrease water level by drying speed.
        self.water_level -= self.drying_speed

        # Ensure water level does not fall below zero.
        self.water_level = max(0, self.water_level)


    def update_animation_frame(self, delta):
        # Primary objective is to set frame.
        self.time_elapsed += delta

        if self.new_mood != self.mood and self.finished_animation_loop():
            if self.mood == "grow" and self.new_mood == "idle":
                self.growth_stage += 1            
                self.water_level = 150
                self.age = 0
            if self.mood == "droop" and self.new_mood == "limp":
                self.age = 0
            self.mood = self.new_mood
            self.current_index = 0
            self.time_elapsed = 0
            self.time_per_frame = self.config["time_per_frame"][self.mood][self.growth_stage]
            self.number_of_frames = self.config["number_of_frames"][self.mood][self.growth_stage]
        else:
            self.time_elapsed = self.time_elapsed % int(self.time_per_frame * self.number_of_frames)       

        self.current_index = int(self.time_elapsed // self.time_per_frame)

    def finished_animation_loop(self):
        return (self.time_elapsed >= self.time_per_frame * self.number_of_frames)