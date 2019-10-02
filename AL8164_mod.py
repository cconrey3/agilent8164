import pyvisa

class AL8164(pyvisa.resources.gpib.GPIBInstrument):

    def get_IDN(self):
        print(self.query('*IDN?'))
