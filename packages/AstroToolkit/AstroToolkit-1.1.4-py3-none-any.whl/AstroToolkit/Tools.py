from bokeh.plotting import figure, output_file
from bokeh.layouts import gridplot, row, column
from bokeh.models import CustomJS, Button
from bokeh import events
from bokeh.layouts import layout
import pandas as pd

'''
Changelog:
- Implemented a new naming convention for objects, with its own function for positions or gaia sources

Known Issues:
- Detections at large distance from focus are slightly innacurate due to lack of projection support in Bokeh 
- Crashes (usually upon multiple consecutive executions) in timseries analysis tool

To Do:
- Clean up errors
- ADD UPPER LIMITS TO SED TOOL + Check issues with plotting
'''

# File handling -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def savefile(data,identifier,extension='csv',pos=None,source=None):
	if pos!=None:
		file_name=getfilename(identifier=identifier,extension=extension,pos=pos)
	elif source!=None:
		file_name=getfilename(identifier=identifier,extension=extension,source=source)
	
	if extension=='csv':
		data.to_csv(file_name,index=False)

def getfilename(identifier,extension,pos=None,source=None):
	import os
	
	if pos!=None:
		middle_str=f'{pos[0]}_{pos[1]}'
		
		file_name=f'{middle_str}_{identifier}.{extension}'
	
	elif source!=None:
		prefix_str=convertsource(source=source)
		middle_str=str(source)
		
		file_name=f'{prefix_str}_{middle_str}_{identifier}.{extension}'

	file_name=os.path.join(os.getcwd(),file_name)

	return file_name

def convertsource(source):
	from .Surveys.Gaia import GaiaGetCoords
	from .Miscellaneous.ProperMotionCorrection import PMCorrection as CorrectPM
	
	gaia_data=gaiaquery(source=source)

	ra,dec,pmra,pmdec=gaia_data['ra'].values[0],gaia_data['dec'].values[0],gaia_data['pmra'].values[0],gaia_data['pmdec'].values[0]
	pos=[ra,dec]
	
	pos=correctPM([2016,0],[2000,0],ra,dec,pmra,pmdec)

	ObjRef=convertpos(pos=pos)
	
	return ObjRef

def convertpos(pos):
	from astropy.coordinates import Angle
	from astropy import units as u
	import numpy as np

	ra,dec=pos[0],pos[1]
	if dec<0:
		negativeDec=True
	else:
		negativeDec=False

	ra=Angle(ra,u.degree)
	dec=Angle(dec,u.degree)
	
	ra=ra.hms
	dec=dec.dms
	
	ra_arr=np.array([0,0,0],dtype=float)
	dec_arr=np.array([0,0,0],dtype=float)		

	ra_arr[0]=ra[0]
	ra_arr[1]=ra[1]
	ra_arr[2]=ra[2]

	dec_arr[0]=dec[0]
	dec_arr[1]=dec[1]
	dec_arr[2]=dec[2]

	ra_str_arr=[]
	for element in ra_arr:
		if element<0:
			element=element*-1

		# Will only retain the SS part from final iteration
		ra_remainder=element-int(element)		

		element=int(element)
		element=str(element).zfill(2)
		ra_str_arr.append(element)

	dec_str_arr=[]
	for element in dec_arr:
		if element<0:
			element=element*-1
		
		dec_remainder=element-int(element)
		
		element=int(element)
		element=str(element).zfill(2)
		dec_str_arr.append(element)

	# Format remainder: force 2 decimal places, round to 2 decimal places and remove '0.'
	ra_str_arr[2]+=str('{:.2f}'.format(round(ra_remainder,2))[1:])
	dec_str_arr[2]+=str('{:.2f}'.format(round(dec_remainder,2))[1:])
	
	if negativeDec==True:
		objRef=f'J{ra_str_arr[0]}{ra_str_arr[1]}{ra_str_arr[2]}-{dec_str_arr[0]}{dec_str_arr[1]}{dec_str_arr[2]}'
	elif negativeDec==False:
		objRef=f'J{ra_str_arr[0]}{ra_str_arr[1]}{ra_str_arr[2]}+{dec_str_arr[0]}{dec_str_arr[1]}{dec_str_arr[2]}'
	else:
		print('objRef Error')
		return None
	
	return objRef

# Data Queries ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def panstarrsquery(source=None,pos=None,radius=3,save_data=False): # maybe have a keep_cols parameter?
	from .Surveys.PanSTARRS import PanSTARRSQueryCoords
	from .Miscellaneous.ProperMotionCorrection import PMCorrection as CorrectPM
	import os

	if source!=None and pos!=None:
		raise Exception('simulatenous source and pos input detected')
	
	if source!=None:
		gaia_data=gaiaquery(source=source)
		if isinstance(gaia_data,pd.DataFrame):
			ra,dec,pmra,pmdec=gaia_data['ra'].values[0],gaia_data['dec'].values[0],gaia_data['pmra'].values[0],gaia_data['pmdec'].values[0]
			pos_corrected=CorrectPM([2016,0],[2012,0],ra,dec,pmra,pmdec)
			ra,dec=pos_corrected[0],pos_corrected[1]
		else:
			return None
	elif pos!=None:
		ra,dec=pos[0],pos[1]
	else:
		raise Exception('either source or pos input required')

	data=PanSTARRSQueryCoords(ra,dec,radius)
	
	if save_data==True:
		savefile(data=data,identifier='PanSTARRS-Data',extension='csv',pos=pos,source=source)

	return data

def skymapperquery(source=None,pos=None,radius=3,save_data=False):
	from .Surveys.SkyMapper import SkyMapperQueryCoords
	from .Miscellaneous.ProperMotionCorrection import PMCorrection as CorrectPM
	
	if source!=None and pos!=None:
		raise Exception('simulatenous source and pos input detected')
	
	if source!=None:
		gaia_data=gaiaquery(source=source)
		if isinstance(gaia_data,pd.DataFrame):
			ra,dec,pmra,pmdec=gaia_data['ra'].values[0],gaia_data['dec'].values[0],gaia_data['pmra'].values[0],gaia_data['pmdec'].values[0]
			pos_corrected=CorrectPM([2016,0],[2016,0],ra,dec,pmra,pmdec)
			ra,dec=pos_corrected[0],pos_corrected[1]
		else:
			return None
		
	elif pos!=None:
		ra,dec=pos[0],pos[1]
	else:
		raise Exception('either source or pos input required')
		return None
	
	data=SkyMapperQueryCoords(ra,dec,radius)
	
	if save_data==True:
		savefile(data=data,identifier='SkyMapper-Data',extension='csv',pos=pos,source=source)

	return data

