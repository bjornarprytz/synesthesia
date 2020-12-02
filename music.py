from pyo import *
import threading

class Chord (threading.Thread):
    def __init__(self, threadID, name, notes):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.notes = notes
    def run(self):
        pass # todo: start sounds here, time them 6 seconds?

class Music:
    def __init__(self):
        self.server = Server().boot()
        self.server.start()
        self.met = Metro(.125, 12).play()
        
        self.wav = SquareTable()
        self.env = CosTable([(0,0), (100,1), (500,.3), (8191,0)])
        self.amp = TrigEnv(self.met, table=self.env, dur=.25, mul=.7)
        self.pit = TrigXnoiseMidi(self.met, dist=3, scale=0, mrange=(24,24))
        
        self.update_osc()
        

    def interpret(self, arg):
        i = 0
        for word in arg.split():
            self.play_chords(word)
            i += 1


    def play_chords(self, word):

        res = sum_word(word)
        print('result ' + str(res))

        self.pit = TrigXnoiseMidi(self.met, dist='loopseg', x1=20, scale=1, mrange=(48,84))
        
        self.lfd = Sine([.4,.2], mul=.2, add=.3)
        
        self.synth = SuperSaw(freq=220, detune=self.lfd, bal=0.5, mul=0.2).out()


    def update_osc(self):
        self.out = Osc(table=self.wav, freq=self.pit, mul=self.amp).out()

    def close(self):
        self.server.stop()

def sum_word(word):
    s = 0
    for char in word:
        s += ord(char)
    return s

def clamp(val, min, max):
    return Max(Min(min, val), max)
