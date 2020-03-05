import glob
import os

import numpy as np
from skimage import io, transform  # conda install -c conda-forge scikit-image
from tqdm import tqdm

max_wh = 2000  # max image size
files = list(glob.iglob('images/**/*.*', recursive=True))
for f in tqdm(files, desc='Scanning images', total=len(files)):

    # Remove bad suffixes
    suffix = f.split('.')[-1]
    if suffix in ['gif', 'svg']:
        print('Removing %s' % f)
        os.remove(f)
        continue

    # Read Image
    try:
        img = io.imread(f)

        # Downsize to max_wh if necessary
        r = max_wh / max(img.shape)  # ratio
        if r < 1:  # resize
            print('Resizing %s' % f)
            img = transform.resize(img, (round(img.shape[0] * r), round(img.shape[1] * r)))
            io.imsave(f, img.astype(np.uint8))

    # Remove corrupted
    except:
        print('Removing corrupted %s' % f)
        os.remove(f)
