from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

class User:

    def __init__(self, user_id, alias, password):
        self.user_id = user_id
        self.alias = alias
        self.password = password
        self.private_key = rsa.generate_private_key(
            public_exponent = 65537,
            key_size = 2048,
        )

        self.public_key = self.private_key.public_key()
        self.save_keys()
        
    def change_password(self, old_password, new_password):
        if (old_password == self.password):
            self.password = new_password
        else:
            print("Wrong password provided")

    def change_alias(self, new_alias):
        self.alias = new_alias

    def get_alias(self):
        return(self.alias)
    

    def save_keys(self):
        pem_priv = self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        with open('private_key.pem', 'wb') as p:
            p.write(pem_priv)

        pem_pub = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        with open('public_key.pem', 'wb') as f:
            f.write(pem_pub)

    def read_keys(self, password):
        if (self.password == password):
            with open('private_key.pem', 'rb') as p:
                self.private_key = serialization.load_pem_private_key(
                    p.read(),
                    password=None,
                )

            with open('public_key.pem', 'rb') as f:
                self.public_key = serialization.load_pem_public_key(
                    f.read()
                )

if __name__ == "__main__":
    user_Chris = User('3184', 'xenos', 'hej123')
