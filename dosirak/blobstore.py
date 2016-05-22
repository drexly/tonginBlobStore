"""
A helper for the app engine blobstore API and Django.

Works with the appengine patch:
http://code.google.com/p/app-engine-patch/

Taken and inspired by:
http://appengine-cookbook.appspot.com/recipe/blobstore-get_uploads-helper-function-for-django-request/

Usage:

def upload_file(request):
    try:
        for upload in blogstore_helper.get_uploads(request,'file'):
            file = BlobFile(blob=upload)
            file.save()
        return HttpResponseRedirect("/redirect/to/file/viewer/")
    except:
        # throw an error
        return HttpResponseRedirect("/redirect/to/error/handler")

def serve_file(request, blob_id):
    blob_id = str(urllib.unquote(blob_id))
    blob = blobstore.BlobInfo.get(blob_id)
    return blogstore_helper.send_blob(request, blob, save_as=True)


awesome,
harper@nata2.org
"""

import cgi
from google.appengine.ext import blobstore


def get_uploads(request, field_name=None, populate_post=False):
    """Get uploads sent to this handler.

    Args:
      field_name: Only select uploads that were sent as a specific field.
      populate_post: Add the non blob fields to request.POST

    Returns:
      A list of BlobInfo records corresponding to each upload.
      Empty list if there are no blob-info records for field_name.
    """

    if hasattr(request, '__uploads') == False:
        request.META['wsgi.input'].seek(0)
        fields = cgi.FieldStorage(request.META['wsgi.input'], environ=request.META)

        request.__uploads = {}
        if populate_post:
            request.POST = {}

        for key in fields.keys():
            field = fields[key]
            if isinstance(field, cgi.FieldStorage) and 'blob-key' in field.type_options:
                request.__uploads.setdefault(key, []).append(blobstore.parse_blob_info(field))
            elif populate_post:
                request.POST[key] = field.value

    if field_name:
        try:
            return list(request.__uploads[field_name])
        except KeyError:
            return []
    else:
        results = []
        for uploads in request.__uploads.itervalues():
            results += uploads
        return results
