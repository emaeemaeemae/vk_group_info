from flask import Flask, render_template, request
import vk_group_info


app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        name = request.form['inputGroup']
        try:
            group_info = vk_group_info.get_info(name)
        except:
            group_info = 'Такой группы не существует'
        print(name)
        return render_template('succsess.html', a=group_info)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
