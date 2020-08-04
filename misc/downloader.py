import os.path
import urllib.request
import urllib.error

try:
    width = int(input("image width: "))
    height = int(input("image height: "))

    url = "http://placekitten.com/{0}/{1}".format(width, height)
    with urllib.request.urlopen(url) as infile:
        with open(os.path.expanduser("~/Downloads/kitten.jpg"), "wb") as outfile:
            outfile.write(infile.read())
except (ValueError, urllib.error.URLError, urllib.error.HTTPError, OSError) as err:
    print(err)
