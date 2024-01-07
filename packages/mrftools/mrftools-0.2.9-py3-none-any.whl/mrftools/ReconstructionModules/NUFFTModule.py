from ..Types import ReconstructionModuleIOType, ImageData
from . import ReconstructionModule, Register
import torch
import numpy as np
import mrftools.Utilities.torchkbnufft as tkbn

@Register
class NUFFTModule(ReconstructionModule):
    """
    NUFFT (Non-Uniform Fast Fourier Transform) module.

    Args:
        reconstructionParameters (dict): Parameters specific to the reconstruction module.
        inputType (ReconstructionModuleIOType, optional): Input data type. Defaults to ReconstructionModuleIOType.KSPACE.
        outputType (ReconstructionModuleIOType, optional): Output data type. Defaults to ReconstructionModuleIOType.IMAGE.
        ktraj (torch.Tensor, optional): k-space trajectory. Defaults to None.
        dcf (torch.Tensor, optional): Density compensation factor. Defaults to None.
        numNearestNeighbors (int, optional): Number of nearest neighbors for NUFFT. Defaults to 3.
        device (torch.device, optional): Device for computation. Defaults to None.
    """

    @staticmethod
    def PrepTrajectoryObjects(reconstructionParameters, trajectoryFilepath, densityFilepath, trajectoryDesignMatrixSize, numSpirals, useMeanDCF=True):
        """
        Prepare trajectory objects for NUFFT.

        Args:
            reconstructionParameters (dict): Parameters specific to the reconstruction module.
            trajectoryFilepath (str): Filepath to the trajectory data.
            densityFilepath (str): Filepath to the density compensation factor data.
            trajectoryDesignMatrixSize (tuple): Size of the trajectory design matrix.
            numSpirals (int): Number of spirals.
            useMeanDCF (bool, optional): Whether to use mean density compensation factor. Defaults to True.

        Returns:
            torch.Tensor: k-space trajectory.
            torch.Tensor: Density compensation factor.
        """
        trajectoryBuffer = np.fromfile(trajectoryFilepath, dtype=np.complex64)
        densityBuffer = np.fromfile(densityFilepath, dtype=np.float32)
        trajectoryBuffer.real = trajectoryBuffer.real * (trajectoryDesignMatrixSize[0]/reconstructionParameters.outputMatrixSize[0])
        trajectoryBuffer.imag = trajectoryBuffer.imag * (trajectoryDesignMatrixSize[1]/reconstructionParameters.outputMatrixSize[1])
        trajectorySplit = np.stack((trajectoryBuffer.real, trajectoryBuffer.imag))*2*np.pi
        ktraj = torch.tensor(trajectorySplit, dtype=torch.float32)
        if(useMeanDCF):
            densityBuffer = np.tile(np.mean(np.split(densityBuffer, numSpirals), axis=0), numSpirals)
        dcf = torch.tensor(densityBuffer)
        return ktraj, dcf
    
    def PerformAdjointNUFFTsImagewise(self, input): 
        """
        Perform adjoint NUFFTs (Non-Uniform Fast Fourier Transforms).

        Args:
            input (torch.Tensor): Input k-space data.

        Returns:
            torch.Tensor: Adjoint NUFFT results.
        """
        with torch.no_grad():
            adjoint_nufft = tkbn.KbNufftAdjoint(im_size=(self.matrixX, self.matrixY), grid_size=(self.matrixX*2, self.matrixY*2), numpoints=self.numNearestNeighbors).to(self.device)
            sizes = input.shape
            numCoils=sizes[0]; numPartitions=sizes[1]; numReadoutPoints=sizes[2]; numSpirals=sizes[3]; numSets=sizes[4]

            ktraj_device = self.ktraj.reshape((2,numSpirals,-1)).swapaxes(0,1).to(self.device)
            densities_device = self.dcf.reshape((numSpirals,-1)).to(self.device).t()

            nufftResults = torch.zeros((numPartitions, numSets, numSpirals, numCoils, self.matrixX, self.matrixY), dtype=torch.complex64)

            for partition in np.arange(0, numPartitions):
                for set in np.arange(0, numSets):
                    # Select readout across [coils, readoutPoints, spirals] and apply density compensation
                    readout_device = input[:, partition, :, :, set].to(self.device) * densities_device
                    # Reshape to [spirals, coils, readoutPoints] for NUFFT batching
                    readout_device = torch.moveaxis(readout_device, 2,0)
                    # Run NUFFT on device
                    nufftResult = adjoint_nufft(readout_device, ktraj_device)
                    # Save NUFFT result off device
                    nufftResults[partition, set, :, :, :, :] = nufftResult
                    del readout_device, nufftResult

            output = nufftResults.moveaxis((0,1,2,3,4,5), (1,4,5,0,2,3))
            if self.collapseToTimeseries:
                output = output.reshape((numCoils,numPartitions,self.matrixX,self.matrixY,-1))
            return output

    def PerformAdjointNUFFTs(self, input): 
        """
        Perform adjoint NUFFTs (Non-Uniform Fast Fourier Transforms).

        Args:
            input (torch.Tensor): Input k-space data.

        Returns:
            torch.Tensor: Adjoint NUFFT results.
        """
        with torch.no_grad():
            adjoint_nufft = tkbn.KbNufftAdjoint(im_size=(self.matrixX, self.matrixY), grid_size=(self.matrixX, self.matrixY), numpoints=self.numNearestNeighbors).to(self.device)
            input = torch.moveaxis(input,-1,0) 
            numImages = input.shape[0]
            numCoils = input.shape[1]
            numPartitions = input.shape[2]
            output = torch.zeros(numImages, numCoils, numPartitions, self.matrixX, self.matrixY, dtype=input.dtype)
            for partition in torch.arange(0,numPartitions):
                readout_device = torch.swapaxes(input[:, :, partition, :, :], -1,-2).reshape(numImages, numCoils, -1).to(self.device) 
                nufftResult = adjoint_nufft(readout_device * self.dcf, self.ktraj, norm="ortho")
                output[:,:,partition,:,:] = nufftResult
                del readout_device, nufftResult
            return torch.moveaxis(output, 0, -1)
    
    def __init__(self, reconstructionParameters, inputType:ReconstructionModuleIOType=ReconstructionModuleIOType.KSPACE, outputType:ReconstructionModuleIOType=ReconstructionModuleIOType.IMAGE, ktraj=None, dcf=None, numNearestNeighbors=3, collapseToTimeseries=False, retainSpirals=True, device=None):
        """
        Initialize the NUFFTModule.

        Args:
            reconstructionParameters (dict): Parameters specific to the reconstruction module.
            inputType (ReconstructionModuleIOType, optional): Input data type. Defaults to ReconstructionModuleIOType.KSPACE.
            outputType (ReconstructionModuleIOType, optional): Output data type. Defaults to ReconstructionModuleIOType.IMAGE.
            ktraj (torch.Tensor, optional): k-space trajectory. Defaults to None.
            dcf (torch.Tensor, optional): Density compensation factor. Defaults to None.
            numNearestNeighbors (int, optional): Number of nearest neighbors for NUFFT. Defaults to 3.
            device (torch.device, optional): Device for computation. Defaults to None.
        """
        ReconstructionModule.__init__(self, reconstructionParameters=reconstructionParameters, inputType=inputType, outputType=outputType) 
        self.numNearestNeighbors = numNearestNeighbors 
        if(device is None):
            self.device = reconstructionParameters.defaultDevice
        else:
            self.device = device
        self.matrixX = reconstructionParameters.outputMatrixSize[0]
        self.matrixY = reconstructionParameters.outputMatrixSize[1]
        self.ktraj = ktraj.to(self.device)
        self.dcf = dcf.to(self.device)
        self.sqrt_dcf = torch.sqrt(self.dcf)
        self.collapseToTimeseries = collapseToTimeseries
        self.retainSpirals = retainSpirals

    def __dict__(self):
        """
        Convert module attributes to a dictionary.

        Returns:
            dict: Dictionary containing module attributes.
        """
        moduleDict  = {
            "type": str(self.__class__.__name__),
            "inputType": str(self.inputType.name),
            "outputType": str(self.outputType.name),
            "ktraj": self.ktraj.tolist(),
            "dcf": self.dcf.tolist(),
            "numNearestNeighbors": self.numNearestNeighbors,
            "collapseToTimeseries": self.collapseToTimeseries,
            "retainSpirals": self.retainSpirals,
            "device": self.device.type
        }
        return moduleDict

    def ProcessKspaceToImage(self, inputData):
        """
        Process k-space data to image data using NUFFT.

        Args:
            inputData (KspaceData): Input k-space data.

        Returns:
            ImageData: Processed image data.
        """
        with torch.no_grad():
            if(self.retainSpirals):
                outputData = self.PerformAdjointNUFFTsImagewise(inputData)
            else:
                outputData = self.PerformAdjointNUFFTs(inputData)
            return ImageData(outputData)

    @staticmethod
    def FromJson(jsonInput, reconstructionParameters, inputType, outputType):  
        """
        Create an instance of NUFFTModule from JSON input.

        Args:
            jsonInput (dict): JSON input containing module details.
            reconstructionParameters (dict): Parameters specific to the reconstruction module.
            inputType (ReconstructionModuleIOType): Input data type.
            outputType (ReconstructionModuleIOType): Output data type.

        Returns:
            NUFFTModule: Instance of NUFFTModule.
        """
        ktrajJson = jsonInput.get("ktraj")
        ktraj = torch.tensor(np.array(ktrajJson))
        dcfJson = jsonInput.get("dcf")
        dcf = torch.tensor(np.array(dcfJson))
        numNearestNeighbors = jsonInput.get("numNearestNeighbors")
        collapseToTimeseries = jsonInput.get("collapseToTimeseries")
        retainSpirals = jsonInput.get("retainSpirals")
        device = jsonInput.get("device")
        if ktrajJson != None and dcfJson != None and numNearestNeighbors != None and device != None:
            return NUFFTModule(reconstructionParameters, inputType, outputType, ktraj, dcf, numNearestNeighbors, collapseToTimeseries, retainSpirals, torch.device(device))
        else:
            print("NUFFTModule requires ktraj, dcf, numNearestNeighbors, and device")