#!/usr/bin/env python
# encoding: utf-8

name = ""
shortDesc = ""
longDesc = """

"""
entry(
    index = 0,
    label = "N#N",
    molecule = 
"""
1 N u0 p1 c0 {2,T}
2 N u0 p1 c0 {1,T}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.50341,-0.000166234,3.0786e-08,1.44515e-09,-9.49756e-13,486.598,3.08248], Tmin=(10,'K'), Tmax=(806.491,'K')),
            NASAPolynomial(coeffs=[3.1079,0.00079013,1.2177e-07,-1.75634e-10,3.17654e-14,583.087,5.10823], Tmin=(806.491,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (4.04703,'kJ/mol'),
        Cp0 = (29.1007,'J/(mol*K)'),
        CpInf = (37.4151,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 1

Geometry:
N       0.54338000    0.00000000    0.00000000
N      -0.54338000    0.00000000   -0.00000000
""",
)

entry(
    index = 1,
    label = "CCCC",
    molecule = 
"""
1  C u0 p0 c0 {2,S} {3,S} {5,S} {6,S}
2  C u0 p0 c0 {1,S} {4,S} {7,S} {8,S}
3  C u0 p0 c0 {1,S} {9,S} {10,S} {11,S}
4  C u0 p0 c0 {2,S} {12,S} {13,S} {14,S}
5  H u0 p0 c0 {1,S}
6  H u0 p0 c0 {1,S}
7  H u0 p0 c0 {2,S}
8  H u0 p0 c0 {2,S}
9  H u0 p0 c0 {3,S}
10 H u0 p0 c0 {3,S}
11 H u0 p0 c0 {3,S}
12 H u0 p0 c0 {4,S}
13 H u0 p0 c0 {4,S}
14 H u0 p0 c0 {4,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.70192,0.0292363,-3.87524e-05,1.27028e-07,-1.16638e-10,-16129.6,7.9717], Tmin=(10,'K'), Tmax=(483.973,'K')),
            NASAPolynomial(coeffs=[-1.83008,0.0503972,-2.82151e-05,7.65594e-09,-8.10467e-13,-15306.5,33.6174], Tmin=(483.973,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-134.111,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (320.107,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 1

Geometry:
C       0.91644000   -0.62912500    0.26174200
C      -0.36759600   -0.65754300   -0.55868400
C       1.35891700    0.78583500    0.61070000
C      -0.81008000   -2.07250700   -0.90751900
H       0.76773200   -1.20700500    1.17781900
H       1.70766000   -1.13769200   -0.29557700
H      -1.15881900   -0.14903200   -0.00133700
H      -0.21893100   -0.07964400   -1.47476200
H       2.27747700    0.78848000    1.19660300
H       1.53644500    1.37019400   -0.29339500
H       0.59055000    1.30013700    1.18990500
H      -0.04161900   -2.58692900   -1.48649700
H      -0.98783100   -2.65669900   -0.00336300
H      -1.72853600   -2.07516500   -1.49358200
""",
)

entry(
    index = 2,
    label = "[O][O]",
    molecule = 
"""
multiplicity 3
1 O u1 p2 c0 {2,S}
2 O u1 p2 c0 {1,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.507,-0.000405671,1.23236e-06,1.57333e-09,-2.02139e-12,-1252.36,4.69557], Tmin=(10,'K'), Tmax=(633.979,'K')),
            NASAPolynomial(coeffs=[2.87701,0.0020651,-1.0549e-06,2.36449e-10,-1.85751e-14,-1142.25,7.68617], Tmin=(633.979,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-10.4099,'kJ/mol'),
        Cp0 = (29.1007,'J/(mol*K)'),
        CpInf = (37.4151,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 3
External symmetry: -1.0
Optical isomers: 1

Geometry:
O       0.59493100    0.00000000    0.00000000
O      -0.59493100    0.00000000   -0.00000000
""",
)

entry(
    index = 3,
    label = "[CH]",
    molecule = 
"""
multiplicity 2
1 C u1 p1 c0 {2,S}
2 H u0 p0 c0 {1,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.4963,0.000296713,-2.04373e-06,4.10065e-09,-2.08377e-12,71250.3,1.32768], Tmin=(10,'K'), Tmax=(780.834,'K')),
            NASAPolynomial(coeffs=[3.18622,0.000481521,2.97712e-07,-2.00668e-10,3.04865e-14,71341.5,3.02094], Tmin=(780.834,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (592.408,'kJ/mol'),
        Cp0 = (29.1007,'J/(mol*K)'),
        CpInf = (37.4151,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 1

Geometry:
C       0.55846600    0.00000000    0.00000000
H      -0.55846600    0.00000000    0.00000000
""",
)

entry(
    index = 4,
    label = "[O]",
    molecule = 
"""
multiplicity 3
1 O u2 p2 c0
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[2.5,-1.5266e-15,6.3226e-18,-7.59355e-21,2.67359e-24,29269.9,4.09089], Tmin=(10,'K'), Tmax=(1363.47,'K')),
            NASAPolynomial(coeffs=[2.5,-1.01797e-13,8.3758e-17,-2.93808e-20,3.72101e-24,29269.9,4.09089], Tmin=(1363.47,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (243.363,'kJ/mol'),
        Cp0 = (20.7862,'J/(mol*K)'),
        CpInf = (20.7862,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 3
External symmetry: -1.0
Optical isomers: 1

Geometry:
O       0.00000000    0.00000000    0.00000000
""",
)

entry(
    index = 5,
    label = "[C-]#[O+]",
    molecule = 
"""
1 O u0 p1 c+1 {2,T}
2 C u0 p1 c-1 {1,T}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.50434,-0.000218354,2.81324e-07,1.45192e-09,-1.10076e-12,-13834.7,3.81704], Tmin=(10,'K'), Tmax=(775.074,'K')),
            NASAPolynomial(coeffs=[2.99705,0.00122368,-2.33586e-07,-6.27275e-11,1.91941e-14,-13720.7,6.36302], Tmin=(775.074,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-115.026,'kJ/mol'),
        Cp0 = (29.1007,'J/(mol*K)'),
        CpInf = (37.4151,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 1

Geometry:
O       0.56089600    0.00000000    0.00000000
C      -0.56089600    0.00000000    0.00000000
""",
)

entry(
    index = 6,
    label = "O",
    molecule = 
"""
1 O u0 p2 c0 {2,S} {3,S}
2 H u0 p0 c0 {1,S}
3 H u0 p0 c0 {1,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[4.00475,-0.000240908,9.43735e-07,1.29488e-09,-1.12343e-12,-28364.7,-0.11592], Tmin=(10,'K'), Tmax=(774.167,'K')),
            NASAPolynomial(coeffs=[3.50595,0.00114664,5.60268e-07,-3.59833e-10,5.19112e-14,-28251.8,2.39304], Tmin=(774.167,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-235.836,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (58.2013,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 1

Geometry:
O      -0.00189400    0.39032300   -0.00000000
H      -0.75864300   -0.19854300    0.00000000
H       0.76053700   -0.19178000   -0.00000000
""",
)

entry(
    index = 7,
    label = "C=O",
    molecule = 
"""
1 O u0 p2 c0 {2,D}
2 C u0 p0 c0 {1,D} {3,S} {4,S}
3 H u0 p0 c0 {2,S}
4 H u0 p0 c0 {2,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[4.03195,-0.00195087,9.19752e-06,2.64444e-09,-7.92665e-12,-13508.1,3.46229], Tmin=(10,'K'), Tmax=(594.329,'K')),
            NASAPolynomial(coeffs=[1.44725,0.00944802,-4.43637e-06,9.60363e-10,-7.68427e-14,-13095,15.4781], Tmin=(594.329,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-112.302,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (83.1447,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 1

Geometry:
O       1.15593100   -0.07496700    0.26242600
C      -0.00747900    0.00051000   -0.00170100
H      -0.64601500   -0.89623700   -0.08090900
H      -0.50243700    0.97059400   -0.17981600
""",
)

entry(
    index = 8,
    label = "C",
    molecule = 
"""
1 C u0 p0 c0 {2,S} {3,S} {4,S} {5,S}
2 H u0 p0 c0 {1,S}
3 H u0 p0 c0 {1,S}
4 H u0 p0 c0 {1,S}
5 H u0 p0 c0 {1,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[4.04165,-0.00250158,1.15317e-05,3.46932e-09,-9.38087e-12,-9325.36,-0.432509], Tmin=(10,'K'), Tmax=(613.438,'K')),
            NASAPolynomial(coeffs=[0.692749,0.0117202,-4.62315e-06,7.89436e-10,-4.15254e-14,-8771.21,15.2553], Tmin=(613.438,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-77.5204,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (108.088,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 1

Geometry:
C       0.00005200    0.00005000    0.00002700
H      -0.67324700    0.84929600   -0.08463900
H      -0.39246700   -0.83245800   -0.57855800
H       0.08511400   -0.29218800    1.04358400
H       0.98054800    0.27530000   -0.38041400
""",
)

entry(
    index = 9,
    label = "C=C",
    molecule = 
"""
1 C u0 p0 c0 {2,D} {3,S} {4,S}
2 C u0 p0 c0 {1,D} {5,S} {6,S}
3 H u0 p0 c0 {1,S}
4 H u0 p0 c0 {1,S}
5 H u0 p0 c0 {2,S}
6 H u0 p0 c0 {2,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[4.10242,-0.00693485,5.16362e-05,-6.17063e-08,2.43246e-11,6017.46,3.21985], Tmin=(10,'K'), Tmax=(759.071,'K')),
            NASAPolynomial(coeffs=[0.491002,0.0180919,-9.66787e-06,2.54142e-09,-2.62687e-13,6392.98,18.5095], Tmin=(759.071,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (50.0538,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (133.032,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 1

Geometry:
C      -0.62796400    0.03314200    0.20283300
C       0.62774700   -0.03482500   -0.20319900
H      -1.25810100   -0.84558200    0.24644200
H      -1.07542300    0.97013500    0.50765100
H       1.25791400    0.84383500   -0.24683200
H       1.07511500   -0.97185700   -0.50799900
""",
)

entry(
    index = 10,
    label = "C=CC",
    molecule = 
"""
1 C u0 p0 c0 {2,S} {4,S} {5,S} {6,S}
2 C u0 p0 c0 {1,S} {3,D} {7,S}
3 C u0 p0 c0 {2,D} {8,S} {9,S}
4 H u0 p0 c0 {1,S}
5 H u0 p0 c0 {1,S}
6 H u0 p0 c0 {1,S}
7 H u0 p0 c0 {2,S}
8 H u0 p0 c0 {3,S}
9 H u0 p0 c0 {3,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.98776,0.000443813,6.72303e-05,-1.03822e-07,5.24159e-11,1782.11,6.97137], Tmin=(10,'K'), Tmax=(510.386,'K')),
            NASAPolynomial(coeffs=[0.40241,0.0285426,-1.53497e-05,4.04264e-09,-4.18474e-13,2148.1,21.8572], Tmin=(510.386,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (14.8057,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (203.705,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 1

Geometry:
C      -1.13076500    0.03315800   -0.34423700
C       0.27021400    0.27432400    0.12086900
C       1.35214100   -0.23723900   -0.44439700
H      -1.14827900   -0.62175300   -1.21420200
H      -1.62026000    0.97208300   -0.60882200
H      -1.72964100   -0.42484300    0.44495200
H       0.38521100    0.91896400    0.98682800
H       1.28038800   -0.88508300   -1.31014400
H       2.34298200   -0.02857000   -0.06494800
""",
)

entry(
    index = 11,
    label = "[H][H]",
    molecule = 
"""
1 H u0 p0 c0 {2,S}
2 H u0 p0 c0 {1,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.49863,8.11307e-05,-2.56091e-07,1.30149e-11,3.05724e-13,-444.289,-4.29111], Tmin=(10,'K'), Tmax=(610.62,'K')),
            NASAPolynomial(coeffs=[3.68701,-0.000782803,9.57072e-07,-3.18948e-10,3.52653e-14,-474.194,-5.16349], Tmin=(610.62,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-3.69451,'kJ/mol'),
        Cp0 = (29.1007,'J/(mol*K)'),
        CpInf = (37.4151,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 1

Geometry:
H       0.36951500    0.00000000    0.00000000
H      -0.36951500    0.00000000   -0.00000000
""",
)

entry(
    index = 12,
    label = "[H]",
    molecule = 
"""
multiplicity 2
1 H u1 p0 c0
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[2.5,-1.5266e-15,6.3226e-18,-7.59355e-21,2.67359e-24,25472.6,-0.461279], Tmin=(10,'K'), Tmax=(1363.47,'K')),
            NASAPolynomial(coeffs=[2.5,-1.01797e-13,8.3758e-17,-2.93808e-20,3.72101e-24,25472.6,-0.461279], Tmin=(1363.47,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (211.791,'kJ/mol'),
        Cp0 = (20.7862,'J/(mol*K)'),
        CpInf = (20.7862,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 1

Geometry:
H       0.00000000    0.00000000    0.00000000
""",
)

entry(
    index = 13,
    label = "[OH]",
    molecule = 
"""
multiplicity 2
1 O u1 p2 c0 {2,S}
2 H u0 p0 c0 {1,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.49686,0.000184709,-1.00336e-06,1.58128e-09,-6.1602e-13,4291.54,1.47257], Tmin=(10,'K'), Tmax=(982.396,'K')),
            NASAPolynomial(coeffs=[3.4502,-0.000290376,7.37488e-07,-2.89186e-10,3.53364e-14,4332.8,1.86016], Tmin=(982.396,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (35.6809,'kJ/mol'),
        Cp0 = (29.1007,'J/(mol*K)'),
        CpInf = (37.4151,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 1

Geometry:
O       0.48557500    0.00000000    0.00000000
H      -0.48557500    0.00000000    0.00000000
""",
)

entry(
    index = 14,
    label = "[O]O",
    molecule = 
"""
multiplicity 2
1 O u0 p2 c0 {2,S} {3,S}
2 O u1 p2 c0 {1,S}
3 H u0 p0 c0 {1,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[4.02904,-0.00171366,1.02111e-05,-1.02434e-08,3.35624e-12,844.521,4.6613], Tmin=(10,'K'), Tmax=(934.06,'K')),
            NASAPolynomial(coeffs=[3.0268,0.00428389,-2.15929e-06,5.40573e-10,-5.33092e-14,957.348,9.02988], Tmin=(934.06,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (7.02952,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (58.2013,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 1

Geometry:
O      -0.16361700    0.43849000    0.00000000
O       0.99492000   -0.17053000   -0.00000000
H      -0.83130300   -0.26796000    0.00000000
""",
)

entry(
    index = 15,
    label = "OO",
    molecule = 
"""
1 O u0 p2 c0 {2,S} {3,S}
2 O u0 p2 c0 {1,S} {4,S}
3 H u0 p0 c0 {1,S}
4 H u0 p0 c0 {2,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.97322,0.00193881,8.28088e-06,-1.20199e-08,5.29065e-12,-16098.4,5.27752], Tmin=(10,'K'), Tmax=(595.386,'K')),
            NASAPolynomial(coeffs=[3.2994,0.00646575,-3.1242e-06,7.50636e-10,-7.1647e-14,-16018.2,8.1789], Tmin=(595.386,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-133.855,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (78.9875,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 2

Geometry:
O      -0.58310700    0.41066200    0.25838500
O       0.58275100   -0.40583300    0.26677300
H      -1.18757900   -0.12904100   -0.26237900
H       1.18803500    0.12421100   -0.26288000
""",
)

entry(
    index = 16,
    label = "[CH3]",
    molecule = 
"""
multiplicity 2
1 C u1 p0 c0 {2,S} {3,S} {4,S}
2 H u0 p0 c0 {1,S}
3 H u0 p0 c0 {1,S}
4 H u0 p0 c0 {1,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.98354,0.00104344,1.03019e-05,-1.78439e-08,1.09976e-11,16909.8,0.220209], Tmin=(10,'K'), Tmax=(399.223,'K')),
            NASAPolynomial(coeffs=[3.70615,0.0038225,-1.38876e-07,-4.10174e-10,8.12296e-14,16932,1.30377], Tmin=(399.223,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (140.588,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (83.1447,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 1

Geometry:
C       0.00001300   -0.00015100   -0.00125300
H       1.05127700   -0.23197600    0.00320900
H      -0.72687200   -0.79416600    0.00243700
H      -0.32451900    1.02629200   -0.00429300
""",
)

entry(
    index = 17,
    label = "[CH]=O",
    molecule = 
"""
multiplicity 2
1 O u0 p2 c0 {2,D}
2 C u1 p0 c0 {1,D} {3,S}
3 H u0 p0 c0 {2,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[4.01388,-0.000821475,4.65313e-06,-5.28908e-11,-2.508e-12,4550.39,4.13326], Tmin=(10,'K'), Tmax=(627.701,'K')),
            NASAPolynomial(coeffs=[2.73913,0.0046589,-2.12741e-06,4.40746e-10,-3.30328e-14,4762.49,10.1043], Tmin=(627.701,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (37.8393,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (58.2013,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 1

Geometry:
O       1.02367400   -0.15576300    0.00000000
C      -0.02592800    0.35746100    0.00000000
H      -0.99764600   -0.20169800    0.00000000
""",
)

entry(
    index = 18,
    label = "C[C]=O",
    molecule = 
"""
multiplicity 2
1 O u0 p2 c0 {3,D}
2 C u0 p0 c0 {3,S} {4,S} {5,S} {6,S}
3 C u1 p0 c0 {1,D} {2,S}
4 H u0 p0 c0 {2,S}
5 H u0 p0 c0 {2,S}
6 H u0 p0 c0 {2,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.90215,0.0119187,-5.027e-05,1.63044e-07,-1.54223e-10,-2162.07,7.44059], Tmin=(10,'K'), Tmax=(414.165,'K')),
            NASAPolynomial(coeffs=[1.72139,0.0167764,-9.17637e-06,2.43095e-09,-2.51063e-13,-1842.46,17.717], Tmin=(414.165,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-17.9812,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (128.874,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 1

Geometry:
O       1.93052600   -0.10668200   -0.26504600
C      -0.46686200   -0.00057500    0.02393400
C       0.98807100    0.25566800    0.33326200
H      -0.56961300   -0.59947800   -0.88104700
H      -0.91415200   -0.50792300    0.87662300
H      -0.96787000    0.95909000   -0.08782500
""",
)

entry(
    index = 19,
    label = "[CH2]C=O",
    molecule = 
"""
multiplicity 2
1 O u0 p2 c0 {3,D}
2 C u1 p0 c0 {3,S} {4,S} {5,S}
3 C u0 p0 c0 {1,D} {2,S} {6,S}
4 H u0 p0 c0 {2,S}
5 H u0 p0 c0 {2,S}
6 H u0 p0 c0 {3,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[4.01594,-0.0015019,5.48131e-05,-8.85282e-08,4.61925e-11,694.157,7.13247], Tmin=(10,'K'), Tmax=(568.406,'K')),
            NASAPolynomial(coeffs=[1.72418,0.0191456,-1.16028e-05,3.35889e-09,-3.74983e-13,881.671,16.2519], Tmin=(568.406,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (5.76787,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (128.874,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 1

Geometry:
O       1.37699400   -0.23918600   -0.96767400
C      -0.71454500   -0.12204000    0.04796000
C       0.68769500    0.12799600   -0.02665800
H      -1.29907000    0.21383800    0.89116500
H      -1.19213200   -0.65817300   -0.75878100
H       1.14095900    0.67746400    0.81398900
""",
)

entry(
    index = 20,
    label = "[CH]=C",
    molecule = 
"""
multiplicity 2
1 C u0 p0 c0 {2,D} {3,S} {4,S}
2 C u1 p0 c0 {1,D} {5,S}
3 H u0 p0 c0 {1,S}
4 H u0 p0 c0 {1,S}
5 H u0 p0 c0 {2,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[4.07386,-0.00582398,5.0714e-05,-7.32813e-08,3.53706e-11,34777.5,4.92419], Tmin=(10,'K'), Tmax=(617.226,'K')),
            NASAPolynomial(coeffs=[1.86051,0.0133028,-7.39176e-06,2.03333e-09,-2.19697e-13,34959.6,13.7963], Tmin=(617.226,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (289.163,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (108.088,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 1

Geometry:
C      -0.47147200   -0.09029300    0.03034400
C       0.77665200   -0.44086600    0.14724800
H      -0.75758600    0.90224100   -0.30157900
H      -1.28372800   -0.77803200    0.26063300
H       1.31875800   -1.32454200    0.44268500
""",
)

entry(
    index = 21,
    label = "[CH2]",
    molecule = 
"""
multiplicity 3
1 C u2 p0 c0 {2,S} {3,S}
2 H u0 p0 c0 {1,S}
3 H u0 p0 c0 {1,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[4.00375,-0.000188169,3.18523e-06,-2.18177e-09,4.47807e-13,44983.1,0.593704], Tmin=(10,'K'), Tmax=(902.691,'K')),
            NASAPolynomial(coeffs=[3.26056,0.00260503,-6.25287e-07,1.87447e-11,8.33073e-15,45137.6,4.21596], Tmin=(902.691,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (374.012,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (58.2013,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 3
External symmetry: -1.0
Optical isomers: 1

Geometry:
C      -0.00104400    0.27927000   -0.00000000
H      -0.99029700   -0.14329200    0.00000000
H       0.99134100   -0.13597800   -0.00000000
""",
)

entry(
    index = 22,
    label = "C=C=O",
    molecule = 
"""
1 O u0 p2 c0 {3,D}
2 C u0 p0 c0 {3,D} {4,S} {5,S}
3 C u0 p0 c0 {1,D} {2,D}
4 H u0 p0 c0 {2,S}
5 H u0 p0 c0 {2,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.98058,0.00114712,3.64751e-05,-6.60924e-08,3.76009e-11,-7904.39,4.88207], Tmin=(10,'K'), Tmax=(542.982,'K')),
            NASAPolynomial(coeffs=[2.87684,0.0133136,-8.28361e-06,2.54984e-09,-3.05607e-13,-7844.02,8.9851], Tmin=(542.982,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-65.7286,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (108.088,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 1

Geometry:
O       1.91077100   -0.17595200    0.28457900
C      -0.53766900   -0.02271400    0.07804700
C       0.76237100   -0.10402100    0.18763000
H      -1.06944400    0.70482700    0.66743000
H      -1.04878800   -0.68553500   -0.59949400
""",
)

entry(
    index = 23,
    label = "C#C",
    molecule = 
"""
1 C u0 p0 c0 {2,T} {3,S}
2 C u0 p0 c0 {1,T} {4,S}
3 H u0 p0 c0 {1,S}
4 H u0 p0 c0 {2,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.98979,0.000590744,1.9909e-05,-3.4401e-08,1.88574e-11,26533,-5.05233], Tmin=(10,'K'), Tmax=(559.9,'K')),
            NASAPolynomial(coeffs=[3.3269,0.007481,-4.32248e-06,1.32394e-09,-1.62849e-13,26573.4,-2.54036], Tmin=(559.9,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (220.603,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (83.1447,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 1

Geometry:
C      -0.59436700    0.24784800    0.00549400
C       0.59436100    0.13708800   -0.00582700
H      -1.65253800    0.34662900    0.01583400
H       1.65254400    0.03863500   -0.01560100
""",
)

entry(
    index = 24,
    label = "CO",
    molecule = 
"""
1 O u0 p2 c0 {2,S} {6,S}
2 C u0 p0 c0 {1,S} {3,S} {4,S} {5,S}
3 H u0 p0 c0 {2,S}
4 H u0 p0 c0 {2,S}
5 H u0 p0 c0 {2,S}
6 H u0 p0 c0 {1,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[4.0044,-0.000356586,2.35176e-05,-2.49087e-08,8.4169e-12,-24817.7,5.26301], Tmin=(10,'K'), Tmax=(777.361,'K')),
            NASAPolynomial(coeffs=[0.873081,0.0157555,-7.57141e-06,1.75253e-09,-1.57109e-13,-24330.8,19.5813], Tmin=(777.361,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-206.343,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (128.874,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 1

Geometry:
O       0.92542800   -0.46582700   -0.33949800
C      -0.35721900    0.03231700   -0.02049900
H      -0.62969800   -0.16333400    1.02012000
H      -0.44311300    1.10541000   -0.21140900
H      -1.06789700   -0.48497400   -0.66110300
H       1.57249900   -0.02359300    0.21229000
""",
)