def gaiaquery(source=None,pos=None,radius=3,save_data=False):
	from .Surveys.Gaia import GaiaQuerySource
	from .Surveys.Gaia import GaiaQueryCoords

	if source!=None and pos!=None:
		raise Exception('simulatenous source and pos input detected')
	
	if source!=None:
		data=GaiaQuerySource(source=source)
	elif pos!=None:
		ra,dec=pos[0],pos[1]
		data=GaiaQueryCoords(ra,dec)
	else:
		raise Exception('either source or pos input required')
	
	if save_data==True:
		savefile(data=data,identifier='Gaia-Data',extension='csv',pos=pos,source=source)

	return data

def galexquery(source=None,pos=None,radius=3,save_data=False):
	from .Surveys.GALEX import GALEXQueryCoords
	from .Miscellaneous.ProperMotionCorrection import PMCorrection as CorrectPM
	
	if source!=None and pos!=None:
		raise Exception('simulatenous source and pos input detected')
	
	if source!=None:
		gaia_data=gaiaquery(source=source)
		if isinstance(gaia_data,pd.DataFrame):
			ra,dec,pmra,pmdec=gaia_data['ra'].values[0],gaia_data['dec'].values[0],gaia_data['pmra'].values[0],gaia_data['pmdec'].values[0]
			pos_corrected=CorrectPM([2016,0],[2007,0],ra,dec,pmra,pmdec)
			ra,dec=pos_corrected[0],pos_corrected[1]
		else:
			return None
		
	elif pos!=None:
		ra,dec=pos[0],pos[1]
	else:
		raise Exception('either source or pos input required')
		return None

	data=GALEXQueryCoords(ra,dec,radius)
	
	if save_data==True:
		savefile(data=data,identifier='GALEX-Data',extension='csv',pos=pos,source=source)

	return data

def rosatquery(source=None,pos=None,radius=3,save_data=False):
	from .Surveys.ROSAT import ROSATQueryCoords
	from .Miscellaneous.ProperMotionCorrection import PMCorrection as CorrectPM	

	if source!=None and pos!=None:
		raise Exception('simulatenous source and pos input detected')
	
	if source!=None:
		gaia_data=gaiaquery(source=source)
		if isinstance(gaia_data,pd.DataFrame):
			ra,dec,pmra,pmdec=gaia_data['ra'].values[0],gaia_data['dec'].values[0],gaia_data['pmra'].values[0],gaia_data['pmdec'].values[0]
			pos_corrected=CorrectPM([2016,0],[1991,0],ra,dec,pmra,pmdec)
			ra,dec=pos_corrected[0],pos_corrected[1]
		else:
			return None
	elif pos!=None:
		ra,dec=pos[0],pos[1]
	else:
		raise Exception('either source or pos input required')
		return None
	
	data=ROSATQueryCoords(ra,dec,radius)
	
	if save_data==True:
		savefile(data=data,identifier='ROSAT-Data',extension='csv',pos=pos,source=source)
		
	return data

def sdssquery(source=None,pos=None,radius=3,save_data=False):
	from .Surveys.SDSS import get_data
	from .Miscellaneous.ProperMotionCorrection import PMCorrection as CorrectPM	

	if source!=None and pos!=None:
		raise Exception('simulatenous source and pos input detected')
	
	if source!=None:
		gaia_data=gaiaquery(source=source)
		if isinstance(gaia_data,pd.DataFrame):
			ra,dec,pmra,pmdec=gaia_data['ra'].values[0],gaia_data['dec'].values[0],gaia_data['pmra'].values[0],gaia_data['pmdec'].values[0]
			pos_corrected=CorrectPM([2016,0],[2017,0],ra,dec,pmra,pmdec)
			ra,dec=pos_corrected[0],pos_corrected[1]
		else:
			return None
		
	elif pos!=None:
		ra,dec=pos[0],pos[1]
	else:
		raise Exception('either source or pos input required')
		return None
		
	data=get_data(ra=ra,dec=dec,radius=radius)
	
	if save_data==True:
		savefile(data=data,identifier='SDSS-Data',extension='csv',pos=pos,source=source)

	return data

def wisequery(source=None,pos=None,radius=3,save_data=False):
	from .Surveys.WISE import get_data
	from .Miscellaneous.ProperMotionCorrection import PMCorrection as CorrectPM		

	if source!=None and pos!=None:
		raise Exception('simulatenous source and pos input detected')
	
	if source!=None:
		gaia_data=gaiaquery(source=source)
		if isinstance(gaia_data,pd.DataFrame):
			ra,dec,pmra,pmdec=gaia_data['ra'].values[0],gaia_data['dec'].values[0],gaia_data['pmra'].values[0],gaia_data['pmdec'].values[0]
			pos_corrected=CorrectPM([2016,0],[2010,5],ra,dec,pmra,pmdec)
			ra,dec=pos_corrected[0],pos_corrected[1]
		else:
			return None
		
	elif pos!=None:
		ra,dec=pos[0],pos[1]
	else:
		raise Exception('either source or pos input required')
		return None
		
	data=get_data(ra=ra,dec=dec,radius=radius)
	
	if save_data==True:
		savefile(data=data,identifier='WISE-Data',extension='csv',pos=pos,source=source)

	return data

def twomassquery(source=None,pos=None,radius=3,save_data=False):
	from .Surveys.TWOMASS import get_data
	from .Miscellaneous.ProperMotionCorrection import PMCorrection as CorrectPM	
	
	if source!=None and pos!=None:
		raise Exception('simulatenous source and pos input detected')
	
	if source!=None:
		gaia_data=gaiaquery(source=source)
		if isinstance(gaia_data,pd.DataFrame):
			ra,dec,pmra,pmdec=gaia_data['ra'].values[0],gaia_data['dec'].values[0],gaia_data['pmra'].values[0],gaia_data['pmdec'].values[0]
			pos_corrected=CorrectPM([2016,0],[2010,5],ra,dec,pmra,pmdec)
			ra,dec=pos_corrected[0],pos_corrected[1]
		else:
			return None
		
	elif pos!=None:
		ra,dec=pos[0],pos[1]
	else:
		raise Exception('either source or pos input required')
		return None
	
	data=get_data(ra=ra,dec=dec,radius=radius)
	
	if save_data==True:
		savefile(data=data,identifier='2MASS-Data',extension='csv',pos=pos,source=source)

	return data

