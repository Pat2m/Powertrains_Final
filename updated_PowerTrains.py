import math
from pandas import *
import numpy as np
import matplotlib.pyplot as plt


class Car():
    def __init__(self, **kwargs):
        #Assumes Cruising Case of Flat Ground unless specified
        self.weight = None
        self.cd = None
        self.force = None
        self.frontalArea = None
        self.rho = 1.2
        self.velocity = 0
        self.power = None
        self.accceleration = 0
        self.w_Units = True
        self.vel_Units = True
        self.angle = True
        self.theta = 0
        self.rolling_Coef = .015
        self.hp = False
        self.HWcycle = None
        self.targetRange = None
        self.tire_MU = None
        self.tire_Radius = None
        self.FirstStepPow = True
        self.FirstStepTank = True
        self.lastRoadTest = None
        for key, value in kwargs.items():
            key = key.lower()
            if key == "weight":
                if self.w_Units:
                    self.weight = value
                else:
                    self.weight = value / 2.205
            elif key == "velocity":
                if self.vel_Units:
                    self.velocity = value
                else:
                    self.velocity = value/2.237
            elif key == "speed":
                if value == "mph":
                    self.vel_Units = False
                    self.velocity /= 2.237
            elif key == "lbs":  
                self.w_Units = False
                self.weight /= 2.205  
            elif key == "degs":  
                self.angle = False
                self.theta *= (3.14/180)   
            elif key == "hp":  
                    self.hp = True
                    self.power *= 745.7
            elif key == "cd":
                self.cd = value
            elif key == "theta":
                if self.angle:
                    self.theta = value
                else:
                    self.theta = value * (3.14/180) 
            elif key == "accel":
                self.accceleration = value
            elif key == "power":
                if self.hp:
                    self.power = value * 745.7
                else:
                    self.power = value 
            elif key == "area":
                self.frontalArea = value
            elif key == "f":
                self.rolling_Coef = value
            elif key == "force":
                self.force = value
            elif key == "grade":
                if value > 1:
                    self.theta = math.tanh(value/100)
                else:
                    self.theta = math.tanh(value)
            elif key == "range":
                self.targetRange = value
            else:
                print("Invalid Key Entered")

class EV(Car):
    def __init__(self, **kwargs):
        self.regen = None
        self.packWeight = 0
        self.KgPerKWH = 6.66
        self.packPower = 0
        keysToPop = []
        for key, value in kwargs.items():
            key = key.lower()
            if key == "regen":
                if value > 1:
                    self.regen = value / 100
                else:
                    self.regen = value
                keysToPop.append(key)
            elif key == "pack":
                self.packWeight = value
                keysToPop.append(key)
            elif key == "power_rating":
                self.packPower = value
                keysToPop.append(key)
        for key in keysToPop:
            kwargs.pop(key)
        super().__init__(**kwargs)

class Fossil_Fuel_Car(Car):
    def __init__(self, **kwargs):
        self.engine_efficiency = .25
        self.fuel = None
        for key, value in kwargs.items():
            key = key.lower()
            if key == "efficiency":
                if value > 1:
                    self.engine_efficiency = value / 100
                else:
                    self.engine_efficiency = value
                #kwargs.pop(key)
        super().__init__(**kwargs)
        

class Hybrid(Fossil_Fuel_Car):
    def __init__(self, **kwargs):
        self.regen = .25
        self.fuel = None
        for key, value in kwargs.items():
            key = key.lower()
            if key == "regen":
                if value > 1:
                    self.regen = value / 100
                else:
                    self.regen = value
                #kwargs.pop(key)
        super().__init__(**kwargs)

