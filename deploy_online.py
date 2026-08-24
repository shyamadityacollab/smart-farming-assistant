import os
import zipfile
import urllib.request
import json
import io

DIRECTORY = os.path.dirname(os.path.abspath(__file__))

def create_zip():
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk(DIRECTORY):
            # Skip python scripts and temporary files
            if '.git' in root or '__pycache__' in root:
                continue
            for file in files:
                if file.endswith(('.py', '.bat', '.log', '.txt')):
                    continue
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, DIRECTORY)
                zip_file.write(file_path, rel_path)
    zip_buffer.seek(0)
    return zip_buffer.getvalue()

def deploy_netlify():
    print("Packing website files into bundle...")
    zip_data = create_zip()
    print(f"Bundle size: {len(zip_data)} bytes")
    
    print("Uploading to global cloud hosting (Netlify API)...")
    url = "https://api.netlify.com/api/v1/sites"
    req = urllib.request.Request(
        url,
        data=zip_data,
        headers={"Content-Type": "application/zip"}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            site_url = res_data.get('ssl_url') or res_data.get('url')
            print(f"\n=======================================================")
            print(f"🎉 WEBSITE IS LIVE ON THE INTERNET!")
            print(f"🌐 Public URL: {site_url}")
            print(f"=======================================================\n")
            with open(os.path.join(DIRECTORY, "public_url.txt"), "w") as f:
                f.write(site_url)
            return site_url
    except Exception as e:
        print(f"Netlify anonymous deploy response: {e}")
        return None

if __name__ == "__main__":
    deploy_netlify()
