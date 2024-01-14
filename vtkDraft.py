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


def vtkPCDLoader(path, model_Num):
    clases=['PLY##', 'CL##', 'PV##', 'PLW##', 'PLXW##', 'PLSB##', 'LDN##', 'SVB', 'VLG', 'BOX', 'VLT', 'ACH', 'MT', 'LPS', 'POLHT', 'MHE', 'MHT', 'JB', 'ANC', 'POLHY', 'GPO', 'PWT', 'MHS', 'CBT', 'MHCB', 'STDP', 'FH', 'VHCL', 'COT', 'VLW', 'MHD', 'SBS', 'SZ', 'SGW', 'IRS', 'SI', 'SSS', 'SNP', 'SP', 'TR', 'PLXW2##', 'PLA##', 'PLBK##', 'HV', 'TLS', 'PWL', 'TREC', 'TRED', 'KSK', 'POLEL', 'MRS', 'PRS', 'PGZ', 'BUSH']

    #path='/home/glugo/project/data/scenes/NW/objects/assets/'# ["VLG","ACH","CBT", "MHCB", "COT", "MHD", "VLT"]:
    
    #pcd = o3d.io.read_point_cloud("/home/glugo/project/data/scenes/MW/objects/assets/sto.san.water.misc/MHD/MHD156-MW.pcd")

    d=[]
    clouds_object = []
    sourceObjects = list()
    sourceObjects2 = list()
    for root, dirs, filenames in os.walk(path):
        for clouds in filenames:
            d.append(root+'/'+clouds)
            clouds_object.append(clouds)
    new_path = ""   
    for samples in d:
        #for clasesss in ["VLG","ACH","CBT", "MHCB", "COT", "MHD", "VLT"]: #["FH","LPS", 'SI','SSS', 'SNP', 'BUSH', 'PWL', 'POLHT', 'BOX']:
        for clasesss in ["MHE"]: #["FH","LPS", 'SI','SSS', 'SNP', 'BUSH', 'PWL', 'POLHT', 'BOX']:
            if clasesss in samples:
                index = samples.find("MHE")
                if index != -1:
                    # Slice the string from the "MHE" index to the end of the path
                    new_path = samples[index:]
                else:
                    # "MHE" is not in the path, so keep the original path
                    new_path = samples

                print (new_path)
                
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

    numOfFiles = len(sourceObjects)

    windowNum = 3

    # np.random.shuffle(sourceObjects)
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

    targetObjects = sourceObjects[model_Num]
    targetObjects2 = sourceObjects2[model_Num]

    def SelectPolygons(widget, event_string):
        boxRep.GetPlanes(planes)
        selectActor.VisibilityOn()

    # Create a source, renderer, mapper, and actor
    # for each object.
    for i in range(0, windowNum):
        mappers.append(vtk.vtkPolyDataMapper())
        mappers[i].SetInputData(targetObjects)

        actors.append(vtk.vtkActor())
        actors[i].SetMapper(mappers[i])
        actors[i].GetProperty().SetOpacity(0.8)
        actors[i].GetProperty().SetColor(colors.GetColor3d('DarkGrey'))
        actors[i].SetBackfaceProperty(backProperty)
        actors[i].GetProperty().SetPointSize(1.0)      

        # # Bounding Box
        # planes = vtk.vtkPlanes()
        # clipper = vtk.vtkClipPolyData()
        # clipper.SetClipFunction(planes)
        # clipper.InsideOutOn()
        # selectMapper = vtk.vtkPolyDataMapper()
        # selectMapper.SetInputConnection(clipper.GetOutputPort())
        # selectActor = vtk.vtkLODActor()
        # selectActor.SetMapper(selectMapper)
        # selectActor.GetProperty().SetColor(0, 1, 0)
        # selectActor.VisibilityOff()
        # selectActor.SetScale(1.01, 1.01, 1.01)

        # boxRep = vtk.vtkBoxRepresentation()
        # boxRep.SetPlaceFactor(0.75)
        # # boxRep.PlaceWidget(sphere.GetOutput().GetBounds())
        # boxWidget = vtk.vtkBoxWidget2()
        # # boxWidget.SetInteractor(iRen)
        # boxWidget.SetRepresentation(boxRep)
        # boxWidget.AddObserver("EndInteractionEvent", SelectPolygons)
        # boxWidget.SetPriority(1)
        
        #  # Bounding Box

        textmappers.append(vtk.vtkTextMapper())
        #textmappers[i].SetInput(sourceObjects[i].GetClassName())
        textmappers[i].SetInput(targetObjects2)
        textmappers[i].SetTextProperty(textProperty)

        textactors.append(vtk.vtkActor2D())
        textactors[i].SetMapper(textmappers[i])
        textactors[i].SetPosition(120, 16)
        renderers.append(vtk.vtkRenderer())
    
    gridDimensions = 2



    # We need a renderer even if there is no actor.
    for i in range(len(sourceObjects), gridDimensions ** 2):
        renderers.append(vtk.vtkRenderer())
        

    print (renderers)


    for index in range(0, windowNum):
        renderers[index].AddActor(actors[index])
        renderers[index].AddActor(textactors[index])
        renderers[index].SetBackground(colors.GetColor3d('White'))
        renderers[index].ResetCamera()

        # # rough Bounding Box
        # outline = vtk.vtkOutlineFilter()
        # print("*******")
        # print (type(targetObjects))
        # outline.SetInputConnection(targetObjects.GetOutputPort())

        # outlineMapper = vtkPolyDataMapper()
        # outlineMapper.SetInputConnection(outline.GetOutputPort())

        # outlineActor = vtkActor()
        # outlineActor.SetMapper(outlineMapper)
        # outlineActor.GetProperty().SetColor(0,1,1)

        # renderers[index].AddActor(outlineActor)


        if index == 0:
            renderers[index].GetActiveCamera().Azimuth(60)# Vertical
            renderers[index].GetActiveCamera().Elevation(100) # Vertical
            renderers[index].GetActiveCamera().Zoom(1.2)# Vertical
        elif index == 1:
            renderers[index].GetActiveCamera().Azimuth(180) # FLAT
            renderers[index].GetActiveCamera().Elevation(100)
            renderers[index].GetActiveCamera().Zoom(1.2)
        elif index == 2:
            renderers[index].GetActiveCamera().Azimuth(-180) # 60 angle view
            renderers[index].GetActiveCamera().Elevation(-00)
            renderers[index].GetActiveCamera().Zoom(1.2)
        renderers[index].ResetCameraClippingRange()


    return renderers, new_path, numOfFiles