entry(
    index = 25,
    label = "C[O]",
    molecule = 
"""
multiplicity 2
1 O u1 p2 c0 {2,S}
2 C u0 p0 c0 {1,S} {3,S} {4,S} {5,S}
3 H u0 p0 c0 {2,S}
4 H u0 p0 c0 {2,S}
5 H u0 p0 c0 {2,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[4.02031,-0.00142487,2.83071e-05,-3.6052e-08,1.50505e-11,628.69,5.39135], Tmin=(10,'K'), Tmax=(621.149,'K')),
            NASAPolynomial(coeffs=[1.75285,0.0131771,-6.95538e-06,1.79518e-09,-1.8247e-13,910.37,15.2507], Tmin=(621.149,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (5.23073,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (108.088,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 1

Geometry:
O       1.30581700   -0.14086000   -0.15466700
C      -0.04575600   -0.02967800    0.01379100
H      -0.36364600   -0.21849800    1.04431900
H      -0.28159500    1.02504800   -0.20493800
H      -0.61481900   -0.63601300   -0.69840600
""",
)

entry(
    index = 26,
    label = "CC",
    molecule = 
"""
1 C u0 p0 c0 {2,S} {3,S} {4,S} {5,S}
2 C u0 p0 c0 {1,S} {6,S} {7,S} {8,S}
3 H u0 p0 c0 {1,S}
4 H u0 p0 c0 {1,S}
5 H u0 p0 c0 {1,S}
6 H u0 p0 c0 {2,S}
7 H u0 p0 c0 {2,S}
8 H u0 p0 c0 {2,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[4.02869,-0.00185478,4.79334e-05,-5.81888e-08,2.2988e-11,-10682.5,3.51647], Tmin=(10,'K'), Tmax=(658.518,'K')),
            NASAPolynomial(coeffs=[-0.35429,0.0247684,-1.27099e-05,3.20469e-09,-3.19411e-13,-10105.2,22.8308], Tmin=(658.518,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-88.8124,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (178.761,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 1

Geometry:
C      -0.76153700    0.00738800   -0.01521000
C       0.76161600   -0.00726200    0.01524100
H      -1.17735400   -0.09939900    0.98626900
H      -1.13895500    0.94075000   -0.43194900
H      -1.15197100   -0.80793900   -0.62354200
H       1.15180200    0.80696000    0.62464400
H       1.17730700    0.10070100   -0.98615700
H       1.13899300   -0.94119800    0.43070400
""",
)

entry(
    index = 27,
    label = "C[CH2]",
    molecule = 
"""
multiplicity 2
1 C u0 p0 c0 {2,S} {3,S} {4,S} {5,S}
2 C u1 p0 c0 {1,S} {6,S} {7,S}
3 H u0 p0 c0 {1,S}
4 H u0 p0 c0 {1,S}
5 H u0 p0 c0 {1,S}
6 H u0 p0 c0 {2,S}
7 H u0 p0 c0 {2,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.9852,0.00067328,3.63603e-05,-4.86683e-08,2.10889e-11,13482,5.70899], Tmin=(10,'K'), Tmax=(597.004,'K')),
            NASAPolynomial(coeffs=[1.28048,0.0187952,-9.17191e-06,2.17692e-09,-2.02923e-13,13805,17.3625], Tmin=(597.004,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (112.088,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (153.818,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 1

Geometry:
C      -0.62062400    0.01459100    0.02556100
C       0.85733800   -0.04835600   -0.09598800
H      -1.06294500    0.62511600   -0.76192100
H      -0.93315000    0.45838000    0.97957700
H      -1.07009800   -0.97764800   -0.01875000
H       1.41842800    0.80168000   -0.45195800
H       1.41105200   -0.87386300    0.32357900
""",
)

entry(
    index = 28,
    label = "CC=O",
    molecule = 
"""
1 O u0 p2 c0 {3,D}
2 C u0 p0 c0 {3,S} {4,S} {5,S} {6,S}
3 C u0 p0 c0 {1,D} {2,S} {7,S}
4 H u0 p0 c0 {2,S}
5 H u0 p0 c0 {2,S}
6 H u0 p0 c0 {2,S}
7 H u0 p0 c0 {3,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.97357,0.00141196,4.01893e-05,-5.93239e-08,2.83514e-11,-20663.5,7.27896], Tmin=(10,'K'), Tmax=(539.57,'K')),
            NASAPolynomial(coeffs=[1.55144,0.0193673,-9.72444e-06,2.34466e-09,-2.20488e-13,-20402.1,17.47], Tmin=(539.57,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-171.82,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (153.818,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 1

Geometry:
O       1.56330700   -0.83998100   -0.42496400
C      -0.64867400   -0.02966500   -0.01745300
C       0.84960000    0.01878100    0.01245200
H      -0.98800600   -0.94740700   -0.48947300
H      -1.03447400    0.03696400    1.00134300
H      -1.02942300    0.83794600   -0.55916900
H       1.28767000    0.92336200    0.47736300
""",
)

entry(
    index = 29,
    label = "[O]C=O",
    molecule = 
"""
multiplicity 2
1 O u1 p2 c0 {3,S}
2 O u0 p2 c0 {3,D}
3 C u0 p0 c0 {1,S} {2,D} {4,S}
4 H u0 p0 c0 {3,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[4.01066,-0.000900996,2.72046e-05,-4.12316e-08,2.00036e-11,-15486.2,7.03964], Tmin=(10,'K'), Tmax=(620.7,'K')),
            NASAPolynomial(coeffs=[2.71528,0.0101917,-6.23564e-06,1.80958e-09,-2.01681e-13,-15378.3,12.2454], Tmin=(620.7,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-128.76,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (83.1447,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 1

Geometry:
O       1.21637300   -0.20722700    0.18914900
O      -0.92792100   -0.84745700   -0.02725100
C      -0.07334900   -0.01874700   -0.00776600
H      -0.21510400    1.07353000   -0.15413200
""",
)

entry(
    index = 30,
    label = "O=CO",
    molecule = 
"""
1 O u0 p2 c0 {3,S} {5,S}
2 O u0 p2 c0 {3,D}
3 C u0 p0 c0 {1,S} {2,D} {4,S}
4 H u0 p0 c0 {3,S}
5 H u0 p0 c0 {1,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[4.07076,-0.00485244,4.88922e-05,-6.3402e-08,2.61962e-11,-46709.6,6.52001], Tmin=(10,'K'), Tmax=(757.004,'K')),
            NASAPolynomial(coeffs=[1.30878,0.017615,-1.12274e-05,3.28217e-09,-3.63403e-13,-46517.1,17.5861], Tmin=(757.004,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-388.352,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (103.931,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 1

Geometry:
O       0.78898000   -0.28233000    0.46542300
O      -0.54817300    0.64115400   -1.08177300
C      -0.39384200    0.09373600   -0.03345100
H      -1.19705900   -0.17453400    0.66091600
H       1.46922600   -0.02863500   -0.17491500
""",
)

entry(
    index = 31,
    label = "CO[O]",
    molecule = 
"""
multiplicity 2
1 O u0 p2 c0 {2,S} {3,S}
2 O u1 p2 c0 {1,S}
3 C u0 p0 c0 {1,S} {4,S} {5,S} {6,S}
4 H u0 p0 c0 {3,S}
5 H u0 p0 c0 {3,S}
6 H u0 p0 c0 {3,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.979,0.00109811,3.17744e-05,-4.57252e-08,2.11649e-11,-29.5869,8.30036], Tmin=(10,'K'), Tmax=(559.146,'K')),
            NASAPolynomial(coeffs=[1.89215,0.0160286,-8.28362e-06,2.04107e-09,-1.9426e-13,203.758,17.1548], Tmin=(559.146,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-0.25682,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (128.874,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 1

Geometry:
O       0.91405100    0.54257000   -0.05705700
O       1.76387300   -0.41024000    0.17461900
C      -0.43134600    0.04772000   -0.03240200
H      -0.63514000   -0.37113800    0.95014600
H      -1.06981300    0.90320600   -0.23299000
H      -0.54172500   -0.71221800   -0.80221700
""",
)

entry(
    index = 32,
    label = "COO",
    molecule = 
"""
1 O u0 p2 c0 {2,S} {3,S}
2 O u0 p2 c0 {1,S} {7,S}
3 C u0 p0 c0 {1,S} {4,S} {5,S} {6,S}
4 H u0 p0 c0 {3,S}
5 H u0 p0 c0 {3,S}
6 H u0 p0 c0 {3,S}
7 H u0 p0 c0 {2,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.90524,0.00955989,9.77453e-06,-1.55068e-08,5.64429e-12,-16324.1,8.41376], Tmin=(10,'K'), Tmax=(966.814,'K')),
            NASAPolynomial(coeffs=[3.26458,0.0168485,-8.72949e-06,2.21452e-09,-2.21161e-13,-16417,10.362], Tmin=(966.814,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-135.726,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (149.66,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 2

Geometry:
O       0.45593800   -0.87205000   -0.26084000
O       1.58456400   -0.00760600   -0.29189900
C      -0.66706000   -0.05600500   -0.02089600
H      -0.60618300    0.42096400    0.95971200
H      -1.52194000   -0.72966100   -0.05295100
H      -0.76446300    0.70500800   -0.79588900
H       2.05449600   -0.27774500    0.50583800
""",
)

entry(
    index = 33,
    label = "CCO[O]",
    molecule = 
"""
multiplicity 2
1 O u0 p2 c0 {2,S} {3,S}
2 O u1 p2 c0 {1,S}
3 C u0 p0 c0 {1,S} {4,S} {5,S} {6,S}
4 C u0 p0 c0 {3,S} {7,S} {8,S} {9,S}
5 H u0 p0 c0 {3,S}
6 H u0 p0 c0 {3,S}
7 H u0 p0 c0 {4,S}
8 H u0 p0 c0 {4,S}
9 H u0 p0 c0 {4,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.77059,0.0242061,-5.67441e-05,1.53643e-07,-1.3814e-10,-4606.86,10.6045], Tmin=(10,'K'), Tmax=(426.911,'K')),
            NASAPolynomial(coeffs=[1.65386,0.0283714,-1.63287e-05,4.56304e-09,-4.96368e-13,-4283.36,20.6869], Tmin=(426.911,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-38.3099,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (199.547,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 2

Geometry:
O       1.57595700    0.40439200   -0.20672000
O       1.19049600    1.60510800    0.09855200
C       0.51676000   -0.55465200    0.00814400
C       0.26986200   -0.74965600    1.48536300
H       0.87568500   -1.46020800   -0.47684700
H      -0.36408900   -0.18054200   -0.51094700
H      -0.03224300    0.19283000    1.93727900
H      -0.52444500   -1.47989100    1.63373800
H       1.17043000   -1.10896700    1.98063600
""",
)

entry(
    index = 34,
    label = "CCOO",
    molecule = 
"""
1  O u0 p2 c0 {2,S} {3,S}
2  O u0 p2 c0 {1,S} {10,S}
3  C u0 p0 c0 {1,S} {4,S} {5,S} {6,S}
4  C u0 p0 c0 {3,S} {7,S} {8,S} {9,S}
5  H u0 p0 c0 {3,S}
6  H u0 p0 c0 {3,S}
7  H u0 p0 c0 {4,S}
8  H u0 p0 c0 {4,S}
9  H u0 p0 c0 {4,S}
10 H u0 p0 c0 {2,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.79178,0.0177039,2.06052e-05,-4.24007e-08,2.0514e-11,-20629.8,11.0663], Tmin=(10,'K'), Tmax=(682.481,'K')),
            NASAPolynomial(coeffs=[2.47598,0.0301749,-1.7264e-05,4.80837e-09,-5.2193e-13,-20561.1,16.0995], Tmin=(682.481,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-171.55,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (220.334,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 2

Geometry:
O       1.13494700   -0.78126200    0.25558000
O       1.48354200   -0.16221800   -0.97784900
C       0.02162000   -0.07758500    0.77863900
C      -1.21918400   -0.23535700   -0.07393700
H      -0.11440000   -0.52271800    1.76544600
H       0.28626000    0.97593600    0.90610400
H      -1.05311400    0.18411000   -1.06378000
H      -2.06021500    0.28276900    0.38651600
H      -1.47256000   -1.28928000   -0.17890200
H       2.32692300    0.24514500   -0.74928200
""",
)

entry(
    index = 35,
    label = "C1CO1",
    molecule = 
"""
1 O u0 p2 c0 {2,S} {3,S}
2 C u0 p0 c0 {1,S} {3,S} {4,S} {5,S}
3 C u0 p0 c0 {1,S} {2,S} {6,S} {7,S}
4 H u0 p0 c0 {2,S}
5 H u0 p0 c0 {2,S}
6 H u0 p0 c0 {3,S}
7 H u0 p0 c0 {3,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[4.15855,-0.0108123,7.995e-05,-9.96064e-08,4.04631e-11,-8554.94,5.89445], Tmin=(10,'K'), Tmax=(762.196,'K')),
            NASAPolynomial(coeffs=[-0.342261,0.0250165,-1.45874e-05,4.09738e-09,-4.44577e-13,-8223.46,24.0597], Tmin=(762.196,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-71.097,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (157.975,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 1

Geometry:
O       0.01782400   -0.28444300    1.12639500
C       0.72980900    0.05448100   -0.04659900
C      -0.73137400   -0.03155000   -0.04586100
H       1.20332100    1.02870300   -0.03482800
H       1.30852600   -0.74971400   -0.48460800
H      -1.31565200    0.88065500   -0.03163600
H      -1.21245400   -0.89823300   -0.48286200
""",
)

entry(
    index = 36,
    label = "[O]OCC=O",
    molecule = 
"""
multiplicity 2
1 O u0 p2 c0 {3,S} {4,S}
2 O u0 p2 c0 {5,D}
3 O u1 p2 c0 {1,S}
4 C u0 p0 c0 {1,S} {5,S} {6,S} {7,S}
5 C u0 p0 c0 {2,D} {4,S} {8,S}
6 H u0 p0 c0 {4,S}
7 H u0 p0 c0 {4,S}
8 H u0 p0 c0 {5,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.76349,0.0206211,1.65934e-05,-6.59422e-08,4.83164e-11,-11918.6,11.7258], Tmin=(10,'K'), Tmax=(506.832,'K')),
            NASAPolynomial(coeffs=[4.23082,0.0242183,-1.56144e-05,4.78423e-09,-5.59748e-13,-12059.5,8.86561], Tmin=(506.832,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-99.119,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (174.604,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 2

Geometry:
O      -1.20291800    0.81153900   -0.02332700
O       1.75012200   -1.06419100    0.53640700
O      -0.82507500    1.40550700   -1.11778800
C      -0.50095000   -0.42268000    0.14044000
C       0.98812700   -0.17704900    0.29380300
H      -0.90194000   -0.89400300    1.03546500
H      -0.68061200   -1.05371000   -0.72963200
H       1.30914300    0.87154800    0.16208800
""",
)

entry(
    index = 37,
    label = "[CH2]C(C)=O",
    molecule = 
"""
multiplicity 2
1 O u0 p2 c0 {3,D}
2 C u0 p0 c0 {3,S} {5,S} {6,S} {7,S}
3 C u0 p0 c0 {1,D} {2,S} {4,S}
4 C u1 p0 c0 {3,S} {8,S} {9,S}
5 H u0 p0 c0 {2,S}
6 H u0 p0 c0 {2,S}
7 H u0 p0 c0 {2,S}
8 H u0 p0 c0 {4,S}
9 H u0 p0 c0 {4,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.90974,0.00976493,4.03154e-05,-6.35723e-08,2.8231e-11,-5304.39,9.52259], Tmin=(10,'K'), Tmax=(743.573,'K')),
            NASAPolynomial(coeffs=[2.23379,0.0283373,-1.64291e-05,4.58796e-09,-4.96849e-13,-5319.35,15.335], Tmin=(743.573,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-44.104,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (199.547,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 1

Geometry:
O       0.36620000   -0.27114400    1.78336700
C      -1.11439300    0.12885300   -0.05188300
C       0.22973100   -0.16972000    0.57225400
C       1.35896500   -0.33360700   -0.30718100
H      -1.86152300    0.22568200    0.72985200
H      -1.39954800   -0.67099900   -0.73635600
H      -1.06588600    1.05185300   -0.63091600
H       2.32319900   -0.54703800    0.12791200
H       1.26077500   -0.24817600   -1.37934100
""",
)

entry(
    index = 38,
    label = "CC(=O)C[O]",
    molecule = 
"""
multiplicity 2
1  O u1 p2 c0 {4,S}
2  O u0 p2 c0 {5,D}
3  C u0 p0 c0 {5,S} {6,S} {7,S} {8,S}
4  C u0 p0 c0 {1,S} {5,S} {9,S} {10,S}
5  C u0 p0 c0 {2,D} {3,S} {4,S}
6  H u0 p0 c0 {3,S}
7  H u0 p0 c0 {3,S}
8  H u0 p0 c0 {3,S}
9  H u0 p0 c0 {4,S}
10 H u0 p0 c0 {4,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.85009,0.0216509,1.06222e-05,-2.54237e-08,1.01893e-11,-19062.7,11.6794], Tmin=(10,'K'), Tmax=(978.502,'K')),
            NASAPolynomial(coeffs=[5.6152,0.0261393,-1.42002e-05,3.71202e-09,-3.77779e-13,-19968.5,0.339075], Tmin=(978.502,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-158.468,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (224.491,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 2

Geometry:
O       2.30949000    0.57474300    0.14331100
O      -1.01275600   -0.27349400   -0.49215600
C      -0.23235400    1.68972200    0.63271300
C       1.29481400   -0.31244100    0.03489800
C      -0.10726200    0.33214200    0.00792300
H       0.20758600    1.68738400    1.63007300
H      -1.27744400    1.98081400    0.66719200
H       0.34397100    2.40443200    0.04357700
H       1.28928000   -0.89172700    0.97886100
H       1.39060700   -1.02831600   -0.78849100
""",
)

entry(
    index = 39,
    label = "CC(=O)CO[O]",
    molecule = 
"""
multiplicity 2
1  O u0 p2 c0 {3,S} {4,S}
2  O u0 p2 c0 {6,D}
3  O u1 p2 c0 {1,S}
4  C u0 p0 c0 {1,S} {6,S} {7,S} {8,S}
5  C u0 p0 c0 {6,S} {9,S} {10,S} {11,S}
6  C u0 p0 c0 {2,D} {4,S} {5,S}
7  H u0 p0 c0 {4,S}
8  H u0 p0 c0 {4,S}
9  H u0 p0 c0 {5,S}
10 H u0 p0 c0 {5,S}
11 H u0 p0 c0 {5,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.54336,0.0459897,-9.05516e-05,1.73105e-07,-1.38803e-10,-19166.6,12.9923], Tmin=(10,'K'), Tmax=(396.683,'K')),
            NASAPolynomial(coeffs=[3.6587,0.0365044,-2.3215e-05,7.05113e-09,-8.20616e-13,-19110.3,13.3679], Tmin=(396.683,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-159.369,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (245.277,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 2

Geometry:
O      -1.89032200   -0.77680900    0.93810900
O       1.46499000   -0.19702400   -0.10523300
O      -2.32819700    0.43065400    1.14306700
C      -0.79647200   -0.77832600    0.01595200
C       0.53264000    0.09715600    2.07459600
C       0.50980100   -0.26783100    0.61998900
H      -1.05710200   -0.16618900   -0.84516900
H      -0.66253600   -1.81511000   -0.28828000
H      -0.12240200    0.95214300    2.24698800
H       0.14025200   -0.72430400    2.67539100
H       1.55077000    0.33634700    2.36437500
""",
)

entry(
    index = 40,
    label = "C=CC=O",
    molecule = 
"""
1 O u0 p2 c0 {4,D}
2 C u0 p0 c0 {3,D} {4,S} {5,S}
3 C u0 p0 c0 {2,D} {6,S} {7,S}
4 C u0 p0 c0 {1,D} {2,S} {8,S}
5 H u0 p0 c0 {2,S}
6 H u0 p0 c0 {3,S}
7 H u0 p0 c0 {3,S}
8 H u0 p0 c0 {4,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.96417,0.00221745,7.99325e-05,-1.51838e-07,9.15799e-11,-8584.82,7.87875], Tmin=(10,'K'), Tmax=(496.886,'K')),
            NASAPolynomial(coeffs=[1.5291,0.0282333,-1.79646e-05,5.48497e-09,-6.4379e-13,-8422,17.1268], Tmin=(496.886,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-71.3893,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (178.761,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 1

Geometry:
O      -2.29403700   -0.34836600   -0.10557000
C      -0.07701200    0.26428400    0.45655200
C       1.19439100    0.21512800    0.08232400
C      -1.12390800   -0.35294600   -0.37906000
H      -0.40406100    0.74647300    1.36909600
H       1.47853700   -0.27856100   -0.84032200
H       1.98760100    0.65663700    0.66920000
H      -0.75405600   -0.83607200   -1.30466200
""",
)

entry(
    index = 41,
    label = "[CH2]CC",
    molecule = 
"""
multiplicity 2
1  C u0 p0 c0 {2,S} {3,S} {4,S} {5,S}
2  C u0 p0 c0 {1,S} {6,S} {7,S} {8,S}
3  C u1 p0 c0 {1,S} {9,S} {10,S}
4  H u0 p0 c0 {1,S}
5  H u0 p0 c0 {1,S}
6  H u0 p0 c0 {2,S}
7  H u0 p0 c0 {2,S}
8  H u0 p0 c0 {2,S}
9  H u0 p0 c0 {3,S}
10 H u0 p0 c0 {3,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.88388,0.0110432,2.97097e-05,-4.14897e-08,1.59773e-11,10928.7,9.90544], Tmin=(10,'K'), Tmax=(837.513,'K')),
            NASAPolynomial(coeffs=[1.27885,0.0300114,-1.59519e-05,4.1619e-09,-4.27278e-13,11136.2,20.6448], Tmin=(837.513,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (90.8648,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (224.491,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 2

Geometry:
C       0.14491400    0.58979200    0.05836500
C      -1.10278900   -0.27221200   -0.11114300
C       1.39797600   -0.14908300   -0.24321100
H       0.06127400    1.46987900   -0.59463500
H       0.18747400    0.99141700    1.07433600
H      -1.16924600   -0.65225100   -1.13129000
H      -2.00987000    0.29355800    0.09736000
H      -1.07231100   -1.12920200    0.56171400
H       2.35619600    0.21733000    0.09213100
H       1.38824800   -0.97333000   -0.94203800
""",
)

entry(
    index = 42,
    label = "C[CH]C",
    molecule = 
"""
multiplicity 2
1  C u0 p0 c0 {3,S} {4,S} {5,S} {6,S}
2  C u0 p0 c0 {3,S} {7,S} {8,S} {9,S}
3  C u1 p0 c0 {1,S} {2,S} {10,S}
4  H u0 p0 c0 {1,S}
5  H u0 p0 c0 {1,S}
6  H u0 p0 c0 {1,S}
7  H u0 p0 c0 {2,S}
8  H u0 p0 c0 {2,S}
9  H u0 p0 c0 {2,S}
10 H u0 p0 c0 {3,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.70594,0.0344517,-0.000167647,4.68707e-07,-4.10623e-10,9212.66,8.1926], Tmin=(10,'K'), Tmax=(420.212,'K')),
            NASAPolynomial(coeffs=[-0.199605,0.0318968,-1.66992e-05,4.21947e-09,-4.15062e-13,9891.68,27.8224], Tmin=(420.212,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (76.5885,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (224.491,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 1

Geometry:
C      -1.28478300   -0.12590500   -0.08531600
C       1.28742900   -0.02562700   -0.12531600
C      -0.01259200    0.47821300    0.38926700
H      -1.30215300   -0.19825800   -1.17635500
H      -1.41460300   -1.14960900    0.29171800
H      -2.15412200    0.44764700    0.23225300
H       1.50857500   -1.03522300    0.24721300
H       2.11877500    0.61483400    0.16491400
H       1.27617900   -0.09886400   -1.21636800
H      -0.02270500    1.09279200    1.27799000
""",
)

