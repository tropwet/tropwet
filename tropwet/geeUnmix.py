import ee

def unmix(img,endmembers,sumToOne:bool=True, nonNegative:bool=True,scaleFactor:int=10000):
  unmixedImage = median_composite.unmix(endmembers,True,True);
  bandNames2 = ['water', 'veg', 'bare','burn'];
  unmixedImage = unmixedImage.rename(bandNames2);
  unmixedImage = unmixedImage.select(bandNames2);
  unmixedImage = unmixedImage.multiply(scaleFactor)
  return unmixedImage
