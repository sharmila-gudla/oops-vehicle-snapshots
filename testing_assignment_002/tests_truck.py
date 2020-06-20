from django.test import TestCase
import pytest
from truck import *
@pytest.fixture
def truck():  # Our Fixture function
    truck_obj_1 = Truck(color="Red", max_speed=40, acceleration=10, tyre_friction=3,max_cargo_weight=100)
    return truck_obj_1
@pytest.fixture
def lorry():
    truck_obj_2 = Truck(color="brown", max_speed=50, acceleration=20, tyre_friction=10,max_cargo_weight=150)
    return truck_obj_2
def test_creation_of_truck_object_once_true(truck):
    #Arrange
    color="Red"
    max_speed=40
    acceleration=10
    tyre_friction=3
    max_cargo_weight=100
    #Assert
    assert truck.color==color
    assert truck.max_speed==max_speed
    assert truck.acceleration==acceleration
    assert truck.tyre_friction==tyre_friction
    assert truck.max_cargo_weight==max_cargo_weight
def test_the_creation_of_truck_objects_twice_true(truck,lorry):
    #Arrange
    color="Red"
    max_speed=40
    acceleration=10
    tyre_friction=3
    max_cargo_weight=100
    #Arrange
    color_1="brown"
    max_speed_1=50
    acceleration_1=20
    tyre_friction_1=10
    max_cargo_weight1=150
    #Assert
    assert truck.color==color
    assert truck.max_speed==max_speed
    assert truck.acceleration==acceleration
    assert truck.tyre_friction==tyre_friction
    assert truck.max_cargo_weight==max_cargo_weight
    #Assert
    assert lorry.color==color_1
    assert lorry.max_speed==max_speed_1
    assert lorry.acceleration==acceleration_1
    assert lorry.tyre_friction==tyre_friction_1
    assert lorry.max_cargo_weight==max_cargo_weight1
#max_speed   
def test_truck_max_speed_is_negative_raise_invalid_max_speed():
        with pytest.raises(Exception) as e:
            assert Truck(color="Red",max_speed=-1,acceleration=10,tyre_friction=3,max_cargo_weight=100)
        assert str(e.value) == "Invalid value for max_speed"
def test_truck_max_speed_is_zero_raise_invalid_max_speed():
        with pytest.raises(Exception) as e:
            assert Truck(color="Red",max_speed=0,acceleration=10,tyre_friction=3,max_cargo_weight=100)
        assert str(e.value) == "Invalid value for max_speed"
def test_truck_max_speed_is_positive_equal_to_true():
    a=Truck(color="Red",max_speed=1,acceleration=10,tyre_friction=3,max_cargo_weight=100)
    assert a.max_speed==1

#acceleration
def test_truck_acceleration_is_negative_raise_invalid_acceleration():
        with pytest.raises(Exception) as e:
            assert Truck(color="Red",max_speed=40,acceleration=-1,tyre_friction=3,max_cargo_weight=100)
        assert str(e.value) == "Invalid value for acceleration"
def test_truck_acceleration_is_zero_raise_invalid_acceleration():
        with pytest.raises(Exception) as e:
            assert Truck(color="Red",max_speed=40,acceleration=0,tyre_friction=3,max_cargo_weight=100)
        assert str(e.value) == "Invalid value for acceleration"
def test_truck_acceleration_is_positive_equal_to_true():
    a=Truck(color="Red",max_speed=40,acceleration=1,tyre_friction=3,max_cargo_weight=100)
    assert a.acceleration==1
    
#tyre_friction     
def test_truck_tyre_friction_is_negative_raise_invalid_tyre_friction():
        with pytest.raises(Exception) as e:
            assert Truck(color="Red",max_speed=40,acceleration=10,tyre_friction=-1,max_cargo_weight=100)
        assert str(e.value) == "Invalid value for tyre_friction"
def test_truck_tyre_friction_is_zero_raise_invalid_tyre_friction():
        with pytest.raises(Exception) as e:
            assert Truck(color="Red",max_speed=40,acceleration=10,tyre_friction=0,max_cargo_weight=100)
        assert str(e.value) == "Invalid value for tyre_friction"
def test_truck_tyre_friction_is_positive_equal_to_true():
    a=Truck(color="Red",max_speed=40,acceleration=10,tyre_friction=1,max_cargo_weight=100)
    assert a.tyre_friction==1



