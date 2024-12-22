import subprocess
import sys
import time
import json
import os
import transmission_rpc

name = "libgen-seedtools"
config_path = os.path.join(os.getcwd(), "tests/testdata/config.json")
base_cmd = [name, f'--config={config_path}'] 
config_schema_version = 1.1
transmission_rpc_min_version = 16

def test_config():
    d='/home/runner/work/libgen-seedtools/'
    print(d)

    print(os.listdir(d))

    d='/home/runner/work/libgen-seedtools/libgen-seedtools/'
    print(d)
    print(os.listdir(d))

    d='/home/runner/work/libgen-seedtools/libgen-seedtools/tests/'
    print(d)
    print(os.listdir(d))

    print("DDDDDDDDDDD:", [*base_cmd, "generate-config"])
 
    result = subprocess.run(
        [*base_cmd, "generate-config"],
        capture_output=True,
        text=True,
    )
    #assert result.returncode == 0, f"Got:\n{result.stderr}"
    assert result.returncode == 0

    with open(config_path, "r") as file:
        #print(file.read())
        config = json.load(file)
    assert config["version"] == config_schema_version


def test_version():
    result = subprocess.run(
        [name, "--version"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert f"{name}, version" in result.stdout.lower()


def test_transmission_rpc():
    client = transmission_rpc.Client(
        host="127.0.0.1", port=9091, username="username", password="password"
    )
    assert client.get_session() is not None
    assert client.get_session().rpc_version > transmission_rpc_min_version


def test_fetch():
    result = subprocess.run(
        [*base_cmd, "fetch", "--auto-verify"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Got:\n{result.stderr}"


def test_dryrun():
    result = subprocess.run(
        [*base_cmd, "fetch", "--dry-run"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Got:\n{result.stderr}"
