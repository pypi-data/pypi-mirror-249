import tempfile
import unittest
import uuid
from datetime import datetime, timedelta

from aos_prov.utils.user_credentials import UserCredentials
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives._serialization import (
    Encoding,
    NoEncryption,
    PrivateFormat,
)
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization.pkcs12 import (
    serialize_key_and_certificates,
)
from cryptography.x509.oid import NameOID


def generate_ca_key_and_cert():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    attributes = [
        x509.NameAttribute(NameOID.COUNTRY_NAME, u'UA'),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u'Kyiv'),
        x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, u'Novus Ordo Seclorum'),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u'Epam'),
        x509.NameAttribute(NameOID.EMAIL_ADDRESS, u'support@aoscloud.io'),
        x509.NameAttribute(NameOID.COMMON_NAME, u'TEST Fusion Root CA'),
    ]

    builder = x509.CertificateBuilder()
    builder = builder.subject_name(x509.Name(attributes))
    builder = builder.issuer_name(x509.Name(attributes))
    builder = builder.not_valid_before(datetime.today() - timedelta(days=1))
    builder = builder.not_valid_after(datetime.today() + timedelta(days=100))
    builder = builder.serial_number(int(uuid.uuid4()))
    builder = builder.public_key(private_key.public_key())
    builder = builder.add_extension(
        x509.BasicConstraints(ca=True, path_length=None), critical=True,
    )

    certificate = builder.sign(
        private_key=private_key, algorithm=hashes.SHA256(),
        backend=default_backend()
    )

    return private_key, certificate


def generate_test_key_certificate(ca_key, domain=u"developer.test.local"):
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"California"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u"San Francisco"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, domain),
        x509.NameAttribute(NameOID.COMMON_NAME, domain),
    ])
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.utcnow()
    ).not_valid_after(
        datetime.utcnow() + timedelta(days=10)
    ).sign(ca_key, hashes.SHA256())

    return private_key, cert


def key_cert_to_pem(private_key, cert, ca_cert):
    private_key_pem_bytes = private_key.private_bytes(
        encoding=Encoding.PEM,
        format=PrivateFormat.PKCS8,
        encryption_algorithm=NoEncryption(),
    )
    return private_key_pem_bytes, b''.join([cert.public_bytes(Encoding.PEM), ca_cert.public_bytes(Encoding.PEM)])


def key_cert_to_pkcs12(private_key, cert, ca_cert):
    return serialize_key_and_certificates(
        name=b'TEST friendly name',
        key=private_key,
        cert=cert,
        cas=[ca_cert],
        encryption_algorithm=NoEncryption(),
    )


class TestUserCredentials(unittest.TestCase):
    def test_attributes(self):
        ca_key, ca_cert = generate_ca_key_and_cert()
        key, cert = generate_test_key_certificate(ca_key)
        pkcs_12_cert = key_cert_to_pkcs12(key, cert, ca_cert)

        with tempfile.NamedTemporaryFile(delete=True) as temp_cert:
            temp_cert.write(pkcs_12_cert)
            temp_cert.seek(0)
            uc = UserCredentials('cert', 'key', temp_cert.name)

        uc.cert_type = 'type1'
        self.assertEqual(uc.cert_type, 'type1')

        uc.certificate = 'some cert 1'
        self.assertEqual(uc.certificate, 'some cert 1')

        uc.csr = 'csr'
        self.assertEqual(uc.csr, 'csr')
