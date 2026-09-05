# Digitised figure data

Empty on purpose. Nothing here yet.

This directory is for values read off published figures where no numeric deposit
exists. `docs/06` identifies the candidates and ranks them; the two that would
most change what this project can fit are DRUSANO2018 (PMC6105790, figures 1 and
3, seven arms, n = 1 per arm) and BROWN2015 (PMC4631805, figure 5A and 5B).

Two rules apply to anything placed here.

First, a digitised series is a measurement of a figure, not of an experiment. It
carries the error of the person reading the axis on top of the error of the assay,
and that has to be reported rather than absorbed. Store the pixel coordinates and
the axis calibration alongside the converted values so a reader can check the
conversion, and record who digitised it and with what tool.

Second, digitisation makes a derivative work. Check `data/raw/SOURCES.json` for
the source's licence first. Several papers in this corpus are free to read but
not free to redistribute, and at least one is CC BY-NC-ND, whose no-derivatives
clause blocks a digitised table from being released without written permission.
Reading the figure for analysis is fine; publishing the numbers may not be.
