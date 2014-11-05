# -*- coding: utf-8 -*-
"""
Created on Fri Oct 24 18:14:50 2014

@author: richard

at each time index:
    generate intensity values x,y,z
    mosquito moves to it's position in t
    where is mozzie x y t
    intensity at x,y,t
    sensor neuron responds to stimulus.
        if it fires, store the spike [(time_index, 1)] and
        amplitude control neuron recompute y_targ

"""
import numpy as np
from numpy import pi, sin, cos
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as axes3d
from scipy import spatial
#from matplotlib import cm


flight_dur = 100.0
timestep = 1.0


class Plume(object):
    def __init__(self,):
        """Our odor plume in x,y, z
        Currenty 0 everywhere at all timesteps
        TODO: feed plume a time parameter, which then calcs all the intensities 
        """
        self.res = 100.0      #Split into 100 straight segments
        self.X = np.linspace(0, BOX_SIZE[0], self.res) #X locs of plume
        self.Y = np.linspace(-1*BOX_SIZE[1], BOX_SIZE[1],self.res) #Y of odor slices
        self.coordinates_list = [(x,y) for x in self.X for y in self.Y]
        self.xx, self.yy = np.meshgrid(self.X, self.Y, sparse=True)
    def current_plume(self,curr_time): #uses current time, not index
        """given the timeindex, return plume intensity values
        currently always returns 0
        input curr_time
        output plume at that frame
        TODO: make vary over time"""
        #odor intensity at x,y
        self.zz = 0 * (self.xx + self.yy) + 1.1 # PLUME1 set to 1.1 everywhere
#==============================================================================
# # un-uniform plume      
#         foo = self.xx + self.yy
#         foo1 = (0 * foo[:len(foo)/2 -10])
#         foo2 = (0 * foo[len(foo)/2 -10:(len(foo)/2 + 20)]+ 3 )
#         foo3 = (0 * foo[len(foo)/2 + 20:])
#         self.zz = np.vstack((foo1,foo2,foo3)) # PLUME2 half 0 half 1.1
#         self.zz = self.zz.ravel()
        #        self.plumexyz = [(x,y,z) for x in self.X for y in self.Y for z in self.zz.ravel()]
        #TODO save 3d array to file so I don't need to recompute every time.

#==============================================================================
        plume_curr = self.xx, self.yy, self.zz
        return plume_curr
    def find_nearest_intensity(self,loc):
        """uses kd tree to find closest intensity coord to a given location
        given a (x,y) location, return index of nearest intensity value
        """
        plumetree = spatial.cKDTree(self.coordinates_list)
        distance, index = plumetree.query(loc)
        return self.coordinates_list[index]
    def intensity_val(self, plume_curr, location):
        """
        given a plume at a certain frame and x,y coords, give intensity at that coord
        input plume, (x,y) coords
        output: plume intensity at x,y
        """
        x, y = self.find_nearest_intensity(location)
        intensitygrid = plume_curr[2] #THIS IS THE SOURCE OF THE ERROR!
        try: 
            return intensitygrid[x][y]
        except IndexError:
            print "mozzie sniffing outside the box"
            return 0.0


class Mozzie(object):
    """our brave mosquito, moving in 2D
        plots the mosquito's path in space
    input: total_velo_max, total_velo_min, wind_velo, y_offset_curr, angular_velo, flight_dur, timestep
    output: times, agent_y_pos, x_velocities, y_velocities 
    TODO: impliment agent_x_pos using velocity max and min
    TODO: implement y offset, and wind velocity
    TODO: make agent_pos list where each item is an (x,y) coord
    TODO: make sensor_neuron control agent flight
    """
    def __init__(self,total_velo_max = 6.6, wind_velocity = 0, y_offset_curr = 0, angular_velo = pi / 15):
        self.total_velo_max = total_velo_max
        self.total_velo_min = total_velo_max / 5
        self.angular_velo = angular_velo
        self.wind_velo = wind_velocity
        self.loc_curr =  0, 0
        self.loc_history = {0 : self.loc_curr}
        self.loc_list = []
        self.y_velocities = {}
        self.x_velocities = {}
        self.time_prev = 0
    def move(self,time_curr):
        """move the mosquito in a cast, add to location history
        input: time in secs
        output: none (location history updates)
        TODO: put in sin equations
        """
        y_pos_curr = amplitude_neuron.amplitude_curr * sin (self.angular_velo * time_curr) + amplitude_neuron.y_offset_curr
        crap, y_pos_prev = self.loc_history[self.time_prev]
        y_velocity_curr = (y_pos_curr - y_pos_prev) / timestep
        self.y_velocities[time_curr] = y_velocity_curr
