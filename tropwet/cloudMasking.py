def bitwiseExtract(value, fromBit, toBit):
  if toBit == None:
    toBit = fromBit
  maskSize = ee.Number(1).add(toBit).subtract(fromBit)
  mask = ee.Number(1).leftShift(maskSize).subtract(1)
  return value.rightShift(fromBit).bitwiseAnd(mask)
  
def cloudMaskLSOLI(image):
  cloudShadowBitMask = (1 << 4);
  cloudsBitMask = (1 << 3);
  cirrusBitMask = (1<<2)
  snowBitMask = (1<<5)
  qa = image.select('QA_PIXEL');
  ra = image.select('QA_RADSAT')
  
  mask = qa.bitwiseAnd(cloudShadowBitMask).eq(0).And(qa.bitwiseAnd(cloudsBitMask).eq(0)).And(qa.bitwiseAnd(cirrusBitMask).eq(0)).Or(ra.bitwiseAnd(1<<1))
  anySaturated = bitwiseExtract(ra, 1, 7).eq(0)
  snowMask = qa.bitwiseAnd(snowBitMask).eq(0)
  
  opticalBands = image.select('SR_B.').multiply(0.0000275).add(-0.2);
  thermalBands = image.select('ST_B.*').multiply(0.00341802).add(149.0);
  correctedImg =  image.addBands(opticalBands, None, True).addBands(thermalBands, None, True);
  
  bandNames = ['SR_B2', 'SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7'];
  maskedImage = correctedImg.updateMask(mask);
  maskedImgSnow = maskedImage.updateMask(snowMask)
  maskedImgSnowSat = maskedImgSnow.updateMask(anySaturated)
  maskedImageSelectedBands = maskedImgSnow.select(bandNames);
  maskedImageSelectedBands = maskedImageSelectedBands.rename('b','g','r','nir','swir1','swir2')
  
  maskedImageSelectedBandsShort = maskedImageSelectedBands.multiply(10000)
  
  blue = maskedImageSelectedBandsShort.select('b')
  green = maskedImageSelectedBandsShort.select('g')
  red = maskedImageSelectedBandsShort.select('r')
  nir = maskedImageSelectedBandsShort.select('nir')
  swir1 = maskedImageSelectedBandsShort.select('swir1')
  swir2 = maskedImageSelectedBandsShort.select('swir2')
  
  secondaryMask = ee.Image(blue.gt(3000).And(green.gt(3000)).And(red.gt(3000)).And(nir.gt(3000)).And(swir1.gt(3000)).And(swir2.gt(3000))).neq(1)
  
  blueVal = ee.Image(blue.subtract(ee.Image(ee.Image(blue.add(green).add(red)).divide(3)))).abs()
  greenVal = ee.Image(green.subtract(ee.Image(ee.Image(blue.add(green).add(red)).divide(3)))).abs()
  redVal = ee.Image(red.subtract(ee.Image(ee.Image(blue.add(green).add(red)).divide(3)))).abs()
  
  whitenessIndex = ee.Image(blueVal.add(greenVal).add(redVal)).divide(ee.Image(blue.add(green).add(red)).divide(3))
  whitenessMask = whitenessIndex.gt(0.2)
  medianCompWhiteMask = maskedImageSelectedBandsShort.updateMask(whitenessMask)
  medianSecondaryMask = medianCompWhiteMask.updateMask(secondaryMask)
  
  return medianSecondaryMask
  
def cloudMaskLSTM(image):
  cloudShadowBitMask = (1 << 4);
  cloudsBitMask = (1 << 3);
  cirrusBitMask = (1<<2)
  snowBitMask = (1<<5)
  qa = image.select('QA_PIXEL');
  ra = image.select('QA_RADSAT')
  mask = qa.bitwiseAnd(cloudShadowBitMask).eq(0).And(qa.bitwiseAnd(cloudsBitMask).eq(0)).And(qa.bitwiseAnd(cirrusBitMask).eq(0)).Or(ra.bitwiseAnd(1<<1))
  anySaturated = bitwiseExtract(ra, 1, 7).eq(0)
  snowMask = qa.bitwiseAnd(snowBitMask).eq(0)
  
  
  opticalBands = image.select('SR_B.').multiply(0.0000275).add(-0.2);
  thermalBands = image.select('ST_B.*').multiply(0.00341802).add(149.0);
  correctedImg =  image.addBands(opticalBands, None, True).addBands(thermalBands, None, True);
  
  bandNames = ['SR_B1', 'SR_B2', 'SR_B3', 'SR_B4', 'SR_B5', 'SR_B7'];
  maskedImage = correctedImg.updateMask(mask);
  maskedImgSnow = maskedImage.updateMask(snowMask)
  maskedImgSnowSat = maskedImgSnow.updateMask(anySaturated)
  maskedImageSelectedBands = maskedImgSnow.select(bandNames);
  maskedImageSelectedBands = maskedImageSelectedBands.rename('b','g','r','nir','swir1','swir2')
  
  maskedImageSelectedBandsShort = maskedImageSelectedBands.multiply(10000)
  
  blue = maskedImageSelectedBandsShort.select('b')
  green = maskedImageSelectedBandsShort.select('g')
  red = maskedImageSelectedBandsShort.select('r')
  nir = maskedImageSelectedBandsShort.select('nir')
  swir1 = maskedImageSelectedBandsShort.select('swir1')
  swir2 = maskedImageSelectedBandsShort.select('swir2')
  
  secondaryMask = ee.Image(blue.gt(3000).And(green.gt(3000)).And(red.gt(3000)).And(nir.gt(3000)).And(swir1.gt(3000)).And(swir2.gt(3000))).neq(1)
  
  blueVal = ee.Image(blue.subtract(ee.Image(ee.Image(blue.add(green).add(red)).divide(3)))).abs()
  greenVal = ee.Image(green.subtract(ee.Image(ee.Image(blue.add(green).add(red)).divide(3)))).abs()
  redVal = ee.Image(red.subtract(ee.Image(ee.Image(blue.add(green).add(red)).divide(3)))).abs()
  
  whitenessIndex = ee.Image(blueVal.add(greenVal).add(redVal)).divide(ee.Image(blue.add(green).add(red)).divide(3))
  whitenessMask = whitenessIndex.gt(0.2)
  medianCompWhiteMask = maskedImageSelectedBandsShort.updateMask(whitenessMask)
  medianSecondaryMask = medianCompWhiteMask.updateMask(secondaryMask)
  
  return medianSecondaryMask
  
