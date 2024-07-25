from flask import Flask, request, jsonify
import CaptchaCracker as cc

app = Flask(__name__)

# 학습된 모델의 가중치 파일 경로
weights_path = "./model/weights.h5"
# 모델을 적용할 이미지 데이터 크기
img_width = 120
img_height = 40
max_length = 6
characters = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
model_instance = cc.ApplyModel(weights_path, img_width, img_height, max_length, characters)

def predict_captcha(image_path, model_instance):
    return model_instance.predict(image_path)

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    
    image_file = request.files['image']
    image_path = "./captcha_image.png"
    image_file.save(image_path)
    
    captcha_text = predict_captcha(image_path, model_instance)
    
    return jsonify({"captcha_text": captcha_text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
