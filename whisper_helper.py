import whisper
import os
from time import sleep, time

# This script was developed to assist non programmers researchers to use the OpenAI Whisper tool.
# This script is based on the CNRS article provided here : https://www.css.cnrs.fr/whisper-for-transcribing-interviews/
# Details about installation of Whisper can be found here : https://github.com/openai/whisper

# Main language used in prompts and prints is French as this script answer

# A function to timestamp the speech segments:
def convert(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def save_transcript(transcription, interview_transcript):
    # Save the transcript
    with open(interview_transcript, 'w', encoding='utf-8') as f:
        for segment in transcription["segments"]:
            start_time = convert(segment['start'])
            end_time = convert(segment['end'])
            f.write(f"{start_time} - {end_time}: {segment['text']}\n")


def model_choice(choice: int):
    if choice == 1:
        model = "large-v2"
        est = "Durée estimée: entre 7 min 30 et 8h36 "
    elif choice == 2:
        model = "medium"
        est = "Durée estimée: entre 4 min 30 et 3h49 "
    elif choice == 3:
        model = "small"
        est = "Durée estimée: entre 2 min 20 et 1h12 "
    elif choice == 4:
        model = "base"
        est = "Durée estimée: entre 2 min et 20 min "
    elif choice == 5:
        model = "tiny"
        est = "Durée estimée: entre 50 secondes et 9 min "

    return model, est


if __name__ == '__main__':
    print("-----------------------------------------------------")
    print("     Script de transcription via whisper (OpenAI)    ")
    print("-----------------------------------------------------")
    print("\n-----------------------------------------------------")
    print("Installation de Whisper : https://github.com/openai/whisper")
    print("CSS - CNRS | Conseils de prise en main, et quelques réflexions. (Yacine Chitour) https://www.css.cnrs.fr/fr/whisper-pour-retranscrire-des-entretiens/")
    print("-----------------------------------------------------")

    print(f"\nVous vous trouvez actuellement dans le dossier : {os.getcwd()}\n")

    interview = input(f"Veuillez saisir le nom du fichier audio contenant l'interview (exemple: audio.mp3):\n")
    interview_transcript = input(
        f"Veuillez saisir le nom du fichier texte qui contiendra le transcript de l'interview (exemple: interview.txt):\n")
    model = input(
        "Veuillez choisir le modèle whisper que vous souhaitez utiliser (saisir le chiffre correspondant):\n[1] - large-v2\n[2] - medium\n[3] - small\n[4] - base\n[5] - tiny\n")

    whisper_model, estimated_duration = model_choice(int(model))
    print(f"Modèle sélectionné: {whisper_model} \n")
    sleep(1)
    print(estimated_duration)
    print(
        "\nLes durées estimées ci-dessus sont données pour un processeur lent (Intel Core i5-6300U CPU @ 2.40GHz 2.50GHz) et un processeur rapide (Intel Core i7-8665U CPU @ 1.90GHz × 8)\n")
    sleep(1)
    # (Down)load the model
    print("\nChargement du modèle")
    model = whisper.load_model(whisper_model)
    # Transcription
    print("Transcription en cours")
    start = time()
    transcription = model.transcribe(interview)
    elapsed=time()-start
    print(f"Transcription effectuée en {round(elapsed/60,2)} minutes sur la base du modèle {whisper_model}")
    # Saving
    print("Enregistrement de la transcription...")
    save_transcript(transcription=transcription, interview_transcript=interview_transcript)
    print(f"... fichier {interview_transcript} enregistré !")
