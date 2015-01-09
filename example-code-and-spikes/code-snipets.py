You can also access some of the features of this video using cap.get(propId) method where propId is a number from 0 to 18.
 Each number denotes a property of the video (if it is applicable to that video) and full details can be seen here: Property Identifier.
 Some of these values can be modified using cap.set(propId, value). Value is the new value you want.

For example, I can check the frame width and height by cap.get(3) and cap.get(4). 
It gives me 640x480 by default. But I want to modify it to 320x240.
 Just use ret = cap.set(3,320) and ret = cap.set(4,240).
