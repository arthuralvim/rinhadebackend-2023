#! /usr/bin/env sh

WORKSPACE=$(pwd)
GATLING_BIN_DIR="${WORKSPACE}/test-runner/gatling/bin"
GATLING_VERSION="3.9.5"

function install_gatling() {
  [ -d test-runner ] || mkdir -p test-runner
  echo "Downloading: version ${GATLING_VERSION}"
  curl -fsSL "https://repo1.maven.org/maven2/io/gatling/highcharts/gatling-charts-highcharts-bundle/${GATLING_VERSION}/gatling-charts-highcharts-bundle-${GATLING_VERSION}-bundle.zip" > ./test-runner/gatling.zip
  cd test-runner/
  rm -rf ./gatling
  unzip gatling.zip
  mv gatling-charts-highcharts-bundle-3.9.5 gatling
  rm gatling.zip
  cd ..
  echo "All done!"
}

function generate_scenarios() {
  echo "Test scenarios not found. Generating them now!"
  python "${WORKSPACE}/data/gerar-pessoas.py" > ./user-files/resources/pessoas-payloads.tsv
  python "${WORKSPACE}/data/gerar-termos-busca.py" > ./user-files/resources/termos-busca.tsv
  echo "Generation finished!"
}

if ! [ -d "test-runner" ]; then
  echo "Gatling not found. Installing it now!"
  install_gatling
fi

if ! [[ -f "./user-files/resources/pessoas-payloads.tsv" ]] || ! [[ -f "./user-files/resources/termos-busca.tsv" ]]
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

COUNT=$(curl -fsSL "http://localhost:9999/contagem-pessoas")
echo "${COUNT}"
