import ee
from tropwet import cloudMasking


def getLandsatComposite(
  geometry,
  first_month: int,
  last_month: int,
  first_year: int,
  last_year: int,
  landsats: list = [8,9]
):
  
  landsat9Collection = ee.ImageCollection("LANDSAT/LC09/C02/T1_L2")\
                    .filterBounds(geometry)\
                    .filter(ee.Filter.calendarRange(first_year,last_year,'year'))\
                    .filter(ee.Filter.calendarRange(first_month,last_month,'month'))
  ls9CloudMasked = landsat9Collection.map(cloudMasking.cloudMaskLSOLI)
  
  landsat8Collection = ee.ImageCollection("LANDSAT/LC08/C02/T1_L2")\
                    .filterBounds(geometry)\
                    .filter(ee.Filter.calendarRange(first_year,last_year,'year'))\
                    .filter(ee.Filter.calendarRange(first_month,last_month,'month'))
  ls8CloudMasked = landsat8Collection.map(cloudMasking.cloudMaskLSOLI)
  
  landsat7Collection = ee.ImageCollection("LANDSAT/LE07/C02/T1_L2")\
                    .filterBounds(geometry)\
                    .filter(ee.Filter.calendarRange(first_year,last_year,'year'))\
                    .filter(ee.Filter.calendarRange(first_month,last_month,'month'))
  ls7CloudMasked = landsat7Collection.map(cloudMasking.cloudMaskLSTM)
  
  landsat5Collection = ee.ImageCollection("LANDSAT/LT05/C02/T1_L2")\
                    .filterBounds(geometry)\
                    .filter(ee.Filter.calendarRange(first_year,last_year,'year'))\
                    .filter(ee.Filter.calendarRange(first_month,last_month,'month'))
  ls5CloudMasked = landsat5Collection.map(cloudMasking.cloudMaskLSTM)
  
  #### Match Case for Composite ####
  
  match sorted(landsats):
    case [9]:
      median_compositeCol = ls9CloudMasked
    case [8]:
      median_compositeCol = ls8CloudMasked
    case [7]:
      median_compositeCol = ls7CloudMasked
    case [5]:
      median_compositeCol = ls5CloudMasked
    case [8,9]:
      median_compositeCol = ls8CloudMasked.merge(ls9CloudMasked)
    case [7,9]:
      median_compositeCol = ls7CloudMasked.merge(ls9CloudMasked)
    case [5,9]:
      median_compositeCol = ls5CloudMasked.merge(ls9CloudMasked)
    case [7,8]:
      median_compositeCol = ls7CloudMasked.merge(ls8CloudMasked)
    case [5,8]:
      median_compositeCol = ls7CloudMasked.merge(ls8CloudMasked)
    case [5,7]:
      median_compositeCol = ls7CloudMasked.merge(ls5CloudMasked)
    case [5,8,9]:
      median_compositeCol = ls5CloudMasked.merge(ls8CloudMasked).merge(ls9CloudMasked)
    case [7,8,9]:
      median_compositeCol = ls7CloudMasked.merge(ls8CloudMasked).merge(ls9CloudMasked)
    case [5,7,8]:
      median_compositeCol = ls5CloudMasked.merge(ls7CloudMasked).merge(ls8CloudMasked)
    case [5,7,9]:
      median_compositeCol = ls5CloudMasked.merge(ls7CloudMasked).merge(ls9CloudMasked)
    case [5,7,8,9]:
      median_compositeCol = ls5CloudMasked.merge(ls7CloudMasked).merge(ls8CloudMasked).merge(ls9CloudMasked)
  
  median_composite = median_compositeCol.reduce(ee.Reducer.median(),parScale).clip(geometry)
  
  median_composite = median_composite.select(['b_median', 'g_median', 'r_median','nir_median','swir1_median','swir2_median'],['b', 'g', 'r','nir','swir1','swir2'])
  
  return median_composite
