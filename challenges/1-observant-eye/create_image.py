from PIL import Image
from PIL.ExifTags import TAGS
import os

# Create a simple image or use existing one
img = Image.new('RGB', (400, 300), color='lightblue')

# Add some text to make it look like a real image
from PIL import ImageDraw, ImageFont
draw = ImageDraw.Draw(img)
# You can skip the text part if you want a plain image

# Save with EXIF metadata
img.save('secret-image.jpg', 
         quality=95,
         exif=img.getexif())  # This preserves basic EXIF

print("Image created: secret-image.jpg")
print("Now manually add metadata via:")
print("Windows: Right-click → Properties → Details")
print("Add to 'Subject' or 'Comments' field: CRYPTON{m3t4d4t4_1s_c00l}")
