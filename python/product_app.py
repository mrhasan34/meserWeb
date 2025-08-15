import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
import json
import shutil
import uuid
import subprocess

class ProductApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ürün Yönetim Sistemi")
        self.root.geometry("700x600")
        self.root.configure(bg="#f0f0f0")
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # Stil ayarları
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabel", background="#f0f0f0", font=("Arial", 10))
        self.style.configure("TButton", font=("Arial", 10), padding=6)
        self.style.configure("Header.TLabel", font=("Arial", 14, "bold"), foreground="#2c3e50")
        
        # Dizin yollarını ayarla (2 üst dizine çık)
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.assets_dir = os.path.join(base_dir, "meserweb", "src", "assets")
        self.data_dir = os.path.join(base_dir, "meserweb", "src", "data")
        
        # Gerekli klasörleri oluştur
        os.makedirs(self.assets_dir, exist_ok=True)
        os.makedirs(self.data_dir, exist_ok=True)
        
        # JSON dosya yolu
        self.json_file = os.path.join(self.data_dir, "products.json")
        if not os.path.exists(self.json_file):
            with open(self.json_file, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=4)
        
        # Değişkenler
        self.product_name = tk.StringVar()
        self.product_description = tk.StringVar()
        self.image_path = None
        self.image_preview = None
        
        # Arayüzü oluştur
        self.create_widgets()
        
    def create_widgets(self):
        # Header
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill=tk.X, padx=20, pady=15)
        
        ttk.Label(header_frame, text="ÜRÜN YÖNETİM SİSTEMİ", style="Header.TLabel").pack()
        
        # Ana çerçeve
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Ürün Bilgileri Çerçevesi
        input_frame = ttk.LabelFrame(main_frame, text="Ürün Bilgileri", padding=15)
        input_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Ürün Adı
        name_frame = ttk.Frame(input_frame)
        name_frame.pack(fill=tk.X, pady=5)
        ttk.Label(name_frame, text="Ürün Adı*:", width=12).pack(side=tk.LEFT)
        name_entry = ttk.Entry(name_frame, textvariable=self.product_name, width=40)
        name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
        # Açıklama
        desc_frame = ttk.Frame(input_frame)
        desc_frame.pack(fill=tk.X, pady=10)
        ttk.Label(desc_frame, text="Açıklama:", width=12).pack(side=tk.LEFT)
        self.desc_entry = tk.Text(desc_frame, height=4, width=40, font=("Arial", 10))
        self.desc_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
        # Resim Seç
        image_frame = ttk.Frame(input_frame)
        image_frame.pack(fill=tk.X, pady=10)
        ttk.Label(image_frame, text="Ürün Resmi*:", width=12).pack(side=tk.LEFT)
        ttk.Button(image_frame, text="Resim Seç", command=self.select_image, width=15).pack(side=tk.LEFT, padx=(5, 10))
        self.image_status = ttk.Label(image_frame, text="Resim seçilmedi", foreground="#e74c3c")
        self.image_status.pack(side=tk.LEFT)
        
        # Resim önizleme
        preview_frame = ttk.Frame(input_frame)
        preview_frame.pack(fill=tk.X, pady=10)
        ttk.Label(preview_frame, text="Önizleme:", width=12).pack(side=tk.LEFT)
        self.preview_canvas = tk.Canvas(preview_frame, width=200, height=200, 
                                      bg="#ecf0f1", highlightthickness=1, highlightbackground="#bdc3c7")
        self.preview_canvas.pack(side=tk.LEFT, padx=(5, 0))
        self.preview_label = ttk.Label(preview_frame, text="Resim seçilmedi", 
                                     foreground="#7f8c8d", font=("Arial", 9))
        self.preview_label.pack(side=tk.LEFT, padx=10)
        
        # Butonlar
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=15)
        ttk.Button(button_frame, text="Ürünü Kaydet", command=self.save_product, 
                  style="TButton").pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Temizle", command=self.clear_form).pack(side=tk.LEFT)
        
        # Durum çubuğu
        self.status_bar = ttk.Label(self.root, text="Hazır", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def select_image(self):
        file_path = filedialog.askopenfilename(
            title="Ürün Resmi Seçin",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
        )
        
        if file_path:
            self.image_path = file_path
            self.image_status.config(text="Resim seçildi", foreground="#27ae60")
            
            try:
                # Resmi küçülterek önizleme yap
                image = Image.open(file_path)
                image.thumbnail((200, 200))
                photo = ImageTk.PhotoImage(image)
                
                # Önizleme canvas'ını güncelle
                self.preview_canvas.delete("all")
                self.preview_canvas.create_image(100, 100, image=photo)
                self.preview_canvas.image = photo  # Referansı tut
                self.preview_label.config(text="")
            except Exception as e:
                self.image_status.config(text=f"Hata: {str(e)}", foreground="#e74c3c")
    
    def generate_unique_id(self):
        """Benzersiz bir ID oluştur"""
        return str(uuid.uuid4().int)[:8]
    
    def github_commit(self):
        """Değişiklikleri GitHub'a gönder"""
        try:
            original_cwd = os.getcwd()
            os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            subprocess.run(["git", "add", "--all"], check=True)

            status_result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True, text=True, check=True
            )

            if not status_result.stdout.strip():
                self.status_bar.config(text="GitHub: Değişiklik yok")
                return

            commit_message = f"Ürün eklendi: {self.product_name.get()}"
            subprocess.run(["git", "commit", "-m", commit_message], check=True)
            push_result = subprocess.run(["git", "push"], capture_output=True, text=True)

            if push_result.returncode == 0:
                self.status_bar.config(text="Değişiklikler GitHub'a başarıyla gönderildi!")
            else:
                error_msg = push_result.stderr if push_result.stderr else push_result.stdout
                self.status_bar.config(text=f"GitHub Hatası: {error_msg[:150]}...")
                
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr if e.stderr else str(e)
            self.status_bar.config(text=f"GitHub Hatası: {error_msg}")
        except Exception as e:
            self.status_bar.config(text=f"Hata: {str(e)}")
        finally:
            os.chdir(original_cwd)

    def save_product(self):
        if not self.product_name.get():
            messagebox.showerror("Hata", "Ürün adı boş olamaz!")
            return

        if not self.image_path:
            messagebox.showerror("Hata", "Lütfen bir resim seçin!")
            return

        try:
            product_id = self.generate_unique_id()
            ext = os.path.splitext(self.image_path)[1].lower()
            if ext not in ['.jpg', '.jpeg', '.png']:
                messagebox.showerror("Hata", "Desteklenmeyen dosya formatı! (JPG, PNG kullanın)")
                return

            new_image_name = f"{product_id}{ext}"
            target_path = os.path.join(self.assets_dir, new_image_name)
            shutil.copy2(self.image_path, target_path)
            relative_image_path = f"assets/{new_image_name}"

            product_data = {
                "id": product_id,
                "name": self.product_name.get(),
                "description": self.desc_entry.get("1.0", tk.END).strip(),
                "image": relative_image_path
            }

            if os.path.exists(self.json_file):
                with open(self.json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                data = []

            data.append(product_data)

            with open(self.json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            self.github_commit()

            messagebox.showinfo("Başarılı", 
                f"Ürün başarıyla kaydedildi ve GitHub'a gönderildi!\n"
                f"Ürün ID: {product_id}\n"
                f"Resim: {target_path}\n"
                f"Veri: {self.json_file}")
            
            self.clear_form()
            
        except Exception as e:
            messagebox.showerror("Hata", f"Bir hata oluştu: {str(e)}")
            self.status_bar.config(text=f"Hata: {str(e)}")
    
    def clear_form(self):
        self.product_name.set("")
        self.desc_entry.delete("1.0", tk.END)
        self.image_path = None
        self.image_status.config(text="Resim seçilmedi", foreground="#e74c3c")
        self.preview_canvas.delete("all")
        self.preview_canvas.create_text(100, 100, text="Resim Önizleme", 
                                      fill="#7f8c8d", font=("Arial", 10))
        self.preview_label.config(text="Resim seçilmedi")
        self.status_bar.config(text="Hazır")

if __name__ == "__main__":
    root = tk.Tk()
    app = ProductApp(root)
    app.preview_canvas.create_text(100, 100, text="Resim Önizleme", 
                                 fill="#7f8c8d", font=("Arial", 10))
    root.mainloop()
