# Reduce PDF

This is a simple script to reduce the size of a PDF file by removing images or compressing images.

It can also output a subset of the pages of the PDF.

## Usage

To use this tool, run

```bash
reduce-pdf <input_pdf> <output_pdf>
```

where `<input_pdf>` is the path to the input PDF file and `<output_pdf>` is the path to the output PDF file.

You can also specify the following options:

- `--remove` to remove images from the PDF
- `--compress` to compress images in the PDF and the compression level between 0 and 100
- `start_page` to specify the first page to include in the output PDF
- `end_page` to specify the last page to include in the output PDF

By default, images are compressed with value of 0. All pages are included.