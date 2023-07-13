import json
import random
from datetime import datetime, timedelta
from json import JSONDecodeError
import time
import jwt
import numpy as np

OLD_TOKENS_TO_NEW_TOKENS = {}

TOKEN_KEY = "random"


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
    authorization_header_value = (
        log.get("http", {})
            .get("request", {})
            .get("headers", {})
            .get("authorization", {})
    )
    if authorization_header_value:
        scheme, token = extract_token(authorization_header_value)
        renewed_token = get_renewed_token(token, timestamp)
        log["http"]["request"]["headers"]["authorization"] = f"{scheme} {renewed_token}"

    response_body_value = (
        log.get("http", {}).get("response", {}).get("body", {}).get("content", "")
    )
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


def create_traffic():
    ts_index = 1  # generated_timestamps.size
    final_array = []

    with open("/home/labuser/wwt-lab-files/modified_30d_traffic.txt", "r") as f:
        content = f.readlines()

    admin_numbers = set()
    for line in content:
        json_obj = json.loads(line)
        seq_number_header = json_obj["http"]["request"]["headers"]["seq_number"]

        if seq_number_header == "admin_ip":
            json_obj["http"]["request"]["headers"]["seq_number"] = str(ts_index)
            admin_numbers.add(ts_index)
        else:
            ts_index = int(json_obj["http"]["request"]["headers"]["seq_number"]) + 1

    ts_index = -1
    random_numbers = [str(random.randint(1, 1470)), str(random.randint(1, 1470))]
    for random_number in random_numbers:
        ts_index += 1
        acc_seq = 0
        for line in content:

            json_obj = json.loads(line)
            seq_number_header = json_obj["http"]["request"]["headers"]["seq_number"]

            if random_number == seq_number_header:
                timestamp = generate_timestamps()[ts_index] + acc_seq
                acc_seq += random.random() * 3
                json_obj["event"]["start"] = (
                        datetime.utcfromtimestamp(timestamp).isoformat(timespec="milliseconds") + "Z")

                if int(random_number) in admin_numbers:
                    json_obj["http"]["request"]["headers"]["seq_number"] = "admin_ip"

                json_obj = replace_with_new_tokens(json_obj, timestamp)
                final_array.append(json_obj)

            else:
                continue

    with open("/home/labuser/wwt-lab-files/benign_traffic/modified_1h_traffic.txt", "a+") as f:
        for line in final_array:
            f.write(f"{json.dumps(line)}\n")


def generate_timestamps():
    number_of_sequences = 2
    generated_deltas = (
            np.arange(number_of_sequences) * 30 * 60
            + np.random.rand(number_of_sequences) * 10 * 60
    )

    return generated_deltas + datetime.utcnow().timestamp() - 3600


if __name__ == "__main__":
    while True:
        print(
            "[*] Now is: {0}Z".format(
                datetime.utcfromtimestamp(datetime.utcnow().timestamp()).isoformat(
                    timespec="milliseconds"
                )
            )
        )
        for i in generate_timestamps():
            print(datetime.utcfromtimestamp(i).isoformat(timespec="milliseconds") + "Z")
        create_traffic()
        time.sleep(3600)
