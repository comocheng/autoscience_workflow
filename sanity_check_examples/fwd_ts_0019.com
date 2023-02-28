%mem=5GB
%nprocshared=24
#P m062x/cc-pVTZ ! ASE formatted method and basis
opt=(ts,calcfc,noeigentest,maxcycles=900) freq scf=(maxcycle=900) IOP(7/33=1,2/16=3)

Gaussian input prepared by ASE

0 2
O                -2.6153940000       -0.3738200000        0.3398920000
O                -2.2699860000       -0.9989100000       -0.8841100000
O                -0.6475570000        2.5289640000       -0.2408750000
C                 3.3110910000        0.4370200000       -0.3382500000
C                 2.4794950000       -0.5843160000       -1.1040490000
C                -2.4840780000        0.9951770000        0.1625270000
C                 2.7423050000        0.6937060000        1.0522830000
C                -0.0146330000       -1.7755420000        1.1509280000
C                -1.0304010000        1.4409710000       -0.0319720000
C                -0.1366970000       -1.8688650000       -0.2814380000
H                 4.3426210000        0.0905330000       -0.2586600000
H                 3.3361250000        1.3726720000       -0.8973080000
H                 2.8684280000       -0.7662160000       -2.1048440000
H                 1.4489730000       -0.2359620000       -1.2023430000
H                -3.0528610000        1.3444570000       -0.7036840000
H                -2.8431170000        1.4797460000        1.0734310000
H                 3.3308170000        1.4267300000        1.6014910000
H                 2.7260710000       -0.2275460000        1.6365970000
H                 1.7198050000        1.0673880000        0.9780010000
H                -1.0837340000       -2.0055710000        1.3764360000
H                 0.6050460000       -2.5098730000        1.6612900000
H                 2.4727150000       -1.5425820000       -0.5761170000
H                 0.0642520000       -2.8723980000       -0.6552710000
H                 0.1216700000       -0.7590730000        1.5198180000
H                -0.9958110000       -1.1410840000       -0.8282650000

