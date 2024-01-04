import ex_cd.gallery_dl_exec as gallery_dl
from .validate import _validate_gallery
from .collect import _load_gallery_history
from .common import metadata_args
from .history import _get_gallery_parent_url, _get_gallery_dir
from .deprecate import _deprecate_gallery_history
from .collect import _collect_gallery_history


def download_gallery_history(url, gallery_dir, config, logger, history={}):
    """Download all the history of the gallery"""
    parent_url = _get_gallery_parent_url(url, gallery_dir, config, logger)
    if parent_url == '':  # if no parent
        return _download_gallery(url, gallery_dir, config, logger, history)  # just download it
    # if has parent
    parent_gallery_dir = _get_gallery_dir(parent_url, config, logger)
    history = {**history, **_collect_gallery_history(gallery_dir, config, logger)}  # collect existing history
    download_gallery_history(parent_url, parent_gallery_dir, config, logger, history)  # download parent
    _deprecate_gallery_history(parent_url, parent_gallery_dir, url, gallery_dir,
                               config, logger)  # deprecate from parent
    return _download_gallery(url, gallery_dir, config, logger, history)  # download the rest


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
