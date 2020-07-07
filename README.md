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
Foi implementada dentro do Tracker uma variavel que guarda o numero limite de pessoas que estão dentro do shopping, 
o numero real de pessoas dentro do shopping é administrado pelos clientes, que deixaram de enviar mensagens soltas e por
sua vez passaram a enviar mensagens especificas sobre entrada e/ou saída de pessoas.<br/><br/>
Também foi criado um sistema aonde peers novos precisam registrar informações sobre a identidade deles, se são lojas,
andares, ou o shopping, assim permitindo uma base para a implementação de hierarquia, ainda não existente.<br/><br/>
E junto a isso foi criado um sistema para a melhor segurança da entrega de um pacote, como os peers estão usando o
protocolo UDP, não há como garantir a entrega de um pacote apenas pelo envio do mesmo, então foi criado um sistema onde,
assim que for recebido um pacote o peer envia uma mensagem a quem enviou de que o mesmo foi entregue. Assim como um
limitador de tempo para que o sistema de cada peer receba um pacote.<br/>
<h4>Versão 1.2</h4>
Sistema de Login e Senha implementado do lado do tracker, a fim de manter segurança, os usuarios não tem acesso ao arquivo
contendo os dados de entrada, apenas o tracker pode autenticar a entrada de novos usuarios.<br/>
<h4>Versão 1.3 : EM BREVE</h4>
- Fazer um sistema para diferenciar mais entradas, funcionarios, clientes, etc...<br/>
- Junto a isso criar o sistema de hierarquia dentro de cada peer, assim eles funcionam sozinhos.<br/>