#        ## TODO: make x_velocities as in Sharri's
        self.x_velocities[time_curr] = (time_curr - self.time_prev)/ timestep
        self.loc_curr = time_curr, y_pos_curr #TODO: make x coord not the time!
        self.time_prev = time_curr
        self.loc_history[time_curr] = self.loc_curr
        self.loc_list.append(self.loc_curr)
    def where(self, time):
        """ given time, where was the mozzie?
        input: time in seconds
        output: x,y coords
        TODO: make real"""
        where = self.loc_history[time]
        return where
    # def _xspeedcalc

def plume_plotter(plume, plotting = False):
    if plotting == False:
        pass
    else:
        # Set up a figure
        fig = plt.figure(0, figsize=(6,6))
        ax = axes3d.Axes3D(fig)
        x, y, z = plume.xx, plume.yy, plume.zz
        ax.plot_wireframe(x , y , z, rstride=10, cstride=10)
        ax.set_xlim3d([0.0, BOX_SIZE[0]])
        ax.set_ylim3d([-1*BOX_SIZE[1], BOX_SIZE[1]])
        ax.set_zlim3d([0.0, BOX_SIZE[2]])
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('intensity')
        ax.set_title("plume intensity in space")
        plt.show()

def mozzie_plotter(plotting = False):
    if plotting == False:
        pass
    else:
        # Set up a figure
        fig = plt.figure(1, figsize=(6,6))
        location_times, locations = mozzie.loc_history.keys(), mozzie.loc_history.values()
        #x = [float(xycoord[0]) for xycoord in mozzie.loc_history.values() ] #don't need this since x is just = locationtimes
        y = [float(xycoord[1]) for xycoord in mozzie.loc_history.values() ]
        y_velocity_times, y_velocities = mozzie.y_velocities.keys(), mozzie.y_velocities.values()
        x_velocities_times, x_velocities = mozzie.x_velocities.keys(), mozzie.x_velocities.values()
        #print max(voltages)+5    
        plt.plot(location_times, y, 'k',label= 'agent y_pos over time' )
#        plt.plot(y_velocity_times, y_velocities,'b',label= 'y velocity over t')
        plt.plot(x_velocities_times,x_velocities,'r',label= 'x velocity over t')
        plt.plot(x_velocities_times,len(x_velocities_times)*[BOX_SIZE[1]])
        plt.plot(x_velocities_times,len(x_velocities_times)*[-1*BOX_SIZE[1]])
        for spot in sniffspots:
            plt.scatter(spot[0], spot[1])
#        plt.scatter[sniffspots]
        plt.xlabel('time')
        plt.ylabel('Y position')
        plt.legend()
        plt.title("Flying mosquito")   
        plt.show()


class Neuron(object):
    def __init__(self, tau_e = 1.2, spikethresh = 3.0):
        self.spikethresh = spikethresh
        self.tau_e = tau_e
        self.voltage_history = {}
        self.spike_history = {} 
        self.spiketime_index = {}
        self.time_prev = 0
        #if spiking, return true

sniffspots = []

class Sensor_neuron(Neuron):
    def spiker(self,time, intensity_now):
        '''evaluator leaky integrate and fire neuron. stimulus intensity -> cellular voltages -> spikes
        input time (sec) and intensity
        updates spiking history and voltage history
        output spiking True and timestep
        '''
        if len(self.voltage_history) == 0: 
            """at very first timestep, start neuron fresh
            TODO: could this be avoided? remove self.tau weighted computation"""
            self.voltage_history[time] = 0.0
            self.spike_history[time] = 0
            self.time_prev = time
        else:
            voltage_prev = self.voltage_history[self.time_prev]
            if voltage_prev > self.spikethresh: #crossing threshold at prev timestep discharges neuron voltage
                self.voltage_history[time] = 0
                self.spike_history[time] = 1
                self.spiketime_index[time] = 1
                sniffspots.append(mozzie.where(time))
                self.time_prev = time
                return "spike!"
            else:
                #updating voltage
                self.voltage = (1/self.tau_e) * voltage_prev + intensity_now #intensity at this timestep + weighted past intensity
                self.voltage_history[time] = self.voltage
                self.spike_history[time] = 0
                self.time_prev = time        

