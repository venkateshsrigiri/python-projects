import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from pdf2image import convert_from_path
from PyPDF2 import PdfMerger
import pythoncom
import win32com.client
from docx2pdf import convert as docx2pdf
from fpdf import FPDF
import tempfile

class PDFConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Converter and Merger")
        self.root.geometry("600x500")
        
        # Configure styles
        style = ttk.Style()
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        style.configure('TButton', font=('Arial', 10), padding=5)
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        
        # Create main container
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create Convert Tab
        self.convert_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.convert_tab, text="Convert to PDF")
        
        # Create Merge Tab
        self.merge_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.merge_tab, text="Merge PDFs")
        
        # Setup Convert Tab
        self.setup_convert_tab()
        
        # Setup Merge Tab
        self.setup_merge_tab()
        
    def setup_convert_tab(self):
        # Header
        header = ttk.Label(self.convert_tab, text="Convert Files to PDF", style='Header.TLabel')
        header.pack(pady=10)
        
        # File selection
        file_frame = ttk.Frame(self.convert_tab)
        file_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(file_frame, text="Select File:").pack(side=tk.LEFT)
        
        self.file_path = tk.StringVar()
        self.file_entry = ttk.Entry(file_frame, textvariable=self.file_path, width=50)
        self.file_entry.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
        browse_btn = ttk.Button(file_frame, text="Browse", command=self.browse_file)
        browse_btn.pack(side=tk.LEFT)
        
        # Output location
        output_frame = ttk.Frame(self.convert_tab)
        output_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(output_frame, text="Output Folder:").pack(side=tk.LEFT)
        
        self.output_path = tk.StringVar()
        self.output_entry = ttk.Entry(output_frame, textvariable=self.output_path, width=50)
        self.output_entry.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
        output_browse_btn = ttk.Button(output_frame, text="Browse", command=self.browse_output)
        output_browse_btn.pack(side=tk.LEFT)
        
        # Convert button
        convert_btn = ttk.Button(self.convert_tab, text="Convert to PDF", command=self.convert_to_pdf)
        convert_btn.pack(pady=20)
        
        # Status label
        self.status_label = ttk.Label(self.convert_tab, text="", foreground="green")
        self.status_label.pack()
        
        # Supported formats label
        formats_label = ttk.Label(self.convert_tab, 
                                 text="Supported formats: Images (jpg, png, bmp, etc.), " +
                                      "Word (doc, docx), Excel (xls, xlsx), PowerPoint (ppt, pptx), " +
                                      "Text (txt), and PDF (for conversion from images)")
        formats_label.pack(pady=10, padx=10)
    
    def setup_merge_tab(self):
        # Header
        header = ttk.Label(self.merge_tab, text="Merge PDF Files", style='Header.TLabel')
        header.pack(pady=10)
        
        # File list
        list_frame = ttk.Frame(self.merge_tab)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        ttk.Label(list_frame, text="PDF Files to Merge:").pack(anchor=tk.W)
        
        self.file_listbox = tk.Listbox(list_frame, selectmode=tk.EXTENDED, height=8)
        self.file_listbox.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Button frame
        btn_frame = ttk.Frame(list_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        add_btn = ttk.Button(btn_frame, text="Add PDFs", command=self.add_pdfs)
        add_btn.pack(side=tk.LEFT, padx=5)
        
        remove_btn = ttk.Button(btn_frame, text="Remove Selected", command=self.remove_selected)
        remove_btn.pack(side=tk.LEFT, padx=5)
        
        up_btn = ttk.Button(btn_frame, text="Move Up", command=self.move_up)
        up_btn.pack(side=tk.LEFT, padx=5)
        
        down_btn = ttk.Button(btn_frame, text="Move Down", command=self.move_down)
        down_btn.pack(side=tk.LEFT, padx=5)
        
        # Output location
        output_frame = ttk.Frame(self.merge_tab)
        output_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(output_frame, text="Output File:").pack(side=tk.LEFT)
        
        self.merge_output_path = tk.StringVar()
        self.merge_output_entry = ttk.Entry(output_frame, textvariable=self.merge_output_path, width=50)
        self.merge_output_entry.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
        merge_output_browse_btn = ttk.Button(output_frame, text="Browse", command=self.browse_merge_output)
        merge_output_browse_btn.pack(side=tk.LEFT)
        
        # Merge button
        merge_btn = ttk.Button(self.merge_tab, text="Merge PDFs", command=self.merge_pdfs)
        merge_btn.pack(pady=20)
        
        # Status label
        self.merge_status_label = ttk.Label(self.merge_tab, text="", foreground="green")
        self.merge_status_label.pack()
    
    def browse_file(self):
        filetypes = (
            ('All files', '*.*'),
            ('Images', '*.jpg *.jpeg *.png *.bmp *.tiff'),
            ('Word Documents', '*.doc *.docx'),
            ('Excel Files', '*.xls *.xlsx'),
            ('PowerPoint', '*.ppt *.pptx'),
            ('Text Files', '*.txt'),
            ('PDF Files', '*.pdf')
        )
        
        filename = filedialog.askopenfilename(title="Select a file", filetypes=filetypes)
        if filename:
            self.file_path.set(filename)
            # Set default output folder to same as input file
            self.output_path.set(os.path.dirname(filename))
    
    def browse_output(self):
        folder = filedialog.askdirectory(title="Select output folder")
        if folder:
            self.output_path.set(folder)
    
    def browse_merge_output(self):
        filename = filedialog.asksaveasfilename(
            title="Save merged PDF as",
            defaultextension=".pdf",
            filetypes=(("PDF Files", "*.pdf"),)
        )
        if filename:
            self.merge_output_path.set(filename)
    
    def add_pdfs(self):
        files = filedialog.askopenfilenames(
            title="Select PDF files",
            filetypes=(("PDF Files", "*.pdf"),)
        )
        for file in files:
            self.file_listbox.insert(tk.END, file)
    
    def remove_selected(self):
        for i in reversed(self.file_listbox.curselection()):
            self.file_listbox.delete(i)
    
    def move_up(self):
        selected = self.file_listbox.curselection()
        if not selected:
            return
        for pos in selected:
            if pos == 0:
                continue
            text = self.file_listbox.get(pos)
            self.file_listbox.delete(pos)
            self.file_listbox.insert(pos-1, text)
            self.file_listbox.select_set(pos-1)
    
    def move_down(self):
        selected = self.file_listbox.curselection()
        if not selected:
            return
        for pos in reversed(selected):
            if pos == self.file_listbox.size() - 1:
                continue
            text = self.file_listbox.get(pos)
            self.file_listbox.delete(pos)
            self.file_listbox.insert(pos+1, text)
            self.file_listbox.select_set(pos+1)
    
    def convert_to_pdf(self):
        input_file = self.file_path.get()
        output_folder = self.output_path.get()
        
        if not input_file:
            messagebox.showerror("Error", "Please select a file to convert")
            return
        
        if not output_folder:
            messagebox.showerror("Error", "Please select an output folder")
            return
        
        if not os.path.exists(input_file):
            messagebox.showerror("Error", "Input file does not exist")
            return
        
        if not os.path.exists(output_folder):
            try:
                os.makedirs(output_folder)
            except OSError:
                messagebox.showerror("Error", "Could not create output directory")
                return
        
        filename = os.path.basename(input_file)
        file_ext = os.path.splitext(filename)[1].lower()
        output_file = os.path.join(output_folder, os.path.splitext(filename)[0] + ".pdf")
        
        try:
            if file_ext in ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif'):
                self.image_to_pdf(input_file, output_file)
            elif file_ext == '.pdf':
                # Handle PDF to PDF conversion (might be images in PDF)
                self.pdf_to_pdf(input_file, output_file)
            elif file_ext in ('.doc', '.docx'):
                self.word_to_pdf(input_file, output_file)
            elif file_ext in ('.xls', '.xlsx'):
                self.excel_to_pdf(input_file, output_file)
            elif file_ext in ('.ppt', '.pptx'):
                self.powerpoint_to_pdf(input_file, output_file)
            elif file_ext == '.txt':
                self.text_to_pdf(input_file, output_file)
            else:
                messagebox.showerror("Error", f"Unsupported file format: {file_ext}")
                return
            
            self.status_label.config(text=f"Successfully converted to {output_file}", foreground="green")
            messagebox.showinfo("Success", f"File converted successfully to:\n{output_file}")
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}", foreground="red")
            messagebox.showerror("Error", f"Conversion failed: {str(e)}")
    
    def image_to_pdf(self, image_path, output_path):
        image = Image.open(image_path)
        if image.mode == 'RGBA':
            image = image.convert('RGB')
        
        # For multi-page TIFF
        try:
            images = []
            i = 0
            while True:
                images.append(image)
                i += 1
                image.seek(i)
        except EOFError:
            pass
        
        if len(images) > 1:
            images[0].save(output_path, save_all=True, append_images=images[1:], format='PDF')
        else:
            image.save(output_path, format='PDF')
    
    def pdf_to_pdf(self, pdf_path, output_path):
        # This is for cases where the PDF contains images and we want to convert it
        # to a more standard PDF format
        images = convert_from_path(pdf_path)
        if len(images) == 1:
            images[0].save(output_path, format='PDF')
        else:
            images[0].save(output_path, save_all=True, append_images=images[1:], format='PDF')
    
    def word_to_pdf(self, doc_path, output_path):
        # Try using docx2pdf first
        try:
            docx2pdf(doc_path, output_path)
            return
        except:
            pass
        
        # Fallback to COM interface
        pythoncom.CoInitialize()
        try:
            word = win32com.client.Dispatch("Word.Application")
            doc = word.Documents.Open(doc_path)
            doc.SaveAs(output_path, FileFormat=17)  # 17 is PDF format
            doc.Close()
            word.Quit()
        finally:
            pythoncom.CoUninitialize()
    
    def excel_to_pdf(self, xls_path, output_path):
        pythoncom.CoInitialize()
        try:
            excel = win32com.client.Dispatch("Excel.Application")
            workbook = excel.Workbooks.Open(xls_path)
            workbook.ExportAsFixedFormat(0, output_path)  # 0 is PDF format
            workbook.Close()
            excel.Quit()
        finally:
            pythoncom.CoUninitialize()
    
    def powerpoint_to_pdf(self, ppt_path, output_path):
        pythoncom.CoInitialize()
        try:
            powerpoint = win32com.client.Dispatch("PowerPoint.Application")
            presentation = powerpoint.Presentations.Open(ppt_path)
            presentation.SaveAs(output_path, 32)  # 32 is PDF format
            presentation.Close()
            powerpoint.Quit()
        finally:
            pythoncom.CoUninitialize()
    
    def text_to_pdf(self, txt_path, output_path):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        with open(txt_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                pdf.cell(200, 10, txt=line.strip(), ln=1)
        
        pdf.output(output_path)
    
    def merge_pdfs(self):
        if self.file_listbox.size() < 2:
            messagebox.showerror("Error", "Please select at least 2 PDF files to merge")
            return
        
        output_file = self.merge_output_path.get()
        if not output_file:
            messagebox.showerror("Error", "Please specify an output file")
            return
        
        try:
            merger = PdfMerger()
            
            for i in range(self.file_listbox.size()):
                pdf_path = self.file_listbox.get(i)
                merger.append(pdf_path)
            
            merger.write(output_file)
            merger.close()
            
            self.merge_status_label.config(text=f"Successfully merged to {output_file}", foreground="green")
            messagebox.showinfo("Success", f"PDFs merged successfully to:\n{output_file}")
        except Exception as e:
            self.merge_status_label.config(text=f"Error: {str(e)}", foreground="red")
            messagebox.showerror("Error", f"Merge failed: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFConverterApp(root)
    root.mainloop()
