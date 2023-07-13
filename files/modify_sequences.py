import ipaddress
import json
import os
import random
from datetime import datetime, timedelta
from json import JSONDecodeError

import jwt
import numpy as np

BASE_HOUR = float(os.getenv("LAB_CREATION_TIME", datetime.utcnow().timestamp()))
LAB_INSTANCE_IP = os.getenv("LAB_INSTANCE_IP", os.uname()[1])
BASE_IP = "10.0.0.0"
TOKEN_KEY = "random"

OLD_TOKENS_TO_NEW_TOKENS = {}
generated_ips = []


def to_json_safe(json_str, default=None):
    try:
        return json.loads(json_str)
    except JSONDecodeError:
        return default


def extract_token(authorization_header_value: str):
    scheme, _, param = authorization_header_value.partition(" ")
    return scheme, param


def renew_jwt_expiration_date(token, timestamp):
    decoded_jwt = jwt.decode(
        token, algorithms="HS256", options={"verify_signature": False}
    )
    decoded_jwt["iat"] = datetime.fromtimestamp(timestamp).timestamp()
    decoded_jwt["exp"] = (
            datetime.fromtimestamp(timestamp) + timedelta(seconds=1000)
    ).timestamp()
    return jwt.encode(decoded_jwt, TOKEN_KEY)


def get_renewed_token(old_token, timestamp):
    return OLD_TOKENS_TO_NEW_TOKENS.setdefault(
        old_token, renew_jwt_expiration_date(old_token, timestamp)
    )


def replace_with_new_tokens(log, timestamp):
    authorization_header_value = log.get("http", {}).get("request", {}).get("headers", {}).get("authorization", {})
    if authorization_header_value:
        scheme, token = extract_token(authorization_header_value)
        renewed_token = get_renewed_token(token, timestamp)
        log["http"]["request"]["headers"]["authorization"] = f"{scheme} {renewed_token}"

    response_body_value = log.get("http", {}).get("response", {}).get("body", {}).get("content", "")
    if response_body_value:
        response_body = to_json_safe(response_body_value, default={})
        auth_token = response_body.get("auth_token", "")
        if auth_token:
            renewed_token = get_renewed_token(auth_token, timestamp)
            response_body["auth_token"] = renewed_token
            response_body_str = json.dumps(response_body)
            log["http"]["response"]["body"]["content"] = response_body_str
            log["http"]["response"]["body"]["bytes"] = len(response_body_str)

    return log


def modify_log_file():
    seq_number = None
    ts_index = generated_timestamps.size
    acc_seq = 0
    final_array = []

    with open("/wwt-lab-files/basic.json", "r") as f:
        for line in f.readlines():
            json_obj = json.loads(line)
            seq_number_header = json_obj["http"]["request"]["headers"]["seq_number"]
            if seq_number != seq_number_header:
                seq_number = seq_number_header
                acc_seq = 0
                ts_index -= 1

                if seq_number_header == "admin_ip":
                    new_ip = admin_ip
                else:
                    new_ip = random_ip_and_remove()
            json_obj["source"]["ip"] = new_ip
            new_url = json_obj["url"]["full"].replace("localhost:5000", LAB_INSTANCE_IP)
            json_obj["url"]["full"] = new_url
            timestamp = generated_timestamps[ts_index] + acc_seq
            acc_seq += random.random() * 3
            json_obj["event"]["start"] = (
                    datetime.utcfromtimestamp(timestamp).isoformat(timespec="milliseconds")
                    + "Z"
            )
            json_obj = replace_with_new_tokens(json_obj, timestamp)

            final_array.append(json_obj)

    with open("modified_30d_traffic.txt", "w") as f:
        for line in final_array:
            f.write(f"{json.dumps(line)}\n")


def generate_ips():
    ip_array = []
    for ip in ipaddress.IPv4Network(f"{BASE_IP}/21"):
        ip_array.append(str(ip))

    return ip_array


def generate_timestamps():
    number_of_sequences = 30 * 48 + 30  # days * sequences in 1 day + admin sequences
    generated_deltas = (
            np.arange(number_of_sequences) * 30 * 60
            + np.random.rand(number_of_sequences) * 10 * 60
            - 5 * 60
    )
    generated_deltas[0] = 0

    return generated_deltas * -1 + BASE_HOUR


def random_ip_and_remove():
    random_int = random.randint(0, len(generated_ips) - 1)
    chosen_ip = generated_ips[random_int]
    generated_ips.pop(random_int)

    return chosen_ip


if __name__ == "__main__":
    generated_ips = generate_ips()
    generated_timestamps = generate_timestamps()
    admin_ip = random_ip_and_remove()
    print(
        "[*] Now is: "
        + datetime.utcfromtimestamp(BASE_HOUR).isoformat(timespec="milliseconds")
        + "Z"
    )
    modify_log_file()
