import re
import urllib.request

def shorten_url(url):
    apiurl = "http://tinyurl.com/api-create.php?url="
    tinyurl = urllib.request.urlopen(apiurl + url).read()
    return tinyurl.decode("utf-8")

def remove_tags(text):
    copy = "{}".format(text)
    TAG_RE = re.compile(r'<[^>]+>')
    return TAG_RE.sub('', copy)

def strip_ws(text):
    return re.sub('\s+',' ',text)

def match_table_row_cell_value(table, cell_index, value, path=None, contains=None):
    if not path:
        path = 'td/div/*'
    if not contains:
        contains = "text()"
    try:
        row = table.find_element_by_xpath("//tr[{}[contains({}, '{}')]]".format(path, contains, value))
        cells = row.find_elements_by_css_selector("td")
        return (row, cells)
    except Exception as e:
        print(str(e))
        return (None, None)

def table_cells(table):
    cell_rows = []
    rows = table.find_elements_by_css_selector("tr")[1:] # remove table header
    for row in rows:
        cells = row.find_elements_by_css_selector("td")
        cell_rows.append((row, cells))
    return cell_rows

def extract_numbers(exp):
    return [int(s) for s in exp.split() if s.isdigit()]