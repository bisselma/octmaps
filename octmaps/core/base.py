# -*- coding: utf-8 -*-
from pathlib import Path
from typing import IO, Union
import os 
import eyepy as ep
from eyepy.io.heyex import HeyexVolReader
import numpy as np

from pathlib import Path, PosixPath
import matplotlib.pyplot as plt
import sys
from octmaps.io import vol_map_generator, xml_map_generator, config

from collections.abc import MutableMapping
from pathlib import Path
from typing import Callable, Dict, List, Optional, Union
from PIL import Image


class LayerMaps:
	
	"""
	To be described 
 
	"""
	
	def __new__(
		cls,
		ids = None,
		layer_name = None,
		file_obj = None,
		version = None,
		max_intensity_map = None,
		mean_intensity_map = None,
		min_intensity_map = None,
		thickness_map = None,	            
		*args,
		**kwargs
	):
	
		return object.__new__(cls, *args, **kwargs) 
	
	
	def __init__(
		self,
		ids : Optional[List[str]] = None,
		layer_name : Optional[str] = None,
		file_obj: Union[str, Path, IO] = None,
		version = None,
		max_intensity_map: Optional[Union[np.ndarray,Callable]] = None,
		mean_intensity_map: Optional[Union[np.ndarray,Callable]] = None,
		min_intensity_map: Optional[Union[np.ndarray,Callable]] = None,
		thickness_map: Optional[Union[np.ndarray,Callable]] = None,
	):

		if type(file_obj) is str or type(file_obj) is PosixPath:
			try:
				self.file_obj = file_obj
			except FileNotFoundError:
				print("filename: " +  file_obj + " not exist")
	
		self.version = version
		self.ids = ids
		self.layer_name = layer_name
		self.max_intensity_map = max_intensity_map
		self.mean_intensity_map = mean_intensity_map
		self.min_intensity_map = min_intensity_map
		self.thickness_map = thickness_map
	
	
	@classmethod
	def from_heyex_vol(cls, layer_name, path):
	
		data = vol_map_generator.HeyexVolMapsGenerator(path, version= None)
	
		return cls(
			ids = data.ids,
			layer_name = layer_name,
			file_obj=path,
			version= None,
			max_intensity_map = data.get_max_intensity_map(layer_name),
			mean_intensity_map = data.get_mean_intensity_map(layer_name),
			min_intensity_map = data.get_min_intensity_map(layer_name),
			thickness_map = data.get_thickness_map(layer_name),
	)
	
	@classmethod
	def from_heyex_xml(cls, layer_name, path):

	
		data = xml_map_generator.HeyexXmlMapsGenerator(path, version= None)
	
		return cls(
			ids = data.ids,
			layer_name = layer_name,
			file_obj=path,
			version= None,
			max_intensity_map = data.get_max_intensity_map(layer_name),
			mean_intensity_map = data.get_mean_intensity_map(layer_name),
			min_intensity_map = data.get_min_intensity_map(layer_name),
			thickness_map = data.get_thickness_map(layer_name),
	)
	
	 