# Imaging Queries ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def getpanstarrsimage(source=None,pos=None,image_size=30,band='g',overlay=['gaia'],get_time=False):
	from astropy.time import Time

	from .Surveys.PanSTARRS import get_info
	from .Miscellaneous.ProperMotionCorrection import PMCorrection as CorrectPM
	from .Surveys.PanSTARRS import get_plot
	from .Overlays.Overlay_Selection import overlaySelection

	if source!=None and pos!=None:
		raise Exception('simulatenous source and pos input detected')
	
	if source!=None:
		# Fetch coordinates and proper motion for object
		gaia_data=gaiaquery(source=source)
		if isinstance(gaia_data,pd.DataFrame):
			ra,dec,pmra,pmdec=gaia_data['ra'].values[0],gaia_data['dec'].values[0],gaia_data['pmra'].values[0],gaia_data['pmdec'].values[0]
		else:
			if get_time==False:
				return None
			else:
				return None, None
		
		# Get an image and get the time it was taken
		mjd=get_info(ra=ra,dec=dec,size=image_size,band=band)[1]
		if mjd==None:
			if get_time==False:
				return None
			else:
				return None, None
		imageTime=Time(mjd,format='mjd').to_datetime()
		imageTime=[imageTime.year,imageTime.month]
		
		# Correct for proper motion to this image time
		pos_corrected=CorrectPM([2016,0],imageTime,ra,dec,pmra,pmdec)
		ra,dec=pos_corrected[0],pos_corrected[1]
	
	elif pos!=None:
		# No proper motion correction
		ra,dec=pos[0],pos[1]
		mjd=get_info(ra=ra,dec=dec,size=image_size,band=band)[1]
		
		if mjd==None:
			if get_time==False:
				return None
			else:
				return None, None
	else:
		raise Exception('either source or pos input required')
	
	# Fetch final image using coordinates corrected to the time of the original image
	plot=get_plot(ra=ra,dec=dec,size=image_size,band=band)

	if plot==None:
		if get_time==False:
			return None
		else:
			return None, None

	# Get half image size (in deg, used for detection size scaling)
	border=image_size/7200

	if source!=None:
		plot,detections_made=overlaySelection(plot,ra,dec,overlay,mjd,image_size,border,pmra,pmdec)
	elif pos!=None:
		plot,detections_made=overlaySelection(plot,ra,dec,overlay,mjd,image_size,border)

	if plot!=None and detections_made!=False:
		plot.legend.click_policy="hide"	

		# Double click to hide legend
		toggle_legend_js = CustomJS(args=dict(leg=plot.legend[0]), code='''
			 if (leg.visible) {
				 leg.visible = false
				 }
			 else {
				 leg.visible = true
			 }
		''')
	
		plot.js_on_event(events.DoubleTap, toggle_legend_js)  

	if source!=None:
		output_file(f'{source}_image.html')

	elif pos!=None:
		if pos[1]>=0:
			output_file(f"{pos[0]}+{pos[1]}_image.html")	
		else:
			output_file(f"{pos[0]}{pos[1]}_image.html")

	if get_time==True:
		imageTime=Time(mjd,format='mjd').to_datetime()
		imageTime=[imageTime.year,imageTime.month]
		return plot, imageTime
	else:
		return plot

def getskymapperimage(source=None,pos=None,image_size=30,band='g',overlay=['gaia'],get_time=False):
	from astropy.time import Time
	
	from .Surveys.SkyMapper import get_info
	from .Miscellaneous.ProperMotionCorrection import PMCorrection as CorrectPM
	from .Surveys.SkyMapper import get_plot
	from .Overlays.Overlay_Selection import overlaySelection

	if source!=None and pos!=None:
		raise Exception('simulatenous source and pos input detected')
	
	if source!=None:
		# Fetch coordinates and proper motion for object
		gaia_data=gaiaquery(source=source)
		if isinstance(gaia_data,pd.DataFrame):
			ra,dec,pmra,pmdec=gaia_data['ra'].values[0],gaia_data['dec'].values[0],gaia_data['pmra'].values[0],gaia_data['pmdec'].values[0]
		else:
			if get_time==False:
				return None
			else:
				return None, None

		# Get an image and get the time it was taken
		mjd=get_info(ra=ra,dec=dec,size=image_size,band=band)[1]
		if mjd==None:
			if get_time==False:
				return None
			else:
				return None, None
		imageTime=Time(mjd,format='mjd').to_datetime()
		imageTime=[imageTime.year,imageTime.month]
		
		# Correct for proper motion to this image time
		pos_corrected=CorrectPM([2016,0],imageTime,ra,dec,pmra,pmdec)
		ra,dec=pos_corrected[0],pos_corrected[1]
	
	elif pos!=None:
		# No proper motion correction
		ra,dec=pos[0],pos[1]
		mjd=get_info(ra=ra,dec=dec,size=image_size,band=band)[1]
		
		if mjd==None:
			if get_time==False:
				return None
			else:
				return None, None
	else:
		raise Exception('either source or pos input required')
	
	# Fetch final image using coordinates corrected to the time of the original image
	plot=get_plot(ra=ra,dec=dec,size=image_size,band=band)

	if plot==None:
		if get_time==False:
			return None
		else:
			return None, None

	# Get half image size (in deg, used for detection size scaling)
	border=image_size/7200

	if source!=None:
		plot,detections_made=overlaySelection(plot,ra,dec,overlay,mjd,image_size,border,pmra,pmdec)
	elif pos!=None:
		plot,detections_made=overlaySelection(plot,ra,dec,overlay,mjd,image_size,border)
	
	if plot!=None and detections_made!=False:
		plot.legend.click_policy="hide"	

		# Double click to hide legend
		toggle_legend_js = CustomJS(args=dict(leg=plot.legend[0]), code='''
			 if (leg.visible) {
				 leg.visible = false
				 }
			 else {
				 leg.visible = true
			 }
		''')
	
		plot.js_on_event(events.DoubleTap, toggle_legend_js)  

	if source!=None:
		output_file(f'{source}_image.html')

	elif pos!=None:
		if pos[1]>=0:
			output_file(f"{pos[0]}+{pos[1]}_image.html")	
		else:
			output_file(f"{pos[0]}{pos[1]}_image.html")

	if get_time==True:
		imageTime=Time(mjd,format='mjd').to_datetime()
		imageTime=[imageTime.year,imageTime.month]
		return plot, imageTime
	else:
		return plot

