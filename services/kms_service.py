import boto3

kms = boto3.client(
    "kms",
    region_name="us-east-1",
    verify=False
)

def encrypt_text(text, key_id):

    response = kms.encrypt(
        KeyId=key_id,
        Plaintext=text.encode()
    )

    return response["CiphertextBlob"]


def decrypt_text(ciphertext):

    response = kms.decrypt(
        CiphertextBlob=ciphertext
    )

    return response["Plaintext"].decode()

def decrypt_text(ciphertext):

    response = kms.decrypt(
        CiphertextBlob=ciphertext
    )

    return response["Plaintext"].decode()