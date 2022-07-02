# Simple tool to make nice plots from corry output root files
# The code between lines produces and saves 1 png image for 1 histogram from the root file
# Feel free to add options to it if you have any good ideas

# How to use:
# Make sure this script is placed in the same folder as the root file you want to analyse (or change the "infile" path to point to the place where the root file is)
# Copy the example between the lines, paste them below the example, change the number of the canvas object (to prevent memory issues when doing many histograms) and adjust the numbers/values to what you want
# To have the default value of anything, comment out the relevant line of code (for example, commenting the "hist.SetXTitle()" line will make it use the default x label) 
# when only wanting to do one histogram (at the time) you can of course also just change the example
# The output plots can be found in the same directory as this python script is placed in

# The ROOT module is needed, so make sure to source it before trying to use the code
import ROOT
import math


def set_size(width, fraction=1, subplots=(1, 1)):
    """Set figure dimensions to avoid scaling in LaTeX.
    Parameters
    ----------
    width: float or string
            Document width in points, or string of predined document type
    fraction: float, optional
            Fraction of the width which you wish the figure to occupy
    subplots: array-like, optional
            The number of rows and columns of subplots.
    Returns
    -------
    fig_dim: tuple
            Dimensions of figure in inches
    """
    if width == 'thesis':
        width_pt = int(442 * 1.33)
    elif width == 'beamer':
        width_pt = 307.28987
    else:
        width_pt = width

    # Width of figure (in pts)
    fig_width_pt = width_pt * fraction
    # Convert from pt to inches
    #inches_per_pt = 1 / 72.27

    # Golden ratio to set aesthetic figure height
    # https://disq.us/p/2940ij3
    golden_ratio = (5**.5 - 1) / 2

    # Figure width in inches
    fig_width_in = fig_width_pt
    # Figure height in inches
    fig_height_in = int(fig_width_in * golden_ratio)

    return (fig_width_in, fig_height_in)


width, height = set_size("thesis")
print(width,height)
# file name of the input root file 
infile = ROOT.TFile('data_final.root')
simfile = ROOT.TFile('output_corry_cosmic_good_1M.root')

# don't forget this number    HERE below
# ------------------------------------------------------------------------------
canvas_1 = ROOT.TCanvas("canvas_1", "Canvas title here", 1024,512)
#		Below should be the path in the root file of the hist you want
hist = infile.Get('EventLoaderEUDAQ2/ALPIDE_0/hitmap') 

hist.SetStats(1) 					# removes the statistics box
hist.SetLineWidth(2)					# width of the line
hist.SetLineColor(1)					# color of the line
hist.SetFillColor(0)					# color of area under the histogram	
hist.SetTitle("Pixel hitmap alpide 0")			# title of histogram
hist.SetXTitle("row")					# x label
hist.SetYTitle("column")				# y label

ROOT.gStyle.SetPalette(56)
hist.Draw("colz")
hist.SetTitleSize(0.07,axis="X")
hist.SetTitleSize(0.07,axis="Y")
canvas_1.SetRightMargin(0.09);
canvas_1.SetLeftMargin(0.15);
canvas_1.SetBottomMargin(0.15);
canvas_1.SaveAs("hitmap_0.pdf")				# name of the output image

# ------------------------------------------------------------------------------
canvas_2 = ROOT.TCanvas("canvas_2", "Canvas title here", 1024,512)
#		Below should be the path in the root file of the hist you want
hist = infile.Get('EventLoaderEUDAQ2/ALPIDE_1/hitmap') 

hist.SetStats(1) 					# removes the statistics box
hist.SetLineWidth(2)					# width of the line
hist.SetLineColor(1)					# color of the line
hist.SetFillColor(0)					# color of area under the histogram	
hist.SetTitle("Pixel hitmap alpide 1")			# title of histogram
hist.SetXTitle("row")					# x label
hist.SetYTitle("column")				# y label

ROOT.gStyle.SetPalette(56)
hist.Draw("colz")
hist.SetTitleSize(0.07,axis="X")
hist.SetTitleSize(0.07,axis="Y")
canvas_2.SetRightMargin(0.09);
canvas_2.SetLeftMargin(0.15);
canvas_2.SetBottomMargin(0.15);
canvas_2.SaveAs("hitmap_1.pdf")				# name of the output image
# --------------------------------

canvas_3 = ROOT.TCanvas("canvas_3", "Canvas title here", width, height)
#		Below should be the path in the root file of the hist you want
hist = infile.Get('Clustering4D/ALPIDE_0/clusterSize') 

hist.SetStats(1) 					# removes the statistics box
hist.SetLineWidth(2)					# width of the line
hist.SetLineColor(1)					# color of the line
hist.SetFillColor(0)					# color of area under the histogram	
hist.SetTitle("Cluster size alpide 0")			# title of histogram
hist.SetXTitle("cluster size")				# x label
hist.SetYTitle("events")				# y label
hist.GetXaxis().SetRangeUser(0, 10)
#ROOT.gStyle.SetPalette(56)
hist.Draw()
hist.SetTitleSize(0.07,axis="X")
hist.SetTitleSize(0.07,axis="Y")
canvas_3.SetRightMargin(0.09);
canvas_3.SetLeftMargin(0.15);
canvas_3.SetBottomMargin(0.15);
canvas_3.SaveAs("cluster_size_0.pdf")				# name of the output image
# --------------------------------

