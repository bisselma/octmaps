# octmaps
Python package for generating 2D thickness and intensity maps of retinal layers based on oct imaging for ophthalmology


# Environment
First of all it is recommended to work with anaconda and on an additional environment https://docs.anaconda.com/navigator/tutorials/manage-environments/   

In your new environment install the octmap-repository by the following command

```
pip install git+https://github.com/bisselma/octmaps.git
```
# Creating the maps
The module offers two ways for creating the maps

XML-Based
```
OctMaps.write_maps_from_heyex_xml(source_path, target_path, "filename") # In this case the folder in which the maps are stored are named by the "filename"

OctMaps.write_maps_from_heyex_xml(source_path, target_path, "id") # In this case the folder in which the maps are stored are named by the id 
```

vol-Based
```
OctMaps.write_maps_from_heyex_vol(source_path, target_path, "filename") # In this case the folder in which the maps are stored are named by the "filename"

OctMaps.write_maps_from_heyex_vol(source_path, target_path, "id") # In this case the folder in which the maps are stored are named by the id 
```

The data must be stored in the same folder (source_path) and the results are stored in a predefined traget folder (target_path)

# Example
For further informations use the jupyter-notbook 
```
octmaps/example_create_maps.ipynb
```
