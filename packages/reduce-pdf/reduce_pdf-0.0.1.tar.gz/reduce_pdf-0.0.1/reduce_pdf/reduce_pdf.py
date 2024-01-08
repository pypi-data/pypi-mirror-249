import io
import fitz
from PIL import Image


def reduce_pdf(pdf_file, output_file, remove, compress, start_page, end_page):
    """
    Reduce the PDF file by removing images or compressing the images

    :param pdf_file: Input PDF file
    :param output_file: Output PDF file
    :param remove: Remove the images from the PDF flag
    :param compress: Compression quality for images if remove is false
    :return: None
    """
    # Open the original PDF file
    doc = fitz.open(pdf_file)

    # Check if the end page is specified and set the range of pages that will be processed
    if end_page == -1 or end_page > len(doc):
        end_page = len(doc)
    if start_page < 0:
        start_page = 0
    if start_page > end_page:
        start_page = end_page
    pages = range(start_page, end_page)

    # Iterate through the pages
    for page_no in pages:
        page = doc.load_page(page_no)

        # Get list of images on the page
        img_list = page.get_images(full=True)

        for img in img_list:
            xref = img[0]

            if not remove:
                # Compress the image
                base_image = doc.extract_image(xref)

                # Skip if the image is not valid
                if base_image is None or base_image == False:
                    continue

                img_bytes = base_image["image"]

                # Open the image using PIL
                image = Image.open(io.BytesIO(img_bytes))

                # Compress the image - adjust quality as needed
                with io.BytesIO() as output:
                    image.save(output, format='JPEG', quality=compress)  # Adjust quality for higher compression
                    compressed_image_bytes = output.getvalue()

                # Replace the original image with the compressed one
                image_rect = page.get_image_rects(xref)[0]

                page.insert_image(rect=image_rect, stream=compressed_image_bytes)

            # Delete the original image from the PDF
            doc._deleteObject(xref)

    # Get the list of pages to delete amd delete them. Also delete all the objects in the page
    del_pages = list(set(range(len(doc))) - set(pages))
    for page_no in del_pages:
        # Delete objects and images in the page
        page = doc.load_page(page_no)
        objects = page.get_xobjects()
        for obj in objects:
            xref = obj[0]
            doc._deleteObject(xref)
        images = page.get_images()
        for img in images:
            xref = img[0]
            doc._deleteObject(xref)

    doc.delete_pages(del_pages)

    # Save the changes to a new file
    doc.save(output_file, garbage=4, deflate=True, clean=True)
    doc.close()