def getdssimage(source=None,pos=None,image_size=30,overlay=['gaia'],get_time=False):
	from astropy.time import Time
	
	from .Surveys.DSS import get_info
	from .Miscellaneous.ProperMotionCorrection import PMCorrection as CorrectPM
	from .Surveys.DSS import get_plot
	from .Overlays.Overlay_Selection import overlaySelection

	if source!=None and pos!=None:
		raise Exception('simulatenous source and pos input detected')
	
	if source!=None:
		# Fetch coordinates and proper motion for object
		gaia_data=gaiaquery(source=source)
		if isinstance(gaia_data,pd.DataFrame):
			ra,dec,pmra,pmdec=gaia_data['ra'].values[0],gaia_data['dec'].values[0],gaia_data['pmra'].values[0],gaia_data['pmdec'].values[0]
		else:
			if get_time==False:
				return None
			else:
				return None, None
		
		# Get an image and get the time it was taken
		mjd=get_info(ra=ra,dec=dec,size=image_size)[1]
		if mjd==None:
			if get_time==False:
				return None
			else:
				return None, None
			
		imageTime=Time(mjd,format='mjd').to_datetime()
		imageTime=[imageTime.year,imageTime.month]
		
		# Correct for proper motion to this image time
		pos_corrected=CorrectPM([2016,0],imageTime,ra,dec,pmra,pmdec)
		ra,dec=pos_corrected[0],pos_corrected[1]
	
	elif pos!=None:
		# No proper motion correction
		ra,dec=pos[0],pos[1]
		mjd=get_info(ra=ra,dec=dec,size=image_size)[1]
			
		if mjd==None:
			if get_time==False:
				return None
			else:
				return None, None
	else:
		raise Exception('either source or pos input required')
	
	# Fetch final image using coordinates corrected to the time of the original image
	plot=get_plot(ra=ra,dec=dec,size=image_size)

	if plot==None:
		if get_time==False:
			return None
		else:
			return None, None

	# Get half image size (in deg, used for detection size scaling)
	border=image_size/7200

	if source!=None:
		plot,detections_made=overlaySelection(plot,ra,dec,overlay,mjd,image_size,border,pmra,pmdec)
	elif pos!=None:
		plot,detections_made=overlaySelection(plot,ra,dec,overlay,mjd,image_size,border)

	plot.legend.click_policy="hide"	

	if plot!=None and detections_made!=None:
		# Double click to hide legend
		toggle_legend_js = CustomJS(args=dict(leg=plot.legend[0]), code='''
			 if (leg.visible) {
				 leg.visible = false
				 }
			 else {
				 leg.visible = true
			 }
		''')
	
		plot.js_on_event(events.DoubleTap, toggle_legend_js)  

	if source!=None:
		output_file(f'{source}_image.html')
	
	elif pos!=None:
		if pos[1]>=0:
			output_file(f"{pos[0]}+{pos[1]}_image.html")	
		else:
			output_file(f"{pos[0]}{pos[1]}_image.html")

	if get_time==True:
		imageTime=Time(mjd,format='mjd').to_datetime()
		imageTime=[imageTime.year,imageTime.month]
		return plot, imageTime
	else:
		return plot

# Exhaustitive imaging query ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def getimage(source=None,pos=None,image_size=30,overlay=['gaia'],get_time=False,band='g'):
	if source!=None and pos!=None:
		raise Exception('simulatenous source and pos input detected')	
	elif source==None and pos==None:
		raise Exception('either source or pos input required')	

	if source!=None and get_time==True:
		image_axis,image_time=getpanstarrsimage(source=source,get_time=True,band=band,overlay=overlay,image_size=image_size)
		if image_axis==None:
			image_axis,image_time=getskymapperimage(source=source,get_time=True,band=band,overlay=overlay,image_size=image_size)
			if image_axis==None:
				image_axis,image_time=getdssimage(source=source,get_time=True,overlay=overlay,image_size=image_size)
		
		return image_axis,image_time
	
	elif pos!=None and get_time==True:
		image_axis,image_time=getpanstarrsimage(pos=pos,get_time=True,band=band,overlay=overlay,image_size=image_size)
		if image_axis==None:
			image_axis,image_time=getskymapperimage(pos=pos,get_time=True,band=band,overlay=overlay,image_size=image_size)
			if image_axis==None:
				image_axis,image_time=getdssimage(pos=pos,get_time=True,overlay=overlay,image_size=image_size)
				
		return image_axis,image_time
	
	elif source!=None and get_time==False:
		image_axis=getpanstarrsimage(source=source,get_time=False,band=band,overlay=overlay,image_size=image_size)
		if image_axis==None:
			image_axis=getskymapperimage(source=source,get_time=False,band=band,overlay=overlay,image_size=image_size)
			if image_axis==None:
				image_axis=getdssimage(source=source,get_time=False,overlay=overlay,image_size=image_size)
				
		return image_axis
				
	elif pos!=None and get_time==False:
		image_axis=getpanstarrsimage(pos=pos,get_time=False,band=band,overlay=overlay,image_size=image_size)
		if image_axis==None:
			image_axis=getskymapperimage(pos=pos,get_time=False,band=band,overlay=overlay,image_size=image_size)
			if image_axis==None:
				image_axis=getdssimage(pos=pos,get_time=False,overlay=overlay,image_size=image_size)
		
		return image_axis
				
# Photometry Queries  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def getpanstarrsphot(radius=3,source=None,pos=None,save_data=False):
	from .Surveys.PanSTARRS import PanSTARRSGetPhotometryCoords
	from .Miscellaneous.ProperMotionCorrection import PMCorrection as CorrectPM	

	if source!=None and pos!=None:
		raise Exception('simulatenous source and pos input detected')
	
	if source!=None:
		gaia_data=gaiaquery(source=source)
		if isinstance(gaia_data,pd.DataFrame):
			ra,dec,pmra,pmdec=gaia_data['ra'].values[0],gaia_data['dec'].values[0],gaia_data['pmra'].values[0],gaia_data['pmdec'].values[0]
		else:
			return None

		pos_corrected=CorrectPM([2016,0],[2012,0],ra,dec,pmra,pmdec)
		ra,dec=pos_corrected[0],pos_corrected[1]
	elif pos!=None:
		ra,dec=pos[0],pos[1]
	else:
		raise Exception('either source or pos input required')
		
	data=PanSTARRSGetPhotometryCoords(ra,dec,radius)
	
	if save_data==True:
		savefile(data=data,identifier='PanSTARRS-Phot',extension='csv',pos=pos,source=source)

	return data