entry(
    index = 43,
    label = "[CH2]C=C",
    molecule = 
"""
multiplicity 2
1 C u0 p0 c0 {2,S} {3,D} {4,S}
2 C u1 p0 c0 {1,S} {5,S} {6,S}
3 C u0 p0 c0 {1,D} {7,S} {8,S}
4 H u0 p0 c0 {1,S}
5 H u0 p0 c0 {2,S}
6 H u0 p0 c0 {2,S}
7 H u0 p0 c0 {3,S}
8 H u0 p0 c0 {3,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[4.10456,-0.0105141,0.000138648,-2.61518e-07,1.64836e-10,19674.8,6.73676], Tmin=(10,'K'), Tmax=(477.934,'K')),
            NASAPolynomial(coeffs=[0.90977,0.0275956,-1.66489e-05,4.88652e-09,-5.56132e-13,19850.3,18.4324], Tmin=(477.934,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (163.581,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (178.761,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 1

Geometry:
C      -0.00652800    0.14291800    0.52026500
C      -1.21459300    0.31052600   -0.12032800
C       1.17113300   -0.18471500   -0.11426600
H       0.01873600    0.27821300    1.59613200
H      -2.11103400    0.56743800    0.42252500
H      -1.29406800    0.18726600   -1.19195300
H       1.19939900   -0.32955100   -1.18574600
H       2.09311600   -0.30639000    0.43294900
""",
)

entry(
    index = 44,
    label = "CCCO[O]",
    molecule = 
"""
multiplicity 2
1  O u0 p2 c0 {2,S} {4,S}
2  O u1 p2 c0 {1,S}
3  C u0 p0 c0 {4,S} {5,S} {6,S} {7,S}
4  C u0 p0 c0 {1,S} {3,S} {8,S} {9,S}
5  C u0 p0 c0 {3,S} {10,S} {11,S} {12,S}
6  H u0 p0 c0 {3,S}
7  H u0 p0 c0 {3,S}
8  H u0 p0 c0 {4,S}
9  H u0 p0 c0 {4,S}
10 H u0 p0 c0 {5,S}
11 H u0 p0 c0 {5,S}
12 H u0 p0 c0 {5,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.43556,0.0622833,-0.000267773,6.84139e-07,-5.93606e-10,-7433.01,11.5324], Tmin=(10,'K'), Tmax=(399.387,'K')),
            NASAPolynomial(coeffs=[1.34866,0.0401874,-2.33004e-05,6.50367e-09,-7.03449e-13,-6923.39,23.9782], Tmin=(399.387,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-61.8244,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (270.22,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 2

Geometry:
O      -2.12319400   -0.37859000    0.53269900
O      -2.61448800    0.63307600   -0.11478200
C       0.14515000    0.50445000    0.68934400
C      -0.74139300   -0.60868500    0.17321000
C       0.11483300    0.62063000    2.20770200
H      -0.17749300    1.43653700    0.22431900
H       1.16001900    0.30626400    0.33952900
H      -0.70339000   -0.69740900   -0.91131900
H      -0.50579400   -1.56655500    0.63624100
H       0.45363400   -0.30406700    2.67696200
H       0.76029900    1.42751100    2.55006800
H      -0.89569600    0.82481400    2.55946400
""",
)

entry(
    index = 45,
    label = "CC(C)O[O]",
    molecule = 
"""
multiplicity 2
1  O u0 p2 c0 {2,S} {3,S}
2  O u1 p2 c0 {1,S}
3  C u0 p0 c0 {1,S} {4,S} {5,S} {6,S}
4  C u0 p0 c0 {3,S} {7,S} {8,S} {9,S}
5  C u0 p0 c0 {3,S} {10,S} {11,S} {12,S}
6  H u0 p0 c0 {3,S}
7  H u0 p0 c0 {4,S}
8  H u0 p0 c0 {4,S}
9  H u0 p0 c0 {4,S}
10 H u0 p0 c0 {5,S}
11 H u0 p0 c0 {5,S}
12 H u0 p0 c0 {5,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.82462,0.0171308,0.000135793,-5.55929e-07,7.5704e-10,-9534.95,11.7856], Tmin=(10,'K'), Tmax=(185.238,'K')),
            NASAPolynomial(coeffs=[2.93266,0.0363919,-2.01787e-05,5.4138e-09,-5.64344e-13,-9501.9,14.5849], Tmin=(185.238,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-79.2414,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (270.22,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 2

Geometry:
O      -0.55500600   -1.49313800   -0.18668700
O      -1.71055000   -1.66924500   -0.74660000
C      -0.06020000   -0.13694900   -0.38201000
C       1.38672400   -0.16857500    0.05309800
C      -0.91852700    0.82069900    0.41470100
H      -0.15210600    0.05833500   -1.45068600
H       1.95300200   -0.89420300   -0.52765200
H       1.83225200    0.81520000   -0.08605600
H       1.45627900   -0.43250600    1.10827600
H      -0.58293000    1.84350600    0.24739300
H      -1.95879200    0.73759700    0.10780500
H      -0.84061200    0.59811300    1.47915300
""",
)

entry(
    index = 46,
    label = "[CH2]CCOO",
    molecule = 
"""
multiplicity 2
1  O u0 p2 c0 {2,S} {4,S}
2  O u0 p2 c0 {1,S} {12,S}
3  C u0 p0 c0 {4,S} {5,S} {6,S} {7,S}
4  C u0 p0 c0 {1,S} {3,S} {8,S} {9,S}
5  C u1 p0 c0 {3,S} {10,S} {11,S}
6  H u0 p0 c0 {3,S}
7  H u0 p0 c0 {3,S}
8  H u0 p0 c0 {4,S}
9  H u0 p0 c0 {4,S}
10 H u0 p0 c0 {5,S}
11 H u0 p0 c0 {5,S}
12 H u0 p0 c0 {2,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.32248,0.0649355,-0.000170577,2.93498e-07,-1.93051e-10,726.301,11.6129], Tmin=(10,'K'), Tmax=(470.072,'K')),
            NASAPolynomial(coeffs=[5.04393,0.0339601,-1.96355e-05,5.5403e-09,-6.0952e-13,744.847,6.52601], Tmin=(470.072,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (6.01766,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (266.063,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 2

Geometry:
O       0.72844000   -0.28603200    0.78333000
O       0.47112200   -1.65117700    0.48758000
C       1.36269500    0.05525900   -1.55822800
C       0.47557800    0.46318800   -0.38983700
C       2.78795000   -0.09712500   -1.16793400
H       1.24658500    0.81094000   -2.34627900
H       0.98772500   -0.87440500   -1.99421600
H      -0.58021500    0.38671600   -0.65865200
H       0.69028500    1.48699200   -0.07804700
H       3.50516900   -0.51061400   -1.85999000
H       3.15303800    0.32833500   -0.24510300
H       1.36437700   -1.98321600    0.32359300
""",
)

entry(
    index = 47,
    label = "[CH2]OC=C",
    molecule = 
"""
multiplicity 2
1 O u0 p2 c0 {2,S} {4,S}
2 C u0 p0 c0 {1,S} {3,D} {5,S}
3 C u0 p0 c0 {2,D} {6,S} {7,S}
4 C u1 p0 c0 {1,S} {8,S} {9,S}
5 H u0 p0 c0 {2,S}
6 H u0 p0 c0 {3,S}
7 H u0 p0 c0 {3,S}
8 H u0 p0 c0 {4,S}
9 H u0 p0 c0 {4,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.91533,0.0056364,0.000105803,-2.45063e-07,1.73544e-10,8000.14,11.0326], Tmin=(10,'K'), Tmax=(465.583,'K')),
            NASAPolynomial(coeffs=[3.20126,0.027815,-1.73405e-05,5.27886e-09,-6.2162e-13,7892.74,12.0643], Tmin=(465.583,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (66.5026,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (199.547,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 2

Geometry:
O      -0.42864900    0.24471800   -1.21834500
C       0.42322500   -0.51227100   -0.47478900
C       0.09528300   -1.47552100    0.37318200
C      -1.75030200    0.21097000   -0.92819100
H       1.44622800   -0.22894000   -0.67690700
H      -0.92461900   -1.78576600    0.54144600
H       0.88211100   -1.99191700    0.89970300
H      -2.34714700    0.78905400   -1.61300500
H      -2.03249500    0.08635400    0.10820400
""",
)

entry(
    index = 48,
    label = "[CH2]CCC",
    molecule = 
"""
multiplicity 2
1  C u0 p0 c0 {2,S} {3,S} {5,S} {6,S}
2  C u0 p0 c0 {1,S} {4,S} {7,S} {8,S}
3  C u0 p0 c0 {1,S} {9,S} {10,S} {11,S}
4  C u1 p0 c0 {2,S} {12,S} {13,S}
5  H u0 p0 c0 {1,S}
6  H u0 p0 c0 {1,S}
7  H u0 p0 c0 {2,S}
8  H u0 p0 c0 {2,S}
9  H u0 p0 c0 {3,S}
10 H u0 p0 c0 {3,S}
11 H u0 p0 c0 {3,S}
12 H u0 p0 c0 {4,S}
13 H u0 p0 c0 {4,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.80879,0.0249051,1.06202e-05,-2.10531e-08,7.11227e-12,8157.81,10.9521], Tmin=(10,'K'), Tmax=(1146.6,'K')),
            NASAPolynomial(coeffs=[5.20528,0.032478,-1.55671e-05,3.63882e-09,-3.35374e-13,7019.53,0.456593], Tmin=(1146.6,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (67.8409,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (295.164,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 2

Geometry:
C      -0.34849800    0.85286900    0.15511300
C       0.83477700   -0.11611100    0.21987900
C      -1.60583900    0.19747700   -0.40275900
C       0.61256100   -1.23824300    1.16914500
H      -0.54576100    1.23627900    1.15958900
H      -0.07647600    1.71303100   -0.45893100
H       1.03958900   -0.50843100   -0.77997000
H       1.73383900    0.44574700    0.50898600
H      -1.42916300   -0.17350000   -1.41382700
H      -2.43873700    0.89860800   -0.44283500
H      -1.90625800   -0.65204200    0.21167100
H       1.07163500   -2.20331600    1.02087700
H       0.12820400   -1.05170700    2.11768300
""",
)

entry(
    index = 49,
    label = "C[CH]CC",
    molecule = 
"""
multiplicity 2
1  C u0 p0 c0 {2,S} {4,S} {5,S} {6,S}
2  C u0 p0 c0 {1,S} {7,S} {8,S} {9,S}
3  C u0 p0 c0 {4,S} {10,S} {11,S} {12,S}
4  C u1 p0 c0 {1,S} {3,S} {13,S}
5  H u0 p0 c0 {1,S}
6  H u0 p0 c0 {1,S}
7  H u0 p0 c0 {2,S}
8  H u0 p0 c0 {2,S}
9  H u0 p0 c0 {2,S}
10 H u0 p0 c0 {3,S}
11 H u0 p0 c0 {3,S}
12 H u0 p0 c0 {3,S}
13 H u0 p0 c0 {4,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.50824,0.0552645,-0.000245042,6.46503e-07,-5.56306e-10,6605.63,10.7859], Tmin=(10,'K'), Tmax=(416.747,'K')),
            NASAPolynomial(coeffs=[-0.428801,0.043386,-2.35217e-05,6.16955e-09,-6.30671e-13,7365.08,31.5085], Tmin=(416.747,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (54.9057,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (295.164,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 2

Geometry:
C       0.61193900    0.10621400   -0.41049700
C       1.92076800    0.54505600    0.23643600
C      -1.41583100   -1.45556700   -0.06870700
C      -0.04255000   -1.02466300    0.30069100
H       0.79999000   -0.16971100   -1.45887600
H      -0.08318900    0.95174700   -0.46171500
H       2.63350800   -0.28017200    0.25794200
H       1.75204400    0.86545800    1.26468300
H       2.37876300    1.37057600   -0.30672500
H      -1.83054500   -2.16088200    0.64969600
H      -2.09186600   -0.59886400   -0.13634100
H      -1.43836400   -1.94285100   -1.05295400
H       0.57523600   -1.68117700    0.89997700
""",
)

entry(
    index = 50,
    label = "CCCCO[O]",
    molecule = 
"""
multiplicity 2
1  O u0 p2 c0 {2,S} {5,S}
2  O u1 p2 c0 {1,S}
3  C u0 p0 c0 {4,S} {5,S} {9,S} {10,S}
4  C u0 p0 c0 {3,S} {6,S} {7,S} {8,S}
5  C u0 p0 c0 {1,S} {3,S} {11,S} {12,S}
6  C u0 p0 c0 {4,S} {13,S} {14,S} {15,S}
7  H u0 p0 c0 {4,S}
8  H u0 p0 c0 {4,S}
9  H u0 p0 c0 {3,S}
10 H u0 p0 c0 {3,S}
11 H u0 p0 c0 {5,S}
12 H u0 p0 c0 {5,S}
13 H u0 p0 c0 {6,S}
14 H u0 p0 c0 {6,S}
15 H u0 p0 c0 {6,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.17192,0.0926478,-0.000429304,1.12723e-06,-1.00726e-09,-10157.5,12.6969], Tmin=(10,'K'), Tmax=(384.89,'K')),
            NASAPolynomial(coeffs=[0.657057,0.0548781,-3.30523e-05,9.49454e-09,-1.05021e-12,-9490.54,28.5776], Tmin=(384.89,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-84.4944,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (340.893,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 2

Geometry:
O       1.97550700    0.71421000    0.73453300
O       3.20617700    0.57424300    1.12127800
C       1.52352000   -1.66896400    0.47767800
C       0.47298600   -1.72674000    1.58031700
C       1.60052800   -0.32042100   -0.20410800
C       0.42383300   -3.09398700    2.24899900
H       0.69104900   -0.95801900    2.32361900
H      -0.50581900   -1.48367600    1.15865800
H       1.30524400   -2.41874900   -0.28713200
H       2.50989900   -1.90468900    0.88219600
H       2.33608600   -0.30549400   -1.00680600
H       0.63071600    0.00463600   -0.57959100
H      -0.32874400   -3.12647000    3.03547900
H       1.38744700   -3.33978200    2.69679400
H       0.18626600   -3.87417700    1.52429900
""",
)

entry(
    index = 51,
    label = "CCC(C)O[O]",
    molecule = 
"""
multiplicity 2
1  O u0 p2 c0 {2,S} {3,S}
2  O u1 p2 c0 {1,S}
3  C u0 p0 c0 {1,S} {4,S} {5,S} {7,S}
4  C u0 p0 c0 {3,S} {6,S} {8,S} {9,S}
5  C u0 p0 c0 {3,S} {13,S} {14,S} {15,S}
6  C u0 p0 c0 {4,S} {10,S} {11,S} {12,S}
7  H u0 p0 c0 {3,S}
8  H u0 p0 c0 {4,S}
9  H u0 p0 c0 {4,S}
10 H u0 p0 c0 {6,S}
11 H u0 p0 c0 {6,S}
12 H u0 p0 c0 {6,S}
13 H u0 p0 c0 {5,S}
14 H u0 p0 c0 {5,S}
15 H u0 p0 c0 {5,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.4814,0.0505958,-8.60664e-05,1.79225e-07,-1.44601e-10,-12046.2,12.764], Tmin=(10,'K'), Tmax=(450.918,'K')),
            NASAPolynomial(coeffs=[1.29408,0.0519802,-3.07312e-05,8.79432e-09,-9.76457e-13,-11665.8,23.6057], Tmin=(450.918,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-100.173,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (340.893,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 2

Geometry:
O      -0.41962800    1.49101600    0.23024000
O      -1.14522800    2.10058900    1.11419400
C      -0.47909500    0.04323100    0.38087900
C       0.64063400   -0.49327900   -0.48894300
C      -1.86311200   -0.43376800   -0.00056700
C       0.77292100   -2.00817700   -0.39185200
H      -0.28090300   -0.15405000    1.43618800
H       0.45139700   -0.19366400   -1.52207500
H       1.57176800   -0.01479300   -0.18250900
H      -0.10358200   -2.51293900   -0.79622400
H       0.89465800   -2.32464700    0.64520800
H       1.64083300   -2.35443600   -0.94979100
H      -2.04136200   -0.26797200   -1.06376100
H      -1.96722500   -1.49670000    0.21084800
H      -2.61034400    0.10702900    0.57624000
""",
)

entry(
    index = 52,
    label = "CCC(C)OO",
    molecule = 
"""
1  O u0 p2 c0 {2,S} {3,S}
2  O u0 p2 c0 {1,S} {16,S}
3  C u0 p0 c0 {1,S} {4,S} {5,S} {7,S}
4  C u0 p0 c0 {3,S} {6,S} {8,S} {9,S}
5  C u0 p0 c0 {3,S} {13,S} {14,S} {15,S}
6  C u0 p0 c0 {4,S} {10,S} {11,S} {12,S}
7  H u0 p0 c0 {3,S}
8  H u0 p0 c0 {4,S}
9  H u0 p0 c0 {4,S}
10 H u0 p0 c0 {6,S}
11 H u0 p0 c0 {6,S}
12 H u0 p0 c0 {6,S}
13 H u0 p0 c0 {5,S}
14 H u0 p0 c0 {5,S}
15 H u0 p0 c0 {5,S}
16 H u0 p0 c0 {2,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.25102,0.0758211,-0.000241171,5.48415e-07,-4.3885e-10,-27898.1,12.6011], Tmin=(10,'K'), Tmax=(433.347,'K')),
            NASAPolynomial(coeffs=[0.773753,0.0573453,-3.41156e-05,9.72621e-09,-1.07163e-12,-27295.2,26.9599], Tmin=(433.347,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-231.975,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (361.68,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 2

Geometry:
O      -0.98201500    0.51523700    1.42258000
O       0.14514500    1.21001800    1.94087900
C      -0.76506400    0.29886900    0.03043900
C      -1.85367300   -0.68569900   -0.36720500
C      -0.81173200    1.60337800   -0.74214800
C      -1.75580400   -1.11658500   -1.82548600
H       0.21680800   -0.17124200   -0.08645400
H      -1.77563800   -1.55403000    0.28775400
H      -2.82485000   -0.22471000   -0.17245200
H      -0.76269800   -1.50814500   -2.05142600
H      -2.48001900   -1.89939600   -2.04449900
H      -1.95152000   -0.28708800   -2.50399600
H      -0.08048100    2.30481300   -0.34475100
H      -0.57608100    1.43950800   -1.79276100
H      -1.80729700    2.04561000   -0.67285100
H      -0.23849900    2.06719200    2.15832400
""",
)

entry(
    index = 53,
    label = "C=CCC",
    molecule = 
"""
1  C u0 p0 c0 {2,S} {3,S} {5,S} {6,S}
2  C u0 p0 c0 {1,S} {7,S} {8,S} {9,S}
3  C u0 p0 c0 {1,S} {4,D} {10,S}
4  C u0 p0 c0 {3,D} {11,S} {12,S}
5  H u0 p0 c0 {1,S}
6  H u0 p0 c0 {1,S}
7  H u0 p0 c0 {2,S}
8  H u0 p0 c0 {2,S}
9  H u0 p0 c0 {2,S}
10 H u0 p0 c0 {3,S}
11 H u0 p0 c0 {4,S}
12 H u0 p0 c0 {4,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.91053,0.0163679,2.97506e-05,-4.05578e-08,1.41005e-11,-802.294,7.56169], Tmin=(10,'K'), Tmax=(1008.54,'K')),
            NASAPolynomial(coeffs=[2.93143,0.034181,-1.74608e-05,4.34504e-09,-4.24913e-13,-1313.24,8.78142], Tmin=(1008.54,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-6.63394,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (274.378,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 1

Geometry:
C      -0.42028600    0.09135700   -0.56273700
C      -1.62860000    0.17668000    0.35634600
C       0.77261200   -0.60522600    0.02261900
C       0.85044300   -1.13242900    1.23503500
H      -0.69489400   -0.41930900   -1.49039600
H      -0.11498700    1.09629300   -0.86873900
H      -1.97519100   -0.81728200    0.64028500
H      -2.45169800    0.69265000   -0.13535800
H      -1.38756800    0.72037100    1.27013100
H       1.63904100   -0.66956700   -0.62867900
H       1.75438600   -1.61815300    1.57586400
H       0.02095200   -1.09998000    1.92957200
""",
)

entry(
    index = 54,
    label = "CC=CC",
    molecule = 
"""
1  C u0 p0 c0 {3,S} {5,S} {6,S} {7,S}
2  C u0 p0 c0 {4,S} {8,S} {9,S} {10,S}
3  C u0 p0 c0 {1,S} {4,D} {11,S}
4  C u0 p0 c0 {2,S} {3,D} {12,S}
5  H u0 p0 c0 {1,S}
6  H u0 p0 c0 {1,S}
7  H u0 p0 c0 {1,S}
8  H u0 p0 c0 {2,S}
9  H u0 p0 c0 {2,S}
10 H u0 p0 c0 {2,S}
11 H u0 p0 c0 {3,S}
12 H u0 p0 c0 {4,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.74184,0.0195484,2.11149e-05,-3.53979e-08,1.43909e-11,-2327.06,7.76064], Tmin=(10,'K'), Tmax=(682.5,'K')),
            NASAPolynomial(coeffs=[0.498453,0.038557,-2.06613e-05,5.40848e-09,-5.56193e-13,-1884.33,22.1692], Tmin=(682.5,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-19.3863,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (274.378,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 1

Geometry:
C       1.46994000    0.43025100    0.14941500
C      -1.48747100   -2.11625100    0.00253000
C       0.61581700   -0.76576000   -0.13127400
C      -0.63335100   -0.92023800    0.28319500
H       0.93022900    1.16638800    0.74386200
H       2.37422500    0.14861000    0.69210400
H       1.79272500    0.90870600   -0.77711300
H      -2.39176100   -1.83462800   -0.54016200
H      -0.94775600   -2.85240000   -0.59189700
H      -1.81025800   -2.59467800    0.92907300
H       1.06910200   -1.55870400   -0.72086800
H      -1.08663800   -0.12729200    0.87278600
""",
)

entry(
    index = 55,
    label = "C=C[CH]C",
    molecule = 
"""
multiplicity 2
1  C u0 p0 c0 {2,S} {5,S} {6,S} {7,S}
2  C u1 p0 c0 {1,S} {3,S} {8,S}
3  C u0 p0 c0 {2,S} {4,D} {9,S}
4  C u0 p0 c0 {3,D} {10,S} {11,S}
5  H u0 p0 c0 {1,S}
6  H u0 p0 c0 {1,S}
7  H u0 p0 c0 {1,S}
8  H u0 p0 c0 {2,S}
9  H u0 p0 c0 {3,S}
10 H u0 p0 c0 {4,S}
11 H u0 p0 c0 {4,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.84178,0.0173467,2.34309e-05,-3.57119e-08,1.31791e-11,15281.1,8.16724], Tmin=(10,'K'), Tmax=(946.788,'K')),
            NASAPolynomial(coeffs=[2.58759,0.0328901,-1.74252e-05,4.48494e-09,-4.52629e-13,15059.4,11.7245], Tmin=(946.788,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (127.064,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (249.434,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 1

Geometry:
C      -1.75448900    0.02824600   -0.17491900
C      -0.33574500    0.47613700   -0.12947200
C       0.74391800   -0.37365700   -0.00301800
C       2.06030400    0.02731500    0.04056700
H      -2.33728500    0.46903000    0.63817700
H      -1.82883800   -1.05563300   -0.09649500
H      -2.23952200    0.33620600   -1.10493400
H      -0.14314100    1.54133800   -0.20057000
H       0.53366100   -1.43726200    0.06694100
H       2.86384500   -0.68568200    0.14081800
H       2.32326500    1.07435500   -0.02517800
""",
)

