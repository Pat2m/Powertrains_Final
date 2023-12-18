clear all; clc;
%Chevy Malibu 07
f=0.015; %Rolling Resistance
m=3174 ;%lbs
m = m/2.205; %kg
g=9.81;
rho=1.2; 
A=2.3; %Average f.a. for sedan
Cd=0.29; %best cd for 1993 U.S. Sedans in 14 years reasonable estimate for average sedan
P=144*745; %144 hp engine
mu=1.0; %basic all season tires
k=0.4; %40% rear weight bias
eff=0.85;%Assume 85% Efficeincy
L = 106.4; %wheel base inches
L = L/39.4; %meters
hca = .5;%cg height
LDR = -0.25; %Lift Drag ratio
drive = 2;%FWD

sim("foward_simple.slx",60)
%Below is how to search the data and find z60 and quarter mile time
z60=interp1(mph,tout,60);
quarter=interp1(miles,tout,0.250);
disp("Malibu")
disp("The 0-60 mph time, in seconds, is:"), disp(z60)
disp("The quarter mile time, in seconds, is:"), disp(quarter)

%Plotting
figure(1)
subplot(2,2,1)
plot(mph,acell)
grid on
xlabel('mph')
ylabel('Gs')
figure(1)
subplot(2,2,2)
plot(tout,mph)
grid on
xlabel('seconds')
ylabel('mph')


%Chevy Malibu 07 EV
f=0.015; %Rolling Resistance
m=3143.925 ;%lbs with motor and controller
m = m/2.205; %kg
m = m + 655.32; %adding the 98.4 kW-Hr pack 
g=9.81;
rho=1.2; 
A=2.3; %Average f.a. for sedan
Cd=0.29; %best cd for 1993 U.S. Sedans in 14 years reasonable estimate for average sedan
P=205*745; %144 hp engine
mu=1.0; %basic all season tires
k=0.4; %40% rear weight bias
eff=0.85;%Assume 85% Efficeincy
L = 106.4; %wheel base inches
L = L/39.4; %meters
hca = .5;%cg height
LDR = -0.25; %Lift Drag ratio
drive = 2;%FWD

sim("foward_simple.slx",60)
%Below is how to search the data and find z60 and quarter mile time
z60=interp1(mph,tout,60);
quarter=interp1(miles,tout,0.250);
disp("Malibu_EV")
disp("The 0-60 mph time, in seconds, is:"), disp(z60)
disp("The quarter mile time, in seconds, is:"), disp(quarter)

%Plotting
figure(2)
subplot(2,2,1)
plot(mph,acell)
grid on
xlabel('mph')
ylabel('Gs')
figure(2)
subplot(2,2,2)
plot(tout,mph)
grid on
xlabel('seconds')
ylabel('mph')




%Chevy Malibu 07 EV 4WD
f=0.015; %Rolling Resistance
m=3143.925 ;%lbs with motor and controller
m = m/2.205; %kg
m = m + 655.32; %adding the 98.4 kW-Hr pack 
m = m + 200; %adding second motor
g=9.81;
rho=1.2; 
A=2.3; %Average f.a. for sedan
Cd=0.29; %best cd for 1993 U.S. Sedans in 14 years reasonable estimate for average sedan
P=205*745; %144 hp engine
P = P*2;%adding second motor
mu=1.0; %basic all season tires
k=0.4; %40% rear weight bias
eff=0.85;%Assume 85% Efficeincy
L = 106.4; %wheel base inches
L = L/39.4; %meters
hca = .5;%cg height
LDR = -0.25; %Lift Drag ratio
drive = 3;%4WD

sim("foward_simple.slx",60)
%Below is how to search the data and find z60 and quarter mile time
z60=interp1(mph,tout,60);
quarter=interp1(miles,tout,0.250);
disp("Malibu_EV_4WD")
disp("The 0-60 mph time, in seconds, is:"), disp(z60)
disp("The quarter mile time, in seconds, is:"), disp(quarter)

%Plotting
figure(3)
subplot(2,2,1)
plot(mph,acell)
grid on
xlabel('mph')
ylabel('Gs')
figure(3)
subplot(2,2,2)
plot(tout,mph)
grid on
xlabel('seconds')
ylabel('mph')


