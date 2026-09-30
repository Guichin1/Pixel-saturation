# Pixel Saturation

A standalone, browser-based video effect. Pixels are tracked across frames and lock into a selected color after changing a chosen number of times.

## Run

Open `Pixel Saturation - Video Decay.html` in a recent desktop browser. No build step, server, or external dependencies are required.

Choose a video, adjust the lock colors and effect settings, then press **Play** to preview. **Reset effect** clears the accumulated pixel state and returns to the beginning.

## Video formats

The file picker accepts common video files, including MP4, M4V, WebM, Ogg, MOV, MKV, and AVI. Accepted extensions do not guarantee playback: decoding depends on the codecs built into the browser and operating system. H.264 MP4 and VP8/VP9 WebM are widely supported; MOV, MKV, AVI, and other codecs vary by browser.

## Export

Press **Export processed video** to restart processing from the beginning and record the rendered canvas. The browser downloads the result as WebM when supported, or another format exposed by its MediaRecorder implementation. Audio is included only when the browser exposes the source audio track to `captureStream()`; otherwise the exported video is silent. Export runs in real time, so a video takes approximately its playback duration to process.

Processed-video export requires `MediaRecorder` and canvas `captureStream()` support. A recent version of Chrome, Edge, or Firefox is recommended. The browser may ask for permission or block downloads depending on its security settings.

## Effect settings

- **Changes before lock**: Number of detected pixel changes before the pixel is permanently colored.
- **Change sensitivity**: Minimum sum of the red, green, and blue channel differences needed to count as a change.
- **Temporal gradient**: Interpolate between the primary and end colors over the video's duration.
- **Auto color curve**: Cycle through a spectrum of colors over time; takes priority over the temporal gradient.