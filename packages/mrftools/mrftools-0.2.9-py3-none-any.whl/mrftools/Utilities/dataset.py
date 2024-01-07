import numpy as np
import ismrmrd

class FAMode(Enum):
    RequestedFlipAngle = 1
    ReportedFlipAngle = 2

class mrftoolsDataset:
    def __init__(self):
        self.sourceFilename = None
        self.faMode = None
        self.numSpirals = None
        self.numMeasuredPartitions = None
        self.numUndersampledPartitions = None
        self.centerMeasuredPartition = None
        self.numSets = None
        self.numCoils = None
        self.matrixSize = None
        self.FOV = None
        self.ismrmrdHeader = None
        self.undersamplingRatio = None
        self.numTimepoints = None
        self.TRs = None
        self.TEs = None
        self.FAs = None
        self.PHs = None
        self.IDs = None
        self.rawData = None
        self.acqHeaders = None
        self.discardPre = None
        self.discardPost = None
        self.numReadoutPoints = None
        self.usePartialFourier = None
        self.partialFourierRatio = None
        self.sequence = None
        self.sequenceType = None
        self.sequenceHash = None

    def __str__(self):
        descriptionString = f""" 
        Source Filename: {self.sourceFilename} 
        Matrix Size: {self.matrixSize} ({self.numUndersampledPartitions} w/ {self.undersamplingRatio}x undersampling)
        Partial Fourier: {self.partialFourierRatio}
        FOV: {self.FOV}
        Timepoints: {self.numTimepoints} ({self.numSpirals} spirals x {self.numSets} sets)
        Coils: {self.numCoils}
        Raw Data Size: {np.shape(self.rawData)}
        Sequence:
            Hash: {self.sequenceHash}
            TRs: {np.min(self.TRs)}, {np.max(self.TRs)}
            TEs: {np.min(self.TEs)}, {np.max(self.TEs)}
            FAs: {np.min(self.FAs)}, {np.max(self.FAs)}
            PHs: {np.min(self.PHs)}, {np.max(self.PHs)}
            IDs: {np.min(self.IDs)}, {np.max(self.IDs)}
        """
        return descriptionString

    def PopulateIsmrmrdHeader(mdb):
        acqHeader = ismrmrd.Acquisition()
        acqHeader.position[0] = mdb.mdh.SliceData.SlicePos.Sag
        acqHeader.position[1] = mdb.mdh.SliceData.SlicePos.Cor
        acqHeader.position[2] = mdb.mdh.SliceData.SlicePos.Tra
        quat = mdb.mdh.SliceData.Quaternion
        a = quat[0]; b = quat[1]; c = quat[2]; d = quat[3]
        acqHeader.read_dir[0] = 1.0 - 2.0 * (b * b + c * c)
        acqHeader.phase_dir[0] = 2.0 * (a * b - c * d)
        acqHeader.slice_dir[0] = 2.0 * (a * c + b * d)
        acqHeader.read_dir[1] = 2.0 * (a * b + c * d)
        acqHeader.phase_dir[1] = 1.0 - 2.0 * (a * a + c * c)
        acqHeader.slice_dir[1] = 2.0 * (b * c - a * d)
        acqHeader.read_dir[2] = 2.0 * (a * c - b * d)
        acqHeader.phase_dir[2] = 2.0 * (b * c + a * d)
        acqHeader.slice_dir[2] = 1.0 - 2.0 * (a * a + b * b)
        return acqHeader