def getskymapperphot(radius=3,source=None,pos=None,save_data=False):
	from .Surveys.SkyMapper import SkyMapperGetPhotometryCoords
	from .Miscellaneous.ProperMotionCorrection import PMCorrection as CorrectPM
	
	if source!=None and pos!=None:
		raise Exception('simulatenous source and pos input detected')
	
	if source!=None:
		gaia_data=gaiaquery(source=source)
		if isinstance(gaia_data,pd.DataFrame):
			ra,dec,pmra,pmdec=gaia_data['ra'].values[0],gaia_data['dec'].values[0],gaia_data['pmra'].values[0],gaia_data['pmdec'].values[0]
		else:
			return None
		
		pos_corrected=CorrectPM([2016,0],[2016,0],ra,dec,pmra,pmdec)
		ra,dec=pos_corrected[0],pos_corrected[1]
	elif pos!=None:
		ra,dec=pos[0],pos[1]
	else:
		raise Exception('either source or pos input required')

	data=SkyMapperGetPhotometryCoords(ra,dec,radius)
	
	if save_data==True:
		savefile(data=data,identifier='SkyMapper-Phot',extension='csv',pos=pos,source=source)

	return data

def getgaiaphot(radius=3,source=None,pos=None,save_data=False):
	from .Surveys.Gaia import GaiaGetPhotometryCoords
	from .Surveys.Gaia import GaiaGetPhotometrySource
	from .Miscellaneous.ProperMotionCorrection import PMCorrection as CorrectPM

	if source!=None and pos!=None:
		raise Exception('simulatenous source and pos input detected')
	
	if source!=None:
		data=GaiaGetPhotometrySource(source=source)
	elif pos!=None:
		ra,dec=pos[0],pos[1]
		data=GaiaGetPhotometryCoords(ra,dec,radius)
	else:
		raise Exception('either source or pos input required')

	if save_data==True:
		savefile(data=data,identifier='Gaia-Phot',extension='csv',pos=pos,source=source)

	return data

def getgalexphot(radius=3,source=None,pos=None,save_data=False):
	from .Surveys.GALEX import GALEXGetPhotometryCoords
	from .Miscellaneous.ProperMotionCorrection import PMCorrection as CorrectPM

	if source!=None and pos!=None:
		raise Exception('simulatenous source and pos input detected')
	
	if source!=None:
		gaia_data=gaiaquery(source=source)
		if isinstance(gaia_data,pd.DataFrame):
			ra,dec,pmra,pmdec=gaia_data['ra'].values[0],gaia_data['dec'].values[0],gaia_data['pmra'].values[0],gaia_data['pmdec'].values[0]
		else:
			return None

		pos_corrected=CorrectPM([2016,0],[2007,0],ra,dec,pmra,pmdec)
		ra,dec=pos_corrected[0],pos_corrected[1]
	elif pos!=None:
		ra,dec=pos[0],pos[1]
	else:
		raise Exception('either source or pos input required')
		return None

	data=GALEXGetPhotometryCoords(ra,dec,radius)
	
	if save_data==True:
		savefile(data=data,identifier='GALEX-Phot',extension='csv',pos=pos,source=source)

	return data

def getsdssphot(radius=3,source=None,pos=None,save_data=False):
	from .Surveys.SDSS import get_photometry
	from .Miscellaneous.ProperMotionCorrection import PMCorrection as CorrectPM	

	if source!=None and pos!=None:
		raise Exception('simulatenous source and pos input detected')
	
	if source!=None:
		gaia_data=gaiaquery(source=source)
		if isinstance(gaia_data,pd.DataFrame):
			ra,dec,pmra,pmdec=gaia_data['ra'].values[0],gaia_data['dec'].values[0],gaia_data['pmra'].values[0],gaia_data['pmdec'].values[0]
		else:
			return None
		
		pos_corrected=CorrectPM([2016,0],[2007,0],ra,dec,pmra,pmdec)
		ra,dec=pos_corrected[0],pos_corrected[1]
	elif pos!=None:
		ra,dec=pos[0],pos[1]
	else:
		raise Exception('either source or pos input required')
		return None
	
	data=get_photometry(ra=ra,dec=dec,radius=radius)
	
	if save_data==True:
		savefile(data=data,identifier='SDSS-Phot',extension='csv',pos=pos,source=source)

	return data

def getwisephot(radius=3,source=None,pos=None,save_data=False):
	from .Surveys.WISE import get_photometry
	from .Miscellaneous.ProperMotionCorrection import PMCorrection as CorrectPM	
	
	if source!=None and pos!=None:
		raise Exception('simulatenous source and pos input detected')
	
	if source!=None:
		gaia_data=gaiaquery(source=source)
		if isinstance(gaia_data,pd.DataFrame):
			ra,dec,pmra,pmdec=gaia_data['ra'].values[0],gaia_data['dec'].values[0],gaia_data['pmra'].values[0],gaia_data['pmdec'].values[0]
		else:
			return None
		
		pos_corrected=CorrectPM([2016,0],[2007,0],ra,dec,pmra,pmdec)
		ra,dec=pos_corrected[0],pos_corrected[1]
	elif pos!=None:
		ra,dec=pos[0],pos[1]
	else:
		raise Exception('either source or pos input required')
		return None
	
	data=get_photometry(ra=ra,dec=dec,radius=radius)
	
	if save_data==True:
		savefile(data=data,identifier='WISE-Phot',extension='csv',pos=pos,source=source)

	return data

def gettwomassphot(radius=3,source=None,pos=None,save_data=False):
	from .Surveys.TWOMASS import get_photometry
	from .Miscellaneous.ProperMotionCorrection import PMCorrection as CorrectPM	
	
	if source!=None and pos!=None:
		raise Exception('simulatenous source and pos input detected')
	
	if source!=None:
		gaia_data=gaiaquery(source=source)
		if isinstance(gaia_data,pd.DataFrame):
			ra,dec,pmra,pmdec=gaia_data['ra'].values[0],gaia_data['dec'].values[0],gaia_data['pmra'].values[0],gaia_data['pmdec'].values[0]
		else:
			return None
		
		pos_corrected=CorrectPM([2016,0],[2007,0],ra,dec,pmra,pmdec)
		ra,dec=pos_corrected[0],pos_corrected[1]
	elif pos!=None:
		ra,dec=pos[0],pos[1]
	else:
		raise Exception('either source or pos input required')
		return None
	
	data=get_photometry(ra=ra,dec=dec,radius=radius)
	
	if save_data==True:
		savefile(data=data,identifier='2MASS-Phot',extension='csv',pos=pos,source=source)

	return data

