numberOfSlots = 100;
slotAngle = 0;
slotLength = 30;
shaftHole = 3;

diskThickness = 3;
diskDiameter = 150;
diskCercumference = 100 * 3.14;
slotWidth = diskCercumference / numberOfSlots/2;
resolution = 50;




module cutSlots()
{
	for (slotVector = [0:360/numberOfSlots:360]) 
		{
		rotate(slotVector)
		translate([0,diskDiameter/2-(slotLength/2),-.5])
		rotate(slotAngle)
		cube([slotWidth,slotLength,diskThickness+1]);
		}
}


module makeDisk()
{
difference()
	{
	cylinder(diskThickness,d = diskDiameter,d = diskDiameter, $fn = resolution);
	cutSlots();
	translate([0,0,-.5])
	cylinder(diskThickness + 1 ,d = shaftHole,d = shaftHole, $fn = resolution);
	}
}

//cutSlots();


projection(cut = true) makeDisk();

