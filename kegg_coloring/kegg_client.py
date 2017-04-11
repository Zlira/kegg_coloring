from io import BytesIO
from io import StringIO

import requests


DOWNLOAD_URL = 'http://www.kegg.jp/kegg-bin/download'


def download_kgml(pathway_id):
    """
    Given KEGG pathway id (like mu03030) download its xml
    and return its text as filelike object.
    """
    params = {
        'format': 'kgml',
        'entry': pathway_id,
    }
    resp = requests.get(DOWNLOAD_URL, params=params)
    resp.raise_for_status()
    return StringIO(resp.text)


def download_img(img_url):
    """
    Given an url of an image downlaod it and return its
    content as bytes stream.

    This function has nothing specific to KEGG actually.

    ToDo:
        Maybe it should work with pathway_id and not url?
    """
    img_resp = requests.get(img_url)
    img_resp.raise_for_status()
    return BytesIO(img_resp.content)