def test_truck_start_engine_is_engine_started_true(truck):
    #Act
    truck.start_engine()
    #Assert
    assert truck.is_engine_started==True
def test_truck_start_engine_is_engine_started_twice_true(truck):
    #Act
    truck.start_engine()
    truck.start_engine()
    assert truck.is_engine_started==True
def test_more_trucks_called_one_engine_started_other_engines_stop_true(truck,lorry):
    #Act
    truck.start_engine()
    #Assert
    assert lorry.is_engine_started==False

def test_stop_engine_is_engine_stopped_false(truck):
    #Act
    truck.stop_engine()
    #Assert
    assert truck.is_engine_started==False
def test_truck_current_speed_before_start_engine_result_zero(truck):
    #Arrange
    current_speed=0
    #Assert
    assert truck.current_speed==current_speed
def test_current_speed_after_start_engine_result_zero(truck):
    #Arrange
    current_speed=0
    #Act
    truck.start_engine()
    #Assert
    assert truck.current_speed==current_speed
    
    
def test_truck_start_engine_sound_horn_true(truck,capfd):
    #Act
    truck.start_engine()
    truck.sound_horn()
    output=capfd.readouterr()
    #Assert
    assert output.out=="Honk Honk\n"
def test_truck_sound_horn_when_engine_is_not_started_print_start_the_engine(truck,capfd):
    #Act
    truck.sound_horn()
    output=capfd.readouterr()
    #Assert
    assert output.out=="Start the engine to sound_horn\n"
def test_truck_accelerate_when_engine_is_not_started_print_start_the_engine(truck,capfd):
    #Act
    truck.accelerate()
    output=capfd.readouterr()
    #Assert
    assert output.out=="Start the engine to accelerate\n"

#------------------------
def test_apply_break_when_truck_is_in_motion_gives_value(truck):
    #Arrange
    current_speed=7
    #Act
    truck.start_engine()
    truck.accelerate()
    truck.apply_brakes()
    #Assert
    assert truck.current_speed==current_speed

def test_apply_more_breaks_when_truck_is_in_motion_result_negative(truck):
    #Arrange
    current_speed=0
    #Act
    truck.start_engine()
    truck.accelerate()
    truck.apply_brakes()
    truck.apply_brakes()
    truck.apply_brakes()
    truck.apply_brakes()
    #Assert
    assert truck.current_speed==current_speed
def test_apply_breaks_when_truck_is_in_motion_result_zero():
    #Arrange
    current_speed=0
    a=Truck(color="Red", max_speed=40, acceleration=10, tyre_friction=10,max_cargo_weight=100)
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
def test_apply_more_accelerate_when_truck_is_in_motion_does_not_exceed_maxspeed(truck):
    #Act
    truck.start_engine()
    truck.accelerate()
    truck.accelerate()
    truck.accelerate()
    truck.accelerate()
    truck.accelerate()
    #Assert
    assert truck.current_speed==truck.max_speed
#--------------------
def test_apply_more_accelerate_when_truck_is_in_motion_equal_to_maxspeed(truck):
    #Act
    truck.start_engine()
    truck.accelerate()
    truck.accelerate()
    truck.accelerate()
    truck.accelerate()
    #Assert
    assert truck.current_speed==truck.max_speed

def test_truck_encapsulation_for_max_speed_raise_exception(truck):
    #Act
    with pytest.raises(Exception) as e:
        truck.max_speed=300
    #Assert
    assert str(e.value) == "can't set attribute"
def test_truck_encapsulation_for_color_raise_exception(truck):
    #Act
    with pytest.raises(Exception) as e:
        truck.color="brown"
    #Assert
    assert str(e.value) == "can't set attribute"
def test_truck_encapsulation_for_acceletation_raise_exception(truck):
    #Act
    with pytest.raises(Exception) as e:
        truck.acceleration=100
    #Assert
    assert str(e.value) == "can't set attribute"
def test_truck_encapsulation_for_tyre_friction_raise_exception(truck):
    #Act
    with pytest.raises(Exception) as e:
        truck.tyre_friction=10
    #Assert
    assert str(e.value) == "can't set attribute"
#-----------------------------
def test_truck_encapsulation_for_current_speed_raise_exception(truck):
    #Act
    with pytest.raises(Exception) as e:
        truck.current_speed=200
    #Assert
    assert str(e.value) == "can't set attribute"
