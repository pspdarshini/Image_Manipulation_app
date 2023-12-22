import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter

def main():
    st.title("Image Manipulation App")

    # Step 1: Upload Image
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        # Step 2: Display the original image
        st.image(uploaded_image, caption="Original Image", use_column_width=True)

        # Step 3: Image Operations
        st.subheader("Image Operations")
        operation = st.selectbox("Select an operation", ["Enhance", "Filter", "Resize", "Crop"])

        if operation == "Enhance":
            enhance_option = st.selectbox("Select enhancement type", ["Brightness", "Contrast", "Sharpness"])
            enhancement_factor = st.slider(f"{enhance_option} Factor", 0.1, 2.0, 1.0)
            enhanced_image = enhance_image(uploaded_image, enhance_option, enhancement_factor)
            st.image(enhanced_image, caption=f"Enhanced Image ({enhance_option} x {enhancement_factor})", use_column_width=True)

        elif operation == "Filter":
            filter_type = st.selectbox("Select a filter", ["Blur", "Contour", "Detail", "Edge Enhance"])
            filtered_image = apply_filter(uploaded_image, filter_type)
            st.image(filtered_image, caption=f"{filter_type} Filtered Image", use_column_width=True)

        elif operation == "Resize":
            new_size = st.slider("Select a size", 10, 1000, 300)
            resized_image = resize_image(uploaded_image, new_size)
            st.image(resized_image, caption=f"Resized Image ({new_size}px)", use_column_width=True)

        elif operation == "Crop":
            crop_coords = st.text_input("Enter crop coordinates (left, top, right, bottom)", "0, 0, 200, 200")
            cropped_image = crop_image(uploaded_image, crop_coords)
            st.image(cropped_image, caption="Cropped Image", use_column_width=True)

        # Step 4: Download the updated image
        download_button(uploaded_image, operation)

def enhance_image(image, enhance_option, factor):
    img = Image.open(image)

    if enhance_option == "Brightness":
        enhancer = ImageEnhance.Brightness(img)
    elif enhance_option == "Contrast":
        enhancer = ImageEnhance.Contrast(img)
    elif enhance_option == "Sharpness":
        enhancer = ImageEnhance.Sharpness(img)

    enhanced_img = enhancer.enhance(factor)
    return enhanced_img

def apply_filter(image, filter_type):
    img = Image.open(image)
    if filter_type == "Blur":
        return img.filter(ImageFilter.BLUR)
    elif filter_type == "Contour":
        return img.filter(ImageFilter.CONTOUR)
    elif filter_type == "Detail":
        return img.filter(ImageFilter.DETAIL)
    elif filter_type == "Edge Enhance":
        return img.filter(ImageFilter.EDGE_ENHANCE)

def resize_image(image, size):
    img = Image.open(image)
    return img.resize((size, size))

def crop_image(image, coordinates):
    img = Image.open(image)
    coords = tuple(map(int, coordinates.split(',')))
    return img.crop(coords)

def download_button(image, operation):
    if st.button("Download Updated Image"):
        if operation == "Enhance":
            st.download_button(label="Download Enhanced Image", key="enhanced_image", on_click=download_image, args=(image, "enhanced"))
        elif operation == "Filter":
            st.download_button(label="Download Filtered Image", key="filtered_image", on_click=download_image, args=(image, "filtered"))
        elif operation == "Resize":
            st.download_button(label="Download Resized Image", key="resized_image", on_click=download_image, args=(image, "resized"))
        elif operation == "Crop":
            st.download_button(label="Download Cropped Image", key="cropped_image", on_click=download_image, args=(image, "cropped"))

def download_image(image, operation):
    img = Image.open(image)
    img.save(f"{operation}_image.jpg")

if __name__ == "__main__":
    main()
