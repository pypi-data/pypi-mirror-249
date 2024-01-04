from .history import _get_gallery_parent_url, _get_gallery_dir
from .deprecate import _deprecate_gallery_history
from .collect_history import _collect_gallery_history
from .download_image import _download_gallery


def download_gallery_history(url, gallery_dir, config, logger, history={}):
    """Download all the history of the gallery"""
    parent_url = _get_gallery_parent_url(url, gallery_dir, config, logger)
    if parent_url == '':  # if no parent
        return _download_gallery(url, gallery_dir, config, logger, history)  # just download it
    # if has parent
    parent_gallery_dir = _get_gallery_dir(parent_url, config, logger)
    history = {**history, **_collect_gallery_history(gallery_dir, config, logger)}  # collect existing history
    download_gallery_history(parent_url, parent_gallery_dir, config, logger, history)  # download parent
    _deprecate_gallery_history(parent_url, parent_gallery_dir, url, gallery_dir, config, logger)  # deprecate from parent
    return _download_gallery(url, gallery_dir, config, logger, history)  # download the rest