entry(
    index = 56,
    label = "[CH]=CCC",
    molecule = 
"""
multiplicity 2
1  C u0 p0 c0 {2,S} {3,S} {5,S} {6,S}
2  C u0 p0 c0 {1,S} {7,S} {8,S} {9,S}
3  C u0 p0 c0 {1,S} {4,D} {10,S}
4  C u1 p0 c0 {3,D} {11,S}
5  H u0 p0 c0 {1,S}
6  H u0 p0 c0 {1,S}
7  H u0 p0 c0 {2,S}
8  H u0 p0 c0 {2,S}
9  H u0 p0 c0 {2,S}
10 H u0 p0 c0 {3,S}
11 H u0 p0 c0 {4,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.70739,0.023198,9.23633e-06,-2.81797e-08,1.43868e-11,28010.7,9.2358], Tmin=(10,'K'), Tmax=(555.284,'K')),
            NASAPolynomial(coeffs=[2.29022,0.0334066,-1.83404e-05,4.92848e-09,-5.19201e-13,28168,15.2391], Tmin=(555.284,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (232.852,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (249.434,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 1

Geometry:
C      -0.01934600    0.44023400   -0.15101700
C      -1.42973400    0.05673700   -0.57164500
C       0.98304100   -0.66931700   -0.32294400
C       0.71710000   -1.86117000   -0.78377100
H      -0.00832800    0.75512500    0.89585600
H       0.32447300    1.30647400   -0.72255200
H      -2.11954700    0.88740700   -0.43036300
H      -1.45127900   -0.23482300   -1.62171700
H      -1.78711000   -0.79150900    0.01220600
H       2.01002200   -0.43800100   -0.03300400
H       1.26581200   -2.76705800   -0.97968900
""",
)

entry(
    index = 57,
    label = "C=CC=C",
    molecule = 
"""
1  C u0 p0 c0 {2,S} {3,D} {5,S}
2  C u0 p0 c0 {1,S} {4,D} {6,S}
3  C u0 p0 c0 {1,D} {7,S} {8,S}
4  C u0 p0 c0 {2,D} {9,S} {10,S}
5  H u0 p0 c0 {1,S}
6  H u0 p0 c0 {2,S}
7  H u0 p0 c0 {3,S}
8  H u0 p0 c0 {3,S}
9  H u0 p0 c0 {4,S}
10 H u0 p0 c0 {4,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.95498,0.00258436,9.63778e-05,-1.65535e-07,8.89568e-11,12751.2,6.90009], Tmin=(10,'K'), Tmax=(560.45,'K')),
            NASAPolynomial(coeffs=[-0.0673708,0.039963,-2.68697e-05,8.67532e-09,-1.06653e-12,13065.9,22.7617], Tmin=(560.45,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (105.999,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (228.648,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 1

Geometry:
C      -0.16167000   -0.61652600   -0.49564800
C       0.17259400    0.00981200    0.77717200
C      -1.40644900   -0.82421600   -0.91222600
C       1.41736700    0.21726900    1.19385600
H       0.67436200   -0.92038500   -1.11769300
H      -0.66343500    0.31362900    1.39922700
H      -2.25451000   -0.52854800   -0.30665800
H      -1.61670200   -1.29236100   -1.86332800
H       1.62752700    0.68499300    2.14518400
H       2.26548900   -0.07842800    0.58833000
""",
)

entry(
    index = 58,
    label = "CC1CCO1",
    molecule = 
"""
1  O u0 p2 c0 {2,S} {4,S}
2  C u0 p0 c0 {1,S} {3,S} {5,S} {6,S}
3  C u0 p0 c0 {2,S} {4,S} {7,S} {8,S}
4  C u0 p0 c0 {1,S} {3,S} {9,S} {10,S}
5  C u0 p0 c0 {2,S} {11,S} {12,S} {13,S}
6  H u0 p0 c0 {2,S}
7  H u0 p0 c0 {3,S}
8  H u0 p0 c0 {3,S}
9  H u0 p0 c0 {4,S}
10 H u0 p0 c0 {4,S}
11 H u0 p0 c0 {5,S}
12 H u0 p0 c0 {5,S}
13 H u0 p0 c0 {5,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[4.08113,0.00635014,7.81974e-05,-9.91362e-08,3.71181e-11,-16551.1,9.61234], Tmin=(10,'K'), Tmax=(887.562,'K')),
            NASAPolynomial(coeffs=[0.634129,0.0444107,-2.41951e-05,6.36769e-09,-6.53542e-13,-16826.5,20.8327], Tmin=(887.562,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-137.533,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (307.635,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 2

Geometry:
O      -0.28603500   -0.75453000   -1.09452900
C       0.41429500   -0.45224400    0.12867800
C      -0.80997500    0.29307700    0.68540100
C      -1.52397200   -0.28148500   -0.54408300
C       1.67987800    0.32707800   -0.11336700
H       0.62904200   -1.37636900    0.67423600
H      -1.17671400   -0.01704300    1.65928300
H      -0.69409000    1.37463700    0.66019800
H      -2.20398300   -1.10715600   -0.32279100
H      -2.02005100    0.42740500   -1.20643800
H       2.15717600    0.58098600    0.83410300
H       1.45491800    1.24662200   -0.65375100
H       2.37951300   -0.26097900   -0.70694000
""",
)

entry(
    index = 59,
    label = "C[CH]CCOO",
    molecule = 
"""
multiplicity 2
1  O u0 p2 c0 {2,S} {4,S}
2  O u0 p2 c0 {1,S} {15,S}
3  C u0 p0 c0 {4,S} {6,S} {7,S} {8,S}
4  C u0 p0 c0 {1,S} {3,S} {9,S} {10,S}
5  C u0 p0 c0 {6,S} {11,S} {12,S} {13,S}
6  C u1 p0 c0 {3,S} {5,S} {14,S}
7  H u0 p0 c0 {3,S}
8  H u0 p0 c0 {3,S}
9  H u0 p0 c0 {4,S}
10 H u0 p0 c0 {4,S}
11 H u0 p0 c0 {5,S}
12 H u0 p0 c0 {5,S}
13 H u0 p0 c0 {5,S}
14 H u0 p0 c0 {6,S}
15 H u0 p0 c0 {2,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[2.95773,0.103428,-0.000375567,7.72951e-07,-5.68386e-10,-3525.41,13.2308], Tmin=(10,'K'), Tmax=(445.188,'K')),
            NASAPolynomial(coeffs=[3.56389,0.0492714,-2.89695e-05,8.14853e-09,-8.86299e-13,-3096.68,16.2183], Tmin=(445.188,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-29.3334,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (336.736,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 2

Geometry:
O       0.47056100   -1.03677600   -0.19313000
O       1.31162300   -1.92733900    0.52401200
C       1.39712400    0.80647300    1.14114600
C       1.11255200    0.22351400   -0.24125800
C      -1.13207100    1.06610300    1.62888000
C       0.23975500    0.70261700    2.07543200
H       1.68114100    1.85824000    0.98869000
H       2.27175100    0.31632100    1.56785400
H       2.03573700    0.14857900   -0.82025400
H       0.40170700    0.84115300   -0.79295900
H      -1.17254600    2.10135600    1.26526500
H      -1.85674400    0.97274900    2.43476300
H      -1.46026800    0.43179200    0.80126900
H       0.44561000    0.62716800    3.13391800
H       0.92374100   -1.88343400    1.40903300
""",
)

entry(
    index = 60,
    label = "[CH2]CCCOO",
    molecule = 
"""
multiplicity 2
1  O u0 p2 c0 {2,S} {5,S}
2  O u0 p2 c0 {1,S} {15,S}
3  C u0 p0 c0 {4,S} {5,S} {7,S} {8,S}
4  C u0 p0 c0 {3,S} {6,S} {9,S} {10,S}
5  C u0 p0 c0 {1,S} {3,S} {11,S} {12,S}
6  C u1 p0 c0 {4,S} {13,S} {14,S}
7  H u0 p0 c0 {3,S}
8  H u0 p0 c0 {3,S}
9  H u0 p0 c0 {4,S}
10 H u0 p0 c0 {4,S}
11 H u0 p0 c0 {5,S}
12 H u0 p0 c0 {5,S}
13 H u0 p0 c0 {6,S}
14 H u0 p0 c0 {6,S}
15 H u0 p0 c0 {2,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[2.9507,0.112027,-0.000477035,1.10007e-06,-8.94214e-10,-2113.17,12.6756], Tmin=(10,'K'), Tmax=(404.244,'K')),
            NASAPolynomial(coeffs=[3.52177,0.0487766,-2.86013e-05,8.04624e-09,-8.75719e-13,-1688.71,16.2589], Tmin=(404.244,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-17.6027,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (336.736,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 2

Geometry:
O       0.88087600   -1.48755300   -0.59240600
O       0.35342000   -1.93279200    0.65351900
C       0.64989300    0.83598100    0.13440100
C      -0.51386800    1.08833400   -0.82771300
C       1.56820400   -0.27221600   -0.34915900
C      -0.06856900    1.58252800   -2.15704900
H       0.26821500    0.57559300    1.12119700
H       1.24633000    1.74550600    0.24540900
H      -1.08816500    0.16813300   -0.94026000
H      -1.19026200    1.81666200   -0.36152000
H       2.38302700   -0.44702900    0.35901200
H       1.99052900   -0.02886900   -1.32656800
H       0.67543500    2.36497200   -2.22052100
H      -0.57381900    1.29555400   -3.06576500
H       0.88352100   -2.72310600    0.80767800
""",
)

entry(
    index = 61,
    label = "[CH2]CC(C)OO",
    molecule = 
"""
multiplicity 2
1  O u0 p2 c0 {2,S} {3,S}
2  O u0 p2 c0 {1,S} {15,S}
3  C u0 p0 c0 {1,S} {4,S} {5,S} {7,S}
4  C u0 p0 c0 {3,S} {6,S} {8,S} {9,S}
5  C u0 p0 c0 {3,S} {10,S} {11,S} {12,S}
6  C u1 p0 c0 {4,S} {13,S} {14,S}
7  H u0 p0 c0 {3,S}
8  H u0 p0 c0 {4,S}
9  H u0 p0 c0 {4,S}
10 H u0 p0 c0 {5,S}
11 H u0 p0 c0 {5,S}
12 H u0 p0 c0 {5,S}
13 H u0 p0 c0 {6,S}
14 H u0 p0 c0 {6,S}
15 H u0 p0 c0 {2,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.06931,0.103042,-0.000477462,1.21405e-06,-1.0637e-09,-3973.58,12.793], Tmin=(10,'K'), Tmax=(385.968,'K')),
            NASAPolynomial(coeffs=[1.58991,0.0534395,-3.2334e-05,9.31373e-09,-1.03212e-12,-3375.71,24.7875], Tmin=(385.968,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-33.0797,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (336.736,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 2

Geometry:
O       1.84796300   -0.19569800    0.35418800
O       2.02059900   -1.56562700    0.01078500
C       0.54553300    0.19757900   -0.06059500
C      -0.53583900   -0.45619200    0.80117100
C       0.54544000    1.70848700    0.04955500
C      -1.90397000   -0.17667300    0.29676400
H       0.41383900   -0.10995100   -1.10270300
H      -0.34463200   -1.53616000    0.79876400
H      -0.41924300   -0.10889900    1.83003200
H      -0.42699700    2.09710100   -0.24984500
H       0.73507700    2.00681500    1.08125100
H       1.31496500    2.14063600   -0.58668600
H      -2.14195700   -0.35358300   -0.74236800
H      -2.70903700    0.09334100    0.96063400
H       2.12218800   -1.97009300    0.87980900
""",
)

entry(
    index = 62,
    label = "CC(CCOO)O[O]",
    molecule = 
"""
multiplicity 2
1  O u0 p2 c0 {3,S} {7,S}
2  O u0 p2 c0 {4,S} {5,S}
3  O u0 p2 c0 {1,S} {17,S}
4  O u1 p2 c0 {2,S}
5  C u0 p0 c0 {2,S} {6,S} {8,S} {9,S}
6  C u0 p0 c0 {5,S} {7,S} {10,S} {11,S}
7  C u0 p0 c0 {1,S} {6,S} {12,S} {13,S}
8  C u0 p0 c0 {5,S} {14,S} {15,S} {16,S}
9  H u0 p0 c0 {5,S}
10 H u0 p0 c0 {6,S}
11 H u0 p0 c0 {6,S}
12 H u0 p0 c0 {7,S}
13 H u0 p0 c0 {7,S}
14 H u0 p0 c0 {8,S}
15 H u0 p0 c0 {8,S}
16 H u0 p0 c0 {8,S}
17 H u0 p0 c0 {3,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.11979,0.0903639,-0.000219658,4.46828e-07,-3.67231e-10,-22118.9,29.7936], Tmin=(10,'K'), Tmax=(377.315,'K')),
            NASAPolynomial(coeffs=[4.20953,0.0620523,-4.04819e-05,1.25289e-08,-1.47814e-12,-22081.8,27.1792], Tmin=(377.315,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-183.918,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (390.78,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 2

Geometry:
O       1.38364900   -1.20753200    1.73190100
O      -1.88906300   -2.02395400    1.47724000
O       1.54976200   -1.16145000    3.13717400
O      -1.49415500   -1.58802700    2.63328800
C      -1.10682700   -1.48696100    0.37132500
C       0.10206400   -2.38197200    0.13608900
C       0.98454600   -2.51754600    1.36264700
C      -2.04377900   -1.43329100   -0.81356700
H      -0.78663900   -0.49726400    0.68966600
H       0.67448300   -1.94912100   -0.68690200
H      -0.22903600   -3.37309800   -0.18121300
H       0.43202200   -2.96861300    2.18631400
H       1.86071600   -3.13620000    1.15492400
H      -2.41469000   -2.43028400   -1.05087200
H      -2.89190700   -0.78323900   -0.60901400
H      -1.51057600   -1.04883900   -1.68176800
H       0.64935300   -0.94061600    3.41836400
""",
)

entry(
    index = 63,
    label = "CC(CCO[O])OO",
    molecule = 
"""
multiplicity 2
1  O u0 p2 c0 {3,S} {5,S}
2  O u0 p2 c0 {4,S} {7,S}
3  O u0 p2 c0 {1,S} {17,S}
4  O u1 p2 c0 {2,S}
5  C u0 p0 c0 {1,S} {6,S} {8,S} {9,S}
6  C u0 p0 c0 {5,S} {7,S} {10,S} {11,S}
7  C u0 p0 c0 {2,S} {6,S} {12,S} {13,S}
8  C u0 p0 c0 {5,S} {14,S} {15,S} {16,S}
9  H u0 p0 c0 {5,S}
10 H u0 p0 c0 {6,S}
11 H u0 p0 c0 {6,S}
12 H u0 p0 c0 {7,S}
13 H u0 p0 c0 {7,S}
14 H u0 p0 c0 {8,S}
15 H u0 p0 c0 {8,S}
16 H u0 p0 c0 {8,S}
17 H u0 p0 c0 {3,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[2.67134,0.141695,-0.000576677,1.33151e-06,-1.11713e-09,-21667.8,28.8246], Tmin=(10,'K'), Tmax=(379.604,'K')),
            NASAPolynomial(coeffs=[5.36273,0.0593912,-3.82985e-05,1.16501e-08,-1.351e-12,-21483.4,23.5664], Tmin=(379.604,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-180.196,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (382.466,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 2

Geometry:
O      -1.52569000   -0.43290500   -0.38907600
O      -1.83135500   -0.88298000    4.01265100
O      -1.35069800   -1.69588100   -1.02044800
O      -0.76485600   -0.24062900    4.37703600
C      -2.03565400   -0.66252400    0.92066000
C      -0.99916800   -1.40483800    1.75562100
C      -1.51722300   -1.93810000    3.07255100
C      -2.38009200    0.71966900    1.44062400
H      -2.94203000   -1.27317200    0.83115500
H      -0.64700500   -2.25816300    1.17541000
H      -0.14222400   -0.75595000    1.94322500
H      -0.78254500   -2.58016000    3.55519100
H      -2.45843800   -2.47587300    2.95961100
H      -3.04436500    1.22614900    0.74264800
H      -1.47294200    1.31238000    1.55759600
H      -2.86997800    0.64966200    2.40882500
H      -2.02013500   -1.65108200   -1.71277800
""",
)

entry(
    index = 64,
    label = "CC(C[CH]OO)OO",
    molecule = 
"""
multiplicity 2
1  O u0 p2 c0 {3,S} {5,S}
2  O u0 p2 c0 {4,S} {8,S}
3  O u0 p2 c0 {1,S} {17,S}
4  O u0 p2 c0 {2,S} {16,S}
5  C u0 p0 c0 {1,S} {6,S} {7,S} {9,S}
6  C u0 p0 c0 {5,S} {8,S} {10,S} {11,S}
7  C u0 p0 c0 {5,S} {12,S} {13,S} {14,S}
8  C u1 p0 c0 {2,S} {6,S} {15,S}
9  H u0 p0 c0 {5,S}
10 H u0 p0 c0 {6,S}
11 H u0 p0 c0 {6,S}
12 H u0 p0 c0 {7,S}
13 H u0 p0 c0 {7,S}
14 H u0 p0 c0 {7,S}
15 H u0 p0 c0 {8,S}
16 H u0 p0 c0 {4,S}
17 H u0 p0 c0 {3,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[2.96353,0.111698,-0.000441389,1.0726e-06,-9.24596e-10,-16047.3,57.4649], Tmin=(10,'K'), Tmax=(386.84,'K')),
            NASAPolynomial(coeffs=[2.3619,0.0629155,-3.89507e-05,1.14898e-08,-1.30169e-12,-15589.2,65.1154], Tmin=(386.84,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-133.461,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (394.937,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 2

Geometry:
O       0.83830000   -3.59618900    1.90636100
O       0.20352600   -1.05680100    5.17175600
O       2.25404600   -3.54642100    2.01549100
O      -0.30644500   -1.67464200    6.34115600
C       0.36899000   -2.27327900    1.66705800
C       0.64175900   -1.36055300    2.85998400
C      -1.10574700   -2.43977800    1.35749600
C       0.06962300   -1.91048700    4.11651600
H       0.89749200   -1.88012200    0.79528700
H       0.21436200   -0.37525800    2.65705300
H       1.72370500   -1.21269100    2.95458100
H      -1.23894400   -3.08967300    0.49507600
H      -1.54659500   -1.46816300    1.13878900
H      -1.62903700   -2.87211600    2.20946600
H       0.10778300   -2.96450000    4.36183300
H      -1.21541900   -1.34788500    6.35494000
H       2.38542800   -3.69356600    2.96042400
""",
)

entry(
    index = 65,
    label = "C[C](CCOO)OO",
    molecule = 
"""
multiplicity 2
1  O u0 p2 c0 {3,S} {6,S}
2  O u0 p2 c0 {4,S} {8,S}
3  O u0 p2 c0 {1,S} {16,S}
4  O u0 p2 c0 {2,S} {17,S}
5  C u0 p0 c0 {6,S} {8,S} {9,S} {10,S}
6  C u0 p0 c0 {1,S} {5,S} {11,S} {12,S}
7  C u0 p0 c0 {8,S} {13,S} {14,S} {15,S}
8  C u1 p0 c0 {2,S} {5,S} {7,S}
9  H u0 p0 c0 {5,S}
10 H u0 p0 c0 {5,S}
11 H u0 p0 c0 {6,S}
12 H u0 p0 c0 {6,S}
13 H u0 p0 c0 {7,S}
14 H u0 p0 c0 {7,S}
15 H u0 p0 c0 {7,S}
16 H u0 p0 c0 {3,S}
17 H u0 p0 c0 {4,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[2.80896,0.133332,-0.000658655,1.69614e-06,-1.49323e-09,-17906.4,72.6752], Tmin=(10,'K'), Tmax=(384.722,'K')),
            NASAPolynomial(coeffs=[0.704847,0.0647797,-3.87975e-05,1.10604e-08,-1.21348e-12,-17075.2,89.514], Tmin=(384.722,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-148.94,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (403.252,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 2

Geometry:
O       3.11748900    1.17269600   -2.70578700
O       3.95988100    1.68230200   -0.06377500
O       3.07755900   -0.07554000   -2.02663500
O       4.84476900    2.47264500   -0.84297000
C       2.14961400    2.88011900   -1.22582000
C       1.93549600    1.90511400   -2.39234200
C       1.84957100    1.43326200    0.92399100
C       2.69586400    2.24176700    0.00668400
H       1.18995100    3.33675100   -0.97980800
H       2.81336600    3.68073900   -1.55269800
H       1.68908600    2.45634500   -3.30090500
H       1.14118900    1.18844800   -2.18696000
H       2.38117600    1.23042400    1.85291400
H       1.56925900    0.46855000    0.48073000
H       0.93265600    1.97258000    1.15593400
H       3.56261100    0.12453900   -1.20956700
H       4.66462700    2.13366200   -1.73660800
""",
)

entry(
    index = 66,
    label = "C[C]C",
    molecule = 
"""
multiplicity 3
1 C u0 p0 c0 {3,S} {4,S} {5,S} {6,S}
2 C u0 p0 c0 {3,S} {7,S} {8,S} {9,S}
3 C u2 p0 c0 {1,S} {2,S}
4 H u0 p0 c0 {1,S}
5 H u0 p0 c0 {1,S}
6 H u0 p0 c0 {1,S}
7 H u0 p0 c0 {2,S}
8 H u0 p0 c0 {2,S}
9 H u0 p0 c0 {2,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.70262,0.03566,-0.000198074,5.54963e-07,-4.90535e-10,34858.9,7.54184], Tmin=(10,'K'), Tmax=(410.388,'K')),
            NASAPolynomial(coeffs=[0.0952952,0.0281502,-1.46633e-05,3.66099e-09,-3.54068e-13,35514.3,26.1101], Tmin=(410.388,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (289.819,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (199.547,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 3
External symmetry: -1.0
Optical isomers: 1

Geometry:
C      -1.33663900   -0.12068700   -0.00210100
C       1.33813000    0.07516300   -0.07017500
C       0.01111800   -0.33998100   -0.54016700
H      -2.09385300   -0.58682600   -0.63375700
H      -1.57996700    0.94731700    0.06511000
H      -1.44706500   -0.54228500    1.00507900
H       2.12219100   -0.27827500   -0.74094400
H       1.55947700   -0.32198500    0.92863900
H       1.42650700    1.16745900   -0.01158400
""",
)

entry(
    index = 67,
    label = "[CH2]C[CH]C",
    molecule = 
"""
multiplicity 3
1  C u0 p0 c0 {3,S} {4,S} {5,S} {6,S}
2  C u0 p0 c0 {3,S} {7,S} {8,S} {9,S}
3  C u1 p0 c0 {1,S} {2,S} {10,S}
4  C u1 p0 c0 {1,S} {11,S} {12,S}
5  H u0 p0 c0 {1,S}
6  H u0 p0 c0 {1,S}
7  H u0 p0 c0 {2,S}
8  H u0 p0 c0 {2,S}
9  H u0 p0 c0 {2,S}
10 H u0 p0 c0 {3,S}
11 H u0 p0 c0 {4,S}
12 H u0 p0 c0 {4,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.49284,0.0555661,-0.000234328,5.87024e-07,-4.92107e-10,31004.3,12.871], Tmin=(10,'K'), Tmax=(418.751,'K')),
            NASAPolynomial(coeffs=[0.846795,0.0384302,-2.10244e-05,5.57188e-09,-5.75738e-13,31597.7,27.7732], Tmin=(418.751,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (257.769,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (270.22,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 3
External symmetry: -1.0
Optical isomers: 2

Geometry:
C      -0.69533200    0.42553900    0.03569500
C       1.40015000   -0.28815900    1.36050400
C       0.68876200   -0.13531800    0.06461000
C      -1.66737900   -0.36114000    0.85264500
H      -1.03837300    0.48454200   -1.00527900
H      -0.69550100    1.46474100    0.39764400
H       0.74162600   -0.71751700    2.11985800
H       1.73256500    0.68226600    1.75394800
H       2.28303800   -0.91906800    1.27022100
H       1.25152900   -0.18880300   -0.85616400
H      -2.56494200    0.09757900    1.23900000
H      -1.58646100   -1.43792600    0.89120800
""",
)

