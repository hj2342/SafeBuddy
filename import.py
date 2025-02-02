import assemblyai as aai

aai.settings.api_key = "072d9985d282486892e8cf1120ba1f65" 

transcriber = aai.Transcriber()
audio_file = "./help.ogg"

transcript1 = transcriber.transcribe(audio_file)

if transcript1.error:
   print(transcript1.error)

print(transcript1.text)
if "help" in transcript1.text.lower() :
   print("Emergency")
   exit(1)

