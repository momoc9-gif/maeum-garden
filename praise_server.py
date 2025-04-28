from flask import Flask, request, render_template
import json
import os

app = Flask(__name__)

# 대화 수 로딩
if os.path.exists("message_count.json"):
    with open("message_count.json", "r") as f:
        message_count = json.load(f)["count"]
else:
    message_count = 0

def get_flower_stage(count):
    if count < 2000:
        return "🌱", "#8B4513"  # 씨앗, 짙은 갈색
    elif count < 4000:
        return "🌿", "#7CFC00"  # 새싹, 연두색
    elif count < 6000:
        return "🌳", "#228B22"  # 줄기, 초록색
    elif count < 8000:
        return "🌼", "#FFFACD"  # 꽃봉오리, 연한 노랑
    elif count < 10000:
        return "🌼", "#FFB6C1"  # 거의 핀 꽃, 핑크
    else:
        return "🌸", "#FFC0CB"  # 만개, 분홍색

@app.route('/', methods=['GET', 'POST'])
def home():
    global message_count

    if request.method == 'POST':
        user_message = request.form['message']
        message_count += 1

        # 저장
        with open("message_count.json", "w") as f:
            json.dump({"count": message_count}, f)

    flower_emoji, background_color = get_flower_stage(message_count)
    energy_percent = min(message_count / 100, 100)  # 0~100%까지만 표시

    return render_template(
        "index.html",
        flower_emoji=flower_emoji,
        background_color=background_color,
        energy_percent=energy_percent,
        message_count=message_count
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
