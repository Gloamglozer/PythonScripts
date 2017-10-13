"""VCO CHARACTERIZATION
This program interfaces with an Agilent spectrum analyzer over GPIB in order to automate characterization of the VCO 
used in our FMCW synthetic aperture radar. A Teensy microcontroller produces the voltage that goes to the tuning pin of the VCO using it's
analog out pin. 

We are characterizing the nonlinearity of the VCO so that a perfect ramp can be produced by having the use a 
lookup table in order to make a nonlinear voltage ramp which will produce a /linear/ frequency ramp
"""


import visa
import serial
import pickle
from time import sleep
# open serial port for teensy
ser = serial.Serial('COM4', 115200, timeout=None)

class SAInterface:
    def __init__(self,traceNum,averagingNum,RBW,marker,peakEx,refLevel):
        rm = visa.ResourceManager()
        resources = rm.list_resources()
        self.SpectrumAnalyzer = rm.open_resource('USB0::0x0957::0xFFEF::CN01990980::0::INSTR')
        print(self.SpectrumAnalyzer.query("*IDN?"))
        self.traceNum = traceNum
        self.setAveraging(averagingNum)
        self.setRBW(RBW)
        self.setRefLevel(refLevel)
        self.marker = marker
        self.peakEx = peakEx


    def setAveraging(self,averaging):
        self.averagingNum = averaging
        # Build Averaging Command
        AveragingTrace = "SENS:AVER:TRAC{0} ON;:AVER:TRAC{0}:COUN {1};SENS:AVER:TRAC{0} OFF;".format(self.traceNum,self.averagingNum)
        AveragingCount = "SENS;:AVER:COUN %d;:AVER ON;" % self.averagingNum
        AveragingCheck = ":AVER:TYPE:AUTO ON;"

        # Send Averaging Command
        return self.SpectrumAnalyzer.write(AveragingTrace+AveragingCount+AveragingCheck)
    
    def setRBW(self,rbw): #
        self.RBW = rbw
        # Build RBW String
        ResolutionBandwidth = "SENS:BWID %.2f;" % self.RBW
        ResolutionBWAutoOff = ":BWID:AUTO OFF;"
        AutoVideoBandwidth = ":BWID:VID:AUTO ON;"

        # Send RBW Command
        return self.SpectrumAnalyzer.write(ResolutionBandwidth+ResolutionBWAutoOff+AutoVideoBandwidth)

    def setRefLevel(self,ref):
        self.refLevel = ref
        return self.SpectrumAnalyzer.write("DISP:WIND:TRAC:Y:RLEV %.2f" % self.refLevel)

    def setWindow(self,limits): # set frequencies displayed on SA
        [startFrequency, stopFrequency] = limits
        # Sets start and stop frequency
        return self.SpectrumAnalyzer.write("SENS:FREQ:START %.2f;:FREQ:STOP %.2f;" %(startFrequency,stopFrequency))

    def findPeak(self):
        # Peak Search
        PeakSearchMax = ":CALC:MARK%d:MAX;" % self.marker
        ContinuousSearch = ":CALC:MARK%d:CPE ON;" % self.marker
        PeakSearchCriteria = ":CALC:MARK:PEAK:SEAR:MODE MAX;"
        PeakExcursion = "SENS:CALC:MARK:PEAK:EXC %.2f;" % self.peakEx
        DisablePeakThreshold = ":CALC:MARK:PEAK:THR:STAT OFF;"
        # Send Peak Seach
        self.SpectrumAnalyzer.write(PeakSearchMax+ContinuousSearch+PeakSearchCriteria+PeakExcursion+DisablePeakThreshold)
        return(self.SpectrumAnalyzer.query_ascii_values("CALC:MARK:X?")[0])

    def waitOneSweep(self):
        timeToWait = self.SpectrumAnalyzer.query(":SENS:SWE:TIME?")
        sleep(8*float(timeToWait[1:-1]))
        


class sweep:
    # From ROS3800-119+ Datasheet
    def __init__(self,minV,maxV,dacRes,numpoints,minFrequency,maxFrequency,windowRadius):
        self.maxDac = 2**dacRes
        self.numpoints = numpoints # must be a power of 2
        self.minV = minV # Voltage on the VCO when the DAC writes 0
        self.maxV = maxV # Voltage on the VCO when DAC writes 0b11...111
        self.minFrequency = minFrequency
        self.maxFrequency = maxFrequency
        self.currentFrequency = minFrequency
        self.windowRadius = windowRadius
        self.dacStep = int(self.maxDac / numpoints) 
        self.currentDac = 0 # setting the dac to the smallest number for the beginning of the sweep
    
    def expectedVoltage(self): #THIS ASSUMES THE RELATIONSHIP BETWEEN THE DAC'S SET POINT AND THE VOLTAGE BEFORE THE VCO IS LINEAR
        return (self.currentDac/self.maxDac)*(self.maxV-self.minV) + self.minV

    def expectedFrequency(self): #updates currentFrequency as well
        self.currentFrequency = (self.currentDac/self.maxDac)*(self.maxFrequency-self.minFrequency) + self.minFrequency
        return self.currentFrequency

    def zoomIn(self,freq):
        return [freq-self.windowRadius, freq+self.windowRadius]

    def fullSpan(self):
        return [self.minFrequency,self.maxFrequency]

    def setDac(self,dac):
        self.currentDac = dac
        ser.write(bytes([self.currentDac%256,self.currentDac>>8]))
        return ser.read(2)





SA = SAInterface(                                       \
        traceNum=1,             averagingNum=1,        \
        RBW=10e6,               marker = 1,             \
        peakEx = 6,              refLevel = 10           \
        )
swp = sweep(                                            \
        minV = 0.0,             maxV = 10.1,            \
        dacRes= 12,             numpoints = 128,          \
        minFrequency = 1723e6,  maxFrequency = 3121e6,  \
        windowRadius = 2e7,                               \
        )



data =  {}
for i in range(0,swp.maxDac,swp.dacStep):
    #Set voltage for binary number i in the ADC
    print(swp.setDac(i))

    #Set window to full span
    SA.setWindow(swp.fullSpan())

    #Set resolution bandwidth high
    SA.setRBW(1e6)

    #Wait for the spectrum analyzer to get across the screen before detecting peak. 
    SA.waitOneSweep()

    #Zoom in to perceived spike
    SA.setWindow(swp.zoomIn(SA.findPeak()))

    #set reference level every time we zoom
    SA.setRefLevel(7)

    #set resolution bandwidth low
    SA.setRBW(30e3)

    #Wait for the spectrum analyzer to get across the screen before detecting peak. 
    SA.waitOneSweep()

    data[swp.currentDac] = {"Voltage":swp.expectedVoltage(),"Frequency":SA.findPeak()}
    print("{}{}{}".format(swp.currentDac,))

# VCO_Data = open("VCO_Data.pkl",'w') 
# pickle.dump(data,VCO_Data)

SA.setWindow(swp.fullSpan())
swp.setDac(0)

csv = open("data.csv",'w')
for i in sorted(data):
    csv.write("{},{},{}\n".format(i,data[i]["Voltage"],data[i]["Frequency"]))
    print("{},{},{}\n".format(i,data[i]["Voltage"],data[i]["Frequency"]))
csv.close()
ser.close()
SA.SpectrumAnalyzer.close()