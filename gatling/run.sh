#!/usr/bin/env bash

set -o errexit
set -o nounset
set -x

WORKSPACE="/test-runner/"
GATLING_BIN_DIR="/test-runner/gatling/bin"

app_ready() {
python << END
import sys
import json
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

def check_ready(url):
    try:
        with urlopen(url, timeout=10) as response:
            return json.loads(response.read()), response.getcode()

    except (HTTPError, URLError, TimeoutError) as e:
        print(e.status, e.reason)

try:
    content, code = check_ready("http://nginx:9999/ready")
    if content is not None and code == 200 and not content.get('ready', False):
        sys.exit(-1)
except Exception:
    sys.exit(-1)
sys.exit(0)
END
}

until app_ready; do
  >&2 echo 'Waiting for App to be available...'
  sleep 1
done
>&2 echo 'App is ready!'


app_count_zero() {
python << END
import sys
import json
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

def get_url(url):
    try:
        with urlopen(url, timeout=10) as response:
            return json.loads(response.read()), response.getcode()
    except (HTTPError, URLError, TimeoutError) as e:
        print(e.status, e.reason)

try:
    content, code = get_url("http://nginx:9999/contagem-pessoas")
    if content is not None and code == 200 and content != 0:
        sys.exit(-1)
except Exception:
    sys.exit(-1)
sys.exit(0)
END
}

app_count_zero

function generate_scenarios() {
  echo "Test scenarios not found. Generating them now!"
  python "/test-runner/data/gerar-pessoas.py" > /test-runner/user-files/resources/pessoas-payloads.tsv
  python "/test-runner/data/gerar-termos-busca.py" > /test-runner/user-files/resources/termos-busca.tsv
  echo "Generation finished!"
}

if ! [[ -f "/test-runner/user-files/resources/pessoas-payloads.tsv" ]] || ! [[ -f "/test-runner/user-files/resources/termos-busca.tsv" ]]
then
  generate_scenarios
fi

cat rinha.ascii

sh ${GATLING_BIN_DIR}/gatling.sh \
  -rm local \
  -s RinhaBackendSimulation \
  -rd "DESCRICAO" \
  -rf ${WORKSPACE}/user-files/results \
  -sf ${WORKSPACE}/user-files/simulations \
  -rsf ${WORKSPACE}/user-files/resources

sleep 3

COUNT=$(curl -fsSL "http://nginx:9999/contagem-pessoas")
echo "${COUNT}"
