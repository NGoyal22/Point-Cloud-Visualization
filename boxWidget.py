import vtk

sphere = vtk.vtkSphereSource()
sphere.SetThetaResolution(30)
sphere.SetPhiResolution(30)

def testBox():

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(sphere.GetOutputPort())
    actor = vtk.vtkLODActor()
    actor.SetMapper(mapper)
    actor.VisibilityOn()

    planes = vtk.vtkPlanes()
    clipper = vtk.vtkClipPolyData()
    clipper.SetInputConnection(sphere.GetOutputPort())
    clipper.SetClipFunction(planes)
    clipper.InsideOutOn()
    selectMapper = vtk.vtkPolyDataMapper()
    selectMapper.SetInputConnection(clipper.GetOutputPort())
    selectActor = vtk.vtkLODActor()
    selectActor.SetMapper(selectMapper)
    selectActor.GetProperty().SetColor(0, 1, 0)
    selectActor.VisibilityOff()
    selectActor.SetScale(1.01, 1.01, 1.01)

    ren = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)

    iRen = vtk.vtkRenderWindowInteractor()
    iRen.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
    iRen.SetRenderWindow(renWin)

    ren.AddActor(actor)
    ren.AddActor(selectActor)

    ren.SetBackground(0.1, 0.2, 0.4)
    renWin.SetSize(300, 300)

    def SelectPolygons(widget, event_string):
        boxRep.GetPlanes(planes)
        selectActor.VisibilityOn()

    boxRep = vtk.vtkBoxRepresentation()
    boxRep.SetPlaceFactor(0.75)
    boxRep.PlaceWidget(sphere.GetOutput().GetBounds())
    boxWidget = vtk.vtkBoxWidget2()
    boxWidget.SetInteractor(iRen)
    boxWidget.SetRepresentation(boxRep)
    boxWidget.AddObserver("EndInteractionEvent", SelectPolygons)
    boxWidget.SetPriority(1)

    renWin.Render()

    boxWidget.EnabledOn()
    ren.ResetCamera()
    ren.ResetCameraClippingRange()

    return ren