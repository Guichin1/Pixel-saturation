# Pixel Saturation

Um efeito de vídeo que roda diretamente no navegador. O app acompanha os pixels entre os quadros e fixa cada um em uma cor escolhida depois que ele muda um número definido de vezes.

## Executar localmente

Abra [`index.html`](index.html) em uma versão recente de um navegador para desktop. Não é necessário instalar dependências, iniciar um servidor ou executar um processo de build.

Escolha um vídeo, ajuste as cores e os parâmetros do efeito e pressione **Play** para pré-visualizar. **Reset effect** limpa o estado acumulado dos pixels e volta ao início.

## Formatos de vídeo

O seletor aceita formatos comuns, incluindo MP4, M4V, WebM, Ogg, MOV, MKV e AVI. A extensão, por si só, não garante a reprodução: a decodificação depende dos codecs disponíveis no navegador e no sistema operacional. MP4 com H.264 e WebM com VP8/VP9 têm ampla compatibilidade; o suporte a MOV, MKV, AVI e outros codecs varia conforme o navegador.

## Exportar

Pressione **Export processed video** para reiniciar o processamento desde o começo e gravar o canvas processado. O navegador baixa o resultado em WebM quando disponível, ou em outro formato oferecido pela implementação de `MediaRecorder`. O áudio só será incluído se o navegador disponibilizar a faixa original por `captureStream()`; caso contrário, o vídeo exportado será silencioso. A exportação acontece em tempo real, então pode levar aproximadamente a duração do vídeo.

A exportação requer suporte a `MediaRecorder` e `captureStream()` no canvas. Recomendamos uma versão recente do Chrome, Edge ou Firefox. Dependendo das configurações de segurança, o navegador pode solicitar permissão ou bloquear o download.

## Configurações do efeito

- **Changes before lock**: quantidade de mudanças detectadas antes de um pixel ficar permanentemente colorido.
- **Change sensitivity**: score mínimo para contar uma mudança. O significado do valor depende do método de detecção selecionado.
- **Change detection**: `RGB sum` soma as diferenças absolutas dos três canais; `RGB distance` mede a distância euclidiana entre as cores; `Luminance` dá mais peso às mudanças percebidas nos canais verde e vermelho. São métricas alternativas, não algoritmos que possam ser ordenados como melhores em todos os vídeos.
- **Temporal gradient**: interpola entre as cores primária e secundária ao longo do vídeo. A curva pode ser `Linear`, `Logarithmic`, `Exponential`, `Ease in`, `Ease out` ou `Smooth step`.
- **Auto color curve**: percorre uma paleta de cores ao longo do vídeo e tem prioridade sobre o gradiente temporal. Escolha a paleta (`Spectrum`, `Ember`, `Ocean`, `Sunset`, `Forest` ou `Candy`) e uma curva de progressão. Curva e paleta também funcionam independentemente das cores escolhidas para o gradiente.
- **Processing load**: `Low` analisa um a cada quatro frames, `Default` um a cada dois e `Ultra` analisa todos os frames recebidos. Modos de menor carga usam menos CPU, mas podem alterar quando os pixels saturam; resultados não são diretamente comparáveis entre perfis. O navegador e o sistema operacional controlam o escalonamento da CPU: uma página não consegue reservar o computador inteiro nem limitar outras abas ou processos. `Ultra` pode deixar esta aba menos responsiva.
- **Volume**: a última configuração é lembrada neste navegador por meio do armazenamento local.