entry(
    index = 68,
    label = "C[C]CC",
    molecule = 
"""
multiplicity 3
1  C u0 p0 c0 {2,S} {4,S} {5,S} {6,S}
2  C u0 p0 c0 {1,S} {7,S} {8,S} {9,S}
3  C u0 p0 c0 {4,S} {10,S} {11,S} {12,S}
4  C u2 p0 c0 {1,S} {3,S}
5  H u0 p0 c0 {1,S}
6  H u0 p0 c0 {1,S}
7  H u0 p0 c0 {2,S}
8  H u0 p0 c0 {2,S}
9  H u0 p0 c0 {2,S}
10 H u0 p0 c0 {3,S}
11 H u0 p0 c0 {3,S}
12 H u0 p0 c0 {3,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.60636,0.0448797,-0.000195746,5.40104e-07,-4.78177e-10,32468.3,11.8735], Tmin=(10,'K'), Tmax=(412.43,'K')),
            NASAPolynomial(coeffs=[-0.370742,0.0403059,-2.21905e-05,5.90913e-09,-6.12868e-13,33163.3,31.9869], Tmin=(412.43,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (269.941,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (270.22,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 3
External symmetry: -1.0
Optical isomers: 2

Geometry:
C      -0.59502400   -0.35594200    0.26742000
C      -2.09950800   -0.04706400    0.29254700
C       0.17068400    1.32966400   -1.67576400
C       0.20007400    0.72383000   -0.33792100
H      -0.24459400   -0.53899200    1.28579100
H      -0.43118000   -1.29374200   -0.28192100
H      -2.47890500    0.10312100   -0.71823700
H      -2.65826400   -0.86591700    0.74505100
H      -2.29294200    0.86062900    0.86332900
H      -0.78539600    1.82607100   -1.88393900
H       0.95403900    2.08085800   -1.78420000
H       0.32585000    0.57995700   -2.46232500
""",
)

entry(
    index = 69,
    label = "CC(CC[O])OO",
    molecule = 
"""
multiplicity 2
1  O u0 p2 c0 {2,S} {4,S}
2  O u0 p2 c0 {1,S} {16,S}
3  O u1 p2 c0 {7,S}
4  C u0 p0 c0 {1,S} {5,S} {6,S} {8,S}
5  C u0 p0 c0 {4,S} {7,S} {9,S} {10,S}
6  C u0 p0 c0 {4,S} {11,S} {12,S} {13,S}
7  C u0 p0 c0 {3,S} {5,S} {14,S} {15,S}
8  H u0 p0 c0 {4,S}
9  H u0 p0 c0 {5,S}
10 H u0 p0 c0 {5,S}
11 H u0 p0 c0 {6,S}
12 H u0 p0 c0 {6,S}
13 H u0 p0 c0 {6,S}
14 H u0 p0 c0 {7,S}
15 H u0 p0 c0 {7,S}
16 H u0 p0 c0 {2,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.13265,0.0892137,-0.000269203,5.75915e-07,-4.60371e-10,-20565.7,13.6271], Tmin=(10,'K'), Tmax=(405.727,'K')),
            NASAPolynomial(coeffs=[3.59329,0.0551367,-3.40225e-05,1.00566e-08,-1.14432e-12,-20360,14.8162], Tmin=(405.727,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-171.015,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (361.68,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 2

Geometry:
O      -0.12451100    0.71635600    1.15661400
O      -0.95358300    1.84387000    1.40187700
O       0.38512600   -0.69359900   -2.80327700
C      -0.44627500    0.20419300   -0.13426800
C       0.62444400   -0.84750200   -0.38190600
C      -1.86005800   -0.34362900   -0.16544600
C       0.46929600   -1.53758300   -1.72990500
H      -0.34124600    1.01057300   -0.86505100
H       1.60539300   -0.37359500   -0.32838000
H       0.57895000   -1.59630400    0.41263600
H      -2.55358200    0.41212400    0.19567000
H      -2.14939700   -0.60961000   -1.18191000
H      -1.93998000   -1.22615200    0.47151900
H       1.26162400   -2.27963400   -1.89887100
H      -0.46610200   -2.12418100   -1.76549100
H      -0.32378700    2.56760500    1.30383000
""",
)

entry(
    index = 70,
    label = "CC(CCOO)OO",
    molecule = 
"""
1  O u0 p2 c0 {4,S} {5,S}
2  O u0 p2 c0 {3,S} {7,S}
3  O u0 p2 c0 {2,S} {17,S}
4  O u0 p2 c0 {1,S} {18,S}
5  C u0 p0 c0 {1,S} {6,S} {8,S} {9,S}
6  C u0 p0 c0 {5,S} {7,S} {10,S} {11,S}
7  C u0 p0 c0 {2,S} {6,S} {12,S} {13,S}
8  C u0 p0 c0 {5,S} {14,S} {15,S} {16,S}
9  H u0 p0 c0 {5,S}
10 H u0 p0 c0 {6,S}
11 H u0 p0 c0 {6,S}
12 H u0 p0 c0 {7,S}
13 H u0 p0 c0 {7,S}
14 H u0 p0 c0 {8,S}
15 H u0 p0 c0 {8,S}
16 H u0 p0 c0 {8,S}
17 H u0 p0 c0 {3,S}
18 H u0 p0 c0 {4,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[2.90042,0.111752,-0.000318907,6.33553e-07,-4.87924e-10,-37795.9,13.897], Tmin=(10,'K'), Tmax=(399.021,'K')),
            NASAPolynomial(coeffs=[5.38343,0.0621742,-3.97339e-05,1.20738e-08,-1.40381e-12,-37797.6,6.66174], Tmin=(399.021,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-314.276,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (403.252,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 2

Geometry:
O       0.82237400    1.13665300   -1.48390100
O       2.12321100    2.03239300    2.39347700
O       2.26821500    3.41291200    2.69622500
O       2.19517500    1.01548400   -1.84396200
C       0.55702000    0.20877600   -0.43266300
C       1.43384400    0.47595500    0.78154600
C       1.45095700    1.94583200    1.15002400
C       0.64771300   -1.22673000   -0.91409900
H      -0.48068900    0.45687300   -0.19299100
H       1.04882700   -0.10567700    1.62147000
H       2.45143700    0.13823400    0.58570400
H       1.98275100    2.53208600    0.40051700
H       0.43378700    2.34178700    1.24703400
H       0.00493700   -1.38026600   -1.78015900
H       1.67458200   -1.47127100   -1.18344700
H       0.33375900   -1.90891400   -0.12467100
H       1.63859200    3.51952600    3.41879700
H       2.12791200    0.64196300   -2.73001200
""",
)

entry(
    index = 71,
    label = "O=C1COC1",
    molecule = 
"""
1 O u0 p2 c0 {3,S} {4,S}
2 O u0 p2 c0 {5,D}
3 C u0 p0 c0 {1,S} {5,S} {6,S} {7,S}
4 C u0 p0 c0 {1,S} {5,S} {8,S} {9,S}
5 C u0 p0 c0 {2,D} {3,S} {4,S}
6 H u0 p0 c0 {3,S}
7 H u0 p0 c0 {3,S}
8 H u0 p0 c0 {4,S}
9 H u0 p0 c0 {4,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[4.00989,-0.00137784,9.81404e-05,-1.60194e-07,8.29144e-11,-23648.3,8.61571], Tmin=(10,'K'), Tmax=(593.997,'K')),
            NASAPolynomial(coeffs=[0.319809,0.034791,-2.17806e-05,6.48044e-09,-7.37793e-13,-23409.6,22.8152], Tmin=(593.997,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-196.635,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (207.862,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 1

Geometry:
O       0.18115600   -1.21071400   -0.05672200
O      -0.30213600    2.01803300    0.09511300
C       1.04856200   -0.10575500    0.24196300
C      -0.97511600   -0.38478000   -0.26502000
C      -0.12658600    0.84573300    0.03980400
H       1.44634900   -0.14041800    1.25772800
H       1.86151400    0.00323900   -0.47810400
H      -1.77472700   -0.58448500    0.45051700
H      -1.35901700   -0.44085100   -1.28517900
""",
)

entry(
    index = 72,
    label = "C=C([O])C[O]",
    molecule = 
"""
multiplicity 3
1 O u1 p2 c0 {3,S}
2 O u1 p2 c0 {4,S}
3 C u0 p0 c0 {1,S} {4,S} {6,S} {7,S}
4 C u0 p0 c0 {2,S} {3,S} {5,D}
5 C u0 p0 c0 {4,D} {8,S} {9,S}
6 H u0 p0 c0 {3,S}
7 H u0 p0 c0 {3,S}
8 H u0 p0 c0 {5,S}
9 H u0 p0 c0 {5,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.90524,0.00581024,0.000110943,-2.32105e-07,1.45804e-10,2661.52,12.0241], Tmin=(10,'K'), Tmax=(530.215,'K')),
            NASAPolynomial(coeffs=[3.02967,0.0326245,-2.20874e-05,7.04554e-09,-8.50954e-13,2470.31,13.014], Tmin=(530.215,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (22.097,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (203.705,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 3
External symmetry: -1.0
Optical isomers: 2

Geometry:
O      -1.57228300   -1.28226300    0.31570700
O       0.55358300    1.50948100   -0.20007900
C      -1.05244300   -0.22792600   -0.36193100
C       0.18830600    0.42980600    0.24465400
C       0.87633000   -0.24742200    1.29851400
H      -1.80025400    0.54048100   -0.59776100
H      -0.74398300   -0.63168800   -1.34505000
H       0.52652700   -1.19547400    1.67450800
H       1.75575800    0.22003300    1.71376200
""",
)

entry(
    index = 73,
    label = "[O]OCC(=O)COO",
    molecule = 
"""
multiplicity 2
1  O u0 p2 c0 {3,S} {6,S}
2  O u0 p2 c0 {5,S} {7,S}
3  O u0 p2 c0 {1,S} {13,S}
4  O u0 p2 c0 {8,D}
5  O u1 p2 c0 {2,S}
6  C u0 p0 c0 {1,S} {8,S} {11,S} {12,S}
7  C u0 p0 c0 {2,S} {8,S} {9,S} {10,S}
8  C u0 p0 c0 {4,D} {6,S} {7,S}
9  H u0 p0 c0 {7,S}
10 H u0 p0 c0 {7,S}
11 H u0 p0 c0 {6,S}
12 H u0 p0 c0 {6,S}
13 H u0 p0 c0 {3,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.51405,0.0548582,-2.28841e-05,-2.04159e-08,1.51516e-11,-28109.3,14.6979], Tmin=(10,'K'), Tmax=(860.397,'K')),
            NASAPolynomial(coeffs=[12.5152,0.0335811,-2.16505e-05,6.41427e-09,-7.17868e-13,-30419.6,-31.7986], Tmin=(860.397,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-233.709,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (286.849,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 2

Geometry:
O       1.97202800    0.54916700    0.97385000
O       1.63631300   -3.34454800    2.47609700
O       2.38389200    1.37721300    2.05102300
O       0.17623900   -0.12362800    2.87011600
O       1.16631300   -3.66761400    1.30654800
C       1.97341600   -0.76737200    1.43415100
C       0.79640000   -2.37711600    3.11386300
C       0.90685700   -0.99681100    2.48529500
H      -0.23749400   -2.71377100    3.07121200
H       1.13212800   -2.32316500    4.14853700
H       2.94820400   -1.05525100    1.84402700
H       1.77412500   -1.39902800    0.56607700
H       1.53151800    1.57207400    2.46758200
""",
)

entry(
    index = 74,
    label = "[O]C[O]",
    molecule = 
"""
multiplicity 3
1 O u1 p2 c0 {3,S}
2 O u1 p2 c0 {3,S}
3 C u0 p0 c0 {1,S} {2,S} {4,S} {5,S}
4 H u0 p0 c0 {3,S}
5 H u0 p0 c0 {3,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[4.04338,-0.00399987,4.67009e-05,-2.41647e-08,-5.65995e-11,13613,7.1062], Tmin=(10,'K'), Tmax=(310.578,'K')),
            NASAPolynomial(coeffs=[1.64115,0.0175219,-1.17609e-05,3.69683e-09,-4.40071e-13,13807.7,16.6178], Tmin=(310.578,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (113.186,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (108.088,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 3
External symmetry: -1.0
Optical isomers: 1

Geometry:
O      -1.01141900    0.81007300   -0.03331200
O       1.08417400    0.70782800   -0.06205200
C      -0.00114800   -0.02402600    0.00149500
H      -0.02129100   -0.69308500    0.91388600
H      -0.05031700   -0.80069000   -0.82001700
""",
)

entry(
    index = 75,
    label = "C1=CCC1",
    molecule = 
"""
1  C u0 p0 c0 {2,S} {4,S} {5,S} {6,S}
2  C u0 p0 c0 {1,S} {3,S} {7,S} {8,S}
3  C u0 p0 c0 {2,S} {4,D} {9,S}
4  C u0 p0 c0 {1,S} {3,D} {10,S}
5  H u0 p0 c0 {1,S}
6  H u0 p0 c0 {1,S}
7  H u0 p0 c0 {2,S}
8  H u0 p0 c0 {2,S}
9  H u0 p0 c0 {3,S}
10 H u0 p0 c0 {4,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[4.17547,-0.0132178,0.000135315,-1.92139e-07,8.85836e-11,18646.4,7.18585], Tmin=(10,'K'), Tmax=(672.755,'K')),
            NASAPolynomial(coeffs=[-1.50634,0.0393241,-2.3661e-05,6.84689e-09,-7.63444e-13,18986.3,29.1901], Tmin=(672.755,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (155.053,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (232.805,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 1

Geometry:
C      -0.07150400   -0.96245400    0.13583600
C      -0.91255000    0.34027200   -0.04100300
C       0.41935800    1.04753100   -0.15047600
C       1.13645200   -0.06353500    0.00039200
H      -0.20287100   -1.70053900   -0.65526100
H      -0.19009800   -1.45370100    1.10147300
H      -1.53495000    0.36265100   -0.93532300
H      -1.52173600    0.60980300    0.82156100
H       0.67957000    2.08684400   -0.29841500
H       2.19842900   -0.26697300    0.02131400
""",
)

entry(
    index = 76,
    label = "[CH2]C=C[CH2]",
    molecule = 
"""
multiplicity 3
1  C u0 p0 c0 {2,D} {3,S} {5,S}
2  C u0 p0 c0 {1,D} {4,S} {6,S}
3  C u1 p0 c0 {1,S} {7,S} {8,S}
4  C u1 p0 c0 {2,S} {9,S} {10,S}
5  H u0 p0 c0 {1,S}
6  H u0 p0 c0 {2,S}
7  H u0 p0 c0 {3,S}
8  H u0 p0 c0 {3,S}
9  H u0 p0 c0 {4,S}
10 H u0 p0 c0 {4,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.87069,0.00789343,0.000120886,-2.64524e-07,1.69646e-10,40107.1,10.1133], Tmin=(10,'K'), Tmax=(540.725,'K')),
            NASAPolynomial(coeffs=[4.77545,0.0298161,-1.93101e-05,6.19581e-09,-7.68817e-13,39591,2.43635], Tmin=(540.725,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (333.425,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (224.491,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 3
External symmetry: -1.0
Optical isomers: 1

Geometry:
C      -0.62124800   -0.49784600   -0.47461300
C       0.73874900   -0.55488700   -0.20577900
C      -1.51276300    0.53359900    0.04325500
C       1.42142600    0.34475100    0.57734600
H      -1.04807600   -1.26863300   -1.10995900
H       1.29573700   -1.37206000   -0.64999800
H      -2.06446200    0.38632700    0.96212100
H      -1.72648700    1.42672100   -0.52861400
H       0.90905800    1.17626100    1.04203400
H       2.48228600    0.24597400    0.74869100
""",
)

entry(
    index = 77,
    label = "[CH]1CC1",
    molecule = 
"""
multiplicity 2
1 C u0 p0 c0 {2,S} {3,S} {4,S} {5,S}
2 C u0 p0 c0 {1,S} {3,S} {6,S} {7,S}
3 C u1 p0 c0 {1,S} {2,S} {8,S}
4 H u0 p0 c0 {1,S}
5 H u0 p0 c0 {1,S}
6 H u0 p0 c0 {2,S}
7 H u0 p0 c0 {2,S}
8 H u0 p0 c0 {3,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[4.17798,-0.0138511,0.000120601,-1.7705e-07,8.5177e-11,32123.9,7.28792], Tmin=(10,'K'), Tmax=(648.061,'K')),
            NASAPolynomial(coeffs=[-0.0188052,0.0289155,-1.74166e-05,5.08187e-09,-5.72179e-13,32313.8,22.9825], Tmin=(648.061,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (267.108,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (182.918,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 1

Geometry:
C      -0.74680500   -0.30452900    0.06987500
C       0.76831100   -0.24674800   -0.06462600
C      -0.06840400    0.91119000   -0.37918700
H      -1.18256900   -0.32710000    1.06102300
H      -1.27482200   -0.90373600   -0.66153000
H       1.37205400   -0.22978600    0.83424600
H       1.20316600   -0.80924400   -0.88151300
H      -0.07093000    1.91005300    0.02171300
""",
)

entry(
    index = 78,
    label = "C=CCO[O]",
    molecule = 
"""
multiplicity 2
1  O u0 p2 c0 {2,S} {3,S}
2  O u1 p2 c0 {1,S}
3  C u0 p0 c0 {1,S} {4,S} {6,S} {7,S}
4  C u0 p0 c0 {3,S} {5,D} {8,S}
5  C u0 p0 c0 {4,D} {9,S} {10,S}
6  H u0 p0 c0 {3,S}
7  H u0 p0 c0 {3,S}
8  H u0 p0 c0 {4,S}
9  H u0 p0 c0 {5,S}
10 H u0 p0 c0 {5,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.54966,0.0499426,-0.00021372,5.57927e-07,-4.95333e-10,9062.55,11.7136], Tmin=(10,'K'), Tmax=(391.159,'K')),
            NASAPolynomial(coeffs=[1.85914,0.0332998,-1.97857e-05,5.64012e-09,-6.21015e-13,9454.38,21.6006], Tmin=(391.159,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (75.3304,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (224.491,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 2

Geometry:
O       1.93027700    0.16421900    0.21167500
O       1.77487300    1.43841900    0.39813700
C       0.76833900   -0.57215500    0.66408400
C      -0.37966300   -0.36293100   -0.26560200
C      -1.03166500   -1.35480200   -0.84782300
H       0.54828200   -0.21698200    1.67067100
H       1.08554000   -1.61256800    0.69023800
H      -0.66271400    0.67030800   -0.42994300
H      -0.74730800   -2.38791800   -0.68774200
H      -1.87490500   -1.17131600   -1.49901200
""",
)

entry(
    index = 79,
    label = "C1OO1",
    molecule = 
"""
1 O u0 p2 c0 {2,S} {3,S}
2 O u0 p2 c0 {1,S} {3,S}
3 C u0 p0 c0 {1,S} {2,S} {4,S} {5,S}
4 H u0 p0 c0 {3,S}
5 H u0 p0 c0 {3,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[4.10373,-0.00690207,4.95638e-05,-6.04857e-08,2.39226e-11,-789.116,5.80168], Tmin=(10,'K'), Tmax=(790.321,'K')),
            NASAPolynomial(coeffs=[1.25485,0.0158671,-9.49972e-06,2.70551e-09,-2.95427e-13,-599.594,17.2256], Tmin=(790.321,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-6.53764,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (108.088,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 1

Geometry:
O       0.90814500   -0.04594800    0.75405400
O       0.94424500   -0.02969700   -0.70929700
C      -0.24038900    0.00978500   -0.00571100
H      -0.76859600    0.95917400   -0.00820800
H      -0.84340600   -0.89331500   -0.03083800
""",
)

entry(
    index = 80,
    label = "C=CC(C)O[O]",
    molecule = 
"""
multiplicity 2
1  O u0 p2 c0 {2,S} {3,S}
2  O u1 p2 c0 {1,S}
3  C u0 p0 c0 {1,S} {4,S} {5,S} {7,S}
4  C u0 p0 c0 {3,S} {8,S} {9,S} {10,S}
5  C u0 p0 c0 {3,S} {6,D} {11,S}
6  C u0 p0 c0 {5,D} {12,S} {13,S}
7  H u0 p0 c0 {3,S}
8  H u0 p0 c0 {4,S}
9  H u0 p0 c0 {4,S}
10 H u0 p0 c0 {4,S}
11 H u0 p0 c0 {5,S}
12 H u0 p0 c0 {6,S}
13 H u0 p0 c0 {6,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.63427,0.0371316,-1.263e-05,-4.04823e-09,2.63815e-12,4350.26,13.3684], Tmin=(10,'K'), Tmax=(1169.31,'K')),
            NASAPolynomial(coeffs=[8.00675,0.030698,-1.53114e-05,3.7146e-09,-3.54402e-13,2744.97,-10.902], Tmin=(1169.31,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (36.1559,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (295.164,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 2

Geometry:
O       1.02915100   -0.41894500    1.60659100
O       0.35469600   -0.00005300    2.63130700
C       0.70403900    0.33719500    0.41344300
C       1.27264600    1.73890600    0.54211000
C       1.25216100   -0.40292100   -0.76484000
C       1.94378000   -1.52920300   -0.71934800
H      -0.38651600    0.37402900    0.36970500
H       0.85671200    2.22758300    1.42040900
H       2.35743100    1.69193800    0.62923300
H       1.01763600    2.32265600   -0.34145300
H       1.05023300    0.07546500   -1.71729600
H       2.16185900   -2.02699600    0.21488200
H       2.31144500   -1.98575500   -1.62744900
""",
)

entry(
    index = 81,
    label = "CC=CCO[O]",
    molecule = 
"""
multiplicity 2
1  O u0 p2 c0 {2,S} {3,S}
2  O u1 p2 c0 {1,S}
3  C u0 p0 c0 {1,S} {5,S} {7,S} {8,S}
4  C u0 p0 c0 {6,S} {9,S} {10,S} {11,S}
5  C u0 p0 c0 {3,S} {6,D} {13,S}
6  C u0 p0 c0 {4,S} {5,D} {12,S}
7  H u0 p0 c0 {3,S}
8  H u0 p0 c0 {3,S}
9  H u0 p0 c0 {4,S}
10 H u0 p0 c0 {4,S}
11 H u0 p0 c0 {4,S}
12 H u0 p0 c0 {6,S}
13 H u0 p0 c0 {5,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.32415,0.0725219,-0.000286634,6.86307e-07,-5.71859e-10,4520.05,12.9455], Tmin=(10,'K'), Tmax=(407.314,'K')),
            NASAPolynomial(coeffs=[2.0698,0.0431685,-2.50733e-05,7.02304e-09,-7.62943e-13,4967.91,22.1138], Tmin=(407.314,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (37.56,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (295.164,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 2

Geometry:
O       2.30420300   -0.85104000    0.84390700
O       3.15452300   -1.25548800   -0.04790400
C       1.58524800    0.32160400    0.38282600
C      -1.72020400   -0.16642300   -1.59814600
C       0.59795400   -0.04626600   -0.67056900
C      -0.70421700    0.16917900   -0.55576900
H       2.33966700    1.01869300    0.01893500
H       1.10025200    0.71924700    1.27207700
H      -1.25563700   -0.62916100   -2.46695300
H      -2.25106800    0.72920600   -1.92498800
H      -2.46948100   -0.85164500   -1.19865200
H      -1.07758100    0.62751400    0.35636500
H       1.00878500   -0.50680900   -1.56294300
""",
)

entry(
    index = 82,
    label = "[CH2]C1CC1",
    molecule = 
"""
multiplicity 2
1  C u0 p0 c0 {2,S} {3,S} {4,S} {5,S}
2  C u0 p0 c0 {1,S} {3,S} {6,S} {7,S}
3  C u0 p0 c0 {1,S} {2,S} {8,S} {9,S}
4  C u1 p0 c0 {1,S} {10,S} {11,S}
5  H u0 p0 c0 {1,S}
6  H u0 p0 c0 {2,S}
7  H u0 p0 c0 {2,S}
8  H u0 p0 c0 {3,S}
9  H u0 p0 c0 {3,S}
10 H u0 p0 c0 {4,S}
11 H u0 p0 c0 {4,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.96437,0.0021881,0.000109694,-1.96176e-07,1.13712e-10,23623.2,8.67029], Tmin=(10,'K'), Tmax=(446.133,'K')),
            NASAPolynomial(coeffs=[-0.561922,0.0428098,-2.70174e-05,8.31168e-09,-9.87671e-13,24026.6,26.8493], Tmin=(446.133,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (196.402,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (257.749,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 1

Geometry:
C       0.18225700   -0.06555500   -0.55539700
C      -0.68210900    0.91694400    0.21363600
C      -0.99086200   -0.53754000    0.28415700
C       1.54063400   -0.33237800   -0.11385800
H       0.02071300   -0.08313700   -1.62377700
H      -0.22818700    1.38292200    1.07591600
H      -1.33952600    1.55477100   -0.35817400
H      -0.74797000   -1.06547000    1.19464900
H      -1.86148300   -0.90406900   -0.23897200
H       1.77654900   -0.33112800    0.94044400
H       2.32988500   -0.53546000   -0.81852400
""",
)

