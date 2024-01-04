import os
import ex_cd.gallery_dl_exec as gallery_dl
from .common import META_FOLDER, metadata_args, _get_gallery_metadata_filenames, get_gallery_one_metadata


def _download_gallery_meta(url, gallery_dir, config, logger):
    """download gallery metadata by gallery_dl"""
    if _valid_gallery_meta(url, gallery_dir, config, logger):  # validate the gallery
        return  # exit
    gallery_dl_exec = config["gallery-dl-exec"]
    gallery_dl_meta_args = config["gallery-dl-meta-args"]
    args = [*gallery_dl_exec, "--no-download", *metadata_args, *gallery_dl_meta_args, url]
    logger.debug(f"Exec: {args}")
    returncode = gallery_dl.main(*args)
    if _valid_gallery_meta(url, gallery_dir, config, logger):  # validate the gallery
        return  # record that this gallery has been downloaded
    elif returncode != 0:
        raise RuntimeError(f"Download gallery meta failed: {url} -> {gallery_dir}")
    else:
        raise RuntimeError(f"Download gallery meta invalid: {url} -> {gallery_dir}")


META_VALIDATE_COMPLETED_FILE = 'MetaValidateCompleted'


def _valid_gallery_meta(url, gallery_dir, config, logger):
    """validate the gallery metadata"""
    ok_file = os.path.join(gallery_dir, META_FOLDER, META_VALIDATE_COMPLETED_FILE)
    if os.path.isfile(ok_file):  # if valid
        return True  # exit
    # check if has enough metadata json files
    meta = get_gallery_one_metadata(url, gallery_dir, config, logger)
    if 'filecount' not in meta:
        logger.error(f"Invalid {gallery_dir}: 'filecount' not in metadata")
        return False
    metafiles = _get_gallery_metadata_filenames(gallery_dir)
    if int(meta['filecount']) > len(metafiles):
        logger.error(f"Invalid {gallery_dir}: no enough metadata files")
        return False
    with open(ok_file, "w", encoding='utf8'):
        return True  # record that this gallery has been validated
