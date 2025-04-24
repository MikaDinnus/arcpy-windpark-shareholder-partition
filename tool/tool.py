import arcpy
import arcpy.analysis

input_points = r"data/windturbines/windturbines.shp"
buffer_distance = 2500
output_file = r"data/output/output_file.shp"

def create_clipped_regions(input_points, buffer_distance, output_file):
    region_layer = r"data/gem_shape/dvg1gem_nw.shp"
    arcpy.env.overwriteOutput = True

    # Buffer for windturbines to determine the area of influence
    buffered_points = r"data/output/buffered_points.shp"
    arcpy.analysis.Buffer(input_points, buffered_points, buffer_distance)

    # Union and dissolve to calculate the total area of the windpark
    union_output = r"data/output/windpark_union.shp"
    arcpy.analysis.Union([buffered_points], union_output)
    
    dissolved_windpark = r"data/output/windpark_dissolved.shp"
    arcpy.management.Dissolve(union_output, dissolved_windpark, multi_part="SINGLE_PART")
    
    with arcpy.da.SearchCursor(dissolved_windpark, ["SHAPE@"]) as cursor:
        total_windpark_area = sum(row[0].area for row in cursor)
    
    arcpy.AddMessage(f"Size of the windpark: {total_windpark_area:.2f} m²")

    # Clip the municipalities with the windpark area
    clipped_regions = r"data/output/clipped_regions.shp"
    arcpy.analysis.Clip(region_layer, dissolved_windpark, clipped_regions)

    arcpy.management.AddField(clipped_regions, "OArea_m2", "DOUBLE")
    arcpy.management.AddField(clipped_regions, "OPercent", "DOUBLE")

    with arcpy.da.UpdateCursor(clipped_regions, ["gn", "SHAPE@", "OArea_m2", "OPercent"]) as cursor:
        for row in cursor:
            gn = row[0]
            geometry = row[1]
            overlap_area = geometry.area
            row[2] = overlap_area
            row[3] = (overlap_area / total_windpark_area * 100) if total_windpark_area > 0 else 0
            cursor.updateRow(row)
            
            arcpy.AddMessage(f"Municipality '{gn}': {overlap_area:.2f} m² = {row[3]:.2f}%")

    # Save output
    arcpy.management.CopyFeatures(clipped_regions, output_file)

create_clipped_regions(input_points, buffer_distance, output_file)
