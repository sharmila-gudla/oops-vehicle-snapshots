from car import *
class Truck(Car):
    def __init__(self,max_speed,acceleration,tyre_friction,max_cargo_weight,color=None):
        super().__init__(max_speed,acceleration,tyre_friction,color)
        self._max_cargo_weight=max_cargo_weight
        self._cargo_weight=0
    def load(self,weight):
            if (self._current_speed==0 and (self._is_engine_started==True or self._is_engine_started==False)):
                if weight>0:
                    if ((self._cargo_weight+weight)<=self._max_cargo_weight):
                        self._cargo_weight+=weight
                    else:
                        print("Cannot load cargo more than max limit: "+str(self._max_cargo_weight))
                else:
                    raise ValueError("Invalid value for cargo_weight")
            else:
                print("Cannot load cargo during motion")
    def unload(self,weight):
        if weight<=0:
            raise ValueError("Invalid value for cargo_weight")
        else:
            if self._current_speed==0:
                if ((self._cargo_weight-weight)>0):
                   self._cargo_weight-=weight
                else:
                    self._cargo_weight=0
            else:
                print("Cannot unload cargo during motion")
    def sound_horn(self):
        if self._is_engine_started:
            print("Honk Honk")
        else:
            print("Start the engine to sound_horn")  
    @property    
    def max_cargo_weight(self):
        return self._max_cargo_weight
    @property
    def cargo_weight(self):
        return self._cargo_weight