doHw = 0;
if doHw>0
        
    
    %place holder
    % Data needed for a motor curve with gear ratio
    i1=3.23;
    i2=2.19;
    i3=1.61;
    i4=1.23;
    i5=0.97;
    i6=0.8;
    ifd=3.42;
    D=0.69;
    
    rpm=[0 1000 3000 4000 6000 9000 9001 9002];  %engine rpm data points
    T=[275 275 310 325 350 325 0 0]/0.737;      %engine torque data, in ft-lbs, converted to N-m
    launch=5000;
    %LFA
    f=0.015;
    m=1709;
    g=9.81;
    rho=1.2;
    A=2.31;
    Cd=0.31;
    P=560*745;
    mu=1.2;
    k=0.5;
    eff=0.85;
    
    
    L = 102.6; %wheel base inches
    L = L/39.4; %meters
    hca = 20 ;%Cg height inches
    hca = hca/39.4;% meters
    %hca = .5;
    LDR = -0.25; %Lift Drag ratio
    drive = 1;
    
    sim("foward_simple.slx",60)
    
    %Notes:  To output data clean, must change Model Settings to uncheck box for
    %single simulation output.  Also, under solver, maybe limit max time step to 0.1
    %seconds if time steps get too big.
    
    %Below is how to search the data and find z60 and quarter mile time
    z60=interp1(mph,tout,60);
    quarter=interp1(miles,tout,0.250);
    disp("LFA")
    disp("The 0-60 mph time, in seconds, is:"), disp(z60)
    disp("The quarter mile time, in seconds, is:"), disp(quarter)
    
    %Below is how to plot
    figure(1)
    subplot(2,2,1)
    plot(mph,acell)
    grid on
    xlabel('mph')
    ylabel('Gs')
    
    figure(1)
    subplot(2,2,2)
    plot(tout,mph)
    grid on
    xlabel('seconds')
    ylabel('mph')
    
    %FWD fast
    
    f=0.015;
    m=1227;
    g=9.81;
    rho=1.2;
    A=1.7;
    Cd=0.32;
    P=140*745;
    mu=1.0;
    k=0.47;
    eff=0.85;
    
    L = 102.6; %wheel base inches
    L = L/39.4; %meters
    L = 2.47;
    hca = 20 ;%Cg height inches
    hca = hca/39.4;% meters
    hca = .5;
    LDR = 0; %Lift Drag ratio
    drive = 2;
    
    sim("foward_simple.slx",60)
    
    %Notes:  To output data clean, must change Model Settings to uncheck box for
    %single simulation output.  Also, under solver, maybe limit max time step to 0.1
    %seconds if time steps get too big.
    
    %Below is how to search the data and find z60 and quarter mile time
    z60=interp1(mph,tout,60);
    quarter=interp1(miles,tout,0.250);
    disp("FWD Fast")
    disp("The 0-60 mph time, in seconds, is:"), disp(z60)
    disp("The quarter mile time, in seconds, is:"), disp(quarter)
    
    %Below is how to plot
    figure(2)
    subplot(2,2,1)
    plot(mph,acell)
    grid on
    xlabel('mph')
    ylabel('Gs')
    
    figure(2)
    subplot(2,2,2)
    plot(tout,mph)
    grid on
    xlabel('seconds')
    ylabel('mph')
    
    %GTR
    f=0.015;
    m=1740;
    g=9.81;
    rho=1.2;
    A=2.6;
    Cd=0.3;
    P=485*745;
    mu=1.0;
    k=0.65;
    eff=0.8;
    
    L = 102.6; %wheel base inches
    L = L/39.4; %meters
    L = 2.78;
    hca = 20 ;%Cg height inches
    hca = hca/39.4;% meters
    hca = .5;
    LDR = 0; %Lift Drag ratio
    drive = 3;
    
    sim("foward_simple.slx",60)
    
    %Notes:  To output data clean, must change Model Settings to uncheck box for
    %single simulation output.  Also, under solver, maybe limit max time step to 0.1
    %seconds if time steps get too big.
    
    %Below is how to search the data and find z60 and quarter mile time
    z60=interp1(mph,tout,60);
    quarter=interp1(miles,tout,0.250);
    disp("GTR")
    disp("The 0-60 mph time, in seconds, is:"), disp(z60)
    disp("The quarter mile time, in seconds, is:"), disp(quarter)
    
    %Below is how to plot
    figure(3)
    subplot(2,2,1)
    plot(mph,acell)
    grid on
    xlabel('mph')
    ylabel('Gs')
    
    figure(3)
    subplot(2,2,2)
    plot(tout,mph)
    grid on
    xlabel('seconds')
    ylabel('mph')
    
    
    %F1
    f=0.015;
    m=620;
    g=9.81;
    rho=1.2;
    A=1.4;
    Cd=0.7;
    P=745*745;
    mu=2.25;
    k=0.6;
    eff=0.9;
    
    
    L = 3.05;
    hca = .25;
    LDR = -3.3; %Lift Drag ratio
    drive = 1; %REAR
    
    sim("foward_simple.slx",60)
    
    %Notes:  To output data clean, must change Model Settings to uncheck box for
    %single simulation output.  Also, under solver, maybe limit max time step to 0.1
    %seconds if time steps get too big.
    
    %Below is how to search the data and find z60 and quarter mile time
    z60=interp1(mph,tout,60);
    quarter=interp1(miles,tout,0.250);
    disp("F1")
    disp("The 0-60 mph time, in seconds, is:"), disp(z60)
    disp("The quarter mile time, in seconds, is:"), disp(quarter)
    
    %Below is how to plot
    figure(4)
    subplot(2,2,1)
    plot(mph,acell)
    grid on
    xlabel('mph')
    ylabel('Gs')
    
    figure(4)
    subplot(2,2,2)
    plot(tout,mph)
    grid on
    xlabel('seconds')
    ylabel('mph')

end
