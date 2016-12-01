#!/usr/bin/python3

# prerequisite apt-get install python3-pyaudio

import waggle.logging
import waggle.pipeline
import time
import pyaudio
import wave

def get_mic_name(path, default='USB'):
    name = default
    if os.isfile(path):
        try:
            with open(path, 'r') as f:
                data = f.read()
                if data != '':
                    name = data
        except:
            pass
    return name

THE_DEVICE_NAME = get_mic_name('/etc/waggle/waggle_name_microphone', default='USB')

class AudioRecoderPlugin(waggle.pipeline.Plugin):

	plugin_name = 'audio_recoder'
	plugin_version = '1'

	def run(self):
		logging = waggle.logging.getLogger('audio_recoder')
		# The device should be found using other way, this is hardcorded way
		='waggle_microphone'

		FORMAT = pyaudio.paInt16
		CHANNELS = 1
		RATE = 44100
		CHUNK = 8192
		RECORD_SECONDS = 5
		WAVE_OUTPUT_FILENAME = "file.wav"

		pa = pyaudio.PyAudio()

		count = pa.get_device_count()
		idx = -1

		for i in range(count):
			info = pa.get_device_info_by_index(i)
			if THE_DEVICE_NAME in info['name']:
				idx = i

		if idx == -1:
			logging.error("No input audio found")
			return

		try:
			# start Recording
			stream = pa.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK, input_device_index=idx)
			print("recording...")
			frames = []
			
			for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
				data = stream.read(CHUNK)
				frames.append(data)
			print("finished recording")
			
			
			# stop Recording
			stream.stop_stream()
			stream.close()

			waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
			waveFile.setnchannels(CHANNELS)
			waveFile.setsampwidth(pa.get_sample_size(FORMAT))
			waveFile.setframerate(RATE)
			waveFile.writeframes(b''.join(frames))
			waveFile.close()

			self.send_file(sensor='audio_raw', filepath=WAVE_OUTPUT_FILENAME)
		except Exception as e:
			print("Error occurred during record: %s" % str(e))
		pa.terminate()

if __name__ == '__main__':
    #plugin = FaceDetectionPlugin.fileTransferConfig()
    plugin = AudioRecoderPlugin()
    plugin.add_handler(waggle.pipeline.RabbitMQHandler('amqp://localhost', dest_queue='images'))
    plugin.add_file_handler(waggle.pipeline.RabbitMQHandler('amqp://localhost', dest_queue='images'))
    plugin.run()
