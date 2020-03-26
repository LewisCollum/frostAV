difference() {
     cube([11,11, 2], center=true);
     translate([0,0,-1.1]) cylinder(h=2.2, d=7, $fn = 6);
}
