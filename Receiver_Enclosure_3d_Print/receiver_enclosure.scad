// Draft enclosure. Millimetres. Set part to "base" or "lid" before STL export.
part = "base";
length = 100;
width = 75;
wall = 2;
base_height = 28;
lid_thickness = 2;
clearance = 0.3; // Per side; adjust after printer fit test.
skirt_depth = 3;
skirt_wall = 1.2;
module base() {
    difference() {
        translate([-length/2,-width/2,0]) cube([length,width,base_height]);
        translate([-length/2+wall,-width/2+wall,wall])
            cube([length-2*wall,width-2*wall,base_height]);
    }
}
module lid() {
    sx=length-2*wall-2*clearance;
    sy=width-2*wall-2*clearance;
    union() {
        translate([-length/2,-width/2,0]) cube([length,width,lid_thickness]);
        difference() {
            translate([-sx/2,-sy/2,lid_thickness-0.01])
                cube([sx,sy,skirt_depth+0.01]);
            translate([-sx/2+skirt_wall,-sy/2+skirt_wall,lid_thickness-0.02])
                cube([sx-2*skirt_wall,sy-2*skirt_wall,skirt_depth+0.1]);
        }
    }
}
if (part == "base") base(); else lid();
