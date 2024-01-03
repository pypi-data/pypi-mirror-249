# BrainGenix-NES
# AGPLv3

import json

from . import Configuration

from BrainGenix.NES.Client import RequestHandler


class Staple:

    def __init__(self, _Configuration:Configuration, _RequestHandler:RequestHandler, _SimulationID:int):
        # Create Attributes
        self.Name = None
        self.RequestHandler = _RequestHandler
        

        # Create Box On Server
        SourceCompartmentID = _Configuration.SourceCompartment.ID
        DestinationCompartmentID = _Configuration.DestinationCompartment.ID
        Response = self.RequestHandler.MakeAuthenticatedQuery(f"/NES/Connection/Staple/Create?SimulationID={_SimulationID}&Name={_Configuration.Name}&SourceCompartmentID={SourceCompartmentID}&DestinationCompartmentID={DestinationCompartmentID}")
        assert(Response != None)
        self.ID = Response["CompartmentID"]