import os
from pathlib import Path
from horology import timed
from openpecha import serializers
from openpecha.formatters import HFMLFormatter
from openpecha.serializers import HFMLSerializer, EpubSerializer
from openpecha.core.pecha import OpenPechaFS


@timed(unit="min")
def test_serializer(opf_path, hfml_path):
    serializer = HFMLSerializer(opf_path)
    serializer.serialize(output_path=hfml_path)


if __name__ == "__main__":
    # opf_path = "./opfs/P000001/P000001.opf/"
    hfml_path = "./hfml"
    # pecha_id = "1dbba105efc046849872f08cfebfb168"
    # pecha_id = "187ed94f85154ea5b1ac374a651e1770"
    # pecha_id = "T65"
    pecha_id = "P000542"
    # opfs_path = "./tenjur"
    # hfml_text = f"./hfmls/{pecha_id}/"
    # hfml_text = './P000001'
    opf_path = f"./opfs/{pecha_id}/{pecha_id}.opf"
    hfml_text = "./hfml/P000542"
    # opf_path = f"./tests/data/proofreading/P000001_copy/{pecha_id}.opf"
    # Converts HFML to OPF
    formatter = HFMLFormatter(output_path="./completed_opf")
    formatter.create_opf(hfml_text)
    # Converts OPF to HFML
    # text_list = Path("./output/tengyur/text_list.txt").read_text()
    # texts = text_list.splitlines()
    # for text in texts:
    # serializer = HFMLSerializer(opf_path, text_id='D1119')
    # serializer.serialize(output_path=hfml_path)
    #test_serializer(opf_path, hfml_path)
    # opf_path = "./opfs/P1/P1.opf/"
    # serializer = EpubSerializer(opf_path)
    # serializer.serialize()