canvas_4 = ROOT.TCanvas("canvas_4", "Canvas title here", width, height)
#		Below should be the path in the root file of the hist you want
hist = infile.Get('Clustering4D/ALPIDE_1/clusterSize') 

hist.SetStats(1) 					# removes the statistics box
hist.SetLineWidth(2)					# width of the line
hist.SetLineColor(1)					# color of the line
hist.SetFillColor(0)					# color of area under the histogram	
hist.SetTitle("Cluster size alpide 1")			# title of histogram
hist.SetXTitle("cluster size")				# x label
hist.SetYTitle("events")				# y label
hist.GetXaxis().SetRangeUser(0, 10)
#ROOT.gStyle.SetPalette(56)
hist.Draw()
hist.SetTitleSize(0.07,axis="X")
hist.SetTitleSize(0.07,axis="Y")
canvas_4.SetRightMargin(0.09);
canvas_4.SetLeftMargin(0.15);
canvas_4.SetBottomMargin(0.15);
canvas_4.SaveAs("cluster_size_1.pdf")				# name of the output image
# --------------------------------

canvas_5 = ROOT.TCanvas("canvas_5", "Canvas title here", width, height)
#		Below should be the path in the root file of the hist you want
hist = infile.Get('Tracking4D/tracksPerEvent') 

hist.SetStats(0) 					# removes the statistics box
hist.SetLineWidth(2)					# width of the line
hist.SetLineColor(1)					# color of the line
hist.SetFillColor(0)					# color of area under the histogram	
hist.SetTitle("Tracks per event")			# title of histogram
hist.SetXTitle("number of tracks")				# x label
hist.SetYTitle("events")
hist.GetXaxis().SetRangeUser(0, 5)
hist.SetTitleSize(0.07,axis="X")
hist.SetTitleSize(0.07,axis="Y")			# y label
canvas_5.SetRightMargin(0.09);
canvas_5.SetLeftMargin(0.15);
canvas_5.SetBottomMargin(0.15);

#ROOT.gStyle.SetPalette(56)
hist.Draw()
canvas_5.SaveAs("track_multiplicity.pdf")				# name of the output image
# --------------------------------

canvas_6 = ROOT.TCanvas("canvas_6", "Canvas title here", width, height)
#		Below should be the path in the root file of the hist you want
legend = ROOT.TLegend(0.9,0.9)

hist = infile.Get('AnalysisParticleFlux/azimuth_flux') 
hist2 = simfile.Get('AnalysisParticleFlux/azimuth_flux') 

hist3 = infile.Get('AnalysisParticleFlux/azimuth')
hist4 = simfile.Get('AnalysisParticleFlux/azimuth')
scale = hist.GetBinContent(1)/hist3.GetBinContent(1)

hist.SetStats(0) 					# removes the statistics box
hist.SetLineWidth(2)					# width of the line
hist.SetLineColor(3)					# color of the line
hist.SetFillColor(0)
hist.SetMarkerStyle(21)
hist.SetMarkerColor(3)
#hist.SetMarkerSize()					# color of area under the histogram	
hist.SetTitle("Azimuth flux distribution")			# title of histogram
hist.SetXTitle("#phi [#circ]")			# x label
hist.SetYTitle("normalized flux / sr")
for i in range(hist.GetNbinsX()):
	error = math.sqrt(hist3.GetBinContent(i+1))*scale
	hist.SetBinError(i+1,error)
hist.Scale(1/hist.Integral(),"width")
hist.SetTitleSize(0.07,axis="X")
hist.SetTitleSize(0.07,axis="Y")
legend.AddEntry(hist,"Data","l")


hist2.SetStats(0) 					# removes the statistics box
hist2.SetLineWidth(2)					# width of the line
hist2.SetLineColor(2)					# color of the line
hist2.SetFillColor(0)
hist2.SetMarkerStyle(20)
hist2.SetMarkerColor(2)
#hist2.SetMarkerSize()					# color of area under the histogram	
hist2.SetTitle("Azimuth flux distribution")			# title of histogram
hist2.SetXTitle("#phi [#circ]")			# x label
hist2.SetYTitle("normalized flux / sr")
#hist2.Sumw2()
for i in range(hist2.GetNbinsX()):
	error = math.sqrt(hist4.GetBinContent(i+1))*scale
	hist2.SetBinError(i+1,error)
hist2.Scale(1/hist2.Integral(),"width");
hist2.SetTitleSize(0.07,axis="X")
hist2.SetTitleSize(0.07,axis="Y")				# y label
legend.AddEntry(hist2,"Simulation","l")

canvas_6.SetRightMargin(0.09);
canvas_6.SetLeftMargin(0.15);
canvas_6.SetBottomMargin(0.15);