entry(
    index = 83,
    label = "C=CCCO[O]",
    molecule = 
"""
multiplicity 2
1  O u0 p2 c0 {2,S} {4,S}
2  O u1 p2 c0 {1,S}
3  C u0 p0 c0 {4,S} {5,S} {7,S} {8,S}
4  C u0 p0 c0 {1,S} {3,S} {9,S} {10,S}
5  C u0 p0 c0 {3,S} {6,D} {11,S}
6  C u0 p0 c0 {5,D} {12,S} {13,S}
7  H u0 p0 c0 {3,S}
8  H u0 p0 c0 {3,S}
9  H u0 p0 c0 {4,S}
10 H u0 p0 c0 {4,S}
11 H u0 p0 c0 {5,S}
12 H u0 p0 c0 {6,S}
13 H u0 p0 c0 {6,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.72689,0.028929,2.17702e-05,-4.63293e-08,1.9667e-11,-13685.4,12.4133], Tmin=(10,'K'), Tmax=(872.283,'K')),
            NASAPolynomial(coeffs=[4.15327,0.0409487,-2.29308e-05,6.20155e-09,-6.52538e-13,-14291.5,7.367], Tmin=(872.283,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-113.784,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (307.635,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 2

Geometry:
O       0.10518900   -0.42147400   -0.10352200
O      -0.58357500    1.68096500   -1.88628000
C       1.74661100    1.37777800    0.02050100
C       1.29745900    0.05207600   -0.58280900
C       0.80275800    2.53190600   -0.15563300
C      -0.22997800    2.63869900   -0.97757200
H       1.90392300    1.22701700    1.09130000
H       2.72574800    1.63477100   -0.39666300
H       2.03596100   -0.73239900   -0.34649800
H       1.25636500    0.08540400   -1.67757500
H       0.97883500    3.39362200    0.47473300
H      -0.84259000    3.53282400   -0.97867300
H      -1.48037800    1.83436400   -2.18820500
""",
)

entry(
    index = 84,
    label = "[C]1CCC1",
    molecule = 
"""
multiplicity 3
1  C u0 p0 c0 {2,S} {3,S} {5,S} {6,S}
2  C u0 p0 c0 {1,S} {4,S} {7,S} {8,S}
3  C u0 p0 c0 {1,S} {4,S} {9,S} {10,S}
4  C u2 p0 c0 {2,S} {3,S}
5  H u0 p0 c0 {1,S}
6  H u0 p0 c0 {1,S}
7  H u0 p0 c0 {2,S}
8  H u0 p0 c0 {2,S}
9  H u0 p0 c0 {3,S}
10 H u0 p0 c0 {3,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[4.10645,-0.00786536,0.000112787,-1.5755e-07,7.05495e-11,52798.1,8.63895], Tmin=(10,'K'), Tmax=(690.123,'K')),
            NASAPolynomial(coeffs=[-1.42175,0.0396079,-2.3938e-05,6.92843e-09,-7.70749e-13,53193.6,30.5966], Tmin=(690.123,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (439,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (232.805,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 3
External symmetry: -1.0
Optical isomers: 1

Geometry:
C       0.04204300    0.66836500   -0.28681800
C      -1.13920100   -0.21075900    0.23378700
C       1.09861200   -0.43359400    0.04266300
C      -0.07676300   -1.21805700    0.52171600
H      -0.02572900    0.89716600   -1.34681800
H       0.18176700    1.58351200    0.28198500
H      -1.66771500    0.19378400    1.09887900
H      -1.87506000   -0.48834400   -0.52304300
H       1.83368300   -0.15487700    0.79986400
H       1.62816400   -0.83719500   -0.82221400
""",
)

entry(
    index = 85,
    label = "[CH2]C(CCO)OO",
    molecule = 
"""
multiplicity 2
1  O u0 p2 c0 {3,S} {4,S}
2  O u0 p2 c0 {6,S} {15,S}
3  O u0 p2 c0 {1,S} {16,S}
4  C u0 p0 c0 {1,S} {5,S} {7,S} {8,S}
5  C u0 p0 c0 {4,S} {6,S} {9,S} {10,S}
6  C u0 p0 c0 {2,S} {5,S} {11,S} {12,S}
7  C u1 p0 c0 {4,S} {13,S} {14,S}
8  H u0 p0 c0 {4,S}
9  H u0 p0 c0 {5,S}
10 H u0 p0 c0 {5,S}
11 H u0 p0 c0 {6,S}
12 H u0 p0 c0 {6,S}
13 H u0 p0 c0 {7,S}
14 H u0 p0 c0 {7,S}
15 H u0 p0 c0 {2,S}
16 H u0 p0 c0 {3,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.21673,0.0810874,-0.000235891,5.24966e-07,-4.32428e-10,-21573.8,41.8965], Tmin=(10,'K'), Tmax=(404.809,'K')),
            NASAPolynomial(coeffs=[2.61902,0.0569082,-3.48163e-05,1.02315e-08,-1.15922e-12,-21278.9,47.2843], Tmin=(404.809,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-179.395,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (369.994,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 2

Geometry:
O      -3.78236300   -1.92312200   -3.30606400
O      -4.60393600    1.97869700   -1.93217500
O      -2.86103600   -2.02105100   -2.22901700
C      -3.37866800   -0.83243900   -4.14718700
C      -3.34746100    0.48486100   -3.38807100
C      -4.61448000    0.72281800   -2.58367600
C      -2.10296900   -1.13598800   -4.84530500
H      -4.20877700   -0.82136500   -4.86535900
H      -2.48690900    0.50610800   -2.71917300
H      -3.21545500    1.28798700   -4.11977400
H      -4.69726800   -0.02692600   -1.79969100
H      -5.49494400    0.62029800   -3.22940800
H      -2.01150700   -2.04714500   -5.41819500
H      -1.26958900   -0.45116800   -4.81396100
H      -4.56875500    2.66964200   -2.59745700
H      -2.23765000   -2.68130300   -2.55651700
""",
)

entry(
    index = 86,
    label = "OCCC1CO1",
    molecule = 
"""
1  O u0 p2 c0 {3,S} {5,S}
2  O u0 p2 c0 {6,S} {14,S}
3  C u0 p0 c0 {1,S} {4,S} {5,S} {7,S}
4  C u0 p0 c0 {3,S} {6,S} {8,S} {9,S}
5  C u0 p0 c0 {1,S} {3,S} {12,S} {13,S}
6  C u0 p0 c0 {2,S} {4,S} {10,S} {11,S}
7  H u0 p0 c0 {3,S}
8  H u0 p0 c0 {4,S}
9  H u0 p0 c0 {4,S}
10 H u0 p0 c0 {6,S}
11 H u0 p0 c0 {6,S}
12 H u0 p0 c0 {5,S}
13 H u0 p0 c0 {5,S}
14 H u0 p0 c0 {2,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.88882,0.0231758,3.89663e-05,-5.83671e-08,2.1654e-11,-34885.9,10.9667], Tmin=(10,'K'), Tmax=(962.692,'K')),
            NASAPolynomial(coeffs=[3.85427,0.0431372,-2.30151e-05,5.93886e-09,-5.98648e-13,-35797.6,6.36249], Tmin=(962.692,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-289.998,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (332.579,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 2

Geometry:
O       0.13842500   -1.60336600    2.99228600
O      -0.58266100   -0.10449000   -0.69163800
C      -0.04362300   -0.48890400    2.13706500
C      -1.40511500   -0.33229500    1.52104200
C       0.83800800   -1.58951700    1.75651800
C      -1.37179500    0.54822900    0.28814700
H       0.41772900    0.42641200    2.49960200
H      -1.78544700   -1.31897900    1.25154000
H      -2.09128000    0.10047800    2.25218700
H      -2.39084000    0.71033600   -0.07489400
H      -0.94563500    1.52622700    0.54086500
H       0.48687200   -2.29603900    1.01408900
H       1.91193000   -1.47314800    1.83597100
H      -0.54074300    0.44368300   -1.47739100
""",
)

entry(
    index = 87,
    label = "[CH2]C1CO1",
    molecule = 
"""
multiplicity 2
1 O u0 p2 c0 {2,S} {3,S}
2 C u0 p0 c0 {1,S} {3,S} {4,S} {5,S}
3 C u0 p0 c0 {1,S} {2,S} {6,S} {7,S}
4 C u1 p0 c0 {2,S} {8,S} {9,S}
5 H u0 p0 c0 {2,S}
6 H u0 p0 c0 {3,S}
7 H u0 p0 c0 {3,S}
8 H u0 p0 c0 {4,S}
9 H u0 p0 c0 {4,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.97339,0.00169712,9.25378e-05,-1.72731e-07,1.04785e-10,9863.11,9.23918], Tmin=(10,'K'), Tmax=(423.225,'K')),
            NASAPolynomial(coeffs=[0.525716,0.0341411,-2.19513e-05,6.82704e-09,-8.16252e-13,10156.2,22.9226], Tmin=(423.225,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (82.0006,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (207.862,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 2

Geometry:
O      -0.74603700   -0.77950900   -0.89775400
C       0.17663100   -0.46209200    0.15248100
C      -1.21346800    0.05099000    0.13655000
C       1.30049400    0.38304600   -0.20011800
H       0.37598100   -1.29251400    0.82009800
H      -1.37940300    1.08728200   -0.13593600
H      -1.94584300   -0.39253000    0.80198200
H       2.24986000    0.28211300    0.29896200
H       1.18178600    1.12341400   -0.97626600
""",
)

entry(
    index = 88,
    label = "[CH]1CCOOC1",
    molecule = 
"""
multiplicity 2
1  O u0 p2 c0 {2,S} {4,S}
2  O u0 p2 c0 {1,S} {5,S}
3  C u0 p0 c0 {4,S} {6,S} {7,S} {8,S}
4  C u0 p0 c0 {1,S} {3,S} {9,S} {10,S}
5  C u0 p0 c0 {2,S} {6,S} {11,S} {12,S}
6  C u1 p0 c0 {3,S} {5,S} {13,S}
7  H u0 p0 c0 {3,S}
8  H u0 p0 c0 {3,S}
9  H u0 p0 c0 {4,S}
10 H u0 p0 c0 {4,S}
11 H u0 p0 c0 {5,S}
12 H u0 p0 c0 {5,S}
13 H u0 p0 c0 {6,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.95192,0.00291032,0.000139328,-2.46493e-07,1.4054e-10,5418.54,11.2079], Tmin=(10,'K'), Tmax=(454.478,'K')),
            NASAPolynomial(coeffs=[-2.07682,0.0560221,-3.61354e-05,1.11387e-08,-1.31477e-12,5966,35.533], Tmin=(454.478,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (45.0338,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (307.635,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 2

Geometry:
O      -0.48161800    1.28304100    0.90534200
O       0.74455000    1.53784000    0.23194400
C      -0.73393600   -0.84201300   -0.20926800
C      -1.30125100    0.55866900    0.00402700
C       1.47982000    0.32120400    0.22947600
C       0.72872500   -0.75406400   -0.47204600
H      -1.25726200   -1.34702500   -1.02235500
H      -0.91856100   -1.42898400    0.70127400
H      -2.28158200    0.53231900    0.47817100
H      -1.36692200    1.10839100   -0.93719300
H       2.41649400    0.56414900   -0.27289800
H       1.70631600    0.05026100    1.27074300
H       1.26522700   -1.58388700   -0.90731600
""",
)

entry(
    index = 89,
    label = "[O]C=CCC[O]",
    molecule = 
"""
multiplicity 3
1  O u1 p2 c0 {4,S}
2  O u1 p2 c0 {6,S}
3  C u0 p0 c0 {4,S} {5,S} {7,S} {8,S}
4  C u0 p0 c0 {1,S} {3,S} {9,S} {10,S}
5  C u0 p0 c0 {3,S} {6,D} {11,S}
6  C u0 p0 c0 {2,S} {5,D} {12,S}
7  H u0 p0 c0 {3,S}
8  H u0 p0 c0 {3,S}
9  H u0 p0 c0 {4,S}
10 H u0 p0 c0 {4,S}
11 H u0 p0 c0 {5,S}
12 H u0 p0 c0 {6,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.77056,0.0302624,6.60112e-06,-2.45517e-08,9.9427e-12,-536.15,12.7508], Tmin=(10,'K'), Tmax=(1016.7,'K')),
            NASAPolynomial(coeffs=[6.53524,0.0330314,-1.7617e-05,4.53007e-09,-4.54514e-13,-1803.6,-4.10145], Tmin=(1016.7,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-4.42974,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (282.692,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 3
External symmetry: -1.0
Optical isomers: 2

Geometry:
O      -2.40310600   -0.75138200   -0.19103700
O       1.01209900    1.24497200   -1.47592900
C      -0.12660100   -0.32675900    0.59895300
C      -1.53701000    0.19246500    0.27071600
C       0.53235900   -0.86618100   -0.61466200
C       1.06991100    0.02661700   -1.59456200
H       0.45206400    0.51761900    0.97906700
H      -0.20258700   -1.08647400    1.37511900
H      -1.98382000    0.69198500    1.14333100
H      -1.47698500    0.97711600   -0.50243800
H       0.56089700   -1.92982700   -0.80448400
H       1.54225300   -0.42537300   -2.48007300
""",
)

entry(
    index = 90,
    label = "O=CC1CCO1",
    molecule = 
"""
1  O u0 p2 c0 {3,S} {5,S}
2  O u0 p2 c0 {6,D}
3  C u0 p0 c0 {1,S} {4,S} {6,S} {7,S}
4  C u0 p0 c0 {3,S} {5,S} {8,S} {9,S}
5  C u0 p0 c0 {1,S} {4,S} {10,S} {11,S}
6  C u0 p0 c0 {2,D} {3,S} {12,S}
7  H u0 p0 c0 {3,S}
8  H u0 p0 c0 {4,S}
9  H u0 p0 c0 {4,S}
10 H u0 p0 c0 {5,S}
11 H u0 p0 c0 {5,S}
12 H u0 p0 c0 {6,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[4.12608,0.0177379,3.30213e-05,-4.39091e-08,1.45677e-11,-24711.2,10.6859], Tmin=(10,'K'), Tmax=(1110.43,'K')),
            NASAPolynomial(coeffs=[7.33384,0.0294123,-1.41277e-05,3.23642e-09,-2.87806e-13,-26855.8,-11.5743], Tmin=(1110.43,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-205.338,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (282.692,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 2

Geometry:
O      -0.33080600    0.62823800   -1.15100800
O       2.65638000   -0.82153900    0.12067200
C       0.38728000   -0.41436800   -0.48820800
C      -0.56635400   -0.36177600    0.72544500
C      -1.35281200    0.63335600   -0.13878900
C       1.80891000   -0.02768700   -0.17416600
H       0.37641700   -1.35582200   -1.04052200
H      -1.05942700   -1.29467800    0.97581700
H      -0.12125900    0.06983000    1.61872500
H      -2.29818200    0.25335300   -0.52769100
H      -1.50236300    1.62817900    0.27891000
H       2.00221600    1.06291400   -0.19918500
""",
)

entry(
    index = 91,
    label = "C1=COOCC1",
    molecule = 
"""
1  O u0 p2 c0 {2,S} {4,S}
2  O u0 p2 c0 {1,S} {6,S}
3  C u0 p0 c0 {4,S} {5,S} {7,S} {8,S}
4  C u0 p0 c0 {1,S} {3,S} {9,S} {10,S}
5  C u0 p0 c0 {3,S} {6,D} {11,S}
6  C u0 p0 c0 {2,S} {5,D} {12,S}
7  H u0 p0 c0 {3,S}
8  H u0 p0 c0 {3,S}
9  H u0 p0 c0 {4,S}
10 H u0 p0 c0 {4,S}
11 H u0 p0 c0 {5,S}
12 H u0 p0 c0 {6,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[4.07557,-0.00695602,0.000165071,-2.70446e-07,1.4137e-10,-3937.48,10.6186], Tmin=(10,'K'), Tmax=(599.261,'K')),
            NASAPolynomial(coeffs=[-1.00363,0.0491211,-3.07978e-05,9.20091e-09,-1.05246e-12,-3726.88,29.2], Tmin=(599.261,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-32.7516,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (282.692,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 2

Geometry:
O      -0.63202300    1.44650000   -0.54369800
O       0.65734600    1.72322200   -0.01709500
C      -0.47980100   -0.92021100   -0.15769900
C      -1.21116300    0.36812400    0.17817500
C       0.99029600   -0.63944000   -0.07346700
C       1.43649100    0.60383300    0.01674700
H      -0.76154200   -1.26555400   -1.15440800
H      -0.76050600   -1.70411400    0.54838100
H      -1.16594100    0.58735800    1.24739100
H      -2.25095800    0.36251100   -0.14386800
H       1.70614500   -1.44714300   -0.05299400
H       2.47155600    0.88511300    0.15243500
""",
)

entry(
    index = 92,
    label = "[O]OC1CCOOC1",
    molecule = 
"""
multiplicity 2
1  O u0 p2 c0 {2,S} {8,S}
2  O u0 p2 c0 {1,S} {7,S}
3  O u0 p2 c0 {4,S} {5,S}
4  O u1 p2 c0 {3,S}
5  C u0 p0 c0 {3,S} {6,S} {7,S} {9,S}
6  C u0 p0 c0 {5,S} {8,S} {10,S} {11,S}
7  C u0 p0 c0 {2,S} {5,S} {14,S} {15,S}
8  C u0 p0 c0 {1,S} {6,S} {12,S} {13,S}
9  H u0 p0 c0 {5,S}
10 H u0 p0 c0 {6,S}
11 H u0 p0 c0 {6,S}
12 H u0 p0 c0 {8,S}
13 H u0 p0 c0 {8,S}
14 H u0 p0 c0 {7,S}
15 H u0 p0 c0 {7,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.907,0.00599534,0.000195498,-3.97444e-07,2.56437e-10,-12977,13.6037], Tmin=(10,'K'), Tmax=(468.611,'K')),
            NASAPolynomial(coeffs=[-0.973948,0.0637819,-4.10847e-05,1.25521e-08,-1.46397e-12,-12696.6,31.5629], Tmin=(468.611,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-107.917,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (357.522,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 2

Geometry:
O      -1.69356600    0.85507900    0.24674200
O      -0.54233100    1.47018500    0.81280100
O       1.45375500   -0.66453000    0.90824700
O       2.59444300   -0.10885900    1.17206000
C       0.86829500   -0.13511400   -0.31138200
C      -0.36872200   -0.97149500   -0.58159700
C       0.51272200    1.32769100   -0.11270600
C      -1.49754300   -0.54480600    0.34668100
H       1.62289800   -0.24220200   -1.09025800
H      -0.67390900   -0.80578200   -1.61537900
H      -0.13570100   -2.02919300   -0.45982000
H      -1.28719600   -0.80698900    1.38525900
H      -2.44865700   -0.98336600    0.04879300
H       0.24002700    1.77644000   -1.07131500
H       1.35548500    1.86294000    0.32187400
""",
)

entry(
    index = 93,
    label = "C#C[O]",
    molecule = 
"""
multiplicity 2
1 O u1 p2 c0 {3,S}
2 C u0 p0 c0 {3,T} {4,S}
3 C u0 p0 c0 {1,S} {2,T}
4 H u0 p0 c0 {2,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.96408,0.0022751,3.27735e-05,-7.64093e-08,5.21212e-11,19286.6,5.48699], Tmin=(10,'K'), Tmax=(511.318,'K')),
            NASAPolynomial(coeffs=[4.28227,0.00739924,-4.59305e-06,1.4299e-09,-1.74604e-13,19154.5,3.19216], Tmin=(511.318,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (160.348,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (83.1447,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 1

Geometry:
O       1.73849400   -0.04438200    0.00353100
C      -0.68456300    0.26529900   -0.01107200
C       0.57333300    0.01523100    0.00024600
H      -1.62716400   -0.23614900    0.00719500
""",
)

entry(
    index = 94,
    label = "[CH2]O",
    molecule = 
"""
multiplicity 2
1 O u0 p2 c0 {2,S} {5,S}
2 C u1 p0 c0 {1,S} {3,S} {4,S}
3 H u0 p0 c0 {2,S}
4 H u0 p0 c0 {2,S}
5 H u0 p0 c0 {1,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.98815,0.00066702,2.73674e-05,-4.35404e-08,2.24879e-11,-3099.41,5.79493], Tmin=(10,'K'), Tmax=(501.634,'K')),
            NASAPolynomial(coeffs=[2.5583,0.0120854,-6.82653e-06,1.97006e-09,-2.26528e-13,-2956.17,11.7046], Tmin=(501.634,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-25.776,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (108.088,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 2

Geometry:
O       0.92040000    0.03428200    0.44432500
C      -0.42490600    0.17022800    0.29650400
H      -0.92690000    0.49615400    1.19234900
H      -0.81768200    0.42286500   -0.67826400
H       1.31998200   -0.17672000   -0.40226300
""",
)

entry(
    index = 95,
    label = "C=CO",
    molecule = 
"""
1 O u0 p2 c0 {2,S} {7,S}
2 C u0 p0 c0 {1,S} {3,D} {4,S}
3 C u0 p0 c0 {2,D} {5,S} {6,S}
4 H u0 p0 c0 {2,S}
5 H u0 p0 c0 {3,S}
6 H u0 p0 c0 {3,S}
7 H u0 p0 c0 {1,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.96268,0.00210742,5.82986e-05,-1.02367e-07,5.52612e-11,-16314.1,6.2163], Tmin=(10,'K'), Tmax=(589.995,'K')),
            NASAPolynomial(coeffs=[2.27277,0.0221691,-1.45823e-05,4.704e-09,-5.8249e-13,-16264.4,12.2083], Tmin=(589.995,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-135.66,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (153.818,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 1

Geometry:
O       1.29625800   -0.10057900    0.51732600
C       0.11113400    0.40080500    0.09180900
C      -0.59345000    1.36271900    0.66767300
H      -0.21258700   -0.09457900   -0.81394800
H      -1.52800800    1.67903700    0.23341000
H      -0.25921100    1.85127300    1.57423500
H       1.56323800    0.35430300    1.32214800
""",
)

entry(
    index = 96,
    label = "[CH2]CO",
    molecule = 
"""
multiplicity 2
1 O u0 p2 c0 {2,S} {8,S}
2 C u0 p0 c0 {1,S} {3,S} {4,S} {5,S}
3 C u1 p0 c0 {2,S} {6,S} {7,S}
4 H u0 p0 c0 {2,S}
5 H u0 p0 c0 {2,S}
6 H u0 p0 c0 {3,S}
7 H u0 p0 c0 {3,S}
8 H u0 p0 c0 {1,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.96984,0.00214208,8.72398e-05,-1.96077e-07,1.45058e-10,-4607.32,8.43797], Tmin=(10,'K'), Tmax=(389.502,'K')),
            NASAPolynomial(coeffs=[2.18904,0.0244574,-1.42077e-05,4.10486e-09,-4.66512e-13,-4499.15,14.958], Tmin=(389.502,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-38.3051,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (182.918,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 2

Geometry:
O       1.50499600   -0.23722000    0.55335600
C       0.34561600    0.27533000   -0.08081800
C       0.51304200    0.41892900   -1.54611000
H      -0.53310700   -0.34062600    0.14260700
H       0.17009100    1.24917400    0.39073900
H      -0.33840300    0.39351500   -2.20857100
H       1.46763800    0.74301900   -1.93418200
H       1.74848200   -1.05220100    0.10680600
""",
)

