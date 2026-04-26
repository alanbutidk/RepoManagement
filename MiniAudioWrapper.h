#ifndef AUDIO_WRAP_H
#define AUDIO_WRAP_H

#define MINIAUDIO_IMPLEMENTATION
#include "miniaudio.h"
#include <stdlib.h>

typedef struct {
	ma_decoder* aDecode;
	double volume;
	ma_device* aDevice;
	ma_engine* aEngine;
	ma_bool32 isPlay;
} AudioWrap;

AudioWrap* CreateAudioContext() {
	AudioWrap* cac = malloc(sizeof(AudioWrap));
	cac->aDevice = malloc(sizeof(ma_device));
	cac->aEngine = malloc(sizeof(ma_engine));
	cac->aDecode = malloc(sizeof(ma_decoder));

	cac->isPlay = MA_FALSE;
	cac->volume = 1.0;
	return cac;
}

void killAudio(AudioWrap* cac) {
	if (cac) {
		ma_device_uninit(cac->aDevice);
		free(cac->aDevice);
		free(cac->aEngine);
		free(cac->aDecode);
		free(cac);
	}
}

void aDataCallback(ma_device* aDevice, void* aOutput, const void* aInput, ma_uint32 frameCount) {
	AudioWrap* aData = (AudioWrap*)aDevice->pUserData;
	if (aData != NULL && aData->aDecode != NULL) {
		ma_decoder_read_pcm_frames(aData->aDecode, aOutput, frameCount, NULL);
	}
}

#endif
