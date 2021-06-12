//Units: mm

hexHeight = 4.57;

spacerHeight = 1.36;
spacerDiameter = 18;

shaftDiameter = 4.5;

dShaftEnable = true;
dShaftDiameter = 5.8;
dShaftFlatDiameter = 4.9;
dShaftInset = 3.93;

INF = 100; //arbitrarily large value


difference() {
  union() {
    translate([0,0,spacerHeight]) M7();
    Spacer();
  }

  if (dShaftEnable) {
    translate([0,0,dShaftInset]) Shaft();
    DShaft();
  }
  else {
    Shaft();
  }
}


module Shaft() {
  cylinder(h=INF, d=shaftDiameter, $fn=50);  
}

module DShaft() {
  intersection() {
    cylinder(h=dShaftInset, d=dShaftDiameter, $fn=50);
    translate([-dShaftDiameter/2,-dShaftDiameter/2,-INF/2]) cube([dShaftDiameter, dShaftFlatDiameter, INF]);
  }
}

module Spacer() {
  cylinder(h=spacerHeight, d=spacerDiameter, $fn=50);
}

module M7() {
  cylinder(h=hexHeight, d=14.2, $fn = 6);
}
