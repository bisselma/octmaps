# -*- coding: utf-8 -*-
from pathlib import Path
from typing import IO, Union
import os 
from eyepy.io.heyex import HeyexVolReader
import octmaps.io.config
import numpy as np
import eyepy as ep
import cv2
from pathlib import Path, PosixPath
import matplotlib.pyplot as plt



class HeyexVolMapsGenerator:
    
    """
    To be described 
    """
    
    def __init__(self, file_obj: Union[str, Path, IO], version=None):
        
        if type(file_obj) is str or type(file_obj) is PosixPath:
            try:
                self.oct = ep.Oct.from_heyex_vol(file_obj)
            except FileNotFoundError:
                print("filename: " +  file_obj + " not exist")
                
       
        
        # scanfield 
        self.oct_height = self.oct._meta["Distance"] * (self.oct._meta["NumBScans"]-1)
        self.oct_sizeX = self.oct._meta["SizeX"]
        self.oct_width = self.oct._meta["ScaleX"] * self.oct_sizeX
        self.oct_sizeY = round((self.oct_height/self.oct_width)*self.oct_sizeX)
        self.num_bscans = self.oct._meta["NumBScans"]
        
        
        self.layer_order = config.SEG_MAPPING_ORDER
        self.membran = config.MEMBRAN
        self.special_order = config.SPECIAL_ORDER
    

    def get_thickness_map(self, layer_name):
        
        
        thickness_map =  np.zeros((self.num_bscans, self.oct_sizeX), dtype=float) 
        
        if layer_name in self.membran:
            return cv2.resize(thickness_map +1, dsize=(self.oct_sizeX, self.oct_sizeY), interpolation=cv2.INTER_CUBIC) # mebran have thickness = 1
        elif layer_name in self.special_order:
            if layer_name == "ONL":
                layer_name = "ELM"
                upper_layer_name = "OPL"
            else:
                layer_name = "RPE"
                upper_layer_name = "PR2"
        else:
            upper_layer_name = self.layer_order[[x for x in range(0,len(self.layer_order)) if self.layer_order[x] == layer_name][0]-1]
        for bscan,row in zip(reversed(self.oct), thickness_map):  
            try:
                row[...] = bscan.layers[layer_name] - bscan.layers[upper_layer_name]
            except:
                continue  
        
        thickness_map = cv2.resize(thickness_map, dsize=(self.oct_sizeX, self.oct_sizeY), interpolation=cv2.INTER_CUBIC)

        
        return thickness_map


  
       
    def get_max_intensity_map(self, layer_name):
        
        def get_max_intensity(bscan, upper_layer, lower_layer):
            line = np.zeros((1, self.oct_sizeX))
            b = np.copy(bscan)
            b[b >= 3.40282e+38] = 0.
            for idx in range(0 ,self.oct_sizeX):
                if not (np.isnan(upper_layer[idx]) and np.isnan(lower_layer[idx])):
                    line[0,idx] = np.max(b[round(upper_layer[idx])-1:round(lower_layer[idx]),idx])
            return line
        
        intensity_map =  np.zeros((self.num_bscans, self.oct_sizeX), dtype=float) 
        
        if layer_name in self.membran:
            upper_layer_name = layer_name
        elif layer_name in self.special_order:
            if layer_name == "ONL":
                layer_name = "ELM"
                upper_layer_name = "OPL"
            else:
                layer_name = "RPE"
                upper_layer_name = "PR2"
        else:
            upper_layer_name = self.layer_order[[x for x in range(0,len(self.layer_order)) if self.layer_order[x] == layer_name][0]-1]
        for bscan,row in zip(reversed(self.oct), intensity_map):  
            try:
                row[...] = get_max_intensity(bscan._scan_raw, bscan.layers[upper_layer_name], bscan.layers[layer_name])
            except:
                continue  
        
        intensity_map = cv2.resize(intensity_map, dsize=(self.oct_sizeX, self.oct_sizeY), interpolation=cv2.INTER_CUBIC)
        
        return intensity_map


       
    def get_mean_intensity_map(self, layer_name):
        
        def get_mean_intensity(bscan, upper_layer, lower_layer):
            line = np.zeros((1, self.oct_sizeX))
            b = np.copy(bscan)
            b[b >= 3.40282e+38] = 0.
            for idx in range(0 ,self.oct_sizeX):
                if not (np.isnan(upper_layer[idx]) and np.isnan(lower_layer[idx])):
                    line[0,idx] = np.mean(b[round(upper_layer[idx])-1:round(lower_layer[idx]),idx])
            return line
        
        intensity_map =  np.zeros((self.num_bscans, self.oct_sizeX), dtype=float) 
        
        if layer_name in self.membran:
            upper_layer_name = layer_name
        elif layer_name in self.special_order:
            if layer_name == "ONL":
                layer_name = "ELM"
                upper_layer_name = "OPL"
            else:
                layer_name = "RPE"
                upper_layer_name = "PR2"
        else:
            upper_layer_name = self.layer_order[[x for x in range(0,len(self.layer_order)) if self.layer_order[x] == layer_name][0]-1]
        for bscan,row in zip(reversed(self.oct), intensity_map):  
            try:
                row[...] = get_mean_intensity(bscan._scan_raw, bscan.layers[upper_layer_name], bscan.layers[layer_name])
            except:
                continue  
            
        intensity_map = cv2.resize(intensity_map, dsize=(self.oct_sizeX, self.oct_sizeY), interpolation=cv2.INTER_CUBIC)
        
        return intensity_map
    
 
    def get_min_intensity_map(self, layer_name):
        
        def get_min_intensity(bscan, upper_layer, lower_layer):
            line = np.zeros((1, self.oct_sizeX))
            b = np.copy(bscan)
            b[b >= 3.40282e+38] = 0.
            for idx in range(0 ,self.oct_sizeX):
                if not (np.isnan(upper_layer[idx]) and np.isnan(lower_layer[idx])):
                    line[0,idx] = np.min(b[round(upper_layer[idx])-1:round(lower_layer[idx]),idx])
            return line
        
        intensity_map =  np.zeros((self.num_bscans, self.oct_sizeX), dtype=float) 
        
        if layer_name in self.membran:
            upper_layer_name = layer_name
        elif layer_name in self.special_order:
            if layer_name == "ONL":
                layer_name = "ELM"
                upper_layer_name = "OPL"
            else:
                layer_name = "RPE"
                upper_layer_name = "PR2"
        else:
            upper_layer_name = self.layer_order[[x for x in range(0,len(self.layer_order)) if self.layer_order[x] == layer_name][0]-1]
        for bscan,row in zip(reversed(self.oct), intensity_map):  
            try:
                row[...] = get_min_intensity(bscan._scan_raw, bscan.layers[upper_layer_name], bscan.layers[layer_name])
            except:
                continue  
        
        intensity_map = cv2.resize(intensity_map, dsize=(self.oct_sizeX, self.oct_sizeY), interpolation=cv2.INTER_CUBIC)

        
        return intensity_map
    
    