#! /usr/local/bin/python3
import hashlib
import os
import urllib
import urllib.request
import shutil
from optparse import OptionParser


# http://stackoverflow.com/questions/519633/lazy-method-for-reading-big-file-in-python
def read_in_chunks(file_object, chunk_size=1024):
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data


def get_hash_values(filename):
    md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    sha256 = hashlib.sha256()

    with open(filename, 'rb') as fp:
        for chunk in read_in_chunks(fp):
            md5.update(chunk)
            sha1.update(chunk)
            sha256.update(chunk)

    return md5.hexdigest(), sha1.hexdigest(), sha256.hexdigest()


def download_file(url, filename):
    errors = []
    basename = os.path.basename(url)

    if filename == '':
        filename = basename if basename != '' else 'downloaded_file'

    output_filename = os.path.join(os.getcwd(), filename)

    try:
        with urllib.request.urlopen(url) as response, \
                open(output_filename, 'wb') as output_file:
            shutil.copyfileobj(response, output_file)
    except urllib.error.URLError:
        errors.append("Invalid URL")
    return output_filename, errors


def main():
    usage = 'usage: %prog url'
    parser = OptionParser(
        usage=usage,
        description='Download a file and calculate checksum for MD5, SHA-1 '
                    'and SHA-256'
    )
    options, args = parser.parse_args()
    if args:
        print('-> Downloading file')
        output_filename = args[1] if 1 < len(args) else ''
        filename, errors = download_file(args[0], output_filename)
        if errors:
            print('The following errors were found while downloading: ')
            for error in errors:
                print('- ' + error)

        else:
            print('File: ', filename)
            md5, sha1, sha256 = get_hash_values(filename)
            print('-> Calculating checksum values')
            print('MD5: ', md5)
            print('SHA-1: ', sha1)
            print('SHA-256: ', sha256)
    else:
        print('Please provide a url')


if __name__ == '__main__':
    main()