entry(
    index = 97,
    label = "CC=CO",
    molecule = 
"""
1  O u0 p2 c0 {4,S} {10,S}
2  C u0 p0 c0 {3,S} {5,S} {6,S} {7,S}
3  C u0 p0 c0 {2,S} {4,D} {8,S}
4  C u0 p0 c0 {1,S} {3,D} {9,S}
5  H u0 p0 c0 {2,S}
6  H u0 p0 c0 {2,S}
7  H u0 p0 c0 {2,S}
8  H u0 p0 c0 {3,S}
9  H u0 p0 c0 {4,S}
10 H u0 p0 c0 {1,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.83144,0.0147136,2.58502e-05,-4.35317e-08,1.89374e-11,-19671.6,9.18111], Tmin=(10,'K'), Tmax=(749.18,'K')),
            NASAPolynomial(coeffs=[1.95903,0.0303788,-1.68631e-05,4.57596e-09,-4.85936e-13,-19550.1,16.6121], Tmin=(749.18,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-163.574,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (224.491,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 1

Geometry:
O      -0.92213800    1.11553300    0.46246300
C       1.50298800    2.79783300    1.20111300
C       1.37713500    1.75338500    0.13450800
C       0.29076400    1.04551100   -0.14724000
H       0.58263900    2.94705500    1.76742400
H       2.27971600    2.53327600    1.92013000
H       1.77421900    3.76449000    0.77415100
H       2.25138100    1.55065700   -0.46854200
H       0.28145600    0.30691800   -0.93666000
H      -0.89467600    1.77606600    1.16016700
""",
)

entry(
    index = 98,
    label = "O=O",
    molecule = 
"""
1 O u0 p2 c0 {2,D}
2 O u0 p2 c0 {1,D}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.50704,-0.000408874,1.25093e-06,1.57688e-09,-2.04501e-12,17501.9,3.59484], Tmin=(10,'K'), Tmax=(631.57,'K')),
            NASAPolynomial(coeffs=[2.87665,0.00207515,-1.06602e-06,2.40791e-10,-1.91515e-14,17611.6,6.58458], Tmin=(631.57,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (145.522,'kJ/mol'),
        Cp0 = (29.1007,'J/(mol*K)'),
        CpInf = (37.4151,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 1

Geometry:
O       0.59430200    0.00000000    0.00000000
O      -0.59430200    0.00000000   -0.00000000
""",
)

entry(
    index = 99,
    label = "OC1CO1",
    molecule = 
"""
1 O u0 p2 c0 {3,S} {4,S}
2 O u0 p2 c0 {3,S} {8,S}
3 C u0 p0 c0 {1,S} {2,S} {4,S} {5,S}
4 C u0 p0 c0 {1,S} {3,S} {6,S} {7,S}
5 H u0 p0 c0 {3,S}
6 H u0 p0 c0 {4,S}
7 H u0 p0 c0 {4,S}
8 H u0 p0 c0 {2,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[4.05184,-0.00463918,9.76938e-05,-1.59084e-07,8.29262e-11,-31622.2,8.82074], Tmin=(10,'K'), Tmax=(601.086,'K')),
            NASAPolynomial(coeffs=[1.08179,0.0283227,-1.74958e-05,5.20022e-09,-5.93878e-13,-31503.5,19.6545], Tmin=(601.086,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-262.928,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (182.918,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 2

Geometry:
O      -0.39103900    0.41702100    1.06482900
O       1.59685200   -0.00163500   -0.15005200
C       0.32710300    0.52070900   -0.12855900
C      -0.87750500   -0.30409700   -0.07690000
H       0.31582300    1.49159000   -0.60752500
H      -0.76490600   -1.38099200   -0.01592700
H      -1.81686000    0.05182400   -0.48201600
H       1.61043300   -0.79432000    0.39615100
""",
)

entry(
    index = 100,
    label = "[CH2]C(O)C=O",
    molecule = 
"""
multiplicity 2
1  O u0 p2 c0 {3,S} {10,S}
2  O u0 p2 c0 {5,D}
3  C u0 p0 c0 {1,S} {4,S} {5,S} {6,S}
4  C u1 p0 c0 {3,S} {7,S} {8,S}
5  C u0 p0 c0 {2,D} {3,S} {9,S}
6  H u0 p0 c0 {3,S}
7  H u0 p0 c0 {4,S}
8  H u0 p0 c0 {4,S}
9  H u0 p0 c0 {5,S}
10 H u0 p0 c0 {1,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.84446,0.0104144,0.000139924,-3.43416e-07,2.47196e-10,-19230.1,11.2693], Tmin=(10,'K'), Tmax=(475.82,'K')),
            NASAPolynomial(coeffs=[4.15326,0.035202,-2.45426e-05,7.96625e-09,-9.71187e-13,-19569.4,6.75142], Tmin=(475.82,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-159.916,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (220.334,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 2

Geometry:
O      -0.55096000    1.54132500   -0.12647300
O       1.36318400    0.27302600   -1.44950200
C      -0.14918700    0.30924200    0.39283100
C      -1.26367300   -0.67558900    0.42162300
C       0.97137200   -0.27733400   -0.45768600
H       0.26278400    0.43133100    1.40599700
H      -1.23000200   -1.53593600    1.07151900
H      -2.05203200   -0.57749500   -0.30763700
H       1.38104900   -1.24581700   -0.12675000
H       0.00230500    1.71174800   -0.90160500
""",
)

entry(
    index = 101,
    label = "C=C[CH]C=C",
    molecule = 
"""
multiplicity 2
1  C u1 p0 c0 {2,S} {3,S} {7,S}
2  C u0 p0 c0 {1,S} {4,D} {6,S}
3  C u0 p0 c0 {1,S} {5,D} {8,S}
4  C u0 p0 c0 {2,D} {9,S} {10,S}
5  C u0 p0 c0 {3,D} {11,S} {12,S}
6  H u0 p0 c0 {2,S}
7  H u0 p0 c0 {1,S}
8  H u0 p0 c0 {3,S}
9  H u0 p0 c0 {4,S}
10 H u0 p0 c0 {4,S}
11 H u0 p0 c0 {5,S}
12 H u0 p0 c0 {5,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.90113,0.00593355,0.000141804,-2.76556e-07,1.65326e-10,23541.3,8.90268], Tmin=(10,'K'), Tmax=(540.306,'K')),
            NASAPolynomial(coeffs=[1.35568,0.0463207,-3.01261e-05,9.37727e-09,-1.12049e-12,23502,16.7061], Tmin=(540.306,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (195.697,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (274.378,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 1

Geometry:
C      -0.09790300    0.61957900    0.09529900
C       0.79453200   -0.44324300    0.34521600
C      -1.26336100    0.49279100   -0.68838000
C       1.91675900   -0.33946500    1.09430500
C      -2.13019400    1.50141100   -0.93841100
H       0.55084200   -1.40306000   -0.10026600
H       0.12471700    1.58879300    0.52972200
H      -1.46486700   -0.48623200   -1.11264600
H       2.19342800    0.60007500    1.55478900
H       2.56890800   -1.18451800    1.25630600
H      -3.01030400    1.35334300   -1.54600800
H      -1.96386500    2.49116400   -0.53334800
""",
)

entry(
    index = 102,
    label = "C=CCC=C",
    molecule = 
"""
1  C u0 p0 c0 {2,S} {3,S} {6,S} {7,S}
2  C u0 p0 c0 {1,S} {4,D} {8,S}
3  C u0 p0 c0 {1,S} {5,D} {9,S}
4  C u0 p0 c0 {2,D} {10,S} {11,S}
5  C u0 p0 c0 {3,D} {12,S} {13,S}
6  H u0 p0 c0 {1,S}
7  H u0 p0 c0 {1,S}
8  H u0 p0 c0 {2,S}
9  H u0 p0 c0 {3,S}
10 H u0 p0 c0 {4,S}
11 H u0 p0 c0 {4,S}
12 H u0 p0 c0 {5,S}
13 H u0 p0 c0 {5,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.74139,0.0265333,1.26647e-05,-2.69798e-08,1.00856e-11,12002.2,11.6579], Tmin=(10,'K'), Tmax=(1007.61,'K')),
            NASAPolynomial(coeffs=[3.85951,0.0369924,-1.91734e-05,4.8487e-09,-4.8193e-13,11423.6,8.33439], Tmin=(1007.61,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (99.7924,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (299.321,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 2

Geometry:
C       0.21128500    0.15921100   -0.94389100
C       0.91382300   -0.39626600    0.26617100
C      -1.27480000    0.26027100   -0.80012200
C       0.32325000   -0.96436200    1.30573700
C      -2.15104000   -0.38359000   -1.55429400
H       0.45864000   -0.45311500   -1.81567300
H       0.62239400    1.15303100   -1.14909500
H       1.99603200   -0.31597500    0.25260100
H      -1.63055300    0.91192800   -0.00751800
H      -0.75262100   -1.07526600    1.35668700
H       0.90052600   -1.34557700    2.13673900
H      -3.21663000   -0.26892500   -1.40956200
H      -1.82861500   -1.04863600   -2.34674200
""",
)

entry(
    index = 103,
    label = "[CH2]C(C)C",
    molecule = 
"""
multiplicity 2
1  C u0 p0 c0 {2,S} {3,S} {4,S} {5,S}
2  C u0 p0 c0 {1,S} {6,S} {7,S} {8,S}
3  C u0 p0 c0 {1,S} {9,S} {10,S} {11,S}
4  C u1 p0 c0 {1,S} {12,S} {13,S}
5  H u0 p0 c0 {1,S}
6  H u0 p0 c0 {2,S}
7  H u0 p0 c0 {2,S}
8  H u0 p0 c0 {2,S}
9  H u0 p0 c0 {3,S}
10 H u0 p0 c0 {3,S}
11 H u0 p0 c0 {3,S}
12 H u0 p0 c0 {4,S}
13 H u0 p0 c0 {4,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.79745,0.016259,7.12134e-05,-1.48618e-07,9.44919e-11,7599.34,9.91411], Tmin=(10,'K'), Tmax=(407.308,'K')),
            NASAPolynomial(coeffs=[1.17766,0.0419868,-2.35349e-05,6.46259e-09,-6.94341e-13,7812.75,20.2], Tmin=(407.308,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (63.1523,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (295.164,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 1

Geometry:
C      -0.01010200    0.14199100   -0.37366400
C       1.28088500   -0.54586400    0.06937800
C      -1.23504000   -0.67101700    0.04421100
C      -0.08453400    1.53278200    0.15078100
H      -0.00110900    0.18276600   -1.47327900
H       1.35514800   -1.54769500   -0.35432900
H       2.15702300    0.02276100   -0.24319200
H       1.30515500   -0.63268200    1.15723700
H      -1.27237400   -0.76066600    1.13147100
H      -1.20096600   -1.67493800   -0.37968000
H      -2.15686500   -0.19195800   -0.28653600
H      -1.03776500    2.03103000    0.25424000
H       0.81224600    2.12322500    0.27229300
""",
)

entry(
    index = 104,
    label = "C=C(C)C",
    molecule = 
"""
1  C u0 p0 c0 {3,S} {5,S} {6,S} {7,S}
2  C u0 p0 c0 {3,S} {8,S} {9,S} {10,S}
3  C u0 p0 c0 {1,S} {2,S} {4,D}
4  C u0 p0 c0 {3,D} {11,S} {12,S}
5  H u0 p0 c0 {1,S}
6  H u0 p0 c0 {1,S}
7  H u0 p0 c0 {1,S}
8  H u0 p0 c0 {2,S}
9  H u0 p0 c0 {2,S}
10 H u0 p0 c0 {2,S}
11 H u0 p0 c0 {4,S}
12 H u0 p0 c0 {4,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.89111,0.00775127,0.000103,-2.23222e-07,1.59123e-10,-2847.38,7.84689], Tmin=(10,'K'), Tmax=(357.3,'K')),
            NASAPolynomial(coeffs=[1.28961,0.0368748,-1.9263e-05,4.89891e-09,-4.88859e-13,-2661.48,17.7202], Tmin=(357.3,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-23.703,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (274.378,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 1

Geometry:
C      -0.33150800    1.26712800    0.48180100
C       1.24175500   -0.56391600   -0.29606500
C      -0.17183200   -0.13272800   -0.03504200
C      -1.20822400   -0.93336800   -0.24652400
H      -1.37677500    1.51794600    0.65030800
H       0.08993100    1.98609000   -0.22453700
H       0.21276700    1.39266900    1.42064100
H       1.28952600   -1.58507000   -0.66870200
H       1.71428500    0.09625300   -1.02702700
H       1.83667400   -0.49824600    0.61780800
H      -1.07507800   -1.94059000   -0.61976800
H      -2.22162200   -0.60616900   -0.05289300
""",
)

entry(
    index = 105,
    label = "C=CC=CC",
    molecule = 
"""
1  C u0 p0 c0 {2,S} {6,S} {7,S} {8,S}
2  C u0 p0 c0 {1,S} {3,D} {9,S}
3  C u0 p0 c0 {2,D} {4,S} {11,S}
4  C u0 p0 c0 {3,S} {5,D} {10,S}
5  C u0 p0 c0 {4,D} {12,S} {13,S}
6  H u0 p0 c0 {1,S}
7  H u0 p0 c0 {1,S}
8  H u0 p0 c0 {1,S}
9  H u0 p0 c0 {2,S}
10 H u0 p0 c0 {4,S}
11 H u0 p0 c0 {3,S}
12 H u0 p0 c0 {5,S}
13 H u0 p0 c0 {5,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.82862,0.0152875,9.74311e-05,-2.12889e-07,1.44366e-10,9897.61,10.1866], Tmin=(10,'K'), Tmax=(381.087,'K')),
            NASAPolynomial(coeffs=[0.762913,0.0474664,-2.92299e-05,8.69178e-09,-9.97011e-13,10131.3,22.0192], Tmin=(381.087,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (82.2871,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (299.321,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 2

Geometry:
C      -1.64043900   -0.47965100    0.43489800
C      -1.00953800    0.81369900    0.03348300
C       0.23413900    0.94203100   -0.41945800
C       0.84447100    2.20943600   -0.83757800
C       0.20301300    3.19837500   -1.44979300
H      -0.94729600   -1.31088200    0.31440200
H      -2.52725500   -0.68303400   -0.16882500
H      -1.96775900   -0.44991800    1.47581800
H      -1.61733200    1.70810800    0.13640000
H       1.90505100    2.31951700   -0.63549700
H       0.86548800    0.05935700   -0.46903700
H      -0.84178900    3.10799700   -1.71992300
H       0.70553400    4.11961600   -1.70926200
""",
)

entry(
    index = 106,
    label = "C=C=C",
    molecule = 
"""
1 C u0 p0 c0 {3,D} {4,S} {5,S}
2 C u0 p0 c0 {3,D} {6,S} {7,S}
3 C u0 p0 c0 {1,D} {2,D}
4 H u0 p0 c0 {1,S}
5 H u0 p0 c0 {1,S}
6 H u0 p0 c0 {2,S}
7 H u0 p0 c0 {2,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[4.05963,-0.00597423,9.76771e-05,-1.8213e-07,1.13221e-10,21217.8,4.87385], Tmin=(10,'K'), Tmax=(479.249,'K')),
            NASAPolynomial(coeffs=[1.58468,0.0220275,-1.29545e-05,3.74528e-09,-4.22084e-13,21370.6,14.1136], Tmin=(479.249,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (176.411,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (157.975,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 1

Geometry:
C       1.29906700    0.00396800   -0.00349400
C      -1.29907200   -0.00399000    0.00348100
C      -0.00000200   -0.00020800   -0.00030300
H       1.85182000    0.68049500   -0.64144600
H       1.85945500   -0.66873800    0.63164600
H      -1.85561600   -0.64231000   -0.66956000
H      -1.85565300    0.63078300    0.67967600
""",
)

entry(
    index = 107,
    label = "C=CC(=C)C",
    molecule = 
"""
1  C u0 p0 c0 {2,S} {6,S} {7,S} {8,S}
2  C u0 p0 c0 {1,S} {3,S} {4,D}
3  C u0 p0 c0 {2,S} {5,D} {9,S}
4  C u0 p0 c0 {2,D} {12,S} {13,S}
5  C u0 p0 c0 {3,D} {10,S} {11,S}
6  H u0 p0 c0 {1,S}
7  H u0 p0 c0 {1,S}
8  H u0 p0 c0 {1,S}
9  H u0 p0 c0 {3,S}
10 H u0 p0 c0 {5,S}
11 H u0 p0 c0 {5,S}
12 H u0 p0 c0 {4,S}
13 H u0 p0 c0 {4,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.89774,0.0060007,0.000143542,-2.71649e-07,1.57216e-10,8358.37,9.35604], Tmin=(10,'K'), Tmax=(560.273,'K')),
            NASAPolynomial(coeffs=[1.21728,0.0482133,-3.12519e-05,9.85004e-09,-1.19352e-12,8296.55,17.5027], Tmin=(560.273,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (69.4535,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (299.321,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 1

Geometry:
C      -1.03107500   -0.96670400   -0.20344100
C      -0.39278600    0.35475000    0.10943900
C       1.07061400    0.44442700    0.06652300
C      -1.11314400    1.43163400    0.42074300
C       1.89055200   -0.55878700   -0.22992000
H      -0.76390400   -1.29613800   -1.20909700
H      -0.68638800   -1.73585300    0.48993100
H      -2.11452700   -0.90055800   -0.13684600
H       1.48700200    1.41889800    0.29980400
H       2.96238100   -0.41999500   -0.24239200
H       1.52152500   -1.54764800   -0.46897300
H      -2.19373000    1.39807400    0.46092900
H      -0.63661100    2.37760700    0.64399400
""",
)

entry(
    index = 108,
    label = "[CH2]C(C=C)C=C",
    molecule = 
"""
multiplicity 2
1  C u0 p0 c0 {2,S} {3,S} {4,S} {7,S}
2  C u0 p0 c0 {1,S} {5,D} {8,S}
3  C u0 p0 c0 {1,S} {6,D} {9,S}
4  C u1 p0 c0 {1,S} {10,S} {11,S}
5  C u0 p0 c0 {2,D} {12,S} {13,S}
6  C u0 p0 c0 {3,D} {14,S} {15,S}
7  H u0 p0 c0 {1,S}
8  H u0 p0 c0 {2,S}
9  H u0 p0 c0 {3,S}
10 H u0 p0 c0 {4,S}
11 H u0 p0 c0 {4,S}
12 H u0 p0 c0 {5,S}
13 H u0 p0 c0 {5,S}
14 H u0 p0 c0 {6,S}
15 H u0 p0 c0 {6,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.81942,0.0356899,3.77047e-06,-1.95859e-08,7.08612e-12,33527,14.0607], Tmin=(10,'K'), Tmax=(1194.38,'K')),
            NASAPolynomial(coeffs=[9.51944,0.0339885,-1.59304e-05,3.59971e-09,-3.18328e-13,30925.2,-19.643], Tmin=(1194.38,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (278.806,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (345.051,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 2

Geometry:
C      -0.09667600    0.18923000   -0.22660800
C      -1.09307400   -0.44560400    0.71472300
C       1.13443800   -0.68765700   -0.32893500
C       0.32328000    1.56255000    0.17396000
C      -1.71039200    0.16290200    1.71503800
C       1.57145000   -1.24492200   -1.44745500
H      -0.54983200    0.22377800   -1.22231800
H      -1.29412400   -1.49444200    0.51985000
H       1.67327300   -0.83502700    0.60244800
H       0.60028400    2.28361000   -0.57917300
H       0.62949200    1.74903600    1.19366200
H      -2.41524400   -0.36764900    2.34032200
H      -1.54381600    1.20989000    1.93429100
H       2.46424600   -1.85493400   -1.46457900
H       1.04787400   -1.10675200   -2.38598600
""",
)

entry(
    index = 109,
    label = "C=CC(=C)C=C",
    molecule = 
"""
1  C u0 p0 c0 {2,S} {3,S} {4,D}
2  C u0 p0 c0 {1,S} {5,D} {7,S}
3  C u0 p0 c0 {1,S} {6,D} {8,S}
4  C u0 p0 c0 {1,D} {11,S} {12,S}
5  C u0 p0 c0 {2,D} {9,S} {10,S}
6  C u0 p0 c0 {3,D} {13,S} {14,S}
7  H u0 p0 c0 {2,S}
8  H u0 p0 c0 {3,S}
9  H u0 p0 c0 {5,S}
10 H u0 p0 c0 {5,S}
11 H u0 p0 c0 {4,S}
12 H u0 p0 c0 {4,S}
13 H u0 p0 c0 {6,S}
14 H u0 p0 c0 {6,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.64865,0.0350122,1.3318e-05,-4.10545e-08,1.85431e-11,21301.1,25.7877], Tmin=(10,'K'), Tmax=(861.067,'K')),
            NASAPolynomial(coeffs=[4.95756,0.0427378,-2.41906e-05,6.60642e-09,-7.00922e-13,20563.8,16.6968], Tmin=(861.067,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (177.098,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (324.264,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 2

Geometry:
C       0.04535300    0.86038300   -0.23206100
C      -0.98613600    0.11459100    0.51608100
C       1.18956200    0.11628800   -0.77459600
C      -0.03858800    2.18238000   -0.39969400
C      -2.29159200    0.29902000    0.37480900
C       1.30828700   -1.20696300   -0.78015500
H      -0.62494500   -0.63092800    1.21708100
H       1.97766300    0.72351600   -1.20704000
H      -3.00570700   -0.25611500    0.96728800
H      -2.68288900    1.00428800   -0.34770800
H      -0.85283300    2.75220600    0.02603600
H       0.71542000    2.72134400   -0.95874100
H       0.53731800   -1.85071700   -0.37715300
H       2.17974100   -1.68746400   -1.20188000
""",
)

entry(
    index = 110,
    label = "[NH2]",
    molecule = 
"""
multiplicity 2
1 N u1 p1 c0 {2,S} {3,S}
2 H u0 p0 c0 {1,S}
3 H u0 p0 c0 {1,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[4.00627,-0.000314336,1.21122e-06,1.49715e-09,-1.36718e-12,22574.9,0.598696], Tmin=(10,'K'), Tmax=(786.5,'K')),
            NASAPolynomial(coeffs=[3.25181,0.00187379,1.82878e-07,-2.96859e-10,5.03877e-14,22744.5,4.38156], Tmin=(786.5,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (187.7,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (58.2013,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 1

Geometry:
N      -0.00187900    0.42537000   -0.00000000
H      -0.80125100   -0.21615700    0.00000000
H       0.80313000   -0.20921300   -0.00000000
""",
)

entry(
    index = 111,
    label = "N",
    molecule = 
"""
1 N u0 p1 c0 {2,S} {3,S} {4,S}
2 H u0 p0 c0 {1,S}
3 H u0 p0 c0 {1,S}
4 H u0 p0 c0 {1,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[4.0191,-0.00112359,6.8984e-06,-1.30893e-09,-2.19255e-12,-4864.32,0.274633], Tmin=(10,'K'), Tmax=(654.747,'K')),
            NASAPolynomial(coeffs=[2.40794,0.00563885,-1.53678e-06,9.40181e-11,1.54967e-14,-4587.31,7.86944], Tmin=(654.747,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-40.4372,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (83.1447,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 1

Geometry:
N       0.00264200   -0.00131800    0.28771000
H       0.92021900   -0.17191100   -0.10505900
H      -0.61074800   -0.71100400   -0.09359900
H      -0.31211200    0.88433200   -0.08895200
""",
)

entry(
    index = 112,
    label = "[N]=N",
    molecule = 
"""
multiplicity 2
1 N u0 p1 c0 {2,D} {3,S}
2 N u1 p1 c0 {1,D}
3 H u0 p0 c0 {1,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[4.01387,-0.000832823,4.73515e-06,-1.60207e-10,-2.53896e-12,29826.7,4.1331], Tmin=(10,'K'), Tmax=(615.177,'K')),
            NASAPolynomial(coeffs=[2.80227,0.00449184,-2.0222e-06,4.15753e-10,-3.11408e-14,30024.1,9.78238], Tmin=(615.177,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (247.998,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (58.2013,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 1

Geometry:
N      -0.05604500    0.38222300    0.00000000
N       0.97469200   -0.15823800    0.00000000
H      -0.91864600   -0.22408500    0.00000000
""",
)