# Bulk Photometry Query

def getbulkphot(radius=3,source=None,pos=None,save_data=False):
	from .Surveys.Gaia import GaiaGetPhotometryCoords
	from .Surveys.GALEX import GALEXGetPhotometryCoords
	from .Surveys.ROSAT import ROSATGetPhotometryCoords
	from .Surveys.PanSTARRS import PanSTARRSGetPhotometryCoords
	from .Surveys.SkyMapper import SkyMapperGetPhotometryCoords
	from .Surveys.SDSS import get_photometry as get_phot_sdss
	from .Surveys.WISE import get_photometry as get_phot_wise
	from .Surveys.TWOMASS import get_photometry as get_phot_twomass
	from .Miscellaneous.ProperMotionCorrection import PMCorrection as CorrectPM
	
	if source!=None and pos!=None:
		raise Exception('simulatenous source and pos input detected')
	
	if source!=None:		
		gaia_data=gaiaquery(source=source)
		if isinstance(gaia_data,pd.DataFrame):
			ra,dec,pmra,pmdec=gaia_data['ra'].values[0],gaia_data['dec'].values[0],gaia_data['pmra'].values[0],gaia_data['pmdec'].values[0]
		
			pos_corrected=CorrectPM([2016,0],[2012,0],ra,dec,pmra,pmdec)
			ra_panstarrs,dec_panstarrs=pos_corrected[0],pos_corrected[1]
		
			pos_corrected=CorrectPM([2016,0],[2016,0],ra,dec,pmra,pmdec)
			ra_skymapper,dec_skymapper=pos_corrected[0],pos_corrected[1]
		
			ra_gaia,dec_gaia=ra,dec
		
			pos_corrected=CorrectPM([2016,0],[2007,0],ra,dec,pmra,pmdec)
			ra_galex,dec_galex=pos_corrected[0],pos_corrected[1]
		
			pos_corrected=CorrectPM([2016,0],[1991,0],ra,dec,pmra,pmdec)
			ra_rosat,dec_rosat=pos_corrected[0],pos_corrected[1]
		
			pos_corrected=CorrectPM([2016,0],[2017,0],ra,dec,pmra,pmdec)
			ra_sdss,dec_sdss=pos_corrected[0],pos_corrected[1]
		
			pos_corrected=CorrectPM([2016,0],[2010,5],ra,dec,pmra,pmdec)
			ra_wise,dec_wise=pos_corrected[0],pos_corrected[1]
		
			pos_corrected=CorrectPM([2016,0],[1999,0],ra,dec,pmra,pmdec)
			ra_twomass,dec_twomass=pos_corrected[0],pos_corrected[1]
		else:
			return None
		
	elif pos!=None:
		ra_panstarrs,dec_panstarrs=pos[0],pos[1]
		ra_skymapper,dec_skymapper=pos[0],pos[1]
		ra_gaia,dec_gaia=pos[0],pos[1]
		ra_galex,dec_galex=pos[0],pos[1]
		ra_rosat,dec_rosat=pos[0],pos[1]
		ra_sdss,dec_sdss=pos[0],pos[1]
		ra_wise,dec_wise=pos[0],pos[1]
		ra_twomass,dec_twomass=pos[0],pos[1]
		
	else:
		raise Exception('either source or pos input required')

	photometry={'gaia':None,'galex':None,'rosat':None,'panstarrs':None,'skymapper':None,'sdss':None,'wise':None,'twomass':None}
	
	try:
		data=GaiaGetPhotometryCoords(ra_gaia,dec_gaia,radius)
		photometry['gaia']=data
	except:
		print('[Photometry: GetPhotometryCoords] Note: No Gaia photometry found using given coordinates and search radius')
	try:
		data=GALEXGetPhotometryCoords(ra_galex,dec_galex,radius)
		photometry['galex']=data
	except:
		print('[Photometry: GetPhotometryCoords] Note: No GALEX photometry found using given coordinates and search radius')
	try:
		data=ROSATGetPhotometryCoords(ra_rosat,dec_rosat,radius)
		photometry['rosat']=data
	except:
		print('[Photometry: GetPhotometryCoords] Note: No ROSAT photometry found using given coordinates and search radius')
	try:
		data=PanSTARRSGetPhotometryCoords(ra_panstarrs,dec_panstarrs,radius)
		photometry['panstarrs']=data
	except:
		print('[Photometry: GetPhotometryCoords] Note: No Pan-STARRS photometry found using given coordinates and search radius')
	try:
		data=SkyMapperGetPhotometryCoords(ra_skymapper,dec_skymapper,radius)
		photometry['skymapper']=data
	except:
		print('[Photometry: GetPhotometryCoords] Note: No SkyMapper photometry found using given coordinates and search radius')
	try:
		data=get_phot_sdss(ra=ra_sdss,dec=dec_sdss,radius=radius)
		photometry['sdss']=data
	except:
		print('[Photometry: GetPhotometryCoords] Note: No SDSS photometry found using given coordinates and search radius')
	try:
		data=get_phot_wise(ra=ra_wise,dec=dec_wise,radius=radius)
		photometry['wise']=data
	except:
		print('[Photometry: GetPhotometryCoords] Note: No WISE photometry found using given coordinates and search radius')
	try:
		data=get_phot_twomass(ra=ra_twomass,dec=dec_twomass,radius=radius)
		photometry['twomass']=data
	except:
		print('[Photometry: GetPhotometryCoords] Note: No 2MASS photometry found using given coordinates and search radius')
	
	if save_data==True:
		file_name=getfilename(identifier='BulkPhot',extension='csv',pos=pos,source=source)

		with open(file_name,'w') as f:
			for key in photometry:
				try:
					# add a column denoting the survey
					photometry[key].insert(0,'survey',key)
					photometry[key].to_csv(f,index=False,lineterminator='\n',)
					
					f.write('\n')
				except:
					pass

	return photometry

# Timeseries Queries -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def ztfquery(source=None,pos=None,radius=3,save_data=False):
	from .Surveys.ZTF import getData as getZTFData	
	from .Miscellaneous.ProperMotionCorrection import PMCorrection as CorrectPM

	if source!=None and pos!=None:
		raise Exception('simulatenous source and pos input detected')
	
	if source!=None:
		gaia_data=gaiaquery(source=source)
		if isinstance(gaia_data,pd.DataFrame):
			ra,dec,pmra,pmdec=gaia_data['ra'].values[0],gaia_data['dec'].values[0],gaia_data['pmra'].values[0],gaia_data['pmdec'].values[0]
		else:
			return None
		
		pos_corrected=CorrectPM([2016,0],[2019,0],ra,dec,pmra,pmdec)
		ra,dec=pos_corrected[0],pos_corrected[1]
	elif pos!=None:
		ra,dec=pos[0],pos[1]
	else:
		raise Exception('either source or pos input required')
	
	data=getZTFData(ra,dec,radius)

	if save_data==True:
		savefile(data=data,identifier='ZTF-Data',extension='csv',pos=pos,source=source)	

	return data

