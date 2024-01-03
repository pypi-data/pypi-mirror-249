# BrainGenix-NES
# AGPLv3

import json

from . import Configuration

from BrainGenix.NES.Client import RequestHandler


class Receptor:

    def __init__(self, _Configuration:Configuration, _RequestHandler:RequestHandler, _SimulationID:int):
        # Create Attributes
        self.Name = None
        self.RequestHandler = _RequestHandler
        

        # Create Box On Server
        SourceCompartmentID = _Configuration.SourceCompartment.ID
        DestinationCompartmentID = _Configuration.DestinationCompartment.ID
        ReceptorLocation = json.dumps(_Configuration.ReceptorLocation_um)
        Response = self.RequestHandler.MakeAuthenticatedQuery(f"/NES/Connection/Receptor/Create?SimulationID={_SimulationID}&Name={_Configuration.Name}&SourceCompartmentID={SourceCompartmentID}&DestinationCompartmentID={DestinationCompartmentID}&Conductance_nS={_Configuration.Conductance_nS}&TimeConstant_ns={_Configuration.TimeConstant_ns}&ReceptorLocation_um={ReceptorLocation}")
        assert(Response != None)
        self.ID = Response["CompartmentID"]