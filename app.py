from flask import Flask, request, render_template ,jsonify
import PyPDF2 , mammoth 

app = Flask(__name__,template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST', 'GET'])
def upload():   
        def extract_text_from_pdf(file):
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text

        def extract_text_from_word(file):
            result = mammoth.extract_raw_text(file)
            return result.value

        def submit_conversation(text, part, filename):
            print("Submitting part %d" % part)
            print(filename)

        file = request.files['file']
        text = ''
        if file.content_type == "application/pdf":
            text = extract_text_from_pdf(file)
        elif file.content_type in ["application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
            text = extract_text_from_word(file)
        else:
            text = file.read().decode('utf-8')

        chunk_size = int(request.form['chunkSize'])
        num_chunks = (len(text) + chunk_size - 1) // chunk_size

        for i in range(num_chunks):
            chunk = text[i * chunk_size : (i + 1) * chunk_size]
            submit_conversation(chunk, i + 1, file.filename)

        # save the text to a file json
        with open('text.json', 'w',encoding='utf-8') as f:
            f.write(text)
        return jsonify({"text": text})
    

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
