from flask import Flask, request
import os
import subprocess

app = Flask(__name__)

PROJECT = "supple-coral-476916-c8"
ZONE = "us-west1-c"
INSTANCE = "instance-20251102-164456"

@app.route("/", methods=["POST"])
def run_bot():
    # 1. Allumer la VM
    subprocess.run([
        "gcloud", "compute", "instances", "start",
        INSTANCE, "--zone", ZONE, "--project", PROJECT
    ], check=True)

    # 2. Attendre que la VM démarre (optionnel)
    import time
    time.sleep(90)  # Ajuste si nécessaire

    # 3. Exécuter le script sur la VM
    subprocess.run([
        "gcloud", "compute", "ssh",
        f"nathan@{INSTANCE}",
        "--zone", ZONE,
        "--project", PROJECT,
        "--command", "bash ~/bot-cycling/scripts/run_bot.sh"
    ], check=True)

    subprocess.run([
        "gcloud", "compute", "ssh",
        f"nathan@{INSTANCE}",
        "--zone", ZONE,
        "--project", PROJECT,
        "--command", f"BASE_URL='{os.environ['BASE_URL']}' USERNAME='{os.environ['USERNAME']}' PASSWORD='{os.environ['PASSWORD']}' TARGET_START='{os.environ['TARGET_START']}' TARGET_END='{os.environ['TARGET_END']}' TARGET_SUBJECT='{os.environ['TARGET_SUBJECT']}' TARGET_COACH='{os.environ['TARGET_COACH']}' PEOPLE='{os.environ['PEOPLE']}' bash ~/bot-cycling/scripts/run_bot.sh"
    ])

    # 4. Éteindre la VM
    subprocess.run([
        "gcloud", "compute", "instances", "stop",
        INSTANCE, "--zone", ZONE, "--project", PROJECT
    ], check=True)

    return "Bot exécuté et VM éteinte", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)