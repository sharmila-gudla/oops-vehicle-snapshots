from car import *
class RaceCar(Car):
    def __init__(self,max_speed,acceleration,tyre_friction,color=None):
        super().__init__(max_speed,acceleration,tyre_friction,color)
        self._nitro=0
    def apply_brakes(self):
        if self._current_speed>(self._max_speed/2):
            self._nitro+=10
        super().apply_brakes()
    def sound_horn(self):
        if self._is_engine_started:
            print("Peep Peep\nBeep Beep")
        else:
            print("Start the engine to sound_horn")
    def accelerate(self):
        if self._is_engine_started:
            if self._nitro:
                self._current_speed+=self._acceleration+(self._acceleration*0.3)
                self._current_speed=int(math.ceil(self._current_speed))
                self._nitro-=10
                if self._current_speed>self._max_speed:
                   self._current_speed=self._max_speed
            else:
                if self._current_speed+self._acceleration<=self._max_speed:
                    self._current_speed+=self._acceleration
                else:
                    self._current_speed=self._max_speed
        else:
            print("Start the engine to accelerate")
    @property
    def nitro(self):
        return self._nitro
