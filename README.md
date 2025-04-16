# BitDogLab Genius.py
## Introdução e Objetivos
Jogos que envolvem memorização contribuem para o desenvolvimento cognitivo e socioemocional de crianças e adultos. Eles estimulam diversas áreas do cérebro, como a memória visual, a capacidade de percepção espacial, o foco e a tomada de decisões rápidas. Dessa forma, este projeto tem como objetivo criar um jogo que estimule a memória por meio de desafios visuais. Com o uso de LEDs, espera-se que ele possa ser acessível também para pessoas mais velhas, pois elementos luminosos podem facilitar a visualização e a diferenciação dos padrões.
## Funcionamento
O projeto deve cumprir os seguintes requisitos:

• A sequência de LEDs deve ser aleatória a cada rodada. Ela é mostrada em branco, piscando na sequência a ser replicada pelo jogador.

• Para iniciar o jogo, o jogador seleciona até que nível deseja jogar colocando o joystick para cima e/ou para baixo, incrementando/decrementanado assim o nível. Esse nível a ser definido pode ser acompnhado pelo display OLED.Para confirmar, clicamos qualquer um dos botões. Então, ele pressiona qualquer um dos botões e o jogo se inicia.

• O jogador poderá mover um cursor pela matriz de LEDs utilizando o joystick, e selecionar utilizando qualquer um dos botões.

• Ao selecionar um LED da matriz de LEDs, o LED RGB externo à matriz acende em azul, se ainda faltarem LEDs a serem selecionados para completar o nível; em verde se tiver acertado todos os LEDs do nível; ou em vermelho, caso o jogador erre o LED.

• A placa deve tocar um efeito sonoro quando o jogador completar um nível, e outro efeito diferente quando ele errar.

• Cada nível é definido pelo número de LEDs a serem acesos. Esse número vai sendo incrementado até chegar ao nível selecionado inicialmente pelo jogador, onde todos os LEDs acendem em uma sequência específica. O nível em que o jogador está será mostrado no display OLED.

• Após o jogador perder ou completar o jogo, o display OLED irá mostrar uma mensagem perguntando se o jogador deseja jogar novamente. Para reiniciar o jogo, basta apertar um dos botões.
