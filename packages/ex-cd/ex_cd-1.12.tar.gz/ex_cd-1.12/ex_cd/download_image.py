import os
import json
import ex_cd.gallery_dl_exec as gallery_dl
import hashlib
from .common import META_FOLDER, metadata_args, _get_gallery_metadata_filenames
from .download_meta import _valid_gallery_meta
from .collect_history import _load_gallery_history


def _download_gallery(url, gallery_dir, config, logger, history={}):
    """download by gallery_dl and validate"""
    if _validate_gallery(url, gallery_dir, config, logger):  # validate the gallery
        return  # exit
    _load_gallery_history(url, gallery_dir, config, logger, history)  # load existing history
    if _validate_gallery(url, gallery_dir, config, logger):  # validate the gallery
        return  # record that this gallery has been downloaded
    gallery_dl_exec = config["gallery-dl-exec"]
    gallery_dl_meta_args = config["gallery-dl-meta-args"]
    args = [*gallery_dl_exec, *metadata_args, *gallery_dl_meta_args, url]
    logger.debug(f"Exec: {args}")
    returncode = gallery_dl.main(*args)
    if _validate_gallery(url, gallery_dir, config, logger):  # validate the gallery
        return  # record that this gallery has been downloaded
    elif returncode != 0:
        raise RuntimeError(f"Download failed: {url} -> {gallery_dir}")
    else:
        raise RuntimeError(f"Download not valid: {url} -> {gallery_dir}")


VALIDATE_COMPLETED_FILE = 'ValidateCompleted'


def _validate_gallery(url, gallery_dir, config, logger):
    """validate the gallery"""
    ok_file = os.path.join(gallery_dir, META_FOLDER, VALIDATE_COMPLETED_FILE)
    if os.path.isfile(ok_file):  # if valid
        return True  # exit

    # check if has enough metadata json files
    if not _valid_gallery_meta(url, gallery_dir, config, logger):
        return False
    metafiles = _get_gallery_metadata_filenames(gallery_dir)

    # check if has enough image files
    images = []
    for img in os.listdir(gallery_dir):
        if img == META_FOLDER:
            continue
        images.append(img)
    for metafile in metafiles:
        imgfile = metafile[0:-5]
        if imgfile not in images:
            logger.error(f"Invalid {gallery_dir}: no image {imgfile} for {metafile}")
            return False

    ok = True
    # check if image content SHA1 match image_token
    for img in images:
        # read image_token
        metafile = img + '.json'
        if metafile not in metafiles:
            logger.warn(f"Strange {os.path.join(gallery_dir, img)}: it has no meta json")
            continue
        metadata = {}
        metadatapath = os.path.join(gallery_dir, META_FOLDER, metafile)
        try:
            with open(metadatapath, 'r', encoding='utf8') as fp:
                metadata = json.load(fp)
        except Exception as e:
            logger.error(f"Invalid {metafile}: cannot read json file, {e}, delete the meta")
            os.remove(metadatapath)
            ok = False
            continue
        if 'image_token' not in metadata:
            logger.error(f"Invalid {metafile}: 'image_token' not in metadata, delete the meta")
            os.remove(metadatapath)
            ok = False
            continue
        image_token = metadata['image_token']
        # compare image_token
        imgfile = os.path.join(gallery_dir, img)
        try:
            with open(imgfile, mode="rb") as fp:
                sha1 = hashlib.sha1(fp.read()).hexdigest()
            if image_token != sha1[0:10]:
                logger.error(f"Invalid {imgfile}: image token not match, {image_token} != {sha1}, delete the image")
                os.remove(imgfile)
                ok = False
                continue
        except Exception as e:
            logger.error(f"Invalid {imgfile}: cannot compare token, {e}, delete the image")
            os.remove(imgfile)
            ok = False
            continue
    if ok:
        with open(ok_file, "w", encoding='utf8'):
            return True  # record that this gallery has been validated
    else:
        return False
