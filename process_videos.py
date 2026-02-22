import os
import shutil
import subprocess
import sys
import time

# Fix encodage Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# --- Configuration ---
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR   = os.path.join(BASE_DIR, "A traiter")
OUTPUT_DIR  = os.path.join(BASE_DIR, "Vidéos")
POLL_DELAY  = 5  # secondes entre chaque vérification

VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv", ".webm", ".m4v"}

# ---------------------

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}")

def extract_frames(video_path, output_folder, video_name):
    first_frame = os.path.join(output_folder, f"{video_name}_first.jpg")
    last_frame  = os.path.join(output_folder, f"{video_name}_last.jpg")

    # 1ère frame
    cmd_first = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-vframes", "1",
        "-q:v", "1",
        first_frame
    ]

    result = subprocess.run(cmd_first, capture_output=True, text=True)
    if result.returncode != 0:
        log(f"  ⚠️  Erreur extraction première frame : {result.stderr[-200:]}")
        return False

    # Dernière frame — essai avec différents offsets
    for offset in ["-3", "-1", "-0.5"]:
        cmd_last = [
            "ffmpeg", "-y",
            "-sseof", offset,
            "-i", video_path,
            "-update", "1",
            "-q:v", "1",
            last_frame
        ]
        result = subprocess.run(cmd_last, capture_output=True, text=True)
        if result.returncode == 0 and os.path.getsize(last_frame) > 0:
            break
    else:
        log(f"  ⚠️  Erreur extraction dernière frame")
        return False

    # Copie de la 1ère frame comme miniature du dossier
    shutil.copy2(first_frame, os.path.join(output_folder, "folder.jpg"))

    return True

def process_video(video_path):
    video_filename = os.path.basename(video_path)
    video_name     = os.path.splitext(video_filename)[0]

    log(f"  Traitement : {video_filename}")

    # Créer le dossier de destination
    dest_folder = os.path.join(OUTPUT_DIR, video_name)
    os.makedirs(dest_folder, exist_ok=True)

    # Extraire les frames
    success = extract_frames(video_path, dest_folder, video_name)
    if not success:
        log(f"  ❌ Échec pour {video_filename}")
        return

    # Déplacer la vidéo dans son dossier
    dest_video = os.path.join(dest_folder, video_filename)
    try:
        shutil.move(video_path, dest_video)
    except PermissionError:
        log(f"  ⚠️  Fichier verrouillé, nouvelle tentative au prochain cycle...")
        return

    log(f"  ✅ Terminé → Vidéos/{video_name}/")

def scan_and_process():
    entries = os.listdir(INPUT_DIR)
    videos  = [
        f for f in entries
        if os.path.splitext(f)[1].lower() in VIDEO_EXTENSIONS
        and os.path.isfile(os.path.join(INPUT_DIR, f))
        and os.path.getsize(os.path.join(INPUT_DIR, f)) > 0
    ]

    if not videos:
        return

    log(f"📂 {len(videos)} vidéo(s) détectée(s)")
    for video_file in videos:
        process_video(os.path.join(INPUT_DIR, video_file))

def main():
    import sys
    once = "--once" in sys.argv

    os.makedirs(INPUT_DIR,  exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    if once:
        log("⚡ Mode one-shot — traitement en cours...")
        log(f"   Dossier source : {INPUT_DIR}")
        log(f"   Dossier sortie : {OUTPUT_DIR}\n")
        scan_and_process()
        log("✅ Terminé.")
    else:
        log("🚀 Démarrage — surveillance de 'A traiter' (Ctrl+C pour arrêter)")
        log(f"   Dossier source  : {INPUT_DIR}")
        log(f"   Dossier sortie  : {OUTPUT_DIR}")
        log(f"   Vérification toutes les {POLL_DELAY}s\n")
        try:
            while True:
                scan_and_process()
                time.sleep(POLL_DELAY)
        except KeyboardInterrupt:
            log("\n👋 Arrêt du script.")

if __name__ == "__main__":
    main()
