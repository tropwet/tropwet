import ee
import geemap.core as geemap

ee.Authenticate()
ee.Initialize(project='ee-gregoryoakessentone')

def fuzzy_gt(img,lowBound,upBound):
  fuzzyOut = ee.Image(unmixImg.subtract(lowBound)).multiply(ee.Number(1).divide(upBound-lowBound))
  fuzzyOut = fuzzyOut.where(unmixImg.lt(lowBound),0)
  fuzzyOut = fuzzyOut.where(unmixImg.gt(upBound),1)
  return fuzzyOut

def fuzzy_lt(img,lowBound,upBound):
  fuzzyOut = ee.Image(unmixImg.subtract(upBound)).multiply(ee.Number(1).divide(lowBound-upBound))
  fuzzyOut = fuzzyOut.where(unmixImg.lt(lowBound),1)
  fuzzyOut = fuzzyOut.where(unmixImg.gt(upBound),0)
  return fuzzyOut

def fuzzy_and(imgCol):
  minImg = imgCol.min()
  return minImg

def fuzzy_or(imgCol):
  maxImg = imgCol.max()
  return maxImg
