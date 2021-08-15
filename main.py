import gspread
import os


def init_sheet(config_location, sheet_id):
    gc = gspread.service_account(config_location)
    sheet = gc.open_by_key(sheet_id)
    pages = {}
    page_list = sheet.worksheets()
    for page in page_list:
        pages[page.title] = page
    return page_list


def read_template_file(title):
    template_file = []
    with open("Templates/{}.md".format(title), "r") as f:
        lines = f.readlines()
        for line in lines:
            template_file.append(line)
    return template_file


def init_headers(values):
    header_dict = {}
    i = 0
    for value in values:
        header_dict[value] = i
        i = i + 1
    return header_dict


def clear_output():
    dir = 'Output'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))


def generate_page(header_dict, values, template):
    with open("Output/{}.md".format(values[header_dict['Page Name']]), "w") as f:
        for line in template:
            line = line.strip()
            if line.startswith('{') and line.endswith('}'):
                key = line[1:-1]
                f.write(values[header_dict[key]] + '\n')
            else:
                f.write(line + '\n')


def main():
    page_list = init_sheet('token.json', '1RwYma4mTMR_w3eZo4v1d9b_Elh9f26SdNaigYaSCyYQ')
    clear_output()
    for page in page_list:
        values = page.get_all_values()
        header_dict = init_headers(values[0])
        template_file = read_template_file(page.title)
        for i in range(1, len(values)):
            generate_page(header_dict, values[i], template_file)








if __name__ == '__main__':
    main()