#ROOT.gStyle.SetPalette(56)
hist.Draw()
hist2.Draw("same")
legend.Draw()
canvas_6.SaveAs("azimuth_flux_change.pdf")
	
# --------------------------------
canvas_7 = ROOT.TCanvas("canvas_7", "Canvas title here", width, height)
#		Below should be the path in the root file of the hist you want
legend = ROOT.TLegend(0.9,0.9)

hist = infile.Get('AnalysisParticleFlux/zenith_flux') 
hist2 = simfile.Get('AnalysisParticleFlux/zenith_flux') 

hist3 = infile.Get('AnalysisParticleFlux/zenith')
hist4 = simfile.Get('AnalysisParticleFlux/zenith')
scale2 = hist.GetBinContent(1)/hist3.GetBinContent(1)

hist.SetStats(0) 					# removes the statistics box
hist.SetLineWidth(2)					# width of the line
hist.SetLineColor(3)					# color of the line
hist.SetFillColor(0)
hist.SetMarkerStyle(21)
hist.SetMarkerColor(3)					# color of area under the histogram	
hist.SetTitle("Zenith flux distribution")		# title of histogram
hist.SetXTitle("#theta [#circ]")			# x label
hist.SetYTitle("normalized flux / sr")
for i in range(hist.GetNbinsX()):
	error = math.sqrt(hist3.GetBinContent(i+1))*scale2
	hist.SetBinError(i+1,error)	
hist.Scale(1/hist.Integral(), "width");
hist.SetTitleSize(0.07,axis="X")
hist.SetTitleSize(0.07,axis="Y")
legend.AddEntry(hist,"Data","l")


hist2.SetStats(0) 					# removes the statistics box
hist2.SetLineWidth(2)					# width of the line
hist2.SetLineColor(2)					# color of the line
hist2.SetFillColor(0)
hist2.SetMarkerStyle(20)
hist2.SetMarkerColor(2)				# color of area under the histogram	
hist2.SetTitle("Zenith flux distribution")			# title of histogram
hist2.SetXTitle("#phi [#circ]")			# x label
hist2.SetYTitle("normalized flux / sr")
for i in range(hist2.GetNbinsX()):
	error = math.sqrt(hist4.GetBinContent(i+1))*scale2
	hist2.SetBinError(i+1,error)
hist2.Scale(1/hist2.Integral(), "width");	
hist2.SetTitleSize(0.07,axis="X")
hist2.SetTitleSize(0.07,axis="Y")		# y label
legend.AddEntry(hist2,"Simulation","l")

canvas_7.SetRightMargin(0.09);
canvas_7.SetLeftMargin(0.15);
canvas_7.SetBottomMargin(0.15);

#ROOT.gStyle.SetPalette(56)
hist.Draw()
hist2.Draw("same")
legend.Draw()
canvas_7.SaveAs("zenith_flux_change.pdf")	

# --------------------------------
canvas_8 = ROOT.TCanvas("canvas_8", "Canvas title here", width, height)
#		Below should be the path in the root file of the hist you want
hist = infile.Get('Tracking4D/ALPIDE_0/local_residuals/LocalResidualsX') 

hist.SetStats(0) 					# removes the statistics box
hist.SetLineWidth(2)					# width of the line
hist.SetLineColor(1)					# color of the line
hist.SetFillColor(0)					# color of area under the histogram	
hist.SetTitle("Local residuals X alpide 0")			# title of histogram
hist.SetXTitle("x - x_{track} [mm]")				# x label
hist.SetYTitle("events")
canvas_8.SetRightMargin(0.09);
canvas_8.SetLeftMargin(0.15);
canvas_8.SetBottomMargin(0.15);				# y label
#hist.GetXaxis().SetRangeUser(0, 10)
#ROOT.gStyle.SetPalette(56)
hist.Draw()
hist.SetTitleSize(0.07,axis="X")
hist.SetTitleSize(0.07,axis="Y")
canvas_8.SaveAs("residual_x_0.pdf")				# name of the output image
# --------------------------------

canvas_9 = ROOT.TCanvas("canvas_9", "Canvas title here", width, height)
#		Below should be the path in the root file of the hist you want
hist = infile.Get('Tracking4D/ALPIDE_0/local_residuals/LocalResidualsY') 

hist.SetStats(0) 					# removes the statistics box
hist.SetLineWidth(2)					# width of the line
hist.SetLineColor(1)					# color of the line
hist.SetFillColor(0)					# color of area under the histogram	
hist.SetTitle("Local residuals Y alpide 0")			# title of histogram
hist.SetXTitle("y - y_{track} [mm]")				# x label
hist.SetYTitle("events")				# y label
#hist.GetXaxis().SetRangeUser(0, 10)
#ROOT.gStyle.SetPalette(56)
hist.Draw()
hist.SetTitleSize(0.07,axis="X")
hist.SetTitleSize(0.07,axis="Y")
canvas_9.SetRightMargin(0.09);
canvas_9.SetLeftMargin(0.15);
canvas_9.SetBottomMargin(0.15);
canvas_9.SaveAs("residual_y_0.pdf")				# name of the output image
# --------------------------------

