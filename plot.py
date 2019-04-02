import vtk
import numpy as np


def displayTruss(elemNodes, nodeCords, stress, name="Tensão", ite="", title="aaaa"):
    pts = vtk.vtkPoints()

    for x, y in nodeCords:
        pts.InsertNextPoint(x, y, 0.0)

    lines = vtk.vtkCellArray()
    for ii, jj in elemNodes:
        lines.InsertNextCell(2)
        lines.InsertCellPoint(ii)
        lines.InsertCellPoint(jj)

    stdata = vtk.vtkDoubleArray()
    stdata.SetName(name)
    for val in stress:
        stdata.InsertNextValue(val)
    grid = vtk.vtkPolyData()
    grid.SetPoints(pts)
    grid.SetLines(lines)

    grid.GetCellData().SetScalars(stdata)

    mapper = vtk.vtkPolyDataMapper()
    # mapper.SetInput(grid)
    mapper.SetInputData(grid)
    mapper.SetScalarRange(np.min(stress), np.max(stress))

    txt = vtk.vtkTextActor()
    txt.SetInput("Número de iterações:"+ite)
    txtprop = txt.GetTextProperty()
    txtprop.SetFontFamilyToArial()
    txtprop.SetFontSize(32)
    txtprop.SetColor(1, 1, 1)
    txt.SetDisplayPosition(20, 950)

    txt2 = vtk.vtkTextActor()
    txt2.SetInput(title)
    txtprop2 = txt2.GetTextProperty()
    txtprop2.SetFontFamilyToArial()
    txtprop2.SetFontSize(60)
    txtprop2.SetColor(1, 1, 1)
    txt2.SetDisplayPosition(800, 900)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    sbar = vtk.vtkScalarBarActor()
    sbar.SetLookupTable(mapper.GetLookupTable())
    sbar.SetTitle(name)

    ren = vtk.vtkRenderer()

    ren.AddActor2D(sbar)
    ren.AddActor(actor)
    ren.AddActor(txt)
    ren.AddActor(txt2)

    renwin = vtk.vtkRenderWindow()
    renwin.AddRenderer(ren)
    renwin.SetSize(1800, 1000)
    #renwin.SetBackground(0.0, 0.0, 1.0)

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renwin)
    iren.Initialize()
    renwin.Render()
    iren.Start()


def displayTrussDeformation(elemNodes, nodeCords, stress, name="Tensão", ite="", title=""):
    pts = vtk.vtkPoints()

    for x, y in nodeCords:
        pts.InsertNextPoint(x, y, 0.0)

    lines = vtk.vtkCellArray()
    for ii, jj in elemNodes:
        lines.InsertNextCell(2)
        lines.InsertCellPoint(ii)
        lines.InsertCellPoint(jj)

    stdata = vtk.vtkDoubleArray()
    stdata.SetName(name)
    for val in stress:
        stdata.InsertNextValue(val)
    grid = vtk.vtkPolyData()
    grid.SetPoints(pts)
    grid.SetLines(lines)

    grid.GetCellData().SetScalars(stdata)

    mapper = vtk.vtkPolyDataMapper()
    # mapper.SetInput(grid)
    mapper.SetInputData(grid)

    txt = vtk.vtkTextActor()
    txt.SetInput("Número de iterações:"+ite)
    txtprop = txt.GetTextProperty()
    txtprop.SetFontFamilyToArial()
    txtprop.SetFontSize(32)
    txtprop.SetColor(1, 1, 1)
    txt.SetDisplayPosition(20, 950)

    txt2 = vtk.vtkTextActor()
    txt2.SetInput(title)
    txtprop2 = txt2.GetTextProperty()
    txtprop2.SetFontFamilyToArial()
    txtprop2.SetFontSize(60)
    txtprop2.SetColor(1, 1, 1)
    txt2.SetDisplayPosition(800, 900)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    ren = vtk.vtkRenderer()

    ren.AddActor(actor)
    ren.AddActor(txt)
    ren.AddActor(txt2)

    renwin = vtk.vtkRenderWindow()
    renwin.AddRenderer(ren)
    renwin.SetSize(1800, 1000)
    #renwin.SetBackground(0.0, 0.0, 1.0)

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renwin)
    iren.Initialize()
    renwin.Render()
    iren.Start()

# example


def plotExample():
    elemNodes = np.array([[0, 1], [0, 2], [1, 2], [1, 3],
                          [0, 3], [2, 3], [2, 5], [3, 4], [3, 5], [2, 4], [4, 5]])

    nodeCords = np.array([
        [0.0, 0.0], [0.0, 5000.0],
        [3000.0, 0.0], [3000.0, 3000.0],
        [6000.0, 0.0], [6000.0, 9000.0]
    ])

    stress = np.array([-210.902, 122.432, 62.558, -44.235, -
                       173.145, -88.47, 62.558, -173.145, -44.235, 122.432, -210.902])

    displayTruss(elemNodes, nodeCords, stress, 'Tensão')