# Timeseries Plotting ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def getztflc(source=None,pos=None,radius=3,return_raw=False,save_data=False):
	from .Surveys.ZTF import getLightCurve as getZTFLightCurve
	from .Miscellaneous.ProperMotionCorrection import PMCorrection as CorrectPM
	from .Surveys.ZTF import getData

	if source!=None and pos!=None:
		raise Exception('simulatenous source and pos input detected')
	
	if source!=None:
		gaia_data=gaiaquery(source=source)
		if isinstance(gaia_data,pd.DataFrame):
			ra,dec,pmra,pmdec=gaia_data['ra'].values[0],gaia_data['dec'].values[0],gaia_data['pmra'].values[0],gaia_data['pmdec'].values[0]
			pos_corrected=CorrectPM([2016,0],[2019,0],ra,dec,pmra,pmdec)
			ra,dec=pos_corrected[0],pos_corrected[1]
		else:
			return None

	elif pos!=None:
		ra,dec=pos[0],pos[1]
	else:
		raise Exception('either source or pos input required')
		return None
		
	plot=getZTFLightCurve(ra,dec,radius,return_raw)
	
	if source!=None:
		output_file(f'{source}_lightcurve.html')
	
	elif pos!=None:
		if pos[1]>=0:
			output_file(f"{pos[0]}+{pos[1]}_lightcurve.html")	
		else:
			output_file(f"{pos[0]}{pos[1]}_lightcurve.html")

	if save_data==True:
		data=getData(ra,dec,radius)
		savefile(data=data,identifier='ZTF-Data',extension='csv',pos=pos,source=source)	

	return plot

# SED Plotting -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def getsed(source=None,pos=None,radius=3,save_data=False):
	from .Figures.SED import get_plot
	
	if source!=None and pos!=None:
		raise Exception('simulatenous source and pos input detected')

	if source!=None:
		if save_data==False:
			plot=get_plot(source=source,radius=radius)
		else:
			plot,data=get_plot(source=source,radius=radius,save_data=True)
	elif pos!=None:
		if save_data==False:
			plot=get_plot(pos=pos,radius=radius)
		else:
			plot,data=get_plot(pos=pos,radius=radius,save_data=True)
	else:
		raise Exception('either source or pos input required')

	if plot!=None:
		plot.legend.click_policy="hide"	
		
		# Double click to hide legend
		toggle_legend_js = CustomJS(args=dict(leg=plot.legend[0]), code='''
			 if (leg.visible) {
				 leg.visible = false
				 }
			 else {
				 leg.visible = true
			 }
		''')
	
		plot.js_on_event(events.DoubleTap, toggle_legend_js)  
	else:
		return None

	if source!=None:
		output_file(f'{source}_sed.html')

	elif pos!=None:
		if pos[1]>=0:
			output_file(f"{pos[0]}+{pos[1]}_sed.html")	
		else:
			output_file(f"{pos[0]}{pos[1]}_sed.html")
	
	if save_data==True:
		savefile(data=data,identifier='SED-Data',extension='csv',pos=pos,source=source)

	return plot

# Spectra Queries --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def getsdssspectrum(source=None,pos=None,radius=3,save_data=False):
	from .Miscellaneous.ProperMotionCorrection import PMCorrection as CorrectPM
	from .Surveys.SDSS import get_plot

	if source!=None and pos!=None:
		raise Exception('simulatenous source and pos input detected')
	
	if source!=None:
		gaia_data=gaiaquery(source=source)
		if isinstance(gaia_data,pd.DataFrame):
			ra,dec,pmra,pmdec=gaia_data['ra'].values[0],gaia_data['dec'].values[0],gaia_data['pmra'].values[0],gaia_data['pmdec'].values[0]
		else:
			return None
		
		pos_corrected=CorrectPM([2016,0],[2017,0],ra,dec,pmra,pmdec)
		ra,dec=pos_corrected[0],pos_corrected[1]
	elif pos!=None:
		ra,dec=pos[0],pos[1]
	else:
		raise Exception('either source or pos input required')
	
	if save_data==False:
		plot=get_plot(ra=ra,dec=dec,radius=radius)
	else:
		plot,data=get_plot(ra=ra,dec=dec,radius=radius,save_data=True)

	if source!=None:
		output_file(f'{source}_spectrum.html')

	elif pos!=None:
		if pos[1]>=0:
			output_file(f"{pos[0]}+{pos[1]}_spectrum.html")	
		else:
			output_file(f"{pos[0]}{pos[1]}_spectrum.html")
	
	if save_data==True:
		savefile(data=data,identifier='SDSS-Data',extension='csv',pos=pos,source=source)

	return plot

# HR diagram --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def gethrd(source=None,sources=None):
	from .Figures.HRD import get_plot
	if source==None and sources==None:
		raise Exception('source/sources input required')
		return None
	
	if source!=None:
		plot=get_plot(source=source)
	elif sources!=None:
		plot=get_plot(sources=sources)
	else:
		raise Exception('source/sources input required.')
	
	if plot!=None:
		# Double click to hide legend
		toggle_legend_js = CustomJS(args=dict(leg=plot.legend[0]), code='''
			 if (leg.visible) {
				 leg.visible = false
				 }
			 else {
				 leg.visible = true
			 }
		''')
	
		plot.js_on_event(events.DoubleTap, toggle_legend_js) 

	if source!=None:
		output_file(f'{source}_hrd.html')
	elif sources==None:
		sources_str=''
		for i in range(0,len(sources)-1):
			sources_str.append(str(sources[i]))+','
		sources_str.append(source[len(source)-1])
		output_file(f'{sources}_hrd.html')

	return plot

# Timeseries analysis -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def getztfanalysis(source=None,pos=None):
	from .Timeseries.ztfanalysis import getanalysis
	
	if pos!=None:
		data=ztfquery(pos=pos)
	elif source!=None:
		data=ztfquery(source=source)
	else:
		raise Exception('either source or pos input required')

	empty_count=0
	for item in data:
		if not isinstance(item,pd.DataFrame):
			empty_count+=1
			
	if empty_count!=3:
		data=pd.concat(data)
	else:
		print('no ZTF data available for given fields')
		return None

	getanalysis(data)

