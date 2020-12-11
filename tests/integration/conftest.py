import pytest
import pexpect

@pytest.fixture
def lwm2mserver():
    """Provide lwm2mserver instance."""
    server = pexpect.spawn("build-wakaama/examples/server/lwm2mserver",
                           encoding="utf8",
                           timeout=3)
    server.expect_exact("> ")
    yield server
    server.sendline("q")
    server.expect(pexpect.EOF)

@pytest.fixture
def lwm2mclient():
    """Provide lwm2mclient instance."""
    client = pexpect.spawn("build-wakaama/examples/client/lwm2mclient",
                           encoding="utf8",
                           timeout=3)
    client.expect("STATE_READY")
    yield client
    client.sendline("quit")
    client.expect(pexpect.EOF)
