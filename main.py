from flask import Flask, request
import os
import time
import subprocess

app = Flask(__name__)

PROJECT = "supple-coral-476916-c8"
ZONE = "us-west1-c"
INSTANCE = "instance-20251102-164456"

@app.route("/", methods=["POST"])
def run_bot():

    # 1. start VM
    subprocess.run([
        "gcloud", "compute", "instances", "start",
        INSTANCE, "--zone", ZONE, "--project", PROJECT
    ], check=True)

    # 2. on laisse la VM booter + exécuter son startup script
    time.sleep(300)

    # 3. (NE SURTOUT PAS SSH)
    # ton run_bot.sh fera shutdown lui même

    return "OK déclenché", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
