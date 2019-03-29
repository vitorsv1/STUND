import vtk
import numpy as np


def displayTruss(elemNodes, nodeCords, stress, name="Tensão"):
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

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    sbar = vtk.vtkScalarBarActor()
    sbar.SetLookupTable(mapper.GetLookupTable())
    sbar.SetTitle(name)

    ren = vtk.vtkRenderer()

    ren.AddActor2D(sbar)
    ren.AddActor(actor)

    renwin = vtk.vtkRenderWindow()
    renwin.AddRenderer(ren)
    renwin.SetSize(1800, 1000)

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
