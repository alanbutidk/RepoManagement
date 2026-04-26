#include "MiniAudioWrapper.h"
#include <stdio.h>

int main(int argc, char** argv) {
    if (argc < 2) {
        printf("Usage: %s <filename>\n", argv[0]);
        return -1;
    }

    AudioWrap* cac = CreateAudioContext();
    if (cac == NULL) return -2;

    ma_result result = ma_decoder_init_file(argv[1], NULL, cac->aDecode);
    if (result != MA_SUCCESS) {
        printf("Could not load file: %s\n", argv[1]);
        killAudio(cac);
        return -3;
    }

    ma_device_config config = ma_device_config_init(ma_device_type_playback);
    config.playback.format   = cac->aDecode->outputFormat;
    config.playback.channels = cac->aDecode->outputChannels;
    config.sampleRate        = cac->aDecode->outputSampleRate;
    config.dataCallback      = aDataCallback;
    config.pUserData         = cac;

    if (ma_device_init(NULL, &config, cac->aDevice) != MA_SUCCESS) {
        printf("Failed to initialize playback device.\n");
        killAudio(cac);
        return -4;
    }

    if (ma_device_start(cac->aDevice) != MA_SUCCESS) {
        printf("Failed to start device.\n");
        killAudio(cac);
        return -5;
    }

    printf("Playing %s... Press Enter to quit.\n", argv[1]);
    getchar();

    killAudio(cac);
    return 0;
}
