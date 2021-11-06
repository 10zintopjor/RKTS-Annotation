from bs4 import BeautifulSoup
from pathlib import Path
import re


def parse_xml(content):
    soup = BeautifulSoup(content, 'lxml')
    items = soup.find_all("item")
    for item in items:
        parse_item(item)


def parse_item(item):
    if item.find("ref"):
        ref = item.find("ref").text
    else:
        return

    locs = item.find_all("loc")

    for loc in locs:
        if loc.parent.name != "item":
            continue
        if hasattr(loc.find("voln"), 'text'):
            vol = loc.find("voln").text
        else:
            continue
        page = loc.find("p").text
        vol_text = loc.find("vol").text
        pages = extract_pages(page)
        write_annotation(ref, vol, pages, vol_text)


def convert_vol(vol):
    count = 0
    num = int(vol)
    while num != 0:
        num //= 10
        count += 1
    if count == 1:
        vol = "v00"+vol
    elif count == 2:
        vol = "v0"+vol
    elif count == 3:
        vol = "v"+vol
    return vol


def write_annotation(ref, vol, pages, vol_text):
    pecha_id = "P000542"
    vol = convert_vol(vol)
    start = pages["start"]
    if pages["end"] == None:
        return
    end = pages["end"]
    start_count = 0
    end_count = 0

    hfml_path = f"./hfml/{pecha_id}/{vol}.txt"
    start_pattern = f"〔\d+〕\s.+\.jpg\s{start}"
    end_pattern = f"〔\d+〕\s.+\.jpg\s{end}"

    with open(hfml_path, "r") as f:
        lines = f.readlines()

    with open(hfml_path, "w") as f:
        for line in lines:
            if re.match(start_pattern, line):
                start_count += 1
            if start_count > 0:
                if start_count-1 == pages["start_line"]:
                    line = f"\u007b{ref} vol:{vol_text}\u007d"+line
                start_count += 1

            if re.match(end_pattern, line):
                end_count += 1
            if end_count > 0:
                if end_count-1 == pages["end_line"]:
                    line = line.strip(
                        '\n')+f"\u007b/{ref} vol:{vol_text}\u007d\n"
                end_count += 1

            f.write(line)


def extract_pages(page):
    page_spans = {}
    page_span = page.split("-")
    start = page_span[0]
    print(start)

    start_page_index = re.findall("\D", start)
    start_page, start_line = re.split("\D", start)
    start_page = start_page+start_page_index[0]

    if len(page_span) < 2:
        page_spans["start"] = start_page
        page_spans["start_line"] = int(start_line)
        page_spans["end"] = None
        page_spans["end_line"] = None

        return page_spans

    end = page_span[1]
    print(f"-{end}")

    end_page_index = re.findall("\D", end)
    end_page, end_line = re.split("\D", end)
    end_page = end_page+end_page_index[0]

    page_spans["start"] = start_page
    page_spans["start_line"] = int(start_line)
    page_spans["end"] = end_page
    page_spans["end_line"] = int(end_line)

    return page_spans


if __name__ == "__main__":
    xml_path = "./rkts_xml/J.xml"
    content = Path(xml_path).read_text(encoding="utf-8")
    parse_xml(content)
