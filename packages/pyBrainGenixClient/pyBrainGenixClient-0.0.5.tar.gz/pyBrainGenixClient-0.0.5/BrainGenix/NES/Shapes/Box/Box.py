# BrainGenix-NES
# AGPLv3

import json

from . import Configuration

from BrainGenix.NES.Client import RequestHandler


class Box:

    def __init__(self, _Configuration:Configuration, _RequestHandler:RequestHandler, _SimulationID:int):
        # Create Attributes
        self.Name = None
        self.RequestHandler = _RequestHandler
        

        # Create Box On Server
        CenterPos = json.dumps(_Configuration.CenterPosition_um)
        Dimensions = json.dumps(_Configuration.Dimensions_um)
        Rotation = json.dumps(_Configuration.Rotation_rad)
        Response = self.RequestHandler.MakeAuthenticatedQuery(f"/NES/Geometry/Shape/Box/Create?SimulationID={_SimulationID}&Name={_Configuration.Name}&CenterPosition_um={CenterPos}&Dimensions_um={Dimensions}&Rotation_rad={Rotation}")
        assert(Response != None)
        self.ID = Response["ShapeID"]