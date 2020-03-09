def match_table_row_cell_value(table, cell_index, value):
    rows_cells = table_cells(table)
    for row, cells in rows_cells:
        if value in cells[cell_index].text: # allows for "buffer" data in cell
            return (row, cells)
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