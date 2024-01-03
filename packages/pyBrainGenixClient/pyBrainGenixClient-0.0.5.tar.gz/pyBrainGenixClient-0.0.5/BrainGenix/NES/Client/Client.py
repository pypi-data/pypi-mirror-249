# BrainGenix-NES
# AGPLv3

import requests

from . import Configuration
from . import Modes
from . import RequestHandler

from .. import Simulation


class Client:

    def __init__(self, _Configuration:Configuration):

        # Get And Validate Configuration
        self.Configuration = _Configuration
        self.ValidateConfig()
        self.Setup()


    # Helper Functions
    def ValidateConfig(self):

        # Check Mode
        ValidModes =  [Modes.Remote, Modes.Local]
        if self.Configuration.Mode not in ValidModes:
            raise Exception("NES Client Configuration Mode Not Set")


        
        # Local not yet implemented
        if self.Configuration.Mode == Modes.Local:
            raise NotImplementedError("Randal - please copy this over from your vbp repo.")

        # Remote Mode
        elif self.Configuration.Mode == Modes.Remote:

            # Check That User Has Actually Set Host/Port
            if (self.Configuration.Host == ""):
                raise ValueError("Please Set The API Host")
            if (self.Configuration.Port == 0):
                raise ValueError("Please Set The API Port")
            if (self.Configuration.Token == ""):
                raise ValueError("Please Set The API Token")

            # Build Request URI Base
            self.URIBase = f"http://{self.Configuration.Host}:{self.Configuration.Port}"



    def Setup(self): # this should do some logic to make sure the connection is actually good.
        self.RequestHandler = RequestHandler.RequestHandler(self.URIBase, self.Configuration.Token)

        # Check Version
        Status = self.RequestHandler.MakeQuery("/Diagnostic/Version")
        print(f"Initialized BrainGenix API. Server Is Running Version '{Status['Version']}'")

        self.HasConnection = True


    # Getter Functions
    def IsReady(self):
        return self.HasConnection
    

    # Creation Functions
    def CreateSimulation(self, _SimulationConfig):
        return Simulation.Simulation(_SimulationConfig, self.RequestHandler)
