import os
import subprocess


def sign_apk(apk_path):
    # Determine the directory in which this script is located
    dir_of_this_script = os.path.dirname(os.path.abspath(__file__))

    # Construct the path to the uber-apk-signer JAR file
    jar_path = os.path.join(dir_of_this_script, "uber-apk-signer-1.3.0.jar")

    # Construct the command to run
    command = ["java", "-jar", jar_path, "--apks", apk_path]

    try:
        subprocess.run(command, check=True)
        print(f"APK signed successfully: {apk_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error signing APK: {e}")
    except FileNotFoundError:
        print("Java is not installed or not found. Please install Java to use this tool.")


# Example usage
if __name__ == "__main__":
    apk_to_sign = "path/to/your.apk"
    sign_apk(apk_to_sign)
