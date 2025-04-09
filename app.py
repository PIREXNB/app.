from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>إرسال لايكات فري فاير</title>
    <style>
        body { font-family: Arial; text-align: center; margin-top: 50px; background-color: #f5f5f5; }
        input, button { padding: 10px; margin: 5px; font-size: 16px; }
        .result { margin-top: 20px; background: #fff; display: inline-block; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px #ccc; text-align: left; }
    </style>
</head>
<body>
    <h2>موقع إرسال لايكات فري فاير</h2>
    <form method="post">
        <input type="text" name="player_id" placeholder="أدخل معرف اللاعب" required>
        <button type="submit">إرسال لايكات</button>
    </form>

    {% if data %}
    <div class="result">
        <strong>الاسم:</strong> {{ data.name }}<br>
        <strong>المعرف:</strong> {{ data.uid }}<br>
        <strong>المنطقة:</strong> {{ data.region }}<br>
        <strong>المستوى:</strong> {{ data.level }}<br>
        <strong>اللايكات قبل:</strong> {{ data.likes_before }}<br>
        <strong>اللايكات المضافة:</strong> {{ data.likes_added }}<br>
        <strong>اللايكات بعد:</strong> {{ data.likes_after }}<br>
        <strong>لايكات فشلت:</strong> {{ data.failed_likes }}
    </div>
    {% elif message %}
    <div class="result" style="color: red;">{{ message }}</div>
    {% endif %}
</body>
</html>
"""

API_TEMPLATE = "http://207.180.223.38:5008/like?uid={}&key=brad&count=100"

@app.route('/', methods=['GET', 'POST'])
def home():
    data = None
    message = ''
    if request.method == 'POST':
        player_id = request.form['player_id']
        try:
            response = requests.get(API_TEMPLATE.format(player_id))
            if response.status_code == 200:
                json_data = response.json()
                if "uid" in json_data:
                    data = json_data
                else:
                    message = "لم يتم العثور على البيانات المطلوبة."
            else:
                message = f"فشل الاتصال. كود الاستجابة: {response.status_code}"
        except Exception as e:
            message = f"حدث خطأ أثناء الاتصال: {str(e)}"
    return render_template_string(HTML_PAGE, data=data, message=message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
