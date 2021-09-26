import sys

def pub_style():
    from ROOT import gROOT, gStyle, TGaxis
    gROOT.SetStyle('Pub')
    gStyle.SetOptStat(0000)
    gStyle.SetCanvasBorderMode(0)
    gStyle.SetCanvasBorderSize(0)
    gStyle.SetPadTickX(1)
    gStyle.SetPadTickY(1)
    gStyle.SetPadBorderMode(0)
    gStyle.SetPadBorderSize(0)
    gStyle.SetPadLeftMargin(0.17)
    gStyle.SetPadBottomMargin(0.17)
    gStyle.SetLabelSize(0.06, 'xyz')
    gStyle.SetLabelFont(42, 'xyz')
    gStyle.SetLabelOffset(0.01, 'xyz')
    gStyle.SetTitleSize(0.07, 'xyz')
    gStyle.SetTitleFont(42, 'xyz')
    gStyle.SetTitleOffset(1.15, 'xyz')
    gStyle.SetHistLineColor(1)
    gStyle.SetHistLineWidth(2)
    gStyle.SetLegendBorderSize(0)
    gStyle.SetLegendFillColor(0)
    gStyle.SetLegendFont(42)
    gStyle.SetLegendTextSize(0.06)
    gStyle.SetFillStyle(0000)
    gStyle.SetMarkerStyle(0)
    gStyle.SetNdivisions(505, 'xyz')
    gStyle.SetTextSize(0.06)
    gStyle.SetTextFont(42)
    TGaxis.SetMaxDigits(2)

def set_pavetext(pt):
    pt.SetFillStyle(0)
    pt.SetBorderSize(0)
    pt.SetTextAlign(10)
    pt.SetTextSize(0.06)

def set_hist_style(h, xtitle, ytitle, color, fill_style, dot_or_line = ''):
    h.GetXaxis().SetNdivisions(509)
    h.GetYaxis().SetNdivisions(504)
    h.SetLineWidth(2)
    h.SetStats(0)
    h.GetXaxis().SetTitleSize(0.06)
    h.GetXaxis().SetTitleOffset(1.1)
    h.GetXaxis().SetLabelOffset(0.01)
    h.GetYaxis().SetTitleSize(0.06)
    h.GetYaxis().SetTitleOffset(1.2)
    h.GetYaxis().SetLabelOffset(0.01)
    h.GetXaxis().SetTitle(xtitle)
    h.GetXaxis().CenterTitle()
    h.GetYaxis().SetTitle(ytitle)
    h.GetYaxis().CenterTitle()
    h.SetLineColor(color)
    if not fill_style == -1:
        h.SetFillStyle(fill_style) 
        h.SetFillColor(color)

def set_canvas_style(can):
    can.SetFillColor(0)
    can.SetLeftMargin(0.15)
    can.SetRightMargin(0.15)
    can.SetTopMargin(0.1)
    can.SetBottomMargin(0.15)

def set_legend(leg, hists, texts):
    if len(hists) != len(texts):
        print('length of hist must be equal to length of texts, please check!')
        sys.exit()
    for hist, text in zip(hists, texts): leg.AddEntry(hist, text)
    leg.SetBorderSize(0)
    leg.SetFillColor(0)
    leg.SetLineColor(0)
    leg.SetTextSize(0.06)

def set_arrow(arr, color):
    arr.SetLineWidth(4)
    arr.SetLineColor(color)
    arr.SetFillColor(color)
