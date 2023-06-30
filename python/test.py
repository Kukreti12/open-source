import boto3

s3_resource = boto3.resource(
    "s3",
    endpoint_url="https://singlenodedf.ailab.local:9000",
    aws_access_key_id="7GM4BT71Q56BX55FZOCN4XF4ATVQTS0TJIPTVJIPC82KAFZLVGC5Q2ELQIDAJEORM6FWOYSL7D40ZZQC1PJZJANHXSL3LNIRAKGVM3EY2NDYAXPX3AFXS0A6F",
    aws_secret_access_key="BNARYBWC1LSDK02S7O8VQRPHHXTD78Q6K52UZZ5XMRCXZX8K202CNE1VWTXGX4OGJ6T2WNMUX",
    verify="df5.pem",
)
s3_resource.Bucket("landing").upload_file("file.csv", "file.csv")