class OctMaps:
	"""
	To be described 
	"""
	def __new__(
		cls,
		layer_name_list = None,
		file_obj = None,
		version = None,
		layer_maps = None,
	):
	
		return object.__new__(cls) 


	
	def __init__(
		self,
		layer_name_list: Optional[List[str]],
		file_obj: Union[str, Path, IO] = None,
		version = None,
		layer_maps: List[Union[Callable, LayerMaps]] = None
	):
	
	
		if type(file_obj) is str or type(file_obj) is PosixPath:
			try:
				self.file_obj = file_obj
			except FileNotFoundError:
				print("filename: " +  file_obj + " not exist")
		
		
		self.layer_name_list = layer_name_list 
		self.version = version
		self.layer_maps = layer_maps 
	
	
	@classmethod
	def creat_maps_from_heyex_vol(cls, path, *args):
	
	
		if not args:
			name_list = config.SEG_MAPPING_ORDER
		else:
			name_list = args[0]
		
		layer = []
		for layer_name in name_list:
			layer.append(LayerMaps.from_heyex_vol(layer_name, path))
		
		return cls(
			layer_name_list = name_list,
			file_obj = path,
			version = None,
			layer_maps = layer
	)
	
	@classmethod
	def creat_maps_from_heyex_xml(cls, path, *args):
	
	
		if not args:
			name_list = config.SEG_MAPPING_ORDER
		else:
			name_list = args[0]
		
		layer = []
		for layer_name in name_list:
			layer.append(LayerMaps.from_heyex_xml(layer_name, path))
		
		return cls(
			layer_name_list = name_list,
			file_obj = path,
			version = None,
			layer_maps = layer
	)        

	@classmethod
	def write_maps_from_heyex_vol(cls, path, target, named_by, *args):


		# get all data in origin folder by .vol 
		if ".vol" in path:
			id_list = [path]
		else:	
			id_list = []
			dir_list = os.listdir(path)
			for dir in dir_list:
				full_path = os.path.join(path, dir)
				if os.path.isdir(full_path):
					dir_list.extend(os.path.join(dir, subfolder) for subfolder in os.listdir(full_path))
				if os.path.isfile(full_path) and full_path.endswith(".vol"):
					id_list.append(full_path)


	
		if not args:
			name_list = config.SEG_MAPPING_ORDER
		else:
			name_list = args[0]
		
		layer = []

		for ids in id_list:

			for layer_name in name_list:
				l = LayerMaps.from_heyex_vol(layer_name, ids)

				if named_by:
					if named_by == "foldername":
						folder_name = ids.split("\\")[-2]
					if named_by == "id":
						folder_name = l.ids[0]
				
				if not os.path.isdir(os.path.join(target, folder_name)):
					os.makedirs(os.path.join(target, folder_name))
				
				if layer_name in config.MEMBRAN:
					# min intensity map
					im = Image.fromarray(l.min_intensity_map)
					im.save(os.path.join(target, folder_name, l.layer_name + '_intensity_map.tif'))				
				else:
					# thickness map
					im = Image.fromarray(l.thickness_map)
					im.save(os.path.join(target, folder_name, l.layer_name + '_thickness_map.tif'))
					# max intensity map
					im = Image.fromarray(l.max_intensity_map)
					im.save(os.path.join(target, folder_name, l.layer_name + '_max_intensity_map.tif'))
					# mean intensity map
					im = Image.fromarray(l.mean_intensity_map)
					im.save(os.path.join(target, folder_name, l.layer_name + '_mean_intensity_map.tif'))
					# min intensity map
					im = Image.fromarray(l.min_intensity_map)
					im.save(os.path.join(target, folder_name, l.layer_name + '_min_intensity_map.tif'))
		
				layer.append(l)
			
			# retinal thickness
			l = LayerMaps.from_heyex_vol("FULLRET",ids)
			im = Image.fromarray(l.thickness_map)
			im.save(os.path.join(target, folder_name, l.layer_name + '_thickness_map.tif'))
			layer.append(l)
		
		return cls(
			layer_name_list = name_list,
			file_obj = path, 
			version = None,
			layer_maps = layer
	)      
	
	
	@classmethod
	def write_maps_from_heyex_xml(cls, path, target, named_by, *args):
	
		# get all data in origin folder by .xml
		if ".xml" in path:
			id_list = [path]
		else:	
			id_list = []
			dir_list = os.listdir(path)
			for dir in dir_list:
				full_path = os.path.join(path, dir)
				if os.path.isdir(full_path):
					dir_list.extend(os.path.join(dir, subfolder) for subfolder in os.listdir(full_path))
				if os.path.isfile(full_path) and full_path.endswith(".xml"):
					id_list.append(full_path)

	
		if not args:
			name_list = config.SEG_MAPPING_ORDER
		else:
			name_list = args[0]
		
		layer = []

		for ids in id_list:

			for layer_name in name_list:
				l = LayerMaps.from_heyex_xml(layer_name, ids)

				if named_by:
					if named_by == "foldername":
						folder_name = ids.split("\\")[-2]
					if named_by == "id":
						folder_name = l.ids[0]

				if not os.path.isdir(os.path.join(target, folder_name)):
					os.makedirs(os.path.join(target, folder_name))
				
				if layer_name in config.MEMBRAN:
					# min intensity map
					im = Image.fromarray(l.min_intensity_map)
					im.save(os.path.join(target, folder_name, l.layer_name + '_intensity_map.tif'))				
				else:
					# thickness map
					im = Image.fromarray(l.thickness_map)
					im.save(os.path.join(target, folder_name, l.layer_name + '_thickness_map.tif'))
					# max intensity map
					im = Image.fromarray(l.max_intensity_map)
					im.save(os.path.join(target, folder_name, l.layer_name + '_max_intensity_map.tif'))
					# mean intensity map
					im = Image.fromarray(l.mean_intensity_map)
					im.save(os.path.join(target, folder_name, l.layer_name + '_mean_intensity_map.tif'))
					# min intensity map
					im = Image.fromarray(l.min_intensity_map)
					im.save(os.path.join(target, folder_name, l.layer_name + '_min_intensity_map.tif'))
		
				layer.append(l)
		
			# retinal thickness
			l = LayerMaps.from_heyex_xml("FULLRET",ids)
			im = Image.fromarray(l.thickness_map)
			im.save(os.path.join(target, folder_name, l.layer_name + '_thickness_map.tif'))
			layer.append(l)
			

		return cls(
			layer_name_list = name_list,
			file_obj = path, 
			version = None,
			layer_maps = layer
	)     
	
if __name__ == '__main__':
	
    target = "E:\\benis\\Documents\\Arbeit\\Arbeit\\Augenklinik\\Projekt Marlene\\Micro_Retro Vortrag\\Export ad Ben\\res"

    vol_path = "E:\\benis\\Documents\\Arbeit\\Arbeit\\Augenklinik\\Projekt Marlene\\Micro_Retro Vortrag\\Export ad Ben\\ID_124\\"

    ids = "OCT_124"

    # create maps and 
    OctMaps.write_maps_from_heyex_xml(vol_path + ids, target, "foldername")












































	