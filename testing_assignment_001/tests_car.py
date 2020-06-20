from django.test import TestCase
import pytest
from car import *
@pytest.fixture
def car():  # Our Fixture function
    car_obj = Car(color="Red", max_speed=40, acceleration=10, tyre_friction=3)
    return car_obj
@pytest.fixture
def auto():
    auto_obj=Car(color="brown", max_speed=100, acceleration=15, tyre_friction=5)
    return auto_obj


def test_creation_of_car_object_once_true(car):
    #Arrange
    color="Red"
    max_speed=40
    acceleration=10
    tyre_friction=3
    #Assert
    assert car.color==color
    assert car.max_speed==max_speed
    assert car.acceleration==acceleration
    assert car.tyre_friction==tyre_friction
def test_the_creation_of_car_objects_twice_true(car,auto):
    #Arrange
    color="Red"
    max_speed=40
    acceleration=10
    tyre_friction=3
    #Arrange
    color_1="brown"
    max_speed_1=100
    acceleration_1=15
    tyre_friction_1=5
    #Assert
    assert car.color==color
    assert car.max_speed==max_speed
    assert car.acceleration==acceleration
    assert car.tyre_friction==tyre_friction
    #Assert
    assert auto.color==color_1
    assert auto.max_speed==max_speed_1
    assert auto.acceleration==acceleration_1
    assert auto.tyre_friction==tyre_friction_1
    
#max_speed   
def test_given_max_speed_is_negative_raise_invalid_maxspeed():
        with pytest.raises(Exception) as e:
            assert Car(color="Red",max_speed=-1,acceleration=10,tyre_friction=3)
        assert str(e.value) == "Invalid value for max_speed"
def test_given_max_speed_is_zero_raise_invalid_maxspeed():
        with pytest.raises(Exception) as e:
            assert Car(color="Red",max_speed=0,acceleration=10,tyre_friction=3)
        assert str(e.value) == "Invalid value for max_speed"
def test_given_max_speed_is_positive_equal_to_true():
    a=Car(color="Red",max_speed=1,acceleration=10,tyre_friction=3)
    assert a.max_speed==1

#acceleration
def test_given_acceleration_is_negative_raise_invalid_acceleration():
        with pytest.raises(Exception) as e:
            assert Car(color="Red",max_speed=40,acceleration=-1,tyre_friction=3)
        assert str(e.value) == "Invalid value for acceleration"
def test_given_acceleration_is_zero_raise_invalid_acceleration():
        with pytest.raises(Exception) as e:
            assert Car(color="Red",max_speed=40,acceleration=0,tyre_friction=3)
        assert str(e.value) == "Invalid value for acceleration"
def test_given_acceleration_is_positive_equal_to_true():
    a=Car(color="Red",max_speed=40,acceleration=1,tyre_friction=3)
    assert a.acceleration==1


#tyre_friction     
def test_given_tyre_friction_is_negative_raise_invalid_tyre_friction():
        with pytest.raises(Exception) as e:
            assert Car(color="Red",max_speed=40,acceleration=10,tyre_friction=-1)
        assert str(e.value) == "Invalid value for tyre_friction"
def test_given_tyre_friction_is_zero_raise_invalid_tyre_friction():
        with pytest.raises(Exception) as e:
            assert Car(color="Red",max_speed=40,acceleration=10,tyre_friction=0)
        assert str(e.value) == "Invalid value for tyre_friction"
def test_given_tyre_friction_is_positive_equal_to_true():
    a=Car(color="Red",max_speed=40,acceleration=10,tyre_friction=1)
    assert a.tyre_friction==1




def test_start_engine_is_engine_started_true(car):
    #Act
    car.start_engine()
    #Assert
    assert car.is_engine_started==True
def test_start_engine_is_engine_started_twice_true(car):
    #Act
    car.start_engine()
    car.start_engine()
    assert car.is_engine_started==True
def test_more_cars_called_one_engine_started_other_engines_stop_true(car,auto):
    #Act
    car.start_engine()
    #Assert
    assert auto.is_engine_started==False

def test_stop_engine_is_engine_stopped_false(car):
    #Act
    car.stop_engine()
    #Assert
    assert car.is_engine_started==False
def test_current_speed_before_start_engine_result_zero(car):
    #Arrange
    current_speed=0
    #Assert
    assert car.current_speed==current_speed
def test_current_speed_after_start_engine_result_zero(car):
    #Arrange
    current_speed=0
    #Act
    car.start_engine()
    #Assert
    assert car.current_speed==current_speed
