# INPUT : hardcoded audio file path
# OUTPUT : classification for "potential emergency" or "normal"


'''
requirements.txt:

assemblyai
together
torch
torchaudio
soundfile
requests
'''


import assemblyai as aai
import requests
from together import Together

# Set API Keys
ASSEMBLYAI_API_KEY = "072d9985d282486892e8cf1120ba1f65"
TOGETHER_API_KEY = "809aa734077fe63dd547f1512642e26704101bcb5c93d7bb17f40306a00bd2fa"

# ✅ Set AssemblyAI API Key
aai.settings.api_key = ASSEMBLYAI_API_KEY

# ✅ Initialize Together AI client
client = Together(api_key=TOGETHER_API_KEY)
transcriber = aai.Transcriber()

# ✅ Directly use the local audio file
audio_file_path = "help.wav"  # Change to your actual file

try:
    # ✅ Transcribe audio with sentiment analysis enabled
    config = aai.TranscriptionConfig(sentiment_analysis=True)  # ❌ Removed 'emotion_detection'
    transcript = transcriber.transcribe(audio_file_path, config=config)

    if transcript.error:
        print("Error:", transcript.error)
    else:
        # ✅ Extract transcribed text
        transcribed_text = transcript.text.strip()

        # ✅ Extract sentiment analysis results
        sentiment_scores = [s.sentiment for s in transcript.sentiment_analysis]

        # ✅ Determine sentiment category
        negative_count = sentiment_scores.count("NEGATIVE")
        positive_count = sentiment_scores.count("POSITIVE")
        neutral_count = sentiment_scores.count("NEUTRAL")

        if negative_count > positive_count:
            sentiment_category = "NEGATIVE"
        elif positive_count > negative_count:
            sentiment_category = "POSITIVE"
        else:
            sentiment_category = "NEUTRAL"

        #print("Transcribed Text:", transcribed_text)
        #print("Sentiment Category:", sentiment_category)

        # ✅ Send transcribed text + sentiment to Together AI LLM
        prompt = f"""
        A person just said this: "{transcribed_text}".
        Detected sentiment: {sentiment_category}.
        Given both the speech content and emotional tone, does this indicate a potential emergency?
        Respond only with 'normal' or 'potential emergency'.
        """

        try:
            response = client.chat.completions.create(
                model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            llm_classification = response.choices[0].message.content.strip()
        except Exception as e:
            print("Error with LLM classification:", str(e))
            llm_classification = "normal"

        # ✅ Final Decision: If LLM OR strong negative sentiment, classify as emergency
        if llm_classification == "potential emergency" or negative_count > 1:
            print("potential emergency")
        else:
            print("normal")

except Exception as e:
    print("Error processing audio:", str(e))
