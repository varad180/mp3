import streamlit as st
from pydub import AudioSegment
import zipfile
import os
import shutil
import tempfile

st.title("🎵 Bulk Audio Converter: ZIP of MP4/M4A → MP3")

uploaded_zip = st.file_uploader("📁 Upload a ZIP file containing .m4a or .mp4 files", type="zip")

if uploaded_zip is not None:
    with tempfile.TemporaryDirectory() as tmpdir:
        zip_input_path = os.path.join(tmpdir, "input.zip")
        extract_path = os.path.join(tmpdir, "extracted")
        converted_path = os.path.join(tmpdir, "converted")
        output_zip_path = os.path.join(tmpdir, "converted_mp3s.zip")

        # Save and extract uploaded ZIP
        with open(zip_input_path, "wb") as f:
            f.write(uploaded_zip.read())
        with zipfile.ZipFile(zip_input_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)

        # Convert audio files
        os.makedirs(converted_path, exist_ok=True)
        mp3_files = []

        for root, _, files in os.walk(extract_path):
            for file in files:
                if file.lower().endswith((".m4a", ".mp4")):
                    input_path = os.path.join(root, file)
                    output_filename = os.path.splitext(file)[0] + ".mp3"
                    output_path = os.path.join(converted_path, output_filename)

                    try:
                        audio = AudioSegment.from_file(input_path)
                        audio.export(output_path, format="mp3")
                        mp3_files.append(output_path)
                    except Exception as e:
                        st.warning(f"Failed to convert {file}: {e}")

        # Zip all MP3s into one file
        if mp3_files:
            with zipfile.ZipFile(output_zip_path, "w") as zipf:
                for file_path in mp3_files:
                    arcname = os.path.basename(file_path)
                    zipf.write(file_path, arcname=arcname)

            st.success("✅ Conversion complete!")
            with open(output_zip_path, "rb") as f:
                st.download_button(
                    label="📦 Download All Converted MP3s (ZIP)",
                    data=f,
                    file_name="converted_mp3s.zip",
                    mime="application/zip"
                )
        else:
            st.error("No valid audio files were found to convert.")