class PowerTrain_Calcs():
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def rolling_Coef(car):
        car.tire_MU
        car.tire_Radius
        

    @staticmethod
    def aero(car):
        return .5 * car.rho * car.velocity ** 2 * car.frontalArea * car.cd
    
    @staticmethod
    def rolling(car):
        if isinstance(car,EV):
            return (car.weight + car.packWeight) * car.rolling_Coef * 9.81 * math.cos(car.theta)
        else:
            return car.weight * car.rolling_Coef * 9.81 * math.cos(car.theta)
    
    @staticmethod
    def grade(car):
        if isinstance(car,EV):
            return (car.weight + car.packWeight) * 9.81 * math.sin(car.theta)
        else:
            return car.weight * 9.81 * math.sin(car.theta)

    @staticmethod
    def force(car):
        if isinstance(car,EV):
            return (car.weight + car.packWeight) * car.accceleration
        else:
            return car.weight * car.accceleration
    
    @staticmethod
    def total(car):
        return PowerTrain_Calcs.aero(car) + PowerTrain_Calcs.rolling(car) + \
                PowerTrain_Calcs.grade(car) + PowerTrain_Calcs.force(car)

    @staticmethod
    def Power_W(car):
        return  PowerTrain_Calcs.total(car) * car.velocity
    
    @staticmethod
    def Power_HP(car):
        return  PowerTrain_Calcs.Power_W(car) / 745.7
    
    @staticmethod
    def get_acceleration(car):
        if car.power != None:
            if isinstance(car,EV):
                return (car.power/car.velocity - PowerTrain_Calcs.aero(car) -\
                    PowerTrain_Calcs.rolling(car) - PowerTrain_Calcs.grade(car))/\
                    (car.weight+car.packWeight)
            else:
                return (car.power/car.velocity - PowerTrain_Calcs.aero(car) -\
                    PowerTrain_Calcs.rolling(car) - PowerTrain_Calcs.grade(car))/\
                    car.weight
        else:
            return "Please Enter Valid Engine Power"
    
    @staticmethod
    def get_top_speed(car):
        p = 0
        car.velocity = 0
        while car.power > p:
            #print(car.velocity)
            car.velocity += 1
            p = PowerTrain_Calcs.Power_W(car)
            #print(p)
        if car.vel_Units:
            return car.velocity
        else:
            return car.velocity * 2.237
    

    @staticmethod
    def power_speed_chart(car):
        p = 0
        power =[]
        vel = []
        car.velocity = 0
        while car.power > p:
            #print(car.velocity)
            car.velocity += 1
            p = PowerTrain_Calcs.Power_W(car)
            vel.append(car.velocity)
            power.append(p)
            #print(p)
        power = np.array(power)/745.7
        if car.vel_Units:
            return vel, power
        else:
            vel = np.array(vel)* 2.237
            return  vel, power


    #Start of Highway Cycle Code all simulations assume 0% grade
    @staticmethod
    def get_HW_cycle(car):
        data = read_csv("epaHWCycle_Data.csv")
        time = data['time, s'].tolist()
        mph = data['velocity, mph'].tolist()
        meps = np.array(mph) / 2.237
        accel = []
        powers = []
        pos = []
        i = 0
        distance = [0]
        greatest = 0
        for t in time:
            
            car.velocity = meps[i]
            if i == 0:
                car.accceleration = 0
            else:
                car.accceleration = meps[i] - meps[i-1]
            accel.append(car.accceleration)
            power = PowerTrain_Calcs.Power_W(car)
            #print(power)
            powers.append(power)
            distance.append(distance[i] + meps[i])
            if power > 0:
                pos.append(power)
                if power > greatest:
                    greatest=power
            i += 1
            
        HWcycle = (accel, powers, pos, distance)
        #print(f"hW Cycle greatest power J {greatest}")
        car.HWcycle = HWcycle
        return HWcycle

    @staticmethod
    def get_ppg(car):
        ppmd = PowerTrain_Calcs.get_ppmd(car)
        if isinstance(car,Fossil_Fuel_Car):
            mepg = 32.3 * 3600000 / (ppmd / car.engine_efficiency)
        else:
            mepg =  32.3 * 3600 * 1000 / (ppmd / .25) # Assumes 25% Efficiency if not a Fossil Fuel
        return mepg # Meters Per Gallon
    
    @staticmethod
    def get_mpg(car):
        x = PowerTrain_Calcs.get_ppg(car)
        print(f"The car gets {round(x/1609,2)} mpg")
        return  x / 1609 


    @staticmethod
    def get_tank_size(car):
        tankSize = car.targetRange / PowerTrain_Calcs.get_mpg(car)
        if car.FirstStepTank:
            print(f"The car would need about a {round(tankSize,2)} Gallon tank " + 
                f"to reach a range of {car.targetRange} miles")
            car.FirstStepTank = False
        return tankSize

    @staticmethod
    def get_tank_size_Weighted(car):
        if isinstance(car,Fossil_Fuel_Car):
            if car.fuel == "diesel":
                fuelWeight = 3.22 # diesel
            elif car.fuel == "premium":
                fuelWeight = 2.8440242 # premium
            elif car.fuel == "plus":
                fuelWeight = 2.8803115 # Midgrade
            else:
                fuelWeight = 2.7546665 # Regualar
        else:
            fuelWeight = 2.7546665 # Regualar
        last_tank_weight = -999999999999999 # Assign an Arbitrary Large Number
        tank_weight = 0
        tankSize = 0
        first = True
        while .001 < (tank_weight - last_tank_weight): #Gets tank weight within 1g
            last_tank_weight = tank_weight
            tankSize = PowerTrain_Calcs.get_tank_size(car)
            tank_weight = tankSize * fuelWeight
        print(f"The car would need about a {round(tankSize,2)} Gallon tank " + 
                f"to reach a range of {car.targetRange} miles Accounting for the added " +
                "weight of the fuel")
        return tankSize

    @staticmethod
    def get_ppmd(car):
        cycle = PowerTrain_Calcs.get_HW_cycle(car)
        total_power = 0
        greatest = 0
        if isinstance(car,EV) or isinstance(car,Hybrid):
            #print(car.__dir__())
            if car.regen != None:
                #Total energy joules
                for i in cycle[1]:
                    if i < 0:
                        total_power += (i * car.regen)
                    else:
                        total_power += i
            else:
                for i in cycle[2]:
                    if i>greatest:
                        greatest = i
                    total_power += i
        else:
            for i in cycle[2]:
                    #print(i)
                    if i>greatest:
                        greatest = i
                    total_power += i
        print(f"greatest power spent {greatest/1000}")
        total_dist = cycle[3][len(cycle[3])-1] #in meters
        ppmd = total_power/total_dist
        car.lastRoadTest = total_power
        if car.FirstStepPow:
            print(f"Total energy spent in kJ: {round(total_power/1000,2)} on Road Test")
            car.FirstStepPow = False
        #print(ppmd)
        return ppmd #power per meter driven in J


    @staticmethod
    def get_EV_Range_Weight(EV):
        ppmd = PowerTrain_Calcs.get_ppmd(EV)
        power_KWH = ppmd / 3600 / 1000 
        range = (EV.packWeight / EV.KgPerKWH) / power_KWH 
        return range # meters
    
    @staticmethod
    def get_EV_Range_Weight_mi(EV):
        return PowerTrain_Calcs.get_EV_Range_Weight(EV) / 1609

    @staticmethod
    def get_EV_Range_Weight_km(EV):
        return PowerTrain_Calcs.get_EV_Range_Weight(EV) / 1000

    @staticmethod
    def get_EV_Range_Power(EV):
        ppmd = PowerTrain_Calcs.get_ppmd(EV)
        power_KWH = ppmd / 3600 / 1000 
        range = (EV.packPower) / power_KWH
        return range # meters
    
    @staticmethod
    def get_EV_KW_per_meter(EV):
        ppmd = PowerTrain_Calcs.get_ppmd(EV)
        power_KWH = ppmd / 3600 / 1000 
        return power_KWH

    @staticmethod
    def get_EV_KW_per_mi(EV):
        temp = PowerTrain_Calcs.get_EV_KW_per_meter(EV) * 1609
        print(f"Kw {temp} per mile")
        return  temp
    
    @staticmethod
    def get_EV_KW_per_km(EV):
        return PowerTrain_Calcs.get_EV_KW_per_meter(EV) * 1000

    @staticmethod
    def get_EV_Range_Power_mi(EV):
        
        return PowerTrain_Calcs.get_EV_Range_Power(EV) / 1609

    @staticmethod
    def get_EV_Range_Power_Km(EV):
        return PowerTrain_Calcs.get_EV_Range_Power(EV) / 1000

    
    @staticmethod
    def get_pack_Size(EV):
        power_KWH = 0
        last_Size = 0
        last_packWeight = -999999999999999 # Assign an Arbitrary Large Number
        first = True
        while .001 < (EV.packWeight - last_packWeight): #Gets pack weight within 1g
            last_packWeight = EV.packWeight
            ppmd = PowerTrain_Calcs.get_ppmd(EV)
            ppmid = ppmd*1609.34
            #print(ppmid)
            power_KWH = ppmid / 3600 / 1000  * (EV.targetRange)
            #print(power_KWH)
            packWeight = power_KWH * EV.KgPerKWH 
            EV.packWeight = packWeight
            if first:
                print(f"The Car needs a {round(power_KWH,1)} kW-Hr pack that weighs {round(packWeight,2)} Kg before acounting for " +
                      "pack weight's influence on road load")
                first = False
        print(f"Total energy spent in kJ: {round(EV.lastRoadTest/1000,2)} on Last Road Test Iteration")
        print(f"The Car needs a {round(power_KWH,1)} kW-Hr pack that weighs {round(packWeight,2)} Kg")
        return (power_KWH,EV.packWeight)

    #End Of 0% grade Highway estimates

    @staticmethod
    def get_bottom_gear(N_driven, mu, T_crank,i_final,Tire_Diameter):
        Torque_Comp = 2 * T_crank/Tire_Diameter*i_final
        Force = N_driven*mu
        i_bot = Force/Torque_Comp *10
        #i_bot = mu*N_driven/T_crank/2/i_final*Tire_Diameter
        return i_bot
    
    @staticmethod
    def get_top_gear(rpm,v_max,i_final,Tire_Diameter):
        i_top = (rpm/i_final)*Tire_Diameter*(math.pi/60)/v_max
        print(f"Top {i_top}")
        return i_top
    

    @staticmethod
    def geo_space(N_driven, mu, T_crank,rpm,v_max,i_final,Tire_Diameter,Number_of_Gears):
        i_bot = PowerTrain_Calcs.get_bottom_gear(N_driven, mu, T_crank,i_final,Tire_Diameter)
        i_top = PowerTrain_Calcs.get_top_gear(rpm,v_max,i_final,Tire_Diameter)
        span = i_bot/i_top
        print(span)
        ratio = math.pow(span,1/(Number_of_Gears-1))
        print(ratio)
        gears = []
        for i in range(Number_of_Gears):
            if i==0:
                gears.append(i_bot)
            elif i == Number_of_Gears-1:
                gears.append(i_top)
            else:
                gear = gears[i-1]/ratio
                gears.append(gear)
        return gears



