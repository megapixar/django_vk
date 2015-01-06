import httplib
import mimetypes
import urllib2

__author__ = 'Antatoly'

def encode_multipart_data (data, files):
    boundary = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'

    def get_content_type (filename):
        return mimetypes.guess_type (filename)[0] or 'application/octet-stream'

    def encode_field (field_name):
        return ('--' + boundary,
                'Content-Disposition: form-data; name="%s"' % field_name,
                '', str (data [field_name]))

    def encode_file (field_name):
        filename = files [field_name]
        return ('--' + boundary,
                'Content-Disposition: form-data; name="%s"; filename="%s"' % (field_name, filename),
                'Content-Type: %s' % get_content_type(filename),
                '', open (filename, 'rb').read ())

    lines = []
    # for name in data:
    #     lines.extend (encode_field (name))
    for name in files:
        lines.extend (encode_file (name))

    lines.extend (('--%s--' % boundary, ''))
    body = '\r\n'.join (lines)

    headers = {'content-type': 'multipart/form-data; boundary=' + boundary,
               'content-length': str (len (body))}

    return body, headers

def send_files(url, files, data = {}):
    req = urllib2.Request (url)
    connection = httplib.HTTPConnection (req.get_host())
    connection.request ('POST', req.get_selector (),
                        *encode_multipart_data (data, files))
    return connection.getresponse ()