def test_current_speed_always_less_than_max_speed_true(car):
    #Arrange
    max_speed=40
    #Act
    car.start_engine()
    car.accelerate()
    #Assert
    assert car.current_speed<max_speed

def test_start_engine_sound_horn_true(car,capfd):
    #Act
    car.start_engine()
    car.sound_horn()
    output=capfd.readouterr()
    #Assert
    assert output.out=="Beep Beep\n"
def test_sound_horn_when_engine_is_not_started_print_start_the_engine(car,capfd):
    #Act
    car.sound_horn()
    output=capfd.readouterr()
    #Assert
    assert output.out=="Start the engine to sound_horn\n"
def test_accelerate_when_engine_is_not_started_print_start_the_engine(car,capfd):
    #Act
    car.accelerate()
    output=capfd.readouterr()
    #Assert
    assert output.out=="Start the engine to accelerate\n"

def test_apply_break_when_car_is_in_motion_gives_value(car):
    #Arrange
    current_speed=7
    #Act
    car.start_engine()
    car.accelerate()
    car.apply_brakes()
    #Assert
    assert car.current_speed==current_speed

def test_apply_more_breaks_when_car_is_in_motion_result_negative(car):
    #Arrange
    current_speed=0
    #Act
    car.start_engine()
    car.accelerate()
    car.apply_brakes()
    car.apply_brakes()
    car.apply_brakes()
    car.apply_brakes()
    #Assert
    assert car.current_speed==current_speed
def test_apply_breaks_when_car_is_in_motion_result_zero():
    #Arrange
    current_speed=0
    a=Car(color="Red", max_speed=40, acceleration=10, tyre_friction=10)
    #Act
    a.start_engine()
    a.accelerate()
    a.apply_brakes()
    #Assert
    assert a.current_speed==current_speed
'''
def test_apply_accelerate_when_car_is_in_motion_current_speed_less_than_max_speed(car):
    max_speed=40
    car.start_engine()
    car.accelerate()
    assert car.current_speed<max_speed
'''
def test_apply_more_accelerate_when_car_is_in_motion_does_not_exceed_maxspeed(car):
    #Act
    car.start_engine()
    car.accelerate()
    car.accelerate()
    car.accelerate()
    car.accelerate()
    car.accelerate()
    #Assert
    assert car.current_speed==car.max_speed
def test_apply_more_accelerate_when_car_is_in_motion_equal_to_maxspeed(car):
    #Act
    car.start_engine()
    car.accelerate()
    car.accelerate()
    car.accelerate()
    car.accelerate()
    #Assert
    assert car.current_speed==car.max_speed

def test_encapsulation_for_max_speed_raise_exception(car):
    #Act
    with pytest.raises(Exception) as e:
        car.max_speed=300
    #Assert
    assert str(e.value) == "can't set attribute"
def test_encapsulation_for_color_raise_exception(car):
    #Act
    with pytest.raises(Exception) as e:
        car.color="brown"
    #Assert
    assert str(e.value) == "can't set attribute"
def test_encapsulation_for_acceletation_raise_exception(car):
    #Act
    with pytest.raises(Exception) as e:
        car.acceleration=100
    #Assert
    assert str(e.value) == "can't set attribute"
def test_encapsulation_for_tyre_friction_raise_exception(car):
    #Act
    with pytest.raises(Exception) as e:
        car.tyre_friction=10
    #Assert
    assert str(e.value) == "can't set attribute"
def test_encapsulation_for_current_speed_raise_exception(car):
    #Act
    with pytest.raises(Exception) as e:
        car.current_speed=200
    #Assert
    assert str(e.value) == "can't set attribute"
def test_encapsulation_for_is_engine_started_raise_exception(car):
    #Act
    with pytest.raises(Exception) as e:
        car.is_engine_started=True
    #Assert
    assert str(e.value) == "can't set attribute"
def test_apply_more_breaks_when_car_is_in_motion_result_minus_one():
    #Arrange
    a=Car(color="Red", max_speed=40, acceleration=11, tyre_friction=3)
    #Act
    a.start_engine()
    a.accelerate()
    a.apply_brakes()
    a.apply_brakes()
    a.apply_brakes()
    a.apply_brakes()
    #Assert
    assert a.current_speed==0
def test_apply_more_breaks_when_car_is_in_motion_result_plus_one():  
    a=Car(color="Red", max_speed=40, acceleration=10, tyre_friction=3)
    a.start_engine()
    a.accelerate()
    a.apply_brakes()
    a.apply_brakes()
    a.apply_brakes()
    assert a.current_speed==1
