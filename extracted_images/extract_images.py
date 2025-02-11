from pdf2image import convert_from_path
import os

# Path to the uploaded PDF file
pdf_path = "/Users/kishansukhadia/ocr_project/oaksol_Intern_OCR_Assignment.pdf"

# Output directory for extracted images
output_dir = "/Users/kishansukhadia/ocr_project/extracted_images"

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Extract images from PDF
images = convert_from_path(pdf_path)

# Save extracted images
for i, img in enumerate(images):
    image_path = os.path.join(output_dir, f"sample_form_{i+1}.jpg")
    img.save(image_path, "JPEG")
    print(f"Saved: {image_path}")

print("\n✅ Image extraction complete! Check the 'extracted_images' folder.")
