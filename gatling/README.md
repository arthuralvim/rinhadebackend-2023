# Testes com o Gatling

### Instruções

- Antes de executar teste os endpoints usando o código abaixo:

```sh
# exemplos de requests
curl -v -XPOST -H "content-type: application/json" -d '{"apelido" : "xpto", "nome" : "xpto xpto", "nascimento" : "2000-01-01", "stack": null}' "http://localhost:9999/pessoas"
curl -v -XGET "http://localhost:9999/pessoas/1"
curl -v -XGET "http://localhost:9999/pessoas?t=xpto"
curl -v "http://localhost:9999/contagem-pessoas"
```

### Executando os testes

```sh
sh run-test.sh
```
