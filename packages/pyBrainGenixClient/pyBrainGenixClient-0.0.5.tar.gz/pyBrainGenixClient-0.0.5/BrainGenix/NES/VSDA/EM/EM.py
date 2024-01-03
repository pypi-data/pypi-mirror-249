# BrainGenix-NES
# AGPLv3

import json

from . import Configuration

from BrainGenix.NES.Client import RequestHandler


class EM:

    def __init__(self, _Configuration:Configuration, _RequestHandler:RequestHandler, _SimulationID:int):
        # Create Attributes
        self.Name = None
        self.RequestHandler = _RequestHandler
        self.SimulationID = _SimulationID
        

        # Create On Server
        Response = self.RequestHandler.MakeAuthenticatedQuery(f"/NES/VSDA/EM/Initialize?SimulationID={_SimulationID}")
        assert(Response != None)

        Response = self.RequestHandler.MakeAuthenticatedQuery(f"/NES/VSDA/EM/SetupMicroscope?SimulationID={_SimulationID}&PixelResolution_nm={_Configuration.PixelResolution_nm}&ImageWidth_px={_Configuration.ImageWidth_px}&ImageHeight_px={_Configuration.ImageHeight_px}&SliceThickness_nm={_Configuration.SliceThickness_nm}&ScanRegionOverlap_percent={_Configuration.ScanRegionOverlap_percent}")
        assert(Response != None)



    ## Access Methods
    def DefineScanRegion(self, _Point1_um:list, _Point2_um:list):
        Point1 = json.dumps(_Point1_um)
        Point2 = json.dumps(_Point2_um)
        Response = self.RequestHandler.MakeAuthenticatedQuery(f"/NES/VSDA/EM/DefineScanRegion?SimulationID={self.SimulationID}&Point1_um={Point1}&Point2_um={Point2}")
        assert(Response != None)
        self.ScanRegionID = Response["ScanRegionID"]


    def QueueRenderOperation(self):
        Response = self.RequestHandler.MakeAuthenticatedQuery(f"/NES/VSDA/EM/QueueRenderOperation?SimulationID={self.SimulationID}&ScanRegionID={self.ScanRegionID}")
        assert(Response != None)
        return Response["StatusCode"]


    def GetRenderStatus(self):
        Response = self.RequestHandler.MakeAuthenticatedQuery(f"/NES/VSDA/EM/GetRenderStatus?SimulationID={self.SimulationID}")
        assert(Response != None)
        return Response
    

    def GetImageStack(self):
        Response = self.RequestHandler.MakeAuthenticatedQuery(f"/NES/VSDA/EM/GetImageStack?SimulationID={self.SimulationID}&ScanRegionID={self.ScanRegionID}")
        assert(Response != None)
        return Response["RenderedImages"]


    def GetImage(self, _ImageHandle:str):
        Response = self.RequestHandler.MakeAuthenticatedQuery(f"/NES/VSDA/EM/GetImage?SimulationID={self.SimulationID}&ImageHandle={_ImageHandle}")
        assert(Response != None)
        return bytes(Response["ImageData"], 'utf-8')