# BrainGenix-NES
# AGPLv3

from .. import Models
from . import Configuration

from BrainGenix.NES.Client import RequestHandler

from BrainGenix.NES.Shapes import Sphere
from BrainGenix.NES.Shapes import Box
from BrainGenix.NES.Shapes import Cylinder

from BrainGenix.NES.VSDA import EM


class Simulation():

    def __init__(self, _Configuration:Configuration, _RequestHandler:RequestHandler):
        # Create Attributes
        self.Name = None
        self.RequestHandler = _RequestHandler
        

        # Create Sim On Server
        Response = self.RequestHandler.MakeAuthenticatedQuery(f"/NES/Simulation/Create?SimulationName={_Configuration.Name}")
        assert(Response != None)
        self.ID = Response["SimulationID"]


    
    ## Methods For Adding Objects
        

    def AddReceptor(self, _ReceptorConfig):
        return 0 # temp stuff
    
    def AddSynapse(self, _SynapseConfig):
        return 0 # temp stuff

    def AddNeuron(self, _NeuronConfig):
        return 0 # temp stuff

     # VSDA Init Commands
    def AddVSDAEM(self, _VSDAEMConfig:EM.Configuration):
        return EM.EM(_VSDAEMConfig, self.RequestHandler, self.ID)


     # Compartments Add Methods
    def AddBSCompartment(self, _BSCompartmentConfig:Models.Compartments.BS.Configuration):
        return Models.Compartments.BS.BS(_BSCompartmentConfig, self.RequestHandler, self.ID)

    
     # Geometry Add Methods
    def AddSphere(self, _SphereConfig:Sphere.Configuration):
        return Sphere.Sphere(_SphereConfig, self.RequestHandler, self.ID)

    def AddBox(self, _BoxConfig:Box.Configuration):
        return Box.Box(_BoxConfig, self.RequestHandler, self.ID)

    def AddCylinder(self, _CylinderConfig:Cylinder.Configuration):
        return Cylinder.Cylinder(_CylinderConfig, self.RequestHandler, self.ID)


    ## Simulation Update Routes
    def Reset(self):
        Response = self.RequestHandler.MakeAuthenticatedQuery(f"/NES/Simulation/Reset?SimulationID={self.ID}")
        assert(Response != None)

    def RunFor(self, _SimulationDuration_ms:float):
        Response = self.RequestHandler.MakeAuthenticatedQuery(f"/NES/Simulation/RunFor?SimulationID={self.ID}&Runtime_ms={_SimulationDuration_ms}")
        assert(Response != None)

    def RecordAll(self, _MaxRecordTime_ms:float):
        Response = self.RequestHandler.MakeAuthenticatedQuery(f"/NES/Simulation/RecordAll?SimulationID={self.ID}&MaxRecordTime_ms={_MaxRecordTime_ms}")
        assert(Response != None)

    def GetRecording(self):
        Response = self.RequestHandler.MakeAuthenticatedQuery(f"/NES/Simulation/GetRecording?SimulationID={self.ID}")
        assert(Response != None)
        print("GetRecording Is Not Yet Fully Implemented (FYI)!")
        print(Response.json())

    def GetStatus(self):
        Response = self.RequestHandler.MakeAuthenticatedQuery(f"/NES/Simulation/GetStatus?SimulationID={self.ID}")
        assert(Response != None)
        return Response.json()
