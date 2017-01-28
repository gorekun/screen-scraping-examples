#!/usr/bin/env python3

import io
import itertools as it
import urllib.request
import xml.etree.ElementTree as et


def extract(url):
    # create a HTTP request, mimicing the act of Mac Safari browser.
    req = urllib.request.Request(
        url,
        data=None,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
    )
    # read the HTML file content located at the given url by sending the request
    u = urllib.request.urlopen(req)
    # convert the read HTML file content into UTF-8 encoding
    f = io.TextIOWrapper(u, encoding='utf-8')
    # read the converted HTML file content
    text = f.read()
    # build HTML tree data structure from the read
    tree = et.fromstring(text)
    # search HTML tree, using XPath functionality!
    # title: stored in the first h1 tag of the body tag.
    title = tree.findtext('./body/h1[1]')
    # table: stored in the first table tag of the body tag.
    table = tree.find('./body/table[1]')
    # subtheme: second p tag, the only td tag, the third tr tag. (stripped meaningless characters)
    subtheme = table.findtext('./tr[3]/td/p[2]').strip()
    # description: second p tag, the only td tag, the fourth tr tag.
    description = table.findtext('./tr[4]/td/p[2]')
    # panels: second p tag, the only td tag, the fifth tr tag but separated with br tag.
    panel_lines = list(table.find('./tr[5]/td/p[2]').itertext())
    # group by empty line
    panel_line_groups = [list(v) for k, v in it.groupby(panel_lines, lambda x: not x.strip()) if not k]
    panels = []
    # parse name, department and descriptions
    for panel_line_group in panel_line_groups:
        name = panel_line_group[0].strip()
        department = panel_line_group[1].strip()
        descriptions = [l.strip() for l in panel_line_group[2:]]
        panels.append({
            'name': name,
            'department': department,
            'descriptions': descriptions
        })

    # return the result!
    return {
        'title': title,
        'subtheme': subtheme,
        'description': description,
        'panels': panels,
    }


print(extract('https://www.intgovforum.org/cms/wks2015/index.php/proposal/view_public/112'))
