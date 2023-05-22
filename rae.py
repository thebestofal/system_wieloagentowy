class GoodWill:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0


class Agent:
    def __init__(self):
        self.isStrategicAgent = False
        self.Number = 0
        self.wasRecipient = False
        self.serviceAvailability = 0
        self.serviceReception = 0
        self.suppliersNumbers = []
        self.suppliersAmount = []
        self.HonestSuppliersCount = 0
        self.StrategicSuppliersCount = 0
        self.AvailabilitySupplierSum = 0
        self.trust = 0

    def copy_values(self, agent):
        self.isStrategicAgent = agent.isStrategicAgent
        self.Number = agent.Number
        self.wasRecipient = agent.wasRecipient
        self.serviceAvailability = agent.serviceAvailability
        self.serviceReception = agent.serviceReception
        self.suppliersNumbers = agent.suppliersNumbers
        self.suppliersAmount = agent.suppliersAmount
        self.HonestSuppliersCount = agent.HonestSuppliersCount
        self.StrategicSuppliersCount = agent.StrategicSuppliersCount
        self.AvailabilitySupplierSum = agent.AvailabilitySupplierSum


class Cycle:
    def __init__(self, round_number=0):
        self.mAgents = []
        self.Round = round_number
        self.StrategicTrajectory = 0
        self.HonestTrajectory = 0
        self.NetOutflow = 0

    def set_agents(self, agents):
        self.mAgents = agents

    def get_agents(self):
        return self.mAgents


class AgentsFactory:
    def __init__(self, trustLevel=0, strategic=0, logger=None):
        self.mBeginingTrustLevel = trustLevel
        self.mStrategicCount = strategic
        self.mLogger = logger

    def Create(self):
        return Agent(self.mBeginingTrustLevel, self.mStrategicCount, self.mLogger)

    def Create(self, Number):
        return Agent(self.mBeginingTrustLevel, self.mStrategicCount, self.mLogger, Number)


class CycleFactory:
    def __init__(self, logger=None):
        self.mLogger = logger

    def Create(self, Number):
        return Cycle(Number)


class ReportedService:
    def __int__(self):
        self.recipient_number = 0
        self.reported_number = 0.0


class MonteCarlo:
    def __init__(self):
        self.mCurrentCycle = Cycle()
        self.mCurrentRecipient = Agent()
        self.mCurrentSupplier = Agent()
        self.mInteractionIndex = 0
        self.mCycleTempHonestTrajectory = 0
        self.mCycleTempStrategicTrajectory = 0
        self.mCycleTempOutflow = 0
        self.mAgents = []
        self.mCycles = []
        self.mSuppliers = []
        self.mReportedSumForInteraction = {}
        self.mReportedAverage = {}
        self.mIsRunning = False
        self.mIsInitializing = False
        self.mAgentsFactory = AgentsFactory()
        self.mCycleFactory = CycleFactory()
        self.mGeneratingReportDone = False

        self.mAgentsFactory = AgentsFactory()
        self.mCycleFactory = CycleFactory()
        self.mGeneratingReportDone = False
        self.cyclesAmount = 3
        self.agentsAmount = 1000
        self.strategicAgentsAmount = 50
        self.kMin = 50
        self.kMax = 150
        self.expoA = 0.5
        self.expoG = 0.5
        self.Done = False
        self.beginTrustMeasure = 1
        self.boostMode = True
        self.SAgentTrajectoryAvg = []
        self.HAgentTrajectoryAvg = []
        self.NettoOutflow = []
        self.FinalTrust = []
        self.CycleNumbersForPlot = []
        self.goodWill = GoodWill()

    def SetServiceAvailiabilityForSupplier(self):
        pass

    def SetServiceReceptionForRecipient(self):
        pass

    def Interact(self):
        pass

    def Run(self):
        pass

    def Initialize(self):
        pass

    def LogInteraction(self):
        pass

    def MoveToNextInteraction(self):
        pass

    def MoveToNextCycle(self):
        pass

    def MoveToNextRecipient(self):
        pass

    def UpdateAgents(self):
        pass

    def SetSuppliersAmountForRecipient(self):
        pass

    def CreateAgent(self):
        pass

    def UpdateInteraction(self):
        pass

    def ReportAgents(self):
        pass

    def ApplyNewTrustLevels(self):
        pass

    def PreserveCycle(self):
        pass

    def CalculateRecipientTresholdValue(self):
        pass

    def CalculateSupplierTresholdValue(self):
        pass

    def CalculateHonestPolicy(self, trustLevel, goodWill):
        pass

    def CalculateHonestRecipient(self, gij, pij, trustLevel, goodWill):
        pass

    def Start(self):
        pass

    def Update(self):
        pass

    def CurrentRecipientNumberInCycle(self):
        return self.mCurrentRecipient.Number + 1

    def CurrentCycleNumber(self):
        return self.mCurrentCycle.Round

    def IsWorking(self):
        return self.mIsRunning or self.mIsInitializing

    def GenerateReport(self):
        pass

    def GetTrustLevels(self):
        return []

