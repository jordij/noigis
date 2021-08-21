import fiona
import rasterio

from rasterio.mask import mask


def get_geometry_from_shapefile(shpfilepath):
    with fiona.open(shpfilepath) as shapefile:
        shape = shapefile[0]['geometry']
    return shape

def clip_raster(rasterpath, shape_mask, outpath):
    """
    Clips given raster with provided mask. Results saved to outpath.
    Assumes single band.
    Returns proportion of band within clipped area relative to total band sum.
    """
    data = rasterio.open(rasterpath)
    df = data.read(1) # single band
    total_sum = sum(df[df>0])
    
    out_image, out_transform = mask(data, [shape_mask], crop=True, all_touched=True)
    out_meta = data.meta.copy()
    out_meta.update({
        "driver": "GTiff",
        "height": out_image.shape[1],
        "width": out_image.shape[2],
        "transform": out_transform
    })
    clipped_sum = sum(out_image[out_image > 0])    
    with rasterio.open(outpath, "w", **out_meta) as dest:
        dest.write(out_image)
    # return the proportion of the clipped raster band relative to the total 
    # of the original raster
    return (clipped_sum/total_sum * 100)
    