def getps(source=None,pos=None,save_data=False):
	from .Timeseries.ztfanalysis import getpowerspectrum
	
	if pos!=None:
		data=ztfquery(pos=pos)
	elif source!=None:
		data=ztfquery(source=source)
	else:
		raise Exception('either source or pos input required')

	empty_count=0
	for item in data:
		if not isinstance(item,pd.DataFrame):
			empty_count+=1
	
	if empty_count!=3:
		data=pd.concat(data)
	else:
		print('no ZTF data available for given fields')
		return None	

	if save_data==True:
		plot,ps_data=getpowerspectrum(data,save_data=True)
	else:
		plot=getpowerspectrum(data)

	if source!=None:
		output_file(f'{source}_powspec.html')

	elif pos!=None:
		if pos[1]>=0:
			output_file(f"{pos[0]}+{pos[1]}_powspec.html")	
		else:
			output_file(f"{pos[0]}{pos[1]}_powspec.html")

	if save_data==True:
		savefile(data=ps_data,identifier='PS-Data',extension='csv',pos=pos,source=source)

	return plot

# Miscellaneous Tools -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def correctPM(input_time,target_time,ra,dec,pmra,pmdec,radius=None):
	from .Miscellaneous.ProperMotionCorrection import PMCorrection as CorrectPM

	data=CorrectPM(input_time,target_time,ra,dec,pmra,pmdec,radius)
	return data

def getgaiacoords(source):
	from .Surveys.Gaia import GaiaGetCoords
	
	data=GaiaGetCoords(source)
	return data

def getgaiasource(pos,radius=3):
	from .Surveys.Gaia import GaiaGetSource
	
	ra,dec=pos[0],pos[1]
	data=GaiaGetSource(ra,dec,radius)
	return data

def getsources(file_name):
	from .Miscellaneous.ReadFits import get_source_list
	
	sources=get_source_list(file_name)
	return sources

def getpositions(file_name):
	from .Miscellaneous.ReadFits import get_pos_list
	pos_list=get_pos_list(file_name)
	return pos_list

def getsd(file_name):
	from .Figures.SD import get_plot
	plot=get_plot(file_name)
	
	if plot!=None:
		# Double click to hide legend
		toggle_legend_js = CustomJS(args=dict(leg=plot.legend[0]), code='''
			 if (leg.visible) {
				 leg.visible = false
				 }
			 else {
				 leg.visible = true
			 }
		''')
	
		plot.js_on_event(events.DoubleTap, toggle_legend_js) 

	return plot

def getinfobuttons(grid_size,source=None,pos=None,simbad_radius=3,vizier_radius=3):
	button_width=round(grid_size/2)
	button_height=round(button_width/3)

	# SIMBAD button
	simbad_button = Button(label="SIMBAD",button_type='primary',height=button_height,width=button_width)	

	if pos!=None:
		ra,dec=pos[0],pos[1]
	elif source!=None:
		gaia_data=gaiaquery(source=source)
		ra,dec,pmra,pmdec=gaia_data['ra'].values[0],gaia_data['dec'].values[0],gaia_data['pmra'].values[0],gaia_data['pmdec'].values[0]
		
		# Scale search radius to include ~26 years of potential proper motion (don't actually correct coordinates, just give a buffer)
		_,_,simbad_radius=correctPM([2016,0],[1990,0],ra,dec,pmra,pmdec,simbad_radius)
		_,_,vizier_radius=correctPM([2016,0],[1990,0],ra,dec,pmra,pmdec,vizier_radius)

	if pos!=None:
		simbad_url=f'https://simbad.cds.unistra.fr/simbad/sim-coo?Coord={ra}+{dec}&CooFrame=FK5&CooEpoch=2000&CooEqui=2000&CooDefinedFrames=none&Radius={simbad_radius}&Radius.unit=arcsec&submit=submit+query&CoordList='
	elif source!=None:
		simbad_url=f'https://simbad.cds.unistra.fr/simbad/sim-coo?Coord={ra}+{dec}&CooFrame=FK5&CooEpoch=2000&CooEqui=2000&CooDefinedFrames=none&Radius={simbad_radius}&Radius.unit=arcsec&submit=submit+query&CoordList='
	
	simbad_button_js = CustomJS(args=dict(url=simbad_url),code='''
		window.open(url)
	''')
	simbad_button.js_on_event('button_click',simbad_button_js)

	vizier_button = Button(label="Vizier",button_type='primary',height=button_height,width=button_width)	
	
	if dec>=0:
		vizier_url=f'https://vizier.cds.unistra.fr/viz-bin/VizieR-4?-c={ra}+{dec}&-c.rs={vizier_radius}&-out.add=_r&-sort=_r&-out.max=$4'
	else:
		vizier_url=f'https://vizier.cds.unistra.fr/viz-bin/VizieR-4?-c={ra}{dec}&-c.rs={vizier_radius}&-out.add=_r&-sort=_r&-out.max=$4'
	
	vizier_button_js = CustomJS(args=dict(url=vizier_url),code='''
		window.open(url)
	''')
	vizier_button.js_on_event('button_click',vizier_button_js)
	
	# Margin = [Top,Right,Bottom,Left]
	simbad_button.margin=[round(0.1*(grid_size-button_height)),round(1/4*grid_size),0,round(1/4*grid_size)]
	vizier_button.margin=[round(0.05*(grid_size-button_height)),round(1/4*grid_size),0,round(1/4*grid_size)]
	
	buttons=column(simbad_button,vizier_button,align='center')
	
	return buttons

# Grid setup for datapage creation ---------------------------------------------------------------------------------------------------------------------------------------------------------------------

def getgrid(dimensions,plots,grid_size=250):	
	for i in range(0,len(plots)):
		if plots[i][0]==None:
			plots[i][0]=figure(width=plots[i][1]*grid_size,height=plots[i][2]*grid_size)
		else:
			plots[i][0].width,plots[i][0].height=plots[i][1]*grid_size,plots[i][2]*grid_size
	
	unit_area=0
	for i in range(0,len(plots)):
		unit_area+=(plots[i][1]*plots[i][2])

	if unit_area!=dimensions[0]*dimensions[1]:
		raise Exception('Entire dimensions must be filled with figures. Pass None to fill empty space.')

	output_file('datapage.html')

	for i in range(0,len(plots)):
		plots[i]=plots[i][0]

	return plots