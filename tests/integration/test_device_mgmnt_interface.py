import re
import json

def test_querying_basic_information_in_JSON_format(lwm2mserver, lwm2mclient):
    """LightweightM2M-1.1-int-204
    Querying the Resources Values of Device Object ID:3 on the Client using
    JSON data format"""
    lwm2mserver.expect_exact("\r\r\n>")

    lwm2mserver.sendline("read 0 /3/0")
    lwm2mserver.expect_exact("\r\r\n>")
    print(lwm2mserver.before)
    assert lwm2mserver.before.find("OK") > 0
    #lwm2mserver.expect_exact("\r\r\n>")
    #print(lwm2mserver.before)
    #assert lwm2mserver.before.find("COAP_205_CONTENT") > 0
    #assert lwm2mserver.before.find("bytes received of type application/senml+json") > 0

    lwm2mserver.expect_exact("more: 0")
    lwm2mserver.expect_exact("\r\r\n>")
    print(lwm2mserver.before)
    #this is super ugly
    js = re.findall(r"\[(.*)\]", lwm2mserver.before)
    parsed = json.loads("["+js[0]+"]")
    #print(js)
    #print(parsed)    
    '''
    [   {"bn":"/3/0/","n":"0","vs":"Open Mobile Alliance"},
        {"n":"1","vs":"Lightweight M2M Client"},
        {"n":"2","vs":"345000123"},
        {"n":"3","vs":"1.0"},
        {"n":"6/0","v":1},
        {"n":"6/1","v":5},
        {"n":"7/0","v":3800},
        {"n":"7/1","v":5000},
        {"n":"8/0","v":125},
        {"n":"8/1","v":900},
        {"n":"9","v":100},
        {"n":"10","v":15},
        {"n":"11/0","v":0},
        {"n":"13","v":2985897711},
        {"n":"14","vs":"+01:00"},
        {"n":"15","vs":"Europe/Berlin"},
        {"n":"16","vs":"U"}]
    '''

    # the test use (wireshark logs) accept option LWM2M_CONTENT_SENML_JSON = 110 not LWM2M_CONTENT_JSON = 11543

    assert next(item for item in parsed if item["n"] == "0")["vs"] == "Open Mobile Alliance"
    assert next(item for item in parsed if item["n"] == "1")["vs"] == "Lightweight M2M Client"
    assert next(item for item in parsed if item["n"] == "2")["vs"] == "345000123"
    assert next(item for item in parsed if item["n"] == "3")["vs"] == "1.0"
    assert next(item for item in parsed if item["n"] == "11/0")["v"] == 0
    assert next(item for item in parsed if item["n"] == "16")["vs"] == "U"
    