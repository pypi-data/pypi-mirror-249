# BrainGenix-NES
# AGPLv3

import json

from . import Configuration

from BrainGenix.NES.Client import RequestHandler


class Sphere:

    def __init__(self, _Configuration:Configuration, _RequestHandler:RequestHandler, _SimulationID:int):
        # Create Attributes
        self.Name = None
        self.RequestHandler = _RequestHandler
        

        # Create Sphere On Server
        CenterPos = json.dumps(_Configuration.Center_um)
        Response = self.RequestHandler.MakeAuthenticatedQuery(f"/NES/Geometry/Shape/Sphere/Create?SimulationID={_SimulationID}&Name={_Configuration.Name}&Radius_um={_Configuration.Radius_um}&Center_um={CenterPos}")
        assert(Response != None)
        self.ID = Response["ShapeID"]