run_HW1 = False
run_HW2 = False
run_HW3 = False
mid_term = False
Rivian_Test = False




if run_HW1:
    print("Porche 917")
    Porche917 = Car(weight = 800, f = .015, cd = .417, area = 1.546,
                    velocity = 240, speed = "mph")
    print(PowerTrain_Calcs.Power_HP(Porche917))

    print("Random Sedan")
    sed_test = Car(power = 140, weight = 1500, area = 2.5, hp = "hp",
                speed = "mph", CD = .4)

    sed_test_inc = Car(power = 140, weight = 1500, area = 2.5, hp = "hp",
                speed = "mph", CD = .4, grade = .05)

    print("Top Speed on Flat Road")
    print(PowerTrain_Calcs.get_top_speed(sed_test))
    print("Top Speed on Road with 5% Grade")
    print(PowerTrain_Calcs.get_top_speed(sed_test_inc))

if run_HW2:
    print("Ford Ranger")
    #1998-2011 Ford Ranger Extended Cab (6′ Bed)
    FordRanger = Car(weight = 3200, CD = .4, area = 2.4, lbs = True, range = 500,power = 105, hp = "hp")
    
    PowerTrain_Calcs.get_mpg(FordRanger)
    PowerTrain_Calcs.get_tank_size(FordRanger)
    #PowerTrain_Calcs.get_tank_size_Weighted(FordRanger)
    print("As an EV")
    #Engine is approx 350-380 lbs.  for our estimat we use 365 lbs. The drive train swap will be estimated to
    #be of equal weight to the components being swapped
    FordRangerEV = EV(weight = 3200, CD = .4, area = 2.4, lbs = True, range = 300, regen = .0)
    PowerTrain_Calcs.get_pack_Size(FordRangerEV)
    #inches to m
    inches = 28.3
    meter = inches/39.37
    bias = .5 #2 Driven Tires 50% bias
    N_Driven = 3200*bias 
    kg = N_Driven/2.205

    v_max = PowerTrain_Calcs.get_top_speed(FordRanger)
    print(v_max)
    foot_lb = 135
    nm = foot_lb*1.3558179483
    gears = PowerTrain_Calcs.geo_space(kg,1,nm,4800,v_max,3.48,meter,4)
    print(gears)

