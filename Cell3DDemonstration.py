#!/usr/bin/env python
# -*- coding: utf-8 -*-

import vtk
import open3d as o3d
import numpy as np
import numpy as np
import open3d as o3d
from vtkmodules.vtkIOImage import vtkPNGWriter
import os
import random
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkWindowToImageFilter
)

from enamlx.widgets.table_view import (
    TableView, TableViewRow, TableViewItem
)

def main():
    clases=['PLY##', 'CL##', 'PV##', 'PLW##', 'PLXW##', 'PLSB##', 'LDN##', 'SVB', 'VLG', 'BOX', 'VLT', 'ACH', 'MT', 'LPS', 'POLHT', 'MHE', 'MHT', 'JB', 'ANC', 'POLHY', 'GPO', 'PWT', 'MHS', 'CBT', 'MHCB', 'STDP', 'FH', 'VHCL', 'COT', 'VLW', 'MHD', 'SBS', 'SZ', 'SGW', 'IRS', 'SI', 'SSS', 'SNP', 'SP', 'TR', 'PLXW2##', 'PLA##', 'PLBK##', 'HV', 'TLS', 'PWL', 'TREC', 'TRED', 'KSK', 'POLEL', 'MRS', 'PRS', 'PGZ', 'BUSH']

    #path='/home/glugo/project/data/scenes/NW/objects/assets/'# ["VLG","ACH","CBT", "MHCB", "COT", "MHD", "VLT"]:
    path='/Users/millerma/Library/CloudStorage/OneDrive-Personal/Courses/MM 804/Project/VTK Visualization/MM804-Point-Cloud-Visualization/Dataset/assets/hydro.tel'
    #pcd = o3d.io.read_point_cloud("/home/glugo/project/data/scenes/MW/objects/assets/sto.san.water.misc/MHD/MHD156-MW.pcd")

    d=[]
    sourceObjects = list()
    sourceObjects2 = list()
    for root, dirs, filenames in os.walk(path):
        for clouds in filenames:
            d.append(root+'/'+clouds)
    for samples in d:
        #for clasesss in ["VLG","ACH","CBT", "MHCB", "COT", "MHD", "VLT"]: #["FH","LPS", 'SI','SSS', 'SNP', 'BUSH', 'PWL', 'POLHT', 'BOX']:
        for clasesss in ["MHE"]: #["FH","LPS", 'SI','SSS', 'SNP', 'BUSH', 'PWL', 'POLHT', 'BOX']:
            if clasesss in samples:
                print(clasesss)
                print('Processing')
                pcd = o3d.io.read_point_cloud(samples)
                p = np.asarray(pcd.points)
                points = vtk.vtkPoints()
                vertices = vtk.vtkCellArray()
                for i in range(len(p)):
                    point_id = points.InsertNextPoint(p[i])
                    vertices.InsertNextCell(1)
                    vertices.InsertCellPoint(point_id)   
                sourceObjects.append(vtk.vtkPolyData())
                sourceObjects[-1].SetPoints(points)
                sourceObjects[-1].SetVerts(vertices)
                sourceObjects2.append(clasesss)
                break
            break
    np.random.shuffle(sourceObjects)
    colors = vtk.vtkNamedColors()

    # Set the background color.
    colors.SetColor('BkgColor', [0, 0, 0, 255])
    renderers = list()
    mappers = list()
    actors = list()
    textmappers = list()
    textactors = list()

    # Create one text property for all.
    textProperty = vtk.vtkTextProperty()
    textProperty.SetFontSize(8)
    textProperty.SetJustificationToCentered()
    textProperty.SetColor(colors.GetColor3d('LightGoldenrodYellow'))

    backProperty = vtk.vtkProperty()
    backProperty.SetColor(colors.GetColor3d('Tomato'))

    # Create a source, renderer, mapper, and actor
    # for each object.
    for i in range(0, len(sourceObjects)):
        mappers.append(vtk.vtkPolyDataMapper())
        mappers[i].SetInputData(sourceObjects[i])

        actors.append(vtk.vtkActor())
        actors[i].SetMapper(mappers[i])
        actors[i].GetProperty().SetOpacity(0.8)
        actors[i].GetProperty().SetColor(colors.GetColor3d('DarkGrey'))
        actors[i].SetBackfaceProperty(backProperty)
        actors[i].GetProperty().SetPointSize(1.0)

        textmappers.append(vtk.vtkTextMapper())
        #textmappers[i].SetInput(sourceObjects[i].GetClassName())
        textmappers[i].SetInput(sourceObjects2[i])
        textmappers[i].SetTextProperty(textProperty)

        textactors.append(vtk.vtkActor2D())
        textactors[i].SetMapper(textmappers[i])
        textactors[i].SetPosition(120, 16)
        renderers.append(vtk.vtkRenderer())

    gridDimensions = 2

    # We need a renderer even if there is no actor.
    for i in range(len(sourceObjects), gridDimensions ** 2):
        renderers.append(vtk.vtkRenderer())

    renderWindow = vtk.vtkRenderWindow()
    renderWindow.SetWindowName('SourceObjectsDemo')
    rendererSize = 600
    renderWindow.SetSize(rendererSize * gridDimensions, rendererSize * gridDimensions)

    for row in range(0, gridDimensions):
        for col in range(0, gridDimensions):
            index = row * gridDimensions + col
            x0 = float(col) / gridDimensions
            y0 = float(gridDimensions - row - 1) / gridDimensions
            x1 = float(col + 1) / gridDimensions
            y1 = float(gridDimensions - row) / gridDimensions
            renderWindow.AddRenderer(renderers[index])
            renderers[index].SetViewport(x0, y0, x1, y1)

            if index > (len(sourceObjects) - 1):
                continue

            renderers[index].AddActor(actors[index])
            renderers[index].AddActor(textactors[index])
            renderers[index].SetBackground(colors.GetColor3d('White'))
            renderers[index].ResetCamera()
            # renderers[index].GetActiveCamera().Azimuth(-180)# FLAT 
            # renderers[index].GetActiveCamera().Elevation(-00) # FLAT
            # renderers[index].GetActiveCamera().Zoom(1.2)# FLAT
            renderers[index].GetActiveCamera().Azimuth(180) 
            renderers[index].GetActiveCamera().Elevation(100)
            renderers[index].GetActiveCamera().Zoom(1.2)
            renderers[index].ResetCameraClippingRange()
    


    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(renderWindow)
    interactor.Start()

        # screenshot code:
    # w2if = vtkWindowToImageFilter()
    # w2if.SetInput(renderWindow)
    # w2if.SetInputBufferTypeToRGB()
    # w2if.ReadFrontBufferOff()
    # w2if.Update()
    #writer = vtkPNGWriter()
    #writer.SetFileName('TestScreenshot.png')
    #writer.SetInputConnection(w2if.GetOutputPort())
    #writer.Write()


if __name__ == '__main__':
    main()