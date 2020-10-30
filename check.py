from ROOT import TMVA, gApplication
import ROOT


ROOT.TMVA.TMVAGui("test.root")
ROOT.gApplication.Run()