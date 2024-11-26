import ee
from tropwet import fuzzy

def fuzzyClass(img,useBurnWaterMask:bool=True,useForestMask:bool=True):
  forestCover = ee.Image('UMD/hansen/global_forest_change_2023_v1_11').select('treecover2000').gt(50)

  unmixImg = img

  waterFraction = ee.Image(unmixImg.select('water')).float()
  vegFraction = ee.Image(unmixImg.select('veg')).float()
  bareFraction = ee.Image(unmixImg.select('bare')).float()
  burnFraction = ee.Image(unmixImg.select('burn')).float()
  
  burnWaterMask = burnFraction.lt(waterFraction)
  
  slopeArr = ee.Image('projects/ee-gregoryoakessentone/assets/Slope_Tile-34_Re').float()
  handArr = ee.Image('projects/ee-gregoryoakessentone/assets/Hand_Tile-34_Re').float()
  
  wvSumImg = ee.Image(waterFraction.add(vegFraction)).float()
  wbSumImg = ee.Image(waterFraction.add(bareFraction)).float()
  bbvSumImg = ee.Image(ee.Image(bareFraction.add(vegFraction)).add(burnFraction)).float()
  
  #### Open Water ####
  
  ow1_water_frac = ee.Image(fuzzy.fuzzy_gt(waterFraction, low_bound=65, up_bound=80)).float()
  ow1_slope = ee.Image(fuzzy.fuzzy_lt(slopeArr, low_bound=2, up_bound=4)).float()
  ow1_hand = ee.Image(fuzzy.fuzzy_lt(handArr, low_bound=25, up_bound=35)).float()
  ow1 = ee.Image(fuzzy.fuzzy_and(ee.ImageCollection.fromImages([ee.Image(ow1_water_frac), ee.Image(ow1_slope), ee.Image(ow1_hand)]))).float()
  
  #### Flooded Veg ####
  # ]efv = np.where(wvSumImg>=70,np.where((vegFraction >= 25) & (vegFraction < 75),np.where((waterFraction >= 25) & (waterFraction < 75),np.where(slopeArr<2.5,1,0),0),0),0)
  
  efv_sum = ee.Image(fuzzy.fuzzy_gt(wvSumImg, low_bound=55, up_bound=70)).float()
  efv_veg_gt = ee.Image(fuzzy.fuzzy_gt(vegFraction, low_bound=10, up_bound=25)).float()
  efv_veg_lt = ee.Image(fuzzy.fuzzy_lt(vegFraction, low_bound=65, up_bound=75)).float()
  
  efv_veg = ee.Image(fuzzy.fuzzy_and(ee.ImageCollection.fromImages([ee.Image(efv_veg_gt), ee.Image(efv_veg_lt)]))).float().copyProperties(efv_sum,['dimensions'])
  
  efv_water_gt = ee.Image(fuzzy.fuzzy_gt(waterFraction, low_bound=30, up_bound=10)).float()
  efv_water_lt = ee.Image(fuzzy.fuzzy_lt(waterFraction, low_bound=75, up_bound=75)).float()
  efv_water = ee.Image(fuzzy.fuzzy_and(ee.ImageCollection.fromImages([ee.Image(efv_water_gt), ee.Image(efv_water_lt)]))).float()
  
  efv_slope = ee.Image(fuzzy.fuzzy_lt(slopeArr, low_bound=1, up_bound=3)).float()
  
  #### Fuzzy and - GEE Collection error for homogenous Images ####
  efv = ee.Image(efv_sum.min(efv_veg).min(efv_water).min(efv_slope))
  
  #### Wet Bare Sand /  Turbid Water ####
  # wbs = np.where(wbSumImg>=75,np.where((waterFraction >= 25) & (waterFraction < 75),np.where((bareFraction >= 25) & (bareFraction < 75),np.where(slopeArr<=2.5,1,0),0),0),0)
  
  wbs_sum = fuzzy.fuzzy_gt(wbSumImg, low_bound=65, up_bound=80).float()
  wbs_water_gt = fuzzy.fuzzy_gt(waterFraction, low_bound=25, up_bound=30).float()
  wbs_water_lt = fuzzy.fuzzy_lt(waterFraction, low_bound=65, up_bound=75).float()
  wbs_water = fuzzy.fuzzy_and(ee.ImageCollection.fromImages([wbs_water_gt, wbs_water_lt])).float()
  
  wbs_bare_gt = fuzzy.fuzzy_gt(bareFraction, low_bound=20, up_bound=30).float()
  wbs_bare_lt = fuzzy.fuzzy_lt(bareFraction, low_bound=65, up_bound=75).float()
  wbs_bare = fuzzy.fuzzy_and(ee.ImageCollection.fromImages([wbs_bare_gt, wbs_bare_lt])).float()
  
  wbs_hand = fuzzy.fuzzy_lt(handArr, low_bound=8.14301279649998, up_bound=40).float()
  wbs_slope = fuzzy.fuzzy_lt(slopeArr, low_bound=2, up_bound=3).float()
  
  #wbs = fuzzy_and(ee.ImageCollection.fromImages([wbs_sum, wbs_water, wbs_bare, wbs_hand, wbs_slope])).float()
  
  wbs = ee.Image(wbs_sum.min(wbs_water).min(wbs_bare).min(wbs_hand).min(wbs_slope))
  
  #### Bare Earth ####
  ## Part 1 ##
  # bbvP1 = np.where(bbvSumImg>=60,np.where((vegFraction >= 25) & (vegFraction < 75),np.where((burnFraction >= 20) & (burnFraction < 75),1,0),0),0)
  
  bbvp1_sum = fuzzy.fuzzy_gt(bbvSumImg, low_bound=65, up_bound=80).float()
  
  bbvp1_veg_gt = fuzzy.fuzzy_gt(vegFraction, low_bound=10, up_bound=22.9958995187748).float()
  bbvp1_veg_lt = fuzzy.fuzzy_lt(vegFraction, low_bound=60.7087890735419, up_bound=85).float()
  
  bbvp1_veg = fuzzy.fuzzy_and(ee.ImageCollection.fromImages([bbvp1_veg_gt, bbvp1_veg_lt])).float()
  
  bbvp1_burn_gt = fuzzy.fuzzy_gt(burnFraction, low_bound=10, up_bound=20).float()
  bbvp1_burn_lt = fuzzy.fuzzy_lt(burnFraction, low_bound=64.8405077807786, up_bound=75).float()
  bbvp1_burn = fuzzy.fuzzy_and(ee.ImageCollection.fromImages([bbvp1_burn_gt, bbvp1_burn_lt])).float()
  
  # bbvp1 = fuzzy.fuzzy_and(ee.ImageCollection.fromImages([bbvp1_sum, bbvp1_veg, bbvp1_burn])).float()
  
  bbvp1 = ee.Image(bbvp1_sum.min(bbvp1_veg).min(bbvp1_burn))
  
  bbvp2_sum = fuzzy.fuzzy_gt(bbvSumImg, low_bound=54.4905589754301, up_bound=75).float()
  
  bbvp2_veg_gt = fuzzy.fuzzy_gt(vegFraction, low_bound=10, up_bound=30).float()
  bbvp2_veg_lt = fuzzy.fuzzy_lt(vegFraction, low_bound=66.8533402937843, up_bound=75).float()
  
  bbvp2_veg = fuzzy.fuzzy_and(ee.ImageCollection.fromImages([bbvp2_veg_gt, bbvp2_veg_lt])).float()
  
  bbvp2_bare_gt = fuzzy.fuzzy_gt(bareFraction, low_bound=10, up_bound=25).float()
  bbvp2_bare_lt = fuzzy.fuzzy_lt(bareFraction, low_bound=70.2574806945563, up_bound=75).float()
  
  bbvp2_bare = fuzzy.fuzzy_and(ee.ImageCollection.fromImages([bbvp2_bare_gt, bbvp2_bare_lt])).float()
  
  bbvp2_bare = bbvp2_bare_gt.min(bbvp2_bare_lt)
  
  # bbvp2 = fuzzy_and(ee.ImageCollection.fromImages([bbvp2_sum, bbvp2_veg, bbvp2_bare])).float()
  
  bbvp2 = bbvp2_sum.min(bbvp2_veg).min(bbvp2_bare)
  
  #bbv = fuzzy_or(ee.ImageCollection.fromImages([bbvp1, bbvp2])).float()
  
  bbv = bbvp1.max(bbvp2)
  
  #### Green Veg ####
  # gv = np.where(vegFraction>=60,1,0)
  
  gv = fuzzy.fuzzy_gt(vegFraction, low_bound=70, up_bound=85).float()
  
  #### Bare Earth ####
  
  bs = fuzzy.fuzzy_gt(bareFraction, low_bound=65, up_bound=65).float()
  
  #### Burned Land ####
  
  burn = fuzzy.fuzzy_gt(burnFraction, low_bound=34.2861877847087, up_bound=80).float()
  
  #### Topo Unsuit ####
  
  topoSlope = fuzzy.fuzzy_gt(slopeArr, low_bound=3, up_bound=5).float()
  topoHnd = fuzzy.fuzzy_gt(handArr, low_bound=35, up_bound=49.9957150211596).float()
  #topoUnsuit = fuzzy.fuzzy_or(ee.ImageCollection.fromImages([topoSlope, topoHnd])).float()
  
  topoUnsuit = topoSlope.max(topoHnd)
  
  constant = ee.Image.constant(0).add(ee.Image(efv).subtract(efv))
  efvClass = ee.Image.constant(0).add(efv)
  wbsClass = ee.Image.constant(0).add(wbs)
  bbvClass = ee.Image.constant(0).add(bbv)
  owClass = ee.Image.constant(0).add(ow1)
  gvClass = ee.Image.constant(0).add(gv)
  bsClass = ee.Image.constant(0).add(bs)
  burnClass = ee.Image.constant(0).add(burn)
  topoClass = ee.Image.constant(0).add(topoUnsuit)
  
  
  
  stackedMemberShip = ee.ImageCollection.fromImages([constant,efvClass,wbsClass,bbvClass,owClass,gvClass,bsClass,burnClass,topoClass])
  
  print(stackedMemberShip.size().getInfo())
  
  membershipArray = ee.Image(stackedMemberShip.toArray().arrayArgmax().arrayGet(0))
  print(membershipArray.getInfo())

  if useBurnWaterMask == True:
    membershipArray = membershipArray.where(membershipArray.gt(4),3).mask(burnWaterMask).unmask(3)
  if useForestMask == True:
    membershipArray = membershipArray.where(forestCover.eq(1),3)
  return ee.Image(membershipArray).byte() 
