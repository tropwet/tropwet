import ee


def fuzzy_gt(img,low_bound,up_bound):
  fuzzyOut = ee.Image(img.subtract(low_bound)).multiply(ee.Number(1).divide(up_bound-low_bound))
  fuzzyOut = fuzzyOut.where(img.lt(low_bound),0)
  fuzzyOut = fuzzyOut.where(img.gt(up_bound),1)
  return ee.Image(fuzzyOut).float()

def fuzzy_lt(img,low_bound,up_bound):
  fuzzyOut = ee.Image(img.subtract(up_bound)).multiply(ee.Number(1).divide(low_bound-up_bound))
  fuzzyOut = fuzzyOut.where(img.lt(low_bound),1)
  fuzzyOut = fuzzyOut.where(img.gt(up_bound),0)
  return ee.Image(fuzzyOut).float()

def fuzzy_and(imgCol):
  minImg = ee.ImageCollection(imgCol).min()
  return ee.Image(minImg).float()

def fuzzy_or(imgCol):
  maxImg = ee.ImageCollection(imgCol).max()
  return ee.Image(maxImg).float()

