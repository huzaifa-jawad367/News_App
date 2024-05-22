from ecdsa import SigningKey, SECP256k1
from hashlib import sha256

class Schnorr:
    def __init__(self):
        self.curve = SECP256k1
        self.G = self.curve.generator
        self.n = self.curve.order

    def generate_keys(self):
        private_key = SigningKey.generate(curve=self.curve)
        public_key = private_key.get_verifying_key()
        return private_key, public_key

    def sign(self, private_key, message):
        # Hash the message
        h_msg = sha256(message.encode('utf-8')).digest()
        # Generate a random nonce k
        k = SigningKey.generate(curve=self.curve)
        R = k.verifying_key.pubkey.point
        Rx, Ry = R.x(), R.y()
        # Calculate e = H(Rx || m)
        e = int.from_bytes(sha256(Rx.to_bytes(32, byteorder='big') + h_msg).digest(), byteorder='big')
        # Calculate s = k + e * private_key
        s = (k.privkey.secret_multiplier + e * private_key.privkey.secret_multiplier) % self.n
        return Rx, s

    def verify(self, public_key, message, signature):
        Rx, s = signature
        h_msg = sha256(message.encode('utf-8')).digest()
        e = int.from_bytes(sha256(Rx.to_bytes(32, byteorder='big') + h_msg).digest(), byteorder='big')
        R = s * self.G - e * public_key.pubkey.point
        return R.x() == Rx

# Example usage
if __name__ == "__main__":
    schnorr = Schnorr()
    
    # Key generation
    private_key, public_key = schnorr.generate_keys()
    
    # Signing a message
    message = "Hello, this is a test message."
    signature = schnorr.sign(private_key, message)
    
    # Verifying the signature
    is_valid = schnorr.verify(public_key, message, signature)
    print("Signature valid:", is_valid)
