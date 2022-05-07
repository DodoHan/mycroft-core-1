# Copyright 2022 Shore.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""Microsoft tts"""

from mycroft.util.log import LOG

from .tts import TTS, TTSValidator
import azure.cognitiveservices.speech as speechsdk


# https://docs.microsoft.com/zh-cn/azure/cognitive-services/speech-service/language-support?tabs=speechtotext#text-to-speech
class MicrosoftTTS(TTS):

    def __init__(self, lang, config):
        super(MicrosoftTTS, self).__init__(lang, config,
                                           MicrosoftValidator(self), 'wav')

        self.speech_config = speechsdk.SpeechConfig(
            subscription=config['credential']['key'],
            region=config['credential']['region'])
        # Sets the synthesis voice name.
        # e.g. "Microsoft Server Speech Text to Speech Voice (en-US, ChristopherNeural)".
        # The full list of supported voices can be found here:
        # https://aka.ms/csspeech/voicenames
        # And, you can try get_voices_async method to get all available voices (see speech_synthesis_get_available_voices() sample below).
        self.speech_config.speech_synthesis_voice_name = config['voice_name']
        self.speech_config.speech_synthesis_language = config['lang']
        LOG.info("voice_name = " +
                 self.speech_config.speech_synthesis_voice_name)
        LOG.info("lang = " + self.speech_config.speech_synthesis_language)

    def get_tts(self, sentence, wav_file):
        file_config = speechsdk.audio.AudioOutputConfig(filename=wav_file)
        speech_synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=self.speech_config, audio_config=file_config)
        LOG.info(
            '[Flow Learning] in mycroft.tts.baidu_tts.py.MicrosoftTTS.get_tts, after calling TTS api, wav_file will ==' + str(wav_file))
        result = speech_synthesizer.speak_text_async(sentence).get()
        # Check result
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            LOG.info(
                "[Flow Learning] Speech synthesized for text [{}], and the audio was saved to [{}]"
                .format(sentence, wav_file))
            return (wav_file, None)
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            LOG.info("[Flow Learning]  Speech synthesis canceled: {}".format(
                cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                LOG.error("[Flow Learning]  Error details: {}".format(
                    cancellation_details.error_details))


class MicrosoftValidator(TTSValidator):
    """Do no tests."""

    def __init__(self, tts):
        super().__init__(tts)

    def validate_lang(self):
        pass

    def validate_connection(self):
        pass

    def get_tts_class(self):
        return MicrosoftTTS
