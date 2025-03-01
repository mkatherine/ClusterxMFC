from flask import Flask, send_file

app = Flask(__name__)

@app.route('/download')
def download_file():
    file_path = "/Users/katherinetedjokusumo/XCode/ClusterxMFC_Playground/SaveData/SaveData-TestFile.txt"  # Change this to your actual file
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host="192.168.1.158", port=5001)

#192.168.1.158 IP address of mycafe
#192.168.0.156 IP address of TPlink
