import pytest

from . import T001_geant4Box2Fluka
from . import T002_geant4Tubs2Fluka
from . import T003_geant4CutTubs2Fluka
from . import T004_geant4Cons2Fluka
from . import T005_geant4Para2Fluka
from . import T006_geant4Trd2Fluka
from . import T007_geant4Trap2Fluka
from . import T008_geant4Sphere2Fluka
from . import T009_geant4Orb2Fluka
from . import T010_geant4Torus2Fluka
from . import T011_geant4Polycone2Fluka
from . import T012_geant4GenericPolycone2Fluka
from . import T013_geant4Polyhedra2Fluka
from . import T014_geant4GenericPolyhedra2Fluka
from . import T015_geant4EllipticalTube2Fluka
from . import T016_geant4Ellipsoid2Fluka
from . import T017_geant4EllipticalCone2Fluka
from . import T018_geant4Paraboloid2Fluka
from . import T019_geant4Hyperboloid2Fluka
from . import T020_geant4Tet2Fluka
from . import T021_geant4ExtrudedSolid2Fluka
from . import T026_geant4GenericTrap2Fluka

from . import T028_geant4Union2Fluka
from . import T029_geant4Subtraction2Fluka
from . import T030_geant4Intersection2Fluka

from . import T105_geant4Assembly2Fluka
from . import T106_geant4ReplicaX2Fluka
from . import T107_geant4ReplicaY2Fluka
from . import T108_geant4ReplicaZ2Fluka
from . import T109_geant4ReplicaPhi2Fluka
from . import T110_geant4ReplicaRho2Fluka

from . import T200_extrudedIntersection
from . import T201_extrudedSubtraction
from . import T202_extrudedReflection
from . import T203_extrudedReflectionRotation


def test_Geant42FlukaConversion_T001_Box(tmptestdir, testdata):
    T001_geant4Box2Fluka.Test(
        vis=False,
        interactive=False,
        fluka=True,
        outputPath=tmptestdir,
        refFilePath=testdata["convert/T001_geant4Box2Fluka.inp"],
    )


def test_Geant42FlukaConversion_T002_Tubs(tmptestdir, testdata):
    T002_geant4Tubs2Fluka.Test(
        vis=False,
        interactive=False,
        fluka=True,
        outputPath=tmptestdir,
        refFilePath=testdata["convert/T002_geant4Tubs2Fluka.inp"],
    )


def test_Geant42FlukaConversion_T003_CutTubs(tmptestdir, testdata):
    T003_geant4CutTubs2Fluka.Test(
        vis=False,
        interactive=False,
        fluka=True,
        outputPath=tmptestdir,
        refFilePath=testdata["convert/T003_geant4CutTubs2Fluka.inp"],
    )


def test_Geant42FlukaConversion_T004_Cons(tmptestdir, testdata):
    T004_geant4Cons2Fluka.Test(
        vis=False,
        interactive=False,
        fluka=True,
        outputPath=tmptestdir,
        refFilePath=testdata["convert/T004_geant4Cons2Fluka.inp"],
    )


def test_Geant42FlukaConversion_T005_Para(tmptestdir, testdata):
    T005_geant4Para2Fluka.Test(
        vis=False,
        interactive=False,
        fluka=True,
        outputPath=tmptestdir,
        refFilePath=testdata["convert/T005_geant4Para2Fluka.inp"],
    )


def test_Geant42FlukaConversion_T006_Tdr(tmptestdir, testdata):
    T006_geant4Trd2Fluka.Test(
        vis=False,
        interactive=False,
        fluka=True,
        outputPath=tmptestdir,
        refFilePath=testdata["convert/T006_geant4Trd2Fluka.inp"],
    )


def test_Geant42FlukaConversion_T007_Trap(tmptestdir, testdata):
    T007_geant4Trap2Fluka.Test(
        vis=False,
        interactive=False,
        fluka=True,
        outputPath=tmptestdir,
        refFilePath=testdata["convert/T007_geant4Trap2Fluka.inp"],
    )


def test_Geant42FlukaConversion_T008_Sphere(tmptestdir, testdata):
    T008_geant4Sphere2Fluka.Test(
        vis=False,
        interactive=False,
        fluka=True,
        outputPath=tmptestdir,
        refFilePath=testdata["convert/T008_geant4Sphere2Fluka.inp"],
    )


