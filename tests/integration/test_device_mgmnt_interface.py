"""Wakaama integration tests (pytest)"""
import re
import json
import pytest

# lwmclient appears to be unused
# pylint: disable=unused-argument

def get_senml_json_record(parsed, urn, label):
    """helper function returning value of associated label

    example SenML input:

        [{'bn': '/1/', 'n': '0/0', 'v': 123}, {'n': '0/1', 'v': 300},
        {'n': '0/2', 'v': 0}, {'n': '0/3', 'v': 0}, {'n': '0/5', 'v': 0},
        {'n': '0/6', 'vb': False}, {'n': '0/7', 'vs': 'U'}]"""

    return next(item for item in parsed if item["n"] == urn)[label]


def parse_tlv(text, id):
    #print("")
    c = 0
    depth=0
    l=text.split("\n")
    while l[c].find("bytes received of type application/vnd.oma.lwm2m+tlv") < 0:
        c+=1
    while c < len(l):
        if not re.search(r"\w",l[c]) and re.search(r"[{}]",l[c]):
            if l[c].find("{") > 0:
                depth+=1
            else:
                depth-=1
        res = re.findall(r"ID: ([0-9]+) type: Resource Value", l[c])
        if depth == 1 and res and res[0] == str(id):
            #print(depth, res, l[c])
            # found the id, parse and return data
            res = re.findall(r"data \(([0-9]+) bytes\):", l[c+2])
            #print("num bytes = ", res[0])
            #print(int(res[0])//16)
            output = ""
            for i in range (0, int(res[0])//16+1):
                #print(l[c+3+i])
                chars = int(res[0])-i*16
                if chars > 16:
                    chars = 16
                output += l[c+3+i].rstrip("\r")[-1*chars:]
                #print(output)
            return output
        else:
            pass
            #print(depth, l[c])
        c+=1

@pytest.mark.client_args("-f 0")
def test_querying_basic_information_in_plain_text_format(lwm2mserver, lwm2mclient):
    """LightweightM2M-1.1-int-201
    Querying the following data on the client (Device Object: ID 3) using Plain
    Text data format
    """

    # Test Procedure 1
    assert lwm2mserver.commandresponse("read 0 /3/0/0", "OK")
    text = lwm2mserver.waitforpacket()
    # Pass-Criteria A
    assert text.find("COAP_205_CONTENT") > 0
    assert text.find("text/plain") > 0
    assert text.find("Open Mobile Alli") > 0
    assert text.find("ance") > 0


def test_querying_basic_information_in_tlv_format(lwm2mserver, lwm2mclient):
    """LightweightM2M-1.1-int-203
    Querying the Resources Values of Device Object ID:3 on the Client
    Resources Values of Device Object ID:3"""

    # Test Procedure 1
    assert lwm2mserver.commandresponse("read 0 /3/0", "OK")
    text = lwm2mserver.waitforpacket()
    # Pass-Criteria A
    assert text.find("COAP_205_CONTENT") > 0
    assert text.find("lwm2m+tlv") > 0
    #print(text)
    print("")
    assert parse_tlv(text, 0) == "Open Mobile Alliance"
    assert parse_tlv(text, 1) == "Lightweight M2M Client"
    assert parse_tlv(text, 2) == "345000123"
    assert parse_tlv(text, 3) == "1.0"
    #assert parse_tlv(text, 11) == "???" --- Error code...
    assert parse_tlv(text, 16) == "U"


def test_querying_basic_information_in_json_format(lwm2mserver, lwm2mclient):
    """LightweightM2M-1.1-int-204
    Querying the Resources Values of Device Object ID:3 on the Client using
    JSON data format"""

    # Test Procedure 1
    assert lwm2mserver.commandresponse("read 0 /3/0", "OK")
    text = lwm2mserver.waitforpacket()
    # Pass-Criteria A
    assert text.find("COAP_205_CONTENT") > 0
    assert text.find("lwm2m+json") > 0
    packet = re.findall(r"({.*})", text)
    parsed = json.loads("["+packet[0]+"]")[0]
    assert parsed['bn'] == "/3/0/"
    parsed = parsed['e']
    assert next(item for item in parsed if item["n"] == "0")["sv"] == "Open Mobile Alliance"
    assert next(item for item in parsed if item["n"] == "1")["sv"] == "Lightweight M2M Client"
    assert next(item for item in parsed if item["n"] == "2")["sv"] == "345000123"
    assert next(item for item in parsed if item["n"] == "3")["sv"] == "1.0"
    assert next(item for item in parsed if item["n"] == "11/0")["v"] == 0
    assert next(item for item in parsed if item["n"] == "16")["sv"] == "U"


def test_read_on_object(lwm2mserver, lwm2mclient):
    """LightweightM2M-1.1-int-222
    Purpose of this test is to show conformance with the LwM2M Read
    operation on whole Object"""

    lwm2mclient.waitfortext("STATE_READY")
    # Test Procedure 1
    assert lwm2mserver.commandresponse("read 0 /1", "OK")
    text = lwm2mserver.waitforpacket()
    # Pass-Criteria A
    assert text.find("COAP_205_CONTENT") > 0
    packet = re.findall(r"(\[.*\])", text)
    parsed = json.loads(packet[1])
    assert get_senml_json_record(parsed, "0/0", "v") == 123
    assert get_senml_json_record(parsed, "0/0", "bn") == "/1/"
    assert get_senml_json_record(parsed, "0/1", "v") == 300
    assert get_senml_json_record(parsed, "0/2", "v") == 0
    assert get_senml_json_record(parsed, "0/3", "v") == 0
    assert get_senml_json_record(parsed, "0/5", "v") == 86400
    assert get_senml_json_record(parsed, "0/6", "vb") is False
    assert get_senml_json_record(parsed, "0/7", "vs") == 'U'
    # Test Procedure 2
    assert lwm2mserver.commandresponse("read 0 /3", "OK")
    text = lwm2mserver.waitforpacket()
    # Pass-Criteria B
    assert text.find("COAP_205_CONTENT") > 0
    packet = re.findall(r"(\[.*\])", text)
    parsed = json.loads(packet[1])
    # assert that only instance 0 is of object 3 is populated
    for item in parsed:
        assert item["n"].startswith("0/")
    assert get_senml_json_record(parsed, "0/0", "vs") == "Open Mobile Alliance"
    assert get_senml_json_record(parsed, "0/0", "bn") == "/3/"
    assert get_senml_json_record(parsed, "0/2", "vs") == "345000123"
    assert get_senml_json_record(parsed, "0/3", "vs") == "1.0"
    assert get_senml_json_record(parsed, "0/6/0", "v") == 1
    assert get_senml_json_record(parsed, "0/6/1", "v") == 5
    assert get_senml_json_record(parsed, "0/7/0", "v") == 3800
    assert get_senml_json_record(parsed, "0/7/1", "v") == 5000
    assert get_senml_json_record(parsed, "0/8/0", "v") == 125
    assert get_senml_json_record(parsed, "0/8/1", "v") == 900
    assert get_senml_json_record(parsed, "0/9", "v") == 100
    assert get_senml_json_record(parsed, "0/10", "v") == 15
    assert get_senml_json_record(parsed, "0/11/0", "v") == 0
    assert get_senml_json_record(parsed, "0/13", "v") > 0    # current time
    assert get_senml_json_record(parsed, "0/14", "vs") == "+01:00"
    assert get_senml_json_record(parsed, "0/15", "vs") == "Europe/Berlin"
    assert get_senml_json_record(parsed, "0/16", "vs") == "U"