def eval_neuron_plotter(plotting = False):
    if plotting == False:
        pass
    else:
        voltagetimes, voltages = sensor_neuron.voltage_history.keys(), sensor_neuron.voltage_history.values()
        spiketimes, spikes = sensor_neuron.spike_history.keys(), sensor_neuron.spike_history.values()
        #print max(voltages)+5    
        fig = plt.figure(2)
        plt.plot(voltagetimes, voltages, 'r',label='soma voltage')
        plt.plot(spiketimes, spikes, 'b', label= 'spikes')
        plt.xlabel('time')
        plt.ylabel('voltage')
        plt.legend()
        plt.title("Neuron voltage and spikes")   
        plt.show()

class Amplitude_neuron(Neuron):
    """if sensor neuron fires,m amplitude control neuron recompute y_targ and amplitude val.
    else, decay teleporter
    """
    def __init__(self):
        self.time_prev = 0.0
        self.tau_y = 10
        self.y_aim = 0.0
        self.y_aim_history = {0.0:self.y_aim}
        self.y_offset_curr = 0.0
        self.y_offset_history = {0.0:self.y_offset_curr}
        self.angular_velo = mozzie.angular_velo
        self.amplitude_max = (2**0.5 / self.angular_velo) * (((mozzie.total_velo_max + mozzie.wind_velo) **2) - ((mozzie.total_velo_min + mozzie.wind_velo)**2))**0.5 #TODO add vwind
        self.amplitude_curr = self.amplitude_max
    def y_aimer(self,time):
        """if spike, recompute y_aim"""
#        print "y_aimer time is ", time
        x_curr, y_curr = mozzie.where(time)
        self.y_aim = y_curr
        self.y_aim_history[time] = self.y_aim
    def y_offsetter(self,time):
#        print self.y_offset_history[self.time_prev], "this is the prev offset"
        self.y_offset_curr = (self.y_aim - self.y_offset_history[self.time_prev]) / self.tau_y
#        print self.y_offset_curr, "new current y_offset!"
        self.y_offset_history[time] = self.y_offset_curr
        self.time_prev = time
    def amplitude_controller(self):
        """TODO add vwind
        constrain mosquito to the box no matter what"""
        pass
        

def timestepper():
    times = np.arange(0, flight_dur, timestep)
    time_indexes = list(enumerate(times))
    for time in time_indexes:
#        print time[1], "time in stepper"
        plume_curr = plume.current_plume(time[1]) #intensity value of plume at this time
        mozzie.move(time[1])
        loc = mozzie.where(time[1])
        intensity_now = plume.intensity_val(plume_curr,loc)
        if sensor_neuron.spiker(time[1], intensity_now) == "spike!": #if sensor neuron spikes
            amplitude_neuron.y_aimer(time[1])
        amplitude_neuron.y_offsetter(time[1])
        amplitude_neuron.amplitude_controller()
        
            

if __name__ == "__main__":
    sensor_neuron = Sensor_neuron()
    mozzie = Mozzie()
    amplitude_neuron = Amplitude_neuron()
    BOX_SIZE = (flight_dur,(amplitude_neuron.amplitude_max),5.0)
    plume = Plume()
    timestepper()
    plume_plotter(plume, plotting = True)
    eval_neuron_plotter(plotting = True)
    mozzie_plotter(plotting = True)
    
#####
    """
functioning nd array lookup
    intensity_array = plume.coordinates_list
    mozzie_path = mozzie.loc_list
    
    def do_kdtree(intensity_array, mozzie_path):
        mytree = spatial.cKDTree(intensity_array)
        dist, indexes = mytree.query(mozzie_path)
        return dist, indexes
        
    distances, results2 = do_kdtree(intensity_array, mozzie_path)
    """

