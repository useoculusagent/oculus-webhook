import hmac, hashlib
from oculus_webhook.verify import verify_signature


def test_verify_signature_ok():
    secret = "topsecret"
    body = b'{"foo":"bar"}'
    sig = "sha256=" + hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    assert verify_signature(secret, body, sig) is True


def test_verify_signature_bad():
    assert verify_signature("topsecret", b'{}', "sha256=deadbeef") is False
    assert verify_signature("topsecret", b'{}', "") is False
    assert verify_signature("topsecret", b'{}', "md5=abc") is False

# pass 8

# pass 12

# pass 16

# pass 30

# pass 42

# pass 43

# pass 48

# pass 54
