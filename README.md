# Next Release Problem

Este repositório contém informações relacionadas ao problema da próxima release.

## Visão Geral do Sistema

Na Engenharia de Software, é comum nos depararmos com desafios que envolvem a busca por um equilíbrio adequado entre metas que podem ser conflitantes e concorrentes. Esses desafios frequentemente requerem a tomada de decisões em meio a um amplo leque de opções disponíveis, tornando a seleção de soluções apropriadas uma tarefa complexa.

Este artigo aborda o dilema enfrentado por empresas que se dedicam ao desenvolvimento e manutenção de sistemas de software complexos. O cerne da questão reside em determinar quais recursos devem ser incorporados à próxima versão do software. Essa decisão é de suma importância, uma vez que as empresas buscam atender às demandas de seus clientes, enquanto garantem que possuam os recursos necessários para efetuar o desenvolvimento.

O artigo evidencia a complexidade desse problema, classificando-o como NP-difícil, o que significa que encontrar a solução ótima pode demandar recursos computacionais consideráveis.

## Variáveis

| Variável                 | Descrição                                    |
|--------------------------|----------------------------------------------|
| x                        | Identificação do requisito implementado     |
| y                        | Identificação do cliente a ser atendido     |
| n                        | Quantidade de clientes                      |
| m                        | Quantidade de requisitos                    |
| L                        | Limitação do custo de implementação da empresa |
| v                        | Importância do cliente para a empresa      |
| c                        | Custo de cada requisito                     |
| dm                       | Matriz de associação de requisitos           |
| cm                       | Matriz de associação de clientes com requisitos |

## Instâncias

Como em nenhum artigo era disponibilizado às instâncias de forma coerente para usarmos nesse trabalho, tivemos que atuar na geração dessas instâncias. Com isso, temos:

* m: é definida com base no valor colocado no terminal pelo usuário.

* n: é definida com base no valor colocado no terminal pelo usuário.

* v: definido que será gerada uma lista do tamanho da quantidade de requisitos informado, onde nessa lista, os valores serão aleatórios inteiros entre 1 e 10.

* c: definido que serão gerados m valores de custo aleatórios inteiros entre 1 e 10 e adicionados a essa lista.

* dm: definido pela chamada da função de generateDm, onde será gerada a matriz de requisitos dependentes. A função generateDm cria essa matriz com algumas camadas de densidade para validar a quantidade de elementos iguais a 1, representando as dependências.

* cm: é gerada em um loop aninhado que atribui valores 0 ou 1 para cada par de requisitos associados a um cliente. Logo, quando existir o valor 1, significa que aquele requisito será implementado para aquele cliente. Destacamos duas regras principais:
Cada cliente precisa possuir pelo menos um requisito solicitado, isso significa que em cada linha da matriz (representando um cliente), deve haver pelo menos um "1" para garantir que pelo menos um requisito seja solicitado para esse cliente.
Cada requisito precisa ser uma ou mais vezes solicitado para ser implementado, isso significa que em cada coluna da matriz (representando um requisito), deve haver pelo menos um "1" para garantir que o requisito seja solicitado por pelo menos um cliente.

* L:  representa uma versão ponderada do custo total dos requisitos, destacando que o fator alpha é usado para ajustar o peso do custo total na construção do valor L.

## Referências

- [The next release problem](https://www.example.com/nesting-problem.pdf) - Artigo original sobre o problema.
- [Algoritmos de otimização para solução do Problema do Próximo Release](http://www.bsi.ufrpe.br/sites/www.bsi.ufrpe.br/files/Mariana.pdf) - Outro recurso relacionado ao problema.

## Autores

- Ana Fábia
- Luíza Nurnberg
- Maria Cecilia Holler


