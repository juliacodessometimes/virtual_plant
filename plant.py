class Plant:
    config = {
        "idle": {
            "time_per_frame": [500, 500],
            "number_of_frames": [3, 6],
         },
        "happy": {
            "time_per_frame": [250, 250],
            "number_of_frames": [5, 7],
        },
        "grow": {
            "time_per_frame": [250 ,250],
            "number_of_frames": [10, 10],
        }

    }


    def __init__(self):
        # These are variables for keeping track of plant states.
        self.water_level = 100
        self.drying_speed = 1 # Unit per delta.
        self.growth_stage = 0
        self.mood = "idle"
        self.new_mood = "idle"
        self.age = 0

        # Thresholds for moods
        self.happy_threshold = 160

        # Variables for keeping track of rendering states.
        self.current_index = 0
        self.time_per_frame = self.config[self.mood]["time_per_frame"][self.growth_stage]
        self.number_of_frames = self.config[self.mood]["number_of_frames"][self.growth_stage]
        self.time_elapsed = 0

    def add_water(self, amount):
        self.water_level += amount
    
    def update(self, delta):
        self.age += 1

        self.check_mood()
        self.update_animation_frame(delta)

        if self.mood != "grow":
            self.update_water_level(delta)

    def check_mood(self):
        # Check if we need to switch to a new mood/animation list when the current animation loop is finished.
        # If we do need to change, change new_mood to the next mood, and wait to update in the animation frame update.

        # Changing between idle and happy
        if self.water_level >= self.happy_threshold and self.new_mood != "grow":
            self.new_mood = "happy"
        elif self.water_level > 0 and self.water_level < self.happy_threshold:
            self.new_mood = "idle"
        
        # Changing between happy and grow
        if self.age > 200 and self.mood == "happy" and self.growth_stage == 0:
            self.new_mood = "grow"

        if self.mood == "grow":
            self.new_mood = "idle"


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
                self.water_level = 100
            self.mood = self.new_mood
            self.current_index = 0
            self.time_elapsed = 0
            self.time_per_frame = self.config[self.mood]["time_per_frame"][self.growth_stage]
            self.number_of_frames = self.config[self.mood]["number_of_frames"][self.growth_stage]
        else:
            self.time_elapsed = self.time_elapsed % int(self.time_per_frame * self.number_of_frames)       

        self.current_index = int(self.time_elapsed // self.time_per_frame)

    def finished_animation_loop(self):
        return (self.time_elapsed >= self.time_per_frame * self.number_of_frames)