entry(
    index = 113,
    label = "[N]=O",
    molecule = 
"""
multiplicity 2
1 O u0 p2 c0 {2,D}
2 N u1 p1 c0 {1,D}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.50531,-0.000280133,5.62122e-07,1.50444e-09,-1.34564e-12,11006.1,4.72769], Tmin=(10,'K'), Tmax=(727.57,'K')),
            NASAPolynomial(coeffs=[2.93013,0.00157111,-5.51729e-07,4.85144e-11,5.59005e-15,11124.4,7.55813], Tmin=(727.57,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (91.5117,'kJ/mol'),
        Cp0 = (29.1007,'J/(mol*K)'),
        CpInf = (37.4151,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 1

Geometry:
O       0.56875300    0.00000000    0.00000000
N      -0.56875300    0.00000000    0.00000000
""",
)

entry(
    index = 114,
    label = "N=O",
    molecule = 
"""
1 O u0 p2 c0 {2,D}
2 N u0 p1 c0 {1,D} {3,S}
3 H u0 p0 c0 {2,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[4.01515,-0.000844743,2.71706e-06,3.13195e-09,-3.77576e-12,13842,3.73817], Tmin=(10,'K'), Tmax=(674.802,'K')),
            NASAPolynomial(coeffs=[2.54736,0.0045232,-1.80711e-06,2.82796e-10,-8.74979e-15,14116,10.8043], Tmin=(674.802,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (115.095,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (58.2013,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 1

Geometry:
O       0.94509100   -0.19141600    0.00000000
N      -0.06703000    0.43451800    0.00000000
H      -0.87806000   -0.24310200    0.00000000
""",
)

entry(
    index = 115,
    label = "[N]N",
    molecule = 
"""
multiplicity 3
1 N u0 p1 c0 {2,S} {3,S} {4,S}
2 N u2 p1 c0 {1,S}
3 H u0 p0 c0 {1,S}
4 H u0 p0 c0 {1,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[4.04876,-0.00361968,2.98252e-05,-4.03748e-08,1.81706e-11,42490.2,5.3234], Tmin=(10,'K'), Tmax=(668.096,'K')),
            NASAPolynomial(coeffs=[2.58104,0.00842863,-4.54673e-06,1.22912e-09,-1.31227e-13,42613.5,11.2677], Tmin=(668.096,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (353.29,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (83.1447,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 3
External symmetry: -1.0
Optical isomers: 1

Geometry:
N      -0.08652500    0.00337400    0.23064400
N       1.21933000   -0.02829600   -0.05516600
H      -0.58564900   -0.82635700   -0.08299400
H      -0.54715600    0.85138000   -0.09248300
""",
)

entry(
    index = 116,
    label = "N=N",
    molecule = 
"""
1 N u0 p1 c0 {2,D} {3,S}
2 N u0 p1 c0 {1,D} {4,S}
3 H u0 p0 c0 {1,S}
4 H u0 p0 c0 {2,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[4.03139,-0.00190461,8.08998e-06,3.97605e-09,-8.29769e-12,24980.2,3.42236], Tmin=(10,'K'), Tmax=(598.87,'K')),
            NASAPolynomial(coeffs=[1.53401,0.00883618,-3.93523e-06,8.00959e-10,-5.85319e-14,25385.9,15.0796], Tmin=(598.87,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (207.709,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (83.1447,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 1

Geometry:
N      -0.60080000    0.52995800    0.07578200
N       0.59761600    0.30926300   -0.09385700
H      -1.06130400   -0.38902200    0.16317000
H       1.05890000    1.22778300   -0.18134900
""",
)

entry(
    index = 117,
    label = "NN",
    molecule = 
"""
1 N u0 p1 c0 {2,S} {3,S} {4,S}
2 N u0 p1 c0 {1,S} {5,S} {6,S}
3 H u0 p0 c0 {1,S}
4 H u0 p0 c0 {1,S}
5 H u0 p0 c0 {2,S}
6 H u0 p0 c0 {2,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[4.0487,-0.00429001,5.87771e-05,-9.90179e-08,5.65416e-11,11879.5,5.63547], Tmin=(10,'K'), Tmax=(497.019,'K')),
            NASAPolynomial(coeffs=[2.02455,0.0148976,-7.87451e-06,2.11199e-09,-2.25843e-13,12044.9,13.6257], Tmin=(497.019,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (98.7718,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (128.874,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 2

Geometry:
N      -0.66966700   -0.34244500   -0.08224300
N       0.69675700   -0.13103800    0.26875100
H      -0.98398100    0.30629100   -0.79485300
H      -1.22565100   -0.18319900    0.74628200
H       1.26072500   -0.70516600   -0.34223800
H       0.97894300    0.83315500    0.13401600
""",
)

entry(
    index = 118,
    label = "N[O]",
    molecule = 
"""
multiplicity 2
1 O u1 p2 c0 {2,S}
2 N u0 p1 c0 {1,S} {3,S} {4,S}
3 H u0 p0 c0 {2,S}
4 H u0 p0 c0 {2,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.93771,0.0051805,-8.11124e-06,1.53563e-08,-9.52885e-12,6467.2,4.95288], Tmin=(10,'K'), Tmax=(634.455,'K')),
            NASAPolynomial(coeffs=[3.08761,0.00678101,-3.00798e-06,6.55457e-10,-5.64436e-14,6650.72,9.26356], Tmin=(634.455,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (53.7676,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (83.1447,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 1

Geometry:
O       1.19952800   -0.04559600   -0.00433100
N      -0.06388200    0.00237300    0.05900700
H      -0.60104300   -0.85213600   -0.02813700
H      -0.53460300    0.89535900   -0.02653900
""",
)

entry(
    index = 119,
    label = "NO",
    molecule = 
"""
1 O u0 p2 c0 {2,S} {5,S}
2 N u0 p1 c0 {1,S} {3,S} {4,S}
3 H u0 p0 c0 {2,S}
4 H u0 p0 c0 {2,S}
5 H u0 p0 c0 {1,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[4.04866,-0.00340667,4.00315e-05,-5.34631e-08,2.27222e-11,-5181.94,4.80822], Tmin=(10,'K'), Tmax=(743.936,'K')),
            NASAPolynomial(coeffs=[2.13437,0.0137864,-8.54802e-06,2.53872e-09,-2.87074e-13,-5088.06,12.194], Tmin=(743.936,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-43.0762,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (103.931,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 1

Geometry:
O       0.85475600   -0.29205800    0.43529400
N      -0.54007300   -0.00762400    0.35904600
H      -0.73942600    0.50401100    1.21299200
H      -0.98775700   -0.91226900    0.46870400
H       1.19444400    0.07747800   -0.38212000
""",
)

entry(
    index = 120,
    label = "[NH]O",
    molecule = 
"""
multiplicity 2
1 O u0 p2 c0 {2,S} {4,S}
2 N u1 p1 c0 {1,S} {3,S}
3 H u0 p0 c0 {2,S}
4 H u0 p0 c0 {1,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[4.05532,-0.00330923,2.51138e-05,-2.70925e-08,9.31604e-12,10979.5,5.02307], Tmin=(10,'K'), Tmax=(899.698,'K')),
            NASAPolynomial(coeffs=[1.65777,0.0116111,-6.86568e-06,1.86789e-09,-1.93923e-13,11238.5,15.3781], Tmin=(899.698,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (91.3042,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (78.9875,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 1

Geometry:
O      -0.72185800    0.45862000   -0.07263600
N       0.59311200    0.37251700   -0.38493200
H       0.81411200    1.35235000   -0.58714600
H      -0.98345600   -0.44622800    0.12833500
""",
)

entry(
    index = 121,
    label = "C[CH]C(C)OO",
    molecule = 
"""
multiplicity 2
1  O u0 p2 c0 {2,S} {3,S}
2  O u0 p2 c0 {1,S} {15,S}
3  C u0 p0 c0 {1,S} {4,S} {6,S} {7,S}
4  C u0 p0 c0 {3,S} {8,S} {9,S} {10,S}
5  C u0 p0 c0 {6,S} {11,S} {12,S} {13,S}
6  C u1 p0 c0 {3,S} {5,S} {14,S}
7  H u0 p0 c0 {3,S}
8  H u0 p0 c0 {4,S}
9  H u0 p0 c0 {4,S}
10 H u0 p0 c0 {4,S}
11 H u0 p0 c0 {5,S}
12 H u0 p0 c0 {5,S}
13 H u0 p0 c0 {5,S}
14 H u0 p0 c0 {6,S}
15 H u0 p0 c0 {2,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.20496,0.0837954,-0.000308966,7.10264e-07,-5.75716e-10,-5155.04,14.009], Tmin=(10,'K'), Tmax=(415.21,'K')),
            NASAPolynomial(coeffs=[2.21131,0.0498271,-2.89547e-05,8.11611e-09,-8.82866e-13,-4697.21,22.4491], Tmin=(415.21,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-42.8837,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (336.736,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 2

Geometry:
O      -0.52131100    3.10265000    1.51014500
O      -1.55021800    2.12052300    1.59443100
C       0.74077300    2.41855300    1.43067600
C       1.07378100    1.70828800    2.72920100
C       0.28710600    2.01651300   -1.06584100
C       0.79867300    1.53177700    0.23957600
H       1.41112400    3.27715800    1.29233500
H       2.08429300    1.30335100    2.68286800
H       1.01320000    2.39788500    3.57001500
H       0.38355500    0.88125900    2.89236600
H      -0.80824700    1.98337500   -1.09105300
H       0.65870900    1.41695100   -1.89523000
H       0.56575500    3.05954600   -1.23306300
H       1.04982800    0.48948800    0.37600400
H      -1.85438200    2.24050000    2.50113900
""",
)

entry(
    index = 122,
    label = "CCCOO",
    molecule = 
"""
1  O u0 p2 c0 {2,S} {4,S}
2  O u0 p2 c0 {1,S} {13,S}
3  C u0 p0 c0 {4,S} {5,S} {6,S} {7,S}
4  C u0 p0 c0 {1,S} {3,S} {8,S} {9,S}
5  C u0 p0 c0 {3,S} {10,S} {11,S} {12,S}
6  H u0 p0 c0 {3,S}
7  H u0 p0 c0 {3,S}
8  H u0 p0 c0 {4,S}
9  H u0 p0 c0 {4,S}
10 H u0 p0 c0 {5,S}
11 H u0 p0 c0 {5,S}
12 H u0 p0 c0 {5,S}
13 H u0 p0 c0 {2,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.45776,0.053758,-0.000130559,2.60986e-07,-1.95951e-10,-23460.7,11.456], Tmin=(10,'K'), Tmax=(447.512,'K')),
            NASAPolynomial(coeffs=[2.7592,0.0409454,-2.37383e-05,6.69675e-09,-7.35583e-13,-23207.3,16.3965], Tmin=(447.512,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-195.077,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (291.007,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 2

Geometry:
O       1.78292900   -1.17927600    0.14713500
O       1.38444300   -2.40759900   -0.45168600
C       0.81136400    0.15916700   -1.66370000
C       0.80384600   -0.21194900   -0.19188000
C       2.16448900    0.68570200   -2.12431600
H       0.51991900   -0.71457300   -2.24837800
H       0.03675800    0.91181200   -1.82372400
H       1.07868100    0.64538500    0.42666500
H      -0.17780600   -0.57307100    0.12227500
H       2.15419200    0.93389900   -3.18449300
H       2.44099200    1.58379000   -1.57013600
H       2.94788400   -0.05340800   -1.95671100
H       2.06409900   -2.52566800   -1.12546700
""",
)

entry(
    index = 123,
    label = "CCCCOO",
    molecule = 
"""
1  O u0 p2 c0 {2,S} {5,S}
2  O u0 p2 c0 {1,S} {16,S}
3  C u0 p0 c0 {4,S} {5,S} {9,S} {10,S}
4  C u0 p0 c0 {3,S} {6,S} {7,S} {8,S}
5  C u0 p0 c0 {1,S} {3,S} {11,S} {12,S}
6  C u0 p0 c0 {4,S} {13,S} {14,S} {15,S}
7  H u0 p0 c0 {4,S}
8  H u0 p0 c0 {4,S}
9  H u0 p0 c0 {3,S}
10 H u0 p0 c0 {3,S}
11 H u0 p0 c0 {5,S}
12 H u0 p0 c0 {5,S}
13 H u0 p0 c0 {6,S}
14 H u0 p0 c0 {6,S}
15 H u0 p0 c0 {6,S}
16 H u0 p0 c0 {2,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.12172,0.0926729,-0.000351786,8.07138e-07,-6.4966e-10,-26047.3,26.3953], Tmin=(10,'K'), Tmax=(418.171,'K')),
            NASAPolynomial(coeffs=[2.01275,0.053189,-3.04743e-05,8.43341e-09,-9.07129e-13,-25516.6,36.0153], Tmin=(418.171,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-216.593,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (361.68,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 2

Geometry:
O      -0.60894100   -1.75563000    0.79297600
O      -0.59949600   -3.05863000    0.21889000
C      -2.58446100   -1.21472500   -0.55088100
C      -3.48493800   -1.45554000    0.65843900
C      -1.15272800   -0.87299700   -0.17385000
C      -3.52687800   -0.27940600    1.62755100
H      -3.13712600   -2.34670500    1.18262200
H      -4.49255900   -1.67376400    0.30106800
H      -2.97331100   -0.38759500   -1.15165600
H      -2.58167700   -2.09955100   -1.18720700
H      -0.50854300   -0.85196700   -1.05763100
H      -1.09237700    0.09804100    0.32068000
H      -4.26938100   -0.44055500    2.40811000
H      -2.56341800   -0.13850200    2.11752900
H      -3.78255200    0.64778100    1.10998200
H       0.34699700   -3.21116100    0.11709300
""",
)

entry(
    index = 124,
    label = "[O]CCCCOO",
    molecule = 
"""
multiplicity 2
1  O u0 p2 c0 {2,S} {6,S}
2  O u0 p2 c0 {1,S} {16,S}
3  O u1 p2 c0 {7,S}
4  C u0 p0 c0 {5,S} {6,S} {10,S} {11,S}
5  C u0 p0 c0 {4,S} {7,S} {8,S} {9,S}
6  C u0 p0 c0 {1,S} {4,S} {12,S} {13,S}
7  C u0 p0 c0 {3,S} {5,S} {14,S} {15,S}
8  H u0 p0 c0 {5,S}
9  H u0 p0 c0 {5,S}
10 H u0 p0 c0 {4,S}
11 H u0 p0 c0 {4,S}
12 H u0 p0 c0 {6,S}
13 H u0 p0 c0 {6,S}
14 H u0 p0 c0 {7,S}
15 H u0 p0 c0 {7,S}
16 H u0 p0 c0 {2,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.90813,0.00621681,0.000216049,-4.62313e-07,3.18119e-10,-20224.3,15.1367], Tmin=(10,'K'), Tmax=(429.808,'K')),
            NASAPolynomial(coeffs=[-1.09917,0.0665446,-4.23992e-05,1.28695e-08,-1.49547e-12,-19920.6,33.5907], Tmin=(429.808,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-168.162,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (378.308,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 2

Geometry:
O       1.99015000    0.41750100    0.51128300
O       3.32025900    0.67273800    0.08865600
O       3.81294100   -1.67495000    1.66557100
C       1.95313500   -1.78118300   -0.59193400
C       1.80921600   -2.64571500    0.65712100
C       1.36620200   -0.38426000   -0.47669100
C       2.54399700   -2.12059500    1.89663000
H       2.18816500   -3.64623300    0.44212600
H       0.75512000   -2.76070900    0.92150600
H       3.00397600   -1.70249700   -0.87184200
H       1.45123700   -2.28124000   -1.42237400
H       1.41683700    0.13201400   -1.43775400
H       0.32309200   -0.42362800   -0.15263800
H       2.03415500   -1.20585000    2.25635100
H       2.51543500   -2.84407000    2.71997300
H       3.80527800   -0.04505800    0.52913800
""",
)

entry(
    index = 125,
    label = "O=CCCCOO",
    molecule = 
"""
1  O u0 p2 c0 {2,S} {6,S}
2  O u0 p2 c0 {1,S} {15,S}
3  O u0 p2 c0 {7,D}
4  C u0 p0 c0 {5,S} {6,S} {8,S} {9,S}
5  C u0 p0 c0 {4,S} {7,S} {10,S} {11,S}
6  C u0 p0 c0 {1,S} {4,S} {12,S} {13,S}
7  C u0 p0 c0 {3,D} {5,S} {14,S}
8  H u0 p0 c0 {4,S}
9  H u0 p0 c0 {4,S}
10 H u0 p0 c0 {5,S}
11 H u0 p0 c0 {5,S}
12 H u0 p0 c0 {6,S}
13 H u0 p0 c0 {6,S}
14 H u0 p0 c0 {7,S}
15 H u0 p0 c0 {2,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[2.96969,0.118563,-0.00063736,1.75955e-06,-1.6416e-09,-38339.2,71.2391], Tmin=(10,'K'), Tmax=(367.081,'K')),
            NASAPolynomial(coeffs=[0.0916469,0.060948,-3.83468e-05,1.13556e-08,-1.28357e-12,-37528.5,90.405], Tmin=(367.081,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-318.836,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (353.365,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 2

Geometry:
O       1.00446000    1.34917300   -0.12632900
O       1.97582100    1.83421200   -1.04075200
O       3.40182500    2.38706100    1.29924400
C       2.48929400   -0.31834500    0.87108800
C       2.45887600    0.37373300    2.22694400
C       1.24146200   -0.03114100    0.04948500
C       2.89568700    1.81035300    2.22675400
H       3.37393600   -0.00370600    0.31642200
H       2.56432100   -1.39741900    1.00917700
H       3.12045100   -0.12273000    2.94572900
H       1.46313200    0.33530000    2.67974000
H       0.35065200   -0.38547100    0.57380200
H       1.29486300   -0.51863300   -0.92563900
H       2.76357700    2.33850100    3.18810900
H       2.65390800    2.17465900   -0.43281000
""",
)

entry(
    index = 126,
    label = "[O]CCCC=O",
    molecule = 
"""
multiplicity 2
1  O u1 p2 c0 {5,S}
2  O u0 p2 c0 {6,D}
3  C u0 p0 c0 {4,S} {5,S} {7,S} {8,S}
4  C u0 p0 c0 {3,S} {6,S} {9,S} {10,S}
5  C u0 p0 c0 {1,S} {3,S} {11,S} {12,S}
6  C u0 p0 c0 {2,D} {4,S} {13,S}
7  H u0 p0 c0 {3,S}
8  H u0 p0 c0 {3,S}
9  H u0 p0 c0 {4,S}
10 H u0 p0 c0 {4,S}
11 H u0 p0 c0 {5,S}
12 H u0 p0 c0 {5,S}
13 H u0 p0 c0 {6,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.84055,0.0169174,0.000230653,-9.72202e-07,1.37924e-09,-19720,11.8572], Tmin=(10,'K'), Tmax=(177.849,'K')),
            NASAPolynomial(coeffs=[2.45966,0.047976,-3.13076e-05,9.78769e-09,-1.16981e-12,-19670.9,16.1346], Tmin=(177.849,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-163.871,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (299.321,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 2

Geometry:
O      -2.05052300   -0.46783100    0.84320400
O       1.48931900    1.22783800    0.93417000
C      -0.34905000    0.01534700   -0.82476500
C       0.70854600   -0.79174800   -0.09173000
C      -1.43962200    0.51456900    0.11967000
C       1.58797700    0.03752900    0.80079000
H       0.10883300    0.87631500   -1.31347100
H      -0.80972000   -0.60015700   -1.59789800
H       1.36753100   -1.32597200   -0.78223400
H       0.24327200   -1.56467800    0.52820300
H      -0.99116400    1.18257700    0.87812300
H      -2.18468100    1.13227700   -0.39957900
H       2.36817200   -0.52070700    1.35162300
""",
)

entry(
    index = 127,
    label = "O=CC(=O)O",
    molecule = 
"""
1 O u0 p2 c0 {4,S} {7,S}
2 O u0 p2 c0 {4,D}
3 O u0 p2 c0 {5,D}
4 C u0 p0 c0 {1,S} {2,D} {5,S}
5 C u0 p0 c0 {3,D} {4,S} {6,S}
6 H u0 p0 c0 {5,S}
7 H u0 p0 c0 {1,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.87984,0.00839758,9.85114e-05,-2.73236e-07,2.17664e-10,-57770.3,9.51793], Tmin=(10,'K'), Tmax=(443.127,'K')),
            NASAPolynomial(coeffs=[4.97872,0.0199413,-1.32178e-05,4.15972e-09,-5.01354e-13,-58078.4,2.73312], Tmin=(443.127,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-480.34,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (149.66,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 1

Geometry:
O       1.41275800    0.26364400    0.66294200
O      -0.06150700   -0.72130800   -0.71849800
O       0.62188900    2.64897400   -0.37466200
C       0.47510500    0.25439000   -0.27824000
C       0.11367300    1.65218200   -0.78324600
H      -0.66473600    1.62853100   -1.56224000
H       1.57874600   -0.65348300    0.92284100
""",
)

entry(
    index = 128,
    label = "[O]CC(=O)O",
    molecule = 
"""
multiplicity 2
1 O u0 p2 c0 {5,S} {8,S}
2 O u1 p2 c0 {4,S}
3 O u0 p2 c0 {5,D}
4 C u0 p0 c0 {2,S} {5,S} {6,S} {7,S}
5 C u0 p0 c0 {1,S} {3,D} {4,S}
6 H u0 p0 c0 {4,S}
7 H u0 p0 c0 {4,S}
8 H u0 p0 c0 {1,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.92721,0.00467491,9.62876e-05,-2.09222e-07,1.39081e-10,-43628.4,11.8413], Tmin=(10,'K'), Tmax=(490.21,'K')),
            NASAPolynomial(coeffs=[2.82328,0.0278938,-1.82452e-05,5.67607e-09,-6.7325e-13,-43691,14.6385], Tmin=(490.21,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-362.765,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (182.918,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 2

Geometry:
O       1.56491100   -0.38639500    0.33336400
O      -0.73898700    0.43827400    1.37860900
O       0.66294300   -0.63416400   -1.68690400
C      -0.74566400    0.22368600    0.03444200
C       0.56169800   -0.31509400   -0.54214100
H      -1.58132600   -0.42371600   -0.26110200
H      -0.96321700    1.18870000   -0.45328900
H       1.23974400   -0.09129200    1.19702200
""",
)

entry(
    index = 129,
    label = "O=CCCC=O",
    molecule = 
"""
1  O u0 p2 c0 {5,D}
2  O u0 p2 c0 {6,D}
3  C u0 p0 c0 {4,S} {5,S} {7,S} {8,S}
4  C u0 p0 c0 {3,S} {6,S} {9,S} {10,S}
5  C u0 p0 c0 {1,D} {3,S} {11,S}
6  C u0 p0 c0 {2,D} {4,S} {12,S}
7  H u0 p0 c0 {3,S}
8  H u0 p0 c0 {3,S}
9  H u0 p0 c0 {4,S}
10 H u0 p0 c0 {4,S}
11 H u0 p0 c0 {5,S}
12 H u0 p0 c0 {6,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.75478,0.0304841,2.99055e-06,-1.9767e-08,8.07991e-12,-36994.7,10.435], Tmin=(10,'K'), Tmax=(1040.78,'K')),
            NASAPolynomial(coeffs=[6.59458,0.0318859,-1.67795e-05,4.26622e-09,-4.23989e-13,-38252.9,-6.5834], Tmin=(1040.78,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-307.571,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (278.535,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 2

Geometry:
O       0.74234300    0.88551600    1.72077800
O      -1.24989400    1.48611100   -0.78690600
C       0.81862300   -0.30868700   -0.34995700
C      -0.61745800   -0.71318900   -0.09197900
C       1.33809500    0.62418300    0.71294600
C      -1.57094700    0.43238300   -0.31203400
H       1.48509200   -1.17504600   -0.37695600
H       0.92048000    0.19457000   -1.31339500
H      -0.93248500   -1.52964100   -0.74742100
H      -0.75081800   -1.06531400    0.93274100
H       2.33651300    1.05770000    0.52148100
H      -2.62024500    0.24301900   -0.02126600
""",
)

