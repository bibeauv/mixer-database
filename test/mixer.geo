// MIXER GEOMETRY (merge)
// Valérie Bibeau, Polytechnique Montréal
// 2020

SetFactory("OpenCASCADE");

// -------------------------------------------
// Dimensionless geometry variables
// -------------------------------------------

T = 1;

ratioTD = 3.0;
  D = T/ratioTD;
ratioHT = 1.0;
  H = T*ratioHT;
ratioTC = 5.0;
  C = T/ratioTC;
ratioDW = 4.0;
  W = D/ratioDW;
ratioDW = 3.0;
  W_Hub = D/ratioDW;

theta = Pi/4;

H_blade = W;
E = 0.1*W;

// -------------------------------------------
// Cylinder (tank)
// -------------------------------------------
Cylinder(1) = {0, 0, 0, 0, 0, H, T/2, 2*Pi};

// -------------------------------------------
// Cylinder (pbt)
// -------------------------------------------
Cylinder(2) = {0, 0, C, 0, 0, H, W/2, 2*Pi};

// -------------------------------------------
// Cylinder (pbt hub)
// -------------------------------------------
Cylinder(3) = {0, 0, C, 0, 0, H_blade, W_Hub/2, 2*Pi};

// -------------------------------------------
// Blade 1
// -------------------------------------------
Box (4) = { 0, -E/2, C, D/2, E, H_blade };
Rotate { { 1,0,0 }, {0, 0, C+H_blade/2}, -theta } {Volume{4};}

// -------------------------------------------
// Blade 2
// -------------------------------------------
Box (5) = { 0, -D/2, C, E, D/2, H_blade };
Rotate { { 0,1,0 }, {0, 0, C+H_blade/2}, theta } {Volume{5};}

// -------------------------------------------
// Blade 3
// -------------------------------------------
Box (6) = { 0, 0, C, E, D/2, H_blade };
Rotate { { 0,1,0 }, {0, 0, C+H_blade/2}, -theta } {Volume{6};}

// -------------------------------------------
// Blade 4
// -------------------------------------------
Box (7) = { 0, -E/2, C, -D/2, E, H_blade };
Rotate { { 1,0,0 }, {0, 0, C+H_blade/2}, theta } {Volume{7};}

// -------------------------------------------
// Volume (fluid - shaft)
// -------------------------------------------
BooleanDifference{ Volume{1}; Delete; }{ Volume{2:7}; Delete; }

// -------------------------------------------
// Boundary conditions
// -------------------------------------------
Physical Surface(0) = {1:28,32:1000}; // Wall
Physical Surface(1) = {29}; // Wall
Physical Surface(2) = {30}; // Top
Physical Surface(3) = {31}; // Bottom

Physical Volume(0) = {1:100};

// -------------------------------------------
// Mesh
// -------------------------------------------
// Attractors field
Field[1] = Attractor;
Field[1].NNodesByEdge = 1000; // #Attractors on the edges
Field[1].NodesList = {1:34,37:100};
Field[1].EdgesList = {1:49,53:100};

// Threshold field defined on the attractors
lc = 0.05;
Field[2] = Threshold;
Field[2].IField = 1;
Field[2].LcMin = {{mesh_length}}; // char length inside DistMin
Field[2].LcMax = lc; // char length outside DistMax
Field[2].DistMin = 0.1;
Field[2].DistMax = 0.3;

Background Field = 2;

Mesh.ElementOrder = 1;
Mesh.SecondOrderLinear = 1;
Mesh.HighOrderOptimize = 1;
Mesh.SubdivisionAlgorithm = 2; // Hexas