def test_Geant42FlukaConversion_T009_Orb(tmptestdir, testdata):
    T009_geant4Orb2Fluka.Test(
        vis=False,
        interactive=False,
        fluka=True,
        outputPath=tmptestdir,
        refFilePath=testdata["convert/T009_geant4Orb2Fluka.inp"],
    )


def test_Geant42FlukaConversion_T010_Torus(tmptestdir, testdata):
    T010_geant4Torus2Fluka.Test(
        vis=False,
        interactive=False,
        fluka=True,
        outputPath=tmptestdir,
        refFilePath=testdata["convert/T010_geant4Torus2Fluka.inp"],
    )


def test_Geant42FlukaConversion_T011_Polycone(tmptestdir, testdata):
    T011_geant4Polycone2Fluka.Test(
        vis=False,
        interactive=False,
        fluka=True,
        outputPath=tmptestdir,
        refFilePath=testdata["convert/T011_geant4Polycone2Fluka.inp"],
    )


def test_Geant42FlukaConversion_T012_GenericPolycone(tmptestdir, testdata):
    T012_geant4GenericPolycone2Fluka.Test(
        vis=False,
        interactive=False,
        fluka=True,
        outputPath=tmptestdir,
        refFilePath=testdata["convert/T012_geant4GenericPolycone2Fluka.inp"],
    )


def test_Geant42FlukaConversion_T013_Polyhedra(tmptestdir, testdata):
    T013_geant4Polyhedra2Fluka.Test(
        vis=False,
        interactive=False,
        fluka=True,
        outputPath=tmptestdir,
        refFilePath=testdata["convert/T013_geant4Polyhedra2Fluka.inp"],
    )


def test_Geant42FlukaConversion_T014_GenericPolyhedra(tmptestdir, testdata):
    T014_geant4GenericPolyhedra2Fluka.Test(
        vis=False,
        interactive=False,
        fluka=True,
        outputPath=tmptestdir,
        refFilePath=testdata["convert/T014_geant4GenericPolyhedra2Fluka.inp"],
    )


def test_Geant42FlukaConversion_T015_EllipticalTube(tmptestdir, testdata):
    T015_geant4EllipticalTube2Fluka.Test(
        vis=False,
        interactive=False,
        fluka=True,
        outputPath=tmptestdir,
        refFilePath=testdata["convert/T015_geant4EllipticalTube2Fluka.inp"],
    )


def test_Geant42FlukaConversion_T016_Ellipsoid(tmptestdir, testdata):
    T016_geant4Ellipsoid2Fluka.Test(
        vis=False,
        interactive=False,
        fluka=True,
        outputPath=tmptestdir,
        refFilePath=testdata["convert/T016_geant4Ellipsoid2Fluka.inp"],
    )


def test_Geant42FlukaConversion_T017_EllipticalCone(tmptestdir, testdata):
    T017_geant4EllipticalCone2Fluka.Test(
        vis=False,
        interactive=False,
        fluka=True,
        outputPath=tmptestdir,
        refFilePath=testdata["convert/T017_geant4EllipticalCone2Fluka.inp"],
    )


def test_Geant42FlukaConversion_T018_Paraboloid(tmptestdir, testdata):
    T018_geant4Paraboloid2Fluka.Test(
        vis=False,
        interactive=False,
        fluka=True,
        outputPath=tmptestdir,
        refFilePath=testdata["convert/T018_geant4Paraboloid2Fluka.inp"],
    )


def test_Geant42FlukaConversion_T019_Hyperboloid(tmptestdir, testdata):
    T019_geant4Hyperboloid2Fluka.Test(
        vis=False,
        interactive=False,
        fluka=True,
        outputPath=tmptestdir,
        refFilePath=testdata["convert/T019_geant4Hyperboloid2Fluka.inp"],
    )


def test_Geant42FlukaConversion_T020_Tet(tmptestdir, testdata):
    T020_geant4Tet2Fluka.Test(
        vis=False,
        interactive=False,
        fluka=True,
        outputPath=tmptestdir,
        refFilePath=testdata["convert/T020_geant4Tet2Fluka.inp"],
    )


