def read_alice():
    from urllib.request import urlopen
    response = urlopen('http://gaia.cs.umass.edu/wiresharklabs/alice.txt')
    html = response.read()
    return html.decode("utf-8")