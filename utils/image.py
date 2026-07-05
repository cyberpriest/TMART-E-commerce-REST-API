from PIL import Image 
from fastapi import HTTPException,UploadFile
import io ,secrets
from pathlib import Path 

# -------- my guidelines ----------

# 1. check file type - is it jpeg/png/webp?
# 2. check file size - under 2MB?
# 3. open with pillow
# 4. resize if too wide
# 5. save as compressed jpeg


_base_dir = Path(__file__).resolve().parent
UPLOAD_DIR = _base_dir / 'static'
UPLOAD_DIR.mkdir(parents=True,exist_ok=True)


file_types = ["image/jpeg", "image/png", "image/webp"]
MAX_MB_SIZE = 2


def compress_image(file:UploadFile,max_width:int = 800,q:int = 80 ):
    


    # 1. check file type - is it jpeg/png/webp?

    if file.content_type not in file_types :
        raise HTTPException(status_code=400,detail=" must be  jpeg/png/webp ")
    

    image_content = file.file.read()

    if len(image_content) > MAX_MB_SIZE * 1024 * 1024:
        raise HTTPException(status_code=400,detail=f"image must be under {MAX_MB_SIZE} MB")
    
    image = Image.open(io.BytesIO(image_content))

    if image in ('RGBA','P'):
        image = image.convert('RGB')

    if image.width > max_width:
        ratio = max_width / image.width 
        new_height = int(image.height * ratio )
        image.resize((max_width,new_height))
    filename = f"{secrets.token_hex(8)}.jpg"
    filepath = f'{UPLOAD_DIR}/{filename}'


    image.save(filepath, format="JPEG", quality=q, optimize=True)
    return filepath
    


    

