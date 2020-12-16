"""
These tests implement the OMA-ETS-LightweightM2M-V1_1-20190912-D specification:
https://www.openmobilealliance.org/release/LightweightM2M/ETS/OMA-ETS-LightweightM2M-V1_1-20190912-D.pdf
"""

import re

def parse_client_registration(server_output):
    """
    Output from example server with example client:
    165 bytes received from [::1]:56830
    44 02 78 D1  D1 78 B8 FC  B2 72 64 11  28 39 6C 77   D.x..x...rd.(9lw
    6D 32 6D 3D  31 2E 31 0D  05 65 70 3D  74 65 73 74   m2m=1.1..ep=test
    6C 77 6D 32  6D 63 6C 69  65 6E 74 03  62 3D 55 06   lwm2mclient.b=U.
    6C 74 3D 33  30 30 FF 3C  2F 3E 3B 72  74 3D 22 6F   lt=300.</>;rt="o
    6D 61 2E 6C  77 6D 32 6D  22 3B 63 74  3D 31 31 30   ma.lwm2m";ct=110
    2C 3C 2F 31  2F 30 3E 2C  3C 2F 32 2F  30 3E 2C 3C   ,</1/0>,</2/0>,<
    2F 33 2F 30  3E 2C 3C 2F  34 2F 30 3E  2C 3C 2F 35   /3/0>,</4/0>,</5
    2F 30 3E 2C  3C 2F 36 2F  30 3E 2C 3C  2F 37 2F 30   /0>,</6/0>,</7/0
    3E 2C 3C 2F  33 31 30 32  34 2F 31 30  3E 2C 3C 2F   >,</31024/10>,</
    33 31 30 32  34 2F 31 31  3E 2C 3C 2F  33 31 30 32   31024/11>,</3102
    34 2F 31 32  3E                                      4/12>

    New client #0 registered.
    Client #0:
        name: "testlwm2mclient"
        version: "1.1"
        binding: "UDP"
        lifetime: 300 sec
        objects: /1/0, /2/0, /3/0, /4/0, /5/0, /6/0, /7/0, /31024/10, /31024/11, /31024/12, 
    """
    #print(server_output.encode())
    client_id,  = re.findall(r"New client #([0-9]+) registered.", server_output)
    endpoint, = re.findall(r"name: \"([\w-]+)\"\r\r\n", server_output)
    version, = re.findall(r"version: \"([0-9.]+)\"\r\r\n", server_output)
    binding, = re.findall(r"binding: \"([A-Z]+)\"\r\r\n", server_output)
    lifetime, = re.findall(r"lifetime: ([0-9]+) sec\r\r\n", server_output)
    objects, = re.findall(r"objects: ([\/0-9, ]+)\r\r\n", server_output)
    objects = objects.split(",")
    return int(client_id), endpoint, version, binding, int(lifetime), objects


def test_registration_interface(lwm2mserver, lwm2mclient):
    """LightweightM2M-1.1-int-102
    Test that the Client registers with the Server."""
    lwm2mserver.expect_exact("\r\r\n>")
    client_id, endpoint, version, binding, lifetime, objects = \
        parse_client_registration(lwm2mserver.before)
    assert client_id == 0
    assert endpoint == "testlwm2mclient"
    assert version == "1.1"
    assert binding == "UDP"
    assert lifetime == 300
    assert "/1/0" in objects
