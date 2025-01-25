#!/usr/bin/env bash

set -o errexit
set -o nounset
set -x

app_ready() {
python3 << END
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
    content, code = check_ready("http://proxy:9999/ready")
    if content is not None and code == 200 and not content.get('ready', False):
        sys.exit(-1)
except Exception:
    sys.exit(-1)
sys.exit(0)
END
}

until app_ready; do
  >&2 echo 'Waiting for App to be available...'
  sleep 10
done
>&2 echo 'App is ready!'


app_count_zero() {
python3 << END
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
    content, code = get_url("http://proxy:9999/contagem-pessoas")
    if content is not None and code == 200 and content != 0:
        sys.exit(-1)
except Exception:
    sys.exit(-1)
sys.exit(0)
END
}

app_count_zero

cat rinha.ascii

sh ${GATLING_BIN}/gatling.sh \
  -rm local \
  -s RinhaBackendSimulation \
  -rd ${GATLING_DESCRIPTION} \
  -erjo -Dgatling.core.outputDirectoryBaseName=${GATLING_RESULT_PREFIX} \
  -rf ${GATLING_HOME}/user-files/results \
  -sf ${GATLING_HOME}/user-files/simulations \
  -rsf ${GATLING_HOME}/user-files/resources

sleep 3

COUNT=$(curl -fsSL "http://proxy:9999/contagem-pessoas")
echo "${COUNT}"
