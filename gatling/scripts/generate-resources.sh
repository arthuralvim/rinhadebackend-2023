#! /usr/bin/env bash

function generate_scenarios() {
  echo "Test scenarios not found. Generating them now!"
  python3 ${GATLING_BIN}/gerar-pessoas.py > ${GATLING_RESOURCES}/pessoas-payloads.tsv
  python3 ${GATLING_BIN}/gerar-termos-busca.py > ${GATLING_RESOURCES}/termos-busca.tsv
  echo "Generation finished!"
}

if ! [[ -f ${GATLING_RESOURCES}/pessoas-payloads.tsv ]] || ! [[ -f ${GATLING_RESOURCES}/termos-busca.tsv ]]
then
  generate_scenarios
else
  echo "Test scenarios already generated!"
fi
