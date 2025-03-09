import json
import logging
import base64
from rembg import remove
from PIL import Image
from io import BytesIO


logger = logging.getLogger()
logger.setLevel(logging.INFO)


# init code
print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

def lambda_handler(event, context):
    try:
        # API Gateway'den gelen base64 encode edilmiş görüntüyü al
        if 'body' not in event:
            return {
                'statusCode': 400,
                'body': json.dumps({'error1': 'Görüntü verisi bulunamadı'})
            }  
        # Multipart form-data'dan görüntüyü çıkar
        body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
        if 'image' not in body:
            return {
                'statusCode': 400,
                'body': json.dumps({'error2': 'Görüntü verisi bulunamadı'})
            }
        # Base64 encoded image'ı decode et
        image_data = base64.b64decode(body['image'])
        # Görüntüyü PIL Image nesnesine dönüştür
        input_image = Image.open(BytesIO(image_data))
        # Arka planı kaldır
        output_image = remove(input_image, alpha_matting = False)
        # Çıktıyı byte dizisine dönüştür
        img_io = BytesIO()
        output_image.save(img_io, 'PNG')
        img_io.seek(0)
        # Benzersiz dosya adı oluştur
        new_filename = "nobg.png"
            
        # Base64 encoded response döndür
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'filename': new_filename,
                'image': base64.b64encode(img_io.getvalue()).decode('utf-8')
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }