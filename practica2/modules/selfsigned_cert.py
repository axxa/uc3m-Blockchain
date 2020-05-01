import modules.cifrado as cifrado

import datetime
from cryptography import x509
from cryptography.x509 import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


def create_self_signed_cert(cert_dir):
    private_key = cifrado.read_private_key()
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Texas"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u"Austin"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"My Company"),
        x509.NameAttribute(NameOID.COMMON_NAME, u"My CA"),
    ])
    root_cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.utcnow()
    ).not_valid_after(
        datetime.datetime.utcnow() + datetime.timedelta(days=3650)
    ).sign(private_key, hashes.SHA256(), default_backend())

    # Now we want to generate a cert from that root
    cert_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    new_subject = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Texas"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u"Austin"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"New Org Name!"),
    ])
    cert = x509.CertificateBuilder().subject_name(
        new_subject
    ).issuer_name(
        root_cert.issuer
    ).public_key(
        cert_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.utcnow()
    ).not_valid_after(
    datetime.datetime.utcnow() + datetime.timedelta(days=30)
    ).add_extension(
        x509.SubjectAlternativeName([x509.DNSName(u"somedomain.com")]),
        critical=False,
    ).sign(private_key, hashes.SHA256(), default_backend())

    pem = cert.public_bytes(encoding=serialization.Encoding.PEM)
    with open(cert_dir, 'wb') as f:
        f.write(pem)
