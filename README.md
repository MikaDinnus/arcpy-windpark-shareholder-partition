# Windpark Partition Tool BürgEnG
This tool will divide the area covered by the wind farm among the municipalities to be involved, following the BürgEnG in NRW. Only for code users. Usage as static ArcGIS Pro Tool needs parameter table as follows:

| Label           | Name            | Data Type     | Type     | Direction |
|-----------------|-----------------|---------------|----------|-----------|
| Windturbines    | input_points    | Feature-Layer | Required | Input     |
| Buffer distance | buffer_distance | Double        | Required | Input     |
| Output          | output_file     | Feature-Class | Required | Output    |

Then use the following arcpy-Functions to retrieve the data from the input window.

input_points = arcpy.GetParameterAsText(0)
buffer_distance = float(arcpy.GetParameterAsText(1))
output_file = arcpy.GetParameterAsText(2)