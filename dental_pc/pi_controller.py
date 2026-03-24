"""
pi_controller.py  ──  SSH into Pi → trigger libcamera-still → SFTP download
No OpenCV. No Python on Pi. Just a shell command + file transfer.
"""

import os
import paramiko
import config


def capture_and_download() -> bool:
    """
    1. SSH into the Raspberry Pi.
    2. Run libcamera-still to capture a JPEG.
    3. SFTP the file back to the laptop.
    Returns True on success, False on any error.
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        print(f"🔌 Connecting to Pi at {config.PI_HOST} …")
        ssh.connect(
            config.PI_HOST,
            username=config.PI_USER,
            password=config.PI_PASSWORD,
            timeout=10,
        )
        print("✅ SSH connection established.")

        # ── Step 1: Capture image on Pi ───────────────────────────────────────
        remote_path = '/home/sam/captured_teeth.jpg'
        cmd = f"rpicam-still -o {remote_path} --timeout 3000 --nopreview"
        print(f"📸 Running on Pi: {cmd}")

        _, stdout, stderr = ssh.exec_command(cmd)
        exit_status = stdout.channel.recv_exit_status()   # blocks until done

        if exit_status != 0:
            err = stderr.read().decode().strip()
            print(f"❌ Camera error (exit {exit_status}): {err}")
            ssh.close()
            return False

        print("✅ Image captured on Pi.")

        # ── Step 2: Download via SFTP ─────────────────────────────────────────
        os.makedirs(config.DATA_DIR, exist_ok=True)
        sftp = ssh.open_sftp()

        print(f"⬇️  Downloading {remote_path} → {config.CAPTURED_IMAGE} …")
        sftp.get(remote_path, config.CAPTURED_IMAGE)
        print(f"✅ Image saved locally: {config.CAPTURED_IMAGE}")

        sftp.close()
        ssh.close()
        return True

    except paramiko.AuthenticationException:
        print("❌ Authentication failed. Check PI_USER / PI_PASSWORD in .env")
    except paramiko.ssh_exception.NoValidConnectionsError:
        print(f"❌ Cannot reach Pi at {config.PI_HOST}. Are both on the same Wi-Fi?")
    except Exception as exc:
        print(f"❌ Unexpected error: {exc}")

    return False
