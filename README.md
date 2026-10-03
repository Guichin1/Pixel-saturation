# Pixel Saturation

Um efeito de vídeo que roda diretamente no navegador. O app acompanha os pixels entre os quadros e fixa cada um em uma cor escolhida depois que ele muda um número definido de vezes.

## Executar localmente

Abra [`index.html`](index.html) em uma versão recente de um navegador para desktop. Não é necessário instalar dependências ou executar um processo de build. Para usar o vídeo de demonstração incluído, abra o app por um servidor local ou pelo GitHub Pages e pressione **Use sample**; **Choose video** continua disponível para arquivos próprios.

Escolha um vídeo, ajuste as cores e os parâmetros do efeito e pressione **Play** para pré-visualizar. **Reset effect** limpa o estado acumulado dos pixels e volta ao início.

## Diagnóstico em celular pela LAN

Para registrar uma sessão de teste sem publicar o projeto, execute `python lan_logger.py --host 0.0.0.0 --port 8000` neste computador. No celular conectado à mesma rede Wi-Fi, abra `http://IP-DO-COMPUTADOR:8000/`. O endereço IP aparece com `ipconfig` no Windows.

O servidor grava eventos de interface, estado do vídeo, erros e um resumo do processamento a cada cinco segundos em `device-log.jsonl`. Os resumos incluem diferenças de pixels observadas, diferenças acima da sensibilidade, maior contagem acumulada e pixels travados. O vídeo e o nome do arquivo escolhido não são enviados. O log é ignorado pelo Git; compartilhe-o apenas se desejar ajuda para analisar a sessão. Encerre o servidor com `Ctrl+C` no terminal.

## Formatos de vídeo

O seletor aceita formatos comuns, incluindo MP4, M4V, WebM, Ogg, MOV, MKV e AVI. A extensão, por si só, não garante a reprodução: a decodificação depende dos codecs disponíveis no navegador e no sistema operacional. MP4 com H.264 e WebM com VP8/VP9 têm ampla compatibilidade; o suporte a MOV, MKV, AVI e outros codecs varia conforme o navegador.

O repositório inclui `Sample/FROM-EARTH-TO-SPACE-Free-HD-VIDEO-NO-COPYRIGHT_001_720p.mp4` como mídia de demonstração e teste (H.264, 1280×720, aproximadamente 2 min 23 s). O botão **Use sample** carrega esse arquivo diretamente do repositório.

Para um teste rápido, use **Use sample**, confira se a duração aparece como `02:23`, reproduza alguns segundos e pause para verificar a contagem de frames. Para testar exportação sem esperar o vídeo inteiro, escolha um clipe curto derivado da sample.

## Exportar

Pressione **Export processed video** para reiniciar o processamento desde o começo e gravar o canvas processado. O navegador baixa o resultado em WebM quando disponível, ou em outro formato oferecido pela implementação de `MediaRecorder`. O app tenta incluir o áudio usando Web Audio e, como alternativa, `captureStream()`; a exportação será silenciosa se o arquivo não tiver uma faixa de áudio decodificável. A exportação acontece em tempo real, então pode levar aproximadamente a duração do vídeo.

A exportação requer suporte a `MediaRecorder` e `captureStream()` no canvas. Recomendamos uma versão recente do Chrome, Edge ou Firefox. Dependendo das configurações de segurança, o navegador pode solicitar permissão ou bloquear o download.

## Configurações do efeito

- **Changes before lock**: quantidade de mudanças detectadas antes de um pixel ficar permanentemente colorido. O modo `Formula · video frame total` calcula o limite como `ceil(duração × FPS estimado × percentual / 100)`. O FPS é estimado pelas callbacks dos frames durante a reprodução, começando em 30 até haver uma amostra; por isso, o resultado é uma estimativa, não a contagem exata de frames do arquivo.
- **Random on lock**: atribui uma cor aleatória independente a cada pixel no instante em que ele trava. Essa opção substitui a cor escolhida, o gradiente temporal e a curva automática.
- **Source pixel color**: trava o pixel com a cor original do vídeo no frame em que ele alcança o limite. É uma opção exclusiva de `Random on lock`.
- **Change sensitivity**: score mínimo para contar uma mudança. O significado do valor depende do método de detecção selecionado.
- **Change detection**: `RGB sum` soma as diferenças absolutas dos três canais; `RGB distance` mede a distância euclidiana entre as cores; `Luminance` dá mais peso às mudanças percebidas nos canais verde e vermelho. São métricas alternativas, não algoritmos que possam ser ordenados como melhores em todos os vídeos.
- **Temporal gradient**: interpola entre as cores primária e secundária ao longo do vídeo. A curva pode ser `Linear`, `Logarithmic`, `Exponential`, `Ease in`, `Ease out` ou `Smooth step`.
- **Auto color curve**: percorre uma paleta de cores ao longo do vídeo e tem prioridade sobre o gradiente temporal. Escolha a paleta (`Spectrum`, `Ember`, `Ocean`, `Sunset`, `Forest` ou `Candy`) e uma curva de progressão. Curva e paleta também funcionam independentemente das cores escolhidas para o gradiente.
- **Processing load**: `Low` analisa um a cada quatro frames, `Default` um a cada dois e `Ultra` analisa todos os frames recebidos. Modos de menor carga usam menos CPU, mas podem alterar quando os pixels saturam; resultados não são diretamente comparáveis entre perfis. O navegador e o sistema operacional controlam o escalonamento da CPU: uma página não consegue reservar o computador inteiro nem limitar outras abas ou processos. `Ultra` pode deixar esta aba menos responsiva.
- **Pré-visualização ao vivo**: o vídeo toca no ritmo normal do arquivo, independentemente da análise dos pixels. O efeito é mostrado como uma camada transparente e pode ficar alguns frames atrás se o processamento não acompanhar; o playback não é pausado para esperar o efeito.
- **Volume**: começa em 100% quando não há preferência salva; o botão **Mute** alterna o silêncio e a última posição do volume é lembrada neste navegador.
