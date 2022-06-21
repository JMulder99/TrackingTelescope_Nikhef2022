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

# file name of the input root file 
infile = ROOT.TFile('histograms.root')

# don't forget this number    HERE below
# ------------------------------------------------------------------------------
canvas_1 = ROOT.TCanvas("canvas_1", "Canvas title here", 1200,1200)
#		Below should be the path in the root file of the hist you want
hist = infile.Get('Tracking4D/AlpideSensor1/local_residuals/LocalResidualsX') 

hist.SetStats(0) 					# removes the statistics box
hist.SetLineWidth(2)					# width of the line
hist.SetLineColor(1)					# color of the line
hist.SetFillColor(0)					# color of area under the histogram	
hist.SetTitle("Insert a custom title here")		# title of histogram
hist.SetXTitle("Insert x label here")			# x label
hist.SetYTitle("Insert y label here")			# y label

hist.Draw()
canvas_1.SaveAs("example_plot_title.png")		# name of the output image
# ------------------------------------------------------------------------------

