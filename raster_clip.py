import os
import pandas as pd
import sys

from clipper import clip_raster, get_geometry_from_shapefile

# global constatns, change as required
OUTPUT_DIR = 'output'
OUTPUT_SUFFIX = '__clipped'
RASTER_EXTENSIONS = (
    '.bmp',
    '.tif',
    '.jpg',
    '.png',
    )


def main(dirpath, clippath, outpath=OUTPUT_DIR):
    """
    
    Parameters
    ----------
    dirpath : str
        Path to the folder where the rasters to be processed are.
    clippath : str
        Path to the vector file to be used to clip the given rasters.
    outpath : str
        Output path to save the clipped rasters and the results file.

    Returns
    -------
    None.

    """
    df = pd.DataFrame(columns=['Feature','Proportion'])
    # get clipping mask
    clip_mask = get_geometry_from_shapefile(clippath)
    # iterate over rasters, clip using mask and save output
    for file in os.listdir(dirpath):
        fpath = os.path.join(dirpath, file)
        if os.path.isfile(fpath) and fpath.lower().endswith(RASTER_EXTENSIONS):
            fname, fext = os.path.splitext(os.path.basename(fpath))
            dest = os.path.join(outpath, f"{fname}{OUTPUT_SUFFIX}{fext}")
            clipped_proportion = clip_raster(fpath, clip_mask, dest)
            print(f"Proportion of {fname} is {clipped_proportion}")
            new_row = {'Feature': fname, 'Proportion': clipped_proportion}
            df = df.append(new_row, ignore_index=True)
    df.to_csv(os.path.join(outpath, 'results.csv'))
            
if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else OUTPUT_DIR)