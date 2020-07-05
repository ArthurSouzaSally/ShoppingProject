<h1>Trabalho de Shopping</h1>
<h3>Sinopse</h3>
Este é um trabalho para a aula de Sistemas Distribuidos de UFG, feito por Arthur Souza Sally, Carlos Henrique e Helberth.
Com o objetivo de desenvolver uma rede P2P(peer-to-peer) que permita o controle e gerenciamento do numero de pessoas que
pode entrar dentro de um shopping, simulando sensores nas entradas do shopping, nas escadas rolantes para cada andar, em
cada loja, e entradas de funcionarios.<br/>
<h3>Documentação</h3>
<h4>Versão 1.0</h4>
Na primeira versão foi criado um tracker e a engenharia dos peers, o tracker mantinha um arquivo contendo informações de
todos os peers a fim de informar todos os peers da entrada de um novo peer, como ele não faz a comunicação entre os peers
não há como saber se um pacote foi entregue ou não.<br/><br/>
Junto a isso foi implementado um sistema simples de criptografia para os dados enviados de cada pacote, permitindo assim
uma implementação mais segura, mas inicialmente era um grande chat onde os peers podiam enviar uns para os outros qualquer
tipo de mensagem sem maiores problemas nem hierarquia.<br/>
<h4>Versão 1.1</h4>
Foi implementada dentro do Tracker uma variavel que guarda o numero limite de pessoas que estão dentro do shopping, está
o numero real de pessoas dentro do shopping é administrado pelos clientes, que deixaram de enviar mensagens soltas e por
sua vez passaram a enviar mensagens especificas sobre entrada e/ou saída de pessoas.<br/><br/>
