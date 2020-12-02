from pyo import *
import threading

class Player:
    def __init__(self, met, notes):
        self.notes = notes
        self.instrument = Instrument(met)
        self.instrument.start()

        self.active = []

    def note_off(self, key):

        if key not in self.notes:
            return

        self.active.remove(key)

        if len(self.active) == 0:
            self.instrument.silence()
        else:
            self.instrument.strum(self.active)

    def note_on(self, key):
        if key not in self.notes:
            return

        self.active.append(key)
        
        self.instrument.strum(self.active)

class Instrument(threading.Thread):
    def __init__(self, met):
        super(Instrument, self).__init__()

        self.met = met

        self.wav = SquareTable()
        self.env = CosTable([(0,0), (100,1), (500,.3), (8191,0)])
        self.pit = TrigXnoiseMidi(self.met, dist=3, scale=0, mrange=(24,24)) # Noise
        
        self.amp = TrigEnv(self.met, table=self.env, dur=.25, mul=.7) # Attack, Decay, Sustain, Fade (ADSF)

        self.osc = Osc(table=self.wav, freq=self.pit, mul=self.amp).play()
        
    def run(self):
        print('running')

    def strum(self, notes):        
        print('strum', notes)

        if notes.count == 1:
            self.wav = Sine()
            
        if notes.count == 2:
            self.wav = SawTable()
            
        if notes.count == 3:
            self.wav = SquareTable()
        
        if self.osc.isOutputting:
            self.osc.out()
        else:
            self.osc.setTable(self.wav)

    def silence(self):
        self.osc.stop()


