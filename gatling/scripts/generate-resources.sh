#! /usr/bin/env sh

RESOURCES=./gatling/rinhadebackend/resources
SCRIPTS=./gatling/scripts

function generate_scenarios() {
  echo "Test scenarios not found. Generating them now!"
  python ${SCRIPTS}/gerar-pessoas.py > ${RESOURCES}/pessoas-payloads.tsv
  python ${SCRIPTS}/gerar-termos-busca.py > ${RESOURCES}/termos-busca.tsv
  echo "Generation finished!"
}

if ! [[ -f ${RESOURCES}/pessoas-payloads.tsv ]] || ! [[ -f ${RESOURCES}/termos-busca.tsv ]]
then
  generate_scenarios
else
  echo "Test scenarios already generated!"
fi