def test_truck_encapsulation_for_is_engine_started_raise_exception(truck):
    #Act
    with pytest.raises(Exception) as e:
        truck.is_engine_started=True
    #Assert
    assert str(e.value) == "can't set attribute"
    
def test_truck_encapsulation_for_max_cargo_weight_raise_exception(truck):
    with pytest.raises(Exception) as e:
        truck.max_cargo_weight=200
    #Assert
    assert str(e.value) == "can't set attribute"
def test_truck_encapsulation_for_cargo_weight_raise_exception(truck):
    with pytest.raises(Exception) as e:
        truck.cargo_weight=50
    #Assert
    assert str(e.value) == "can't set attribute"

def test_apply_more_breaks_when_truck_is_in_motion_result_minus_one():
    #Arrange
    a=Truck(color="Red", max_speed=40, acceleration=11, tyre_friction=3,max_cargo_weight=100)
    #Act
    a.start_engine()
    a.accelerate()
    a.apply_brakes()
    a.apply_brakes()
    a.apply_brakes()
    a.apply_brakes()
    #Assert
    assert a.current_speed==0
def test_apply_more_breaks_when_truck_is_in_motion_result_plus_one():  
    a=Truck(color="Red", max_speed=40, acceleration=10, tyre_friction=3,max_cargo_weight=100)
    a.start_engine()
    a.accelerate()
    a.apply_brakes()
    a.apply_brakes()
    a.apply_brakes()
    assert a.current_speed==1
    
def test_truck_load_when_acceleratre_print_error(truck,capfd):
    truck.start_engine()
    truck.accelerate()
    truck.load(30)
    output=capfd.readouterr()
    assert output.out=="Cannot load cargo during motion\n"
def test_truck_unload_when_acceleratre_print_error(truck,capfd):
    truck.load(30)
    truck.start_engine()
    truck.accelerate()
    truck.unload(30)
    output=capfd.readouterr()
    assert output.out=="Cannot unload cargo during motion\n"
def test_truck_load_weight_minus_one_raise_invalid_value_exception(truck):
    with pytest.raises(Exception) as e:
        assert truck.load(-1)
    assert str(e.value) == "Invalid value for cargo_weight"
def test_truck_load_weight_zero_raise_invalid_value_exception(truck):
    with pytest.raises(Exception) as e:
        assert truck.load(0)
    assert str(e.value) == "Invalid value for cargo_weight"
def test_truck_unload_weight_minus_one_raise_invalid_value_exception(truck):
    truck.load(10)
    with pytest.raises(Exception) as e:
        assert truck.unload(-1)
    assert str(e.value) == "Invalid value for cargo_weight"
def test_truck_unload_weight_zero_raise_invalid_value_exception(truck):
    truck.load(10)
    with pytest.raises(Exception) as e:
        assert truck.unload(0)
    assert str(e.value) == "Invalid value for cargo_weight"
def test_truck_load_weight_plus_one_stores_value_when_engine_not_started(truck):
    weight=1
    truck.load(1)
    assert truck.cargo_weight==weight
def test_truck_load_weight_plus_one_stores_value_when_engine_started(truck):
    weight=1
    truck.start_engine()
    truck.load(1)
    assert truck.cargo_weight==weight
def test_truck_unload_weight_one_stores_value(truck):
    truck.load(5)
    truck.unload(4)
    weight=1
    assert truck.cargo_weight==weight
def test_truck_unload_weight_zero_stores_value(truck):
    truck.load(5)
    truck.unload(6)
    weight=0
    assert truck.cargo_weight==weight
def test_truck_equal_load_and_unload_weight_zero_stores_value(truck):
    truck.load(5)
    truck.unload(5)
    weight=0
    assert truck.cargo_weight==weight
def test_truck_load_cargo_weight_exceed_max_cargo_weight_print_limit(truck,capfd):
    truck.load(150)
    output=capfd.readouterr()
    assert output.out=="Cannot load cargo more than max limit: 100\n"
def test_truck_load_stores_correct_value(truck):
    truck.load(40)
    assert truck.cargo_weight==40
    
   
    


#with pytest.raises(Exception) as e:
            #assert Truck(color="Red",max_speed=-1,acceleration=10,tyre_friction=3,max_cargo_weight=100)
#        assert str(e.value) == "Invalid value for max_speed"

#output=capfd.readouterr()
    #Assert
    #assert output.out=="Start the engine to sound_horn\n"