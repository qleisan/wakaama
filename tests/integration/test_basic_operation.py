import pexpect
from time import sleep

def test_read():
    """
    Simple read test
    
    - start example server
    - start example client
    - read single value from client
    - exit client
    - exit server
    """
    import os
    print(os.getcwd())
    server = pexpect.spawn("./build-wakaama-examples/server/lwm2mserver", encoding="utf8", timeout=5)
    server.expect_exact(">")

    client = pexpect.spawn("./build-wakaama-examples/client/lwm2mclient", encoding="utf8", timeout=5)
    
    client.expect("STATE_READY")

    server.sendline("read 0 /31024/10")

    server.expect("OK")
    server.expect("COAP_205_CONTENT")
    
    client.sendline("quit")
    client.expect(pexpect.EOF)

    server.sendline("q")
    server.expect(pexpect.EOF)
    