def test_Geant42FlukaConversion_T021_ExtrudedSolid(tmptestdir, testdata):
    T021_geant4ExtrudedSolid2Fluka.Test(
        vis=False,
        interactive=False,
        fluka=True,
        outputPath=tmptestdir,
        refFilePath=testdata["convert/T021_geant4ExtrudedSolid2Fluka.inp"],
    )


#    def test_Geant42FlukaConversion_T026_GenericTrap(tmptestdir, testdata):
#        T026_geant4GenericTrap2Fluka.Test(False,False,True)


def test_Geant42FlukaConversion_T028_Union(tmptestdir, testdata):
    T028_geant4Union2Fluka.Test(
        vis=False,
        interactive=False,
        fluka=True,
        outputPath=tmptestdir,
        refFilePath=testdata["convert/T028_geant4Union2Fluka.inp"],
    )


def test_Geant42FlukaConversion_T029_Subtraction(tmptestdir, testdata):
    T029_geant4Subtraction2Fluka.Test(
        vis=False,
        interactive=False,
        fluka=True,
        outputPath=tmptestdir,
        refFilePath=testdata["convert/T029_geant4Subtraction2Fluka.inp"],
    )


def test_Geant42FlukaConversion_T030_Intersection(tmptestdir, testdata):
    T030_geant4Intersection2Fluka.Test(
        vis=False,
        interactive=False,
        fluka=True,
        outputPath=tmptestdir,
        refFilePath=testdata["convert/T030_geant4Intersection2Fluka.inp"],
    )


def test_Geant42FlukaConversion_T105_Assembly(tmptestdir, testdata):
    T105_geant4Assembly2Fluka.Test(
        vis=False,
        interactive=False,
        fluka=True,
        outputPath=tmptestdir,
        refFilePath=testdata["convert/T105_geant4Assembly2Fluka.inp"],
    )


def test_Geant42FlukaConversion_T106_replica_x(tmptestdir, testdata):
    T106_geant4ReplicaX2Fluka.Test(
        vis=False,
        interactive=False,
        fluka=True,
        outputPath=tmptestdir,
        refFilePath=testdata["convert/T106_geant4ReplicaX2Fluka.inp"],
    )


def test_Geant42FlukaConversion_T107_replica_y(tmptestdir, testdata):
    T107_geant4ReplicaY2Fluka.Test(
        vis=False,
        interactive=False,
        fluka=True,
        outputPath=tmptestdir,
        refFilePath=testdata["convert/T107_geant4ReplicaY2Fluka.inp"],
    )


def test_Geant42FlukaConversion_T108_replica_z(tmptestdir, testdata):
    T108_geant4ReplicaZ2Fluka.Test(
        vis=False,
        interactive=False,
        fluka=True,
        outputPath=tmptestdir,
        refFilePath=testdata["convert/T108_geant4ReplicaZ2Fluka.inp"],
    )


def test_Geant42FlukaConversion_T109_replica_phi(tmptestdir, testdata):
    T109_geant4ReplicaPhi2Fluka.Test(
        vis=False,
        interactive=False,
        fluka=True,
        outputPath=tmptestdir,
        refFilePath=testdata["convert/T109_geant4ReplicaPhi2Fluka.inp"],
    )


def test_Geant42FlukaConversion_T110_replica_rho(tmptestdir, testdata):
    T110_geant4ReplicaRho2Fluka.Test(
        vis=False,
        interactive=False,
        fluka=True,
        outputPath=tmptestdir,
        refFilePath=testdata["convert/T110_geant4ReplicaRho2Fluka.inp"],
    )


def test_Geant42FlukaConversion_T200_extrudedIntersection(tmptestdir, testdata):
    T200_extrudedIntersection.Test(
        vis=False,
        interactive=False,
        fluka=True,
        outputPath=tmptestdir,
        refFilePath=testdata["convert/T200_extrudedIntersection.inp"],
    )


def test_Geant42FlukaConversion_T201_extrudedSubtraction(tmptestdir, testdata):
    T201_extrudedSubtraction.Test(
        vis=False,
        interactive=False,
        fluka=True,
        outputPath=tmptestdir,
        refFilePath=testdata["convert/T201_extrudedSubtraction.inp"],
    )
