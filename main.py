import ROOT

from config import *


def setup():
	signal_file = ROOT.TFile(SIGNALPROCFNM)
	bg_file = ROOT.TFile(BGPROCFNM)

	signal_tree = signal_file.Get(TREENM)
	bg_tree = bg_file.Get(TREENM)


	fout = ROOT.TFile("test.root","RECREATE")


	factory = ROOT.TMVA.Factory("TMVAClassification", fout,
                            ":".join([    "!V",
                                          "!Silent",
                                          "Color",
                                          "DrawProgressBar",
                                          "Transformations=I;D;P;G,D",
                                          "AnalysisType=Classification"]
                                     ))
	dataloader = ROOT.TMVA.DataLoader("dataset")

	dataloader.AddVariable("mJJ","F")
	dataloader.AddVariable("deltaYJJ","F")
	dataloader.AddVariable("metPt","F")
	dataloader.AddVariable("ptBalance","F")
	dataloader.AddVariable("subleadJetEta","F")
	dataloader.AddVariable("leadJetPt","F")
	dataloader.AddVariable("photonEta","F")
	dataloader.AddVariable("ptBalanceRed","F")
	dataloader.AddVariable("nJets","F")
	dataloader.AddVariable("sinDeltaPhiJJOver2","F")
	dataloader.AddVariable("deltaYJPh","F")
	# dataloader.AddVariable("nLeptons", "F")

	cut = make_selections()

	dataloader.AddSignalTree(signal_tree)
	dataloader.AddBackgroundTree(bg_tree)
	dataloader.PrepareTrainingAndTestTree(cut, 
                                   	":".join(["nTrain_Signal=0",
                                             "nTrain_Background=0",
                                             "SplitMode=Random",
                                             "NormMode=NumEvents",
                                             "!V"
                                             ]))


	method = factory.BookMethod(dataloader, ROOT.TMVA.Types.kBDT, "BDTadaboost",
	                            ":".join([ "!H",
	                                       "!V",
	                                       "NTrees=850",
	                                       "nEventsMin=150",
	                                       "MaxDepth=3",
	                                       "BoostType=AdaBoost",
	                                       "AdaBoostBeta=0.5",
	                                       "SeparationType=GiniIndex",
	                                       "nCuts=20",
	                                       "PruneMethod=NoPruning",
	                                       ]))

	method = factory.BookMethod(dataloader, ROOT.TMVA.Types.kBDT, "BDTgrad",
                            ":".join([ "!H",
                                       "!V",
                                       "NTrees=850",
                                       "nEventsMin=150",
                                       "MaxDepth=3",
                                       "BoostType=Grad",
                                       "AdaBoostBeta=0.5",
                                       "SeparationType=GiniIndex",
                                       "nCuts=20",
                                       "PruneMethod=NoPruning",
                                       ]))

	factory.TrainAllMethods()
	factory.TestAllMethods()
	factory.EvaluateAllMethods()
	fout.Close()

	ROOT.TMVA.TMVAGui("test.root")
	ROOT.gApplication.Run()


def make_selections():
	cut = ROOT.TCut("(mJJ > 300)&&(phCentrality < 0.6)&&(nJets > 1)&&(nLeptons == 0)")
	return cut


if __name__ == "__main__":
	ROOT.TMVA.Tools.Instance()

	setup()
