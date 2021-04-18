def longitude_0_360 (longitude) :
    assert -180<=longitude<=180., ("longitude doit être dans [-180,180]" , longitude)
    if longitude >=0. :
        return (longitude)
    else :
        return (360. -abs(longitude))
print (longitude_0_360(12))
print (longitude_0_360(-12))
print (longitude_0_360(-1200))
 