<h1>Trabalho de Shopping</h1>
<h3>Sinopse</h3>
Este é um trabalho para a aula de Sistemas Distribuidos de UFG, feito por Arthur Souza Sally, Carlos Henrique e Helberth.
Com o objetivo de desenvolver uma rede P2P(peer-to-peer) que permita o controle e gerenciamento do numero de pessoas que
pode entrar dentro de um shopping, simulando sensores nas entradas do shopping, nas escadas rolantes para cada andar, em
cada loja, e entradas de funcionarios.<br/>
<h3>Documentação</h3>
<h4>Versão 0.1</h4>
Na primeira versão foi criado um tracker e a engenharia dos peers, o tracker mantinha um arquivo contendo informações de
todos os peers a fim de informar todos os peers da entrada de um novo peer, como ele não faz a comunicação entre os peers
não há como saber se um pacote foi entregue ou não.<br/><br/>
Junto a isso foi implementado um sistema simples de criptografia para os dados enviados de cada pacote, permitindo assim
uma implementação mais segura, mas inicialmente era um grande chat onde os peers podiam enviar uns para os outros qualquer
tipo de mensagem sem maiores problemas nem hierarquia.<br/>
<h4>Versão 0.11</h4>
Foi implementada dentro do Tracker uma variavel que guarda o numero limite de pessoas que estão dentro do shopping, 
o numero real de pessoas dentro do shopping é administrado pelos clientes, que deixaram de enviar mensagens soltas e por
sua vez passaram a enviar mensagens especificas sobre entrada e/ou saída de pessoas.<br/><br/>
Também foi criado um sistema aonde peers novos precisam registrar informações sobre a identidade deles, se são lojas,
andares, ou o shopping, assim permitindo uma base para a implementação de hierarquia, ainda não existente.<br/><br/>
E junto a isso foi criado um sistema para a melhor segurança da entrega de um pacote, como os peers estão usando o
protocolo UDP, não há como garantir a entrega de um pacote apenas pelo envio do mesmo, então foi criado um sistema onde,
assim que for recebido um pacote o peer envia uma mensagem a quem enviou de que o mesmo foi entregue. Assim como um
limitador de tempo para que o sistema de cada peer receba um pacote.<br/>
<h4>Versão 0.12</h4>
Sistema de Login e Senha implementado do lado do tracker, a fim de manter segurança, os usuarios não tem acesso ao arquivo
contendo os dados de entrada, apenas o tracker pode autenticar a entrada de novos usuarios.<br/><br/>
Dentro de um Sistema P2P, é preciso que alguem faça a autenticação dos usuarios, e precisa ser alguem de confiança, os
peers nunca podem ter acesso direto ao arquivo onde estão guardados os dados dos usuarios, se não existe problemas para
manter a segurança e a garantia de que os usuarios são autenticos.<br/>
<h4>Versão 0.13</h4>
O codigo inteiro foi refeito, mas o sistema de login e senha já foi implementado, assim como o funcionamento do tracker
que funciona perfeitamente, os pacotes se tornaram mais complexos e foi implementado um sistema para diferenciar quais
pacotes são mais novos e quais são mais velhos, assim permitindo uma implementação mais segura do codigo.<br/><br/>
A hierarquia foi implementada, mas por problemas no envio de pacotes ainda preciso tornar o UDP ainda mais seguro com
uma confirmação maior de que os pacotes foram processados.<br/>
<h4>Versão 0.14</h4>
Agora quando um peer recebe um pacote sobre a entrada de pessoas que supera o numero limite de pessoas na sua área ele
envia um pacote de recusa informando o contrario, assim nivelando os numeros dentro da rede, além disso foi corrigido
a coerencia dos pacotes enviados e processados por diferentes partes diminuindo erros de comunicação.<br/><br/>
Pacotes são processados na ordem em que eles chegam, além de que o sistema é capaz de diferenciar pacotes mais velhos
de pacotes mais recentes, pois guarda na lista de peers quantos pacotes ele já recebeu de cada peer, e como pacotes na
rede são enumerados é possivel diferenciar o que veio primeiro e o que veio depois.<br/>
<h4>Versão 0.15</h4>
O sistema de envio de mensagens foi totalmente refeito para um sistema onde os pacotes são enumerados para assumir a
lógica de um relogio lógico, e as mensagens são enviadas em exesso na rede, quando um peer recebe um pacote, ele vai e
verifica se aquele pacote já foi levado em consideração, e quando já foi apenas o ignora, se não ele o processa e já
aguarda pelo envio do proximo, esse foi o sistema que se mostrou mais eficiente até agora.<br/><br/>
Na versão anterior tinha sido adicionado um sistema de recusa de pacotes que retornava pacotes quando estes superavam
o limite de pessoas já existentes na área marcada pelo peer, agora esse sistema além de ter sido mais otimizado, foi
concertado alguns bugs que existiam por causa de uma falta de segurança no envio das mensagens, o que faz o sistema
funcionar com maior exatidão.<br/><br/>
Eu tentei também criar um sistema de simulação de entradas e saídas, mas eu fiz merda e as coisas precisam ser feitas
de novo para ter uma qualidade maior, por que como tá ficou uma verdadeira bagunça.<br/>
<h4>Versão 0.16</h4>
Foi adicionado um sistema de hierarquia de rede para diminuir o numero de pacotes enviados na rede, agora existe uma
variavel que salva as identidades dos peers, e quando um pacote precisa ser enviado ele lê essa variavel para ver se
todos precisam receber o pacote ou se apenas um grupo seleto precisa, assim reduzindo o numero de pacotes enviados na
rede.<br/><br/>
Os comandos novos são 'ipeers' para ver a identidades dos peers na rede, 'media' para ver o numero de pacotes que <b>NÃO</b>
é enviado na rede por causa das identidades, a unica desvantagem é que elas só passam a funcionar depois que todos os peers
se comunicaram, ou seja no inicio quando não há informação sobre a identidade dos peers, a fim de evitar falhas, todos os
peers recebem pacotes normalmente.<br/>
<h4>Versão 0.17</h4>
Agora o Peer "Shopping" é apenas visual, ele não define quem entra nem sai, apenas os andares e lojas, e antes havia uma
falha no qual a variavel 'ipeers' era atualizada apenas quando os primeiros pacotes eram enviados pelos usuarios, agora os
mesmos se atualizam assim que entram na rede. Sem a necessidade do tracker, apenas a própria rede P2P é necessaria, isso
se dá por pacotes vazios, onde os peers já informam uns aos outros sobre entradas vazias no inicio já se informando sobre
suas respectivas identidades na rede.<br/>
<h4>Versão 0.18</h4>
Primeiramente agora é necessario que se faça a instalação da biblioteca <code>cryptography</code> pelo pip:<br/><br/>
<code>pip install cryptography</code><br/><br/>
Pois foi implementado um sistema de criptografia na rede, agora depois que os peers se autenticam com o servidor, ele
envia para eles uma chave de criptografia que é usada tanto para criptografar quanto para descriptografar mensagens que
são enviadas na rede, a chave é modificada toda vez que o tracker é reiniciado.<br/><br/>
As mensagens trocadas entre os peers são todas criptografadas seguindo esse modelo a partir de agora.<br/>
<h4>Versão 0.19 : EM BREVE</h4>
- Melhorar mais o programa<br/>
- Procurar e Corrigir Bugs<br/>