if Rivian_Test:
    #3152 Kg is the curb weight before removing the 135 kW-hr pack (899.1 Kg). 2252.9 Kg is curb after subtracting pack weight
    #For a 300 mi range using the 20" all terrain tires the quoted pack size is 135 kW-hr 
    #
    Rivian_R1T = EV(weight = 2252.9, CD = .3,
                    area = 3.27130184, range = 300, regen = .95)
    print("Rivian R1T")
    PowerTrain_Calcs.get_pack_Size(Rivian_R1T)


if run_HW3:
    print("Ford Ranger")
    #1998-2011 Ford Ranger Extended Cab (6′ Bed)
    FordRanger = Car(weight = 3200, CD = .4, area = 2.4, lbs = True, range = 500,power = 105, hp = "hp", speed = "mph")
    FordRanger_Hyb = Hybrid(weight = 3200, CD = .4, area = 2.4, lbs = True, range = 500,power = 105, hp = "hp",efficiency=.32,regen = .75)
    mpg = PowerTrain_Calcs.get_mpg(FordRanger)
    spe = PowerTrain_Calcs.get_top_speed(FordRanger)
    print(f"F Ranger Top speed {spe}")
    distance = 250000
    gallons = distance/mpg
    price = 3.75
    print(gallons*price)
    mpg = PowerTrain_Calcs.get_mpg(FordRanger_Hyb)
    distance = 250000
    gallons = distance/mpg
    price = 3.75
    print(gallons*price)
    FordRanger_EV_no_Regen = EV(weight = 3200, CD = .4, area = 2.4, lbs = True, range = 500,power = 105, hp = "hp")
    mpkw = PowerTrain_Calcs.get_EV_KW_per_mi(FordRanger_EV_no_Regen)
    distance = 250000
    energy = distance*mpkw
    price = .2
    print(energy*price)
    FordRanger_EV_Regen = EV(weight = 3200, CD = .4, area = 2.4, lbs = True, range = 500,power = 105, hp = "hp",regen = .7)
    mpkw = PowerTrain_Calcs.get_EV_KW_per_mi(FordRanger_EV_Regen)
    distance = 250000
    energy = distance*mpkw
    price = .2
    print(energy*price)

