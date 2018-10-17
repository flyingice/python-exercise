import html.parser
import re
import urllib.request


def prep_query(text):
    # replace whitespaces by the separator '+'
    return '+'.join(text.split())


def translate(text, fromLang="auto", toLang="zh-CN"):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }
    url = "http://translate.google.com/m?tl={0}&sl={1}&q={2}".format(
        toLang, fromLang, prep_query(text))
    request = urllib.request.Request(url, headers=headers)
    try:
        # bytes to utf-8 encoding
        data = urllib.request.urlopen(request).read().decode("utf-8")
        regex = r'class="t0">(.*?)<'
        res = re.findall(regex, data)
    except Exception as err:
        print(err)

    return html.unescape(res[0]) if 'res' in locals() and res else ""


res = translate(input("Please enter the text to translate: \n"))
if res:
    print(res)
