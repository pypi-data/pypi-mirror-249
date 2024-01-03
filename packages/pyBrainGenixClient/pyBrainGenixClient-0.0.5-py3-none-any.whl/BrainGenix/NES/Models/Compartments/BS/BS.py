# BrainGenix-NES
# AGPLv3

import json

from . import Configuration

from BrainGenix.NES.Client import RequestHandler


class BS:

    def __init__(self, _Configuration:Configuration, _RequestHandler:RequestHandler, _SimulationID:int):
        # Create Attributes
        self.Name = None
        self.RequestHandler = _RequestHandler
        

        # Create Box On Server
        ShapeID = _Configuration.Shape.ID
        Response = self.RequestHandler.MakeAuthenticatedQuery(f"/NES/Compartment/BS/Create?SimulationID={_SimulationID}&Name={_Configuration.Name}&ShapeID={ShapeID}&MembranePotential_mV={_Configuration.MembranePotential_mV}&SpikeThreshold_mV={_Configuration.SpikeThreshold_mV}&DecayTime_ms={_Configuration.DecayTime_ms}")
        assert(Response != None)
        self.ID = Response["CompartmentID"]