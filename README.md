<h1>Trabalho de Shopping</h1>
<h3>Sinopse</h3>
Este é um trabalho para a aula de Sistemas Distribuidos de UFG, feito por Arthur Souza Sally, Carlos Henrique e Helberth.
Com o objetivo de desenvolver uma rede P2P(peer-to-peer) que permita o controle e gerenciamento do numero de pessoas que
pode entrar dentro de um shopping, simulando sensores nas entradas do shopping, nas escadas rolantes para cada andar, em
cada loja, e entradas de funcionarios.<br/>
<h3>Documentação</h3>
<h4>Versão 0.10</h4>
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
<h4>Versão 0.19</h4>
Modo simulador finalmente concluído! E agora foi bem mais facil de implementar pois usava a variavel ipeers para saber
para onde pacotes poderiam ser enviados ou de onde eles poderiam vir, fazendo não só a simulação funcionar, mas ter os
numeros funcionando perfeitamente sem falhas de quantidade de pessoas confusa.<br/><br/>
Houve problemas de novo com o peer shopping durante o modo simulador, mas quando eu fiz ele deixar de ser levado em
consideração no envio de pacotes, a programação voltou a funcionar completamente, além disso eu desabilitei a chance
de pacotes terem origem no peer shopping, que novamente serve apenas como um peer informativo sobre o total de pessoas
que tem dentro do shopping.<br/>
<h4>Versão 0.20</h4>
Foi implementado um sistema de Log, para corrigir falhas na rede criadas por peers que caem ou quando ocorre um erro
na rede, entretanto o sistema de Log também indiretamente aumentou o nivel de processamento da rede uma vez que cada
peer não consegue saber se os outros receberam os pacotes enviados, assim regredindo a um ponto anterior mas ainda sim
corrigindo erros de peers que caem.<br/>
<h4>Versão 0.21 : PARA QUEM ESTIVER INTERESSADO EM RESOLVER ESSE FINAL</h4>
- Eu tentei inicialmente criar um sistema onde pacotes enviados receberiam um tipo de confirmação que o pacote chegou,
assim como o protocolo TCP, entretanto no UDP, mas por algum motivo que eu não entendo isso não funcionou, eu fiquei
quase um mês parado tentando resolver isso e no fim eu resolvi criando um sistema de flooding.<br/><br/>
- Isso garante que os pacotes cheguem, mas ao mesmo tempo impede que os peers saíbam com toda certeza que um peer
recebeu ou não um pacote, junto ao sistema que decide que peers recebem ou não pacotes eu crio um sistema onde não é
possivel confirmar se um peer está ou não funcionando.<br/><br/>
- No momento em que um peer é derrubado ele entra novamente com o LOG, entretanto para o sistema ele é só uma outra
entrada para aquela mesma loja, isso cria um problema que os outros peers vão enviar pacotes não só para os peers que
já funcionam mas para peers que não funcionam mais.<br/><br/>
- A primeira solução que eu pensei era um comando para confirmar a existencia de um peer, entretanto depois de uma
serie interminavel de problemas no timing para a chegada dos pacotes, eu descartei essa possibilidade, o flooding  e o
timing de limite para a chegada de novos pacotes impede que isso funcione com perfeição.<br/><br/>
- A segunda solução e que foi descartada em seguida foi um pacote que corrige as variaveis e informações de outros
peers, numa rede UDP nem mesmo o tracker que atua em baixo nivel de maneira parecida com um servidor consegue saber
quais peers estão ou não funcionando, mas um peer que atua como LOG substituindo-o, o anterior consegue saber que houve
uma falha e qual é o pacote defeituoso, então bastaria criar um pacote que exclui essa informação da rede, porem a
mesma ideia foi descartada por questões obvias de segurança(Se um atacante conseguisse obter acesso a criptografia
da rede, isso seria literalmente uma forma de foder com toda a rede de comunicação estabelecida até agora).<br/><br/>
- A terceira solução está sendo pensada.
