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
- **Change sensitivity**: diferença mínima total entre os canais vermelho, verde e azul para contar como mudança.
- **Temporal gradient**: interpola entre as cores primária e secundária ao longo do vídeo.
- **Auto color curve**: percorre um espectro de cores ao longo do tempo; tem prioridade sobre o gradiente temporal.