if mid_term:
    Mini_Van = Fossil_Fuel_Car(weight = 1900, CD = .35,f =.015,area = 2.5, power = 266, hp = "hp", efficiency = .2)
    Mini_Van_Hyb = Hybrid(weight = 1900, CD = .35,f =.015,area = 2.5, power = 266, hp = "hp", efficiency = .36, regen = .6)
    print("Top Speed on Flat Road")
    v_max = PowerTrain_Calcs.get_top_speed(Mini_Van)
    print(v_max)
    print("standard")
    mpg = PowerTrain_Calcs.get_mpg(Mini_Van)
    print("Hybrid")
    mpg_Hyb = PowerTrain_Calcs.get_mpg(Mini_Van_Hyb)
    print(f"Mini Van mpg {mpg}, Hybrid mpg {mpg_Hyb}")
        #inches to m
    diameter = 27 # inches
    diameter_m = diameter/39.37 #diameter meters
    bias = .6 #2 Driven Tires 60% bias
    N_Driven = 1900*bias 
    foot_lb = 245
    nm = foot_lb*1.3558179483
    gears = PowerTrain_Calcs.geo_space(N_Driven,1,nm,6200,v_max,3.29,diameter_m,4)
    print(gears)
    ms = 60/2.237
    nd2 = PowerTrain_Calcs.get_top_gear(6200,ms,3.29,diameter_m)
    print(nd2)
    
final_proj = True

if final_proj:
    print("07 Chevy Malibu LS")
    malibu = Fossil_Fuel_Car(power = 144, weight = 3174, area = 2.3, hp = "hp",
                speed = "mph", CD = .29,efficiency = .3, lbs = True)

    
    print("Top Speed on Flat Road")
    print(PowerTrain_Calcs.get_top_speed(malibu))
    vel, power = PowerTrain_Calcs.power_speed_chart(malibu)
    plt.plot(vel, power)
    plt.xlabel("Speed (mph)")
    plt.ylabel("Required Power (Hp)")
    plt.show()
    malibu_Hyb = Hybrid(power = 144, weight = 3174, area = 2.3, hp = "hp",
                speed = "mph", CD = .29,efficiency = .3, regen = .70, lbs = True)
    mpg = PowerTrain_Calcs.get_mpg(malibu)
    mpg_hyb = PowerTrain_Calcs.get_mpg(malibu_Hyb)
    print(f"Malibue mpg {mpg}, Hybrid mpg {mpg_hyb}")
    Malibu_EV_Regen = EV(weight = 3143.925, CD = .29, area = 2.3, lbs = True, range = 300,power = 144, hp = "hp",regen = .7)
    pack_size = PowerTrain_Calcs.get_pack_Size(Malibu_EV_Regen)
    mpkw = PowerTrain_Calcs.get_EV_KW_per_mi(Malibu_EV_Regen)
    Malibu_EV_Regen = EV(weight = 3584.85, CD = .29, area = 2.3, lbs = True, pack = 655.32,power_rating = 98.4,power = 205, hp = "hp",regen = .7)
    print(f"range {PowerTrain_Calcs.get_EV_Range_Power_mi(Malibu_EV_Regen)}")