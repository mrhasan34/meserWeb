import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
import json
import uuid

PRODUCTS_FILE = "products.json"
ASSETS_DIR = "assets"

class ProductApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ürün Yönetim Sistemi")
        self.root.geometry("1000x600")

        # Ana paneller
        main_paned = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True)
        
        # Sol Panel (Sabit)
        frame_left = ttk.Frame(main_paned, width=150)
        main_paned.add(frame_left)
        
        # Sol panel butonları
        ttk.Button(
            frame_left, 
            text="Ürün Ekle", 
            command=self.show_add_product,
            width=15
        ).pack(pady=10, padx=10, fill=tk.X)
        
        ttk.Button(
            frame_left, 
            text="Ürün Sil", 
            command=self.show_delete_product,
            width=15
        ).pack(pady=10, padx=10, fill=tk.X)
        
        # Sağ Panel (Değişken içerik)
        self.frame_right = ttk.Frame(main_paned)
        main_paned.add(self.frame_right, weight=1)
        
        # Başlangıçta ekleme sayfasını göster
        self.current_frame = None
        self.show_add_product()
        
        # Veri yükle
        self.products = self.load_products()
        
    def clear_right_frame(self):
        """Sağ paneli temizle"""
        for widget in self.frame_right.winfo_children():
            widget.destroy()
    
    def show_add_product(self):
        """Ürün ekleme sayfasını göster"""
        self.clear_right_frame()
        self.current_frame = "add"
        
        # Ana ekleme paneli
        frame_add = ttk.Frame(self.frame_right)
        frame_add.pack(fill=tk.BOTH, expand=True)
        
        # Sol: Giriş alanları
        frame_inputs = ttk.Frame(frame_add, padding=10)
        frame_inputs.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        ttk.Label(frame_inputs, text="Ürün Adı:").pack(anchor="w")
        self.entry_name = ttk.Entry(frame_inputs, width=30)
        self.entry_name.pack(anchor="w", pady=5, fill=tk.X)
        
        ttk.Label(frame_inputs, text="Ürün Açıklaması:").pack(anchor="w")
        self.entry_desc = ttk.Entry(frame_inputs, width=30)
        self.entry_desc.pack(anchor="w", pady=5, fill=tk.X)
        
        ttk.Button(frame_inputs, text="Resim Seç", command=self.select_image).pack(anchor="w", pady=5)
        self.image_path = None
        
        ttk.Button(frame_inputs, text="Ürün Ekle", command=self.add_product).pack(anchor="w", pady=10)
        
        # Sağ: Önizleme alanı
        frame_preview = ttk.Frame(frame_add, padding=10)
        frame_preview.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        ttk.Label(frame_preview, text="Resim Önizleme:").pack(anchor="w")
        self.preview_canvas = tk.Canvas(frame_preview, width=300, height=300, bg="white", bd=2, relief=tk.SOLID)
        self.preview_canvas.pack(anchor="w", pady=5)
        
        # Başlangıçta boş bir önizleme göster
        self.update_preview(None)
    
    def show_delete_product(self):
        """Ürün silme sayfasını göster"""
        self.clear_right_frame()
        self.current_frame = "delete"
        
        # Ürün Silme Paneli
        frame_delete = ttk.Frame(self.frame_right, padding=10)
        frame_delete.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame_delete, text="Ürün Ara / Sil:").pack(anchor="w")
        self.entry_search = ttk.Entry(frame_delete, width=40)
        self.entry_search.pack(anchor="w", pady=5, fill=tk.X)
        self.entry_search.bind("<KeyRelease>", self.search_products)
        
        self.listbox = tk.Listbox(frame_delete, width=40, height=15)
        self.listbox.pack(anchor="w", pady=5, fill=tk.BOTH, expand=True)
        self.listbox.bind("<<ListboxSelect>>", self.show_image)
        
        self.canvas = tk.Canvas(frame_delete, width=200, height=200, bg="white")
        self.canvas.pack(anchor="w", pady=5)
        
        ttk.Button(frame_delete, text="Seçili Ürünü Sil", command=self.delete_product).pack(anchor="w", pady=10)
        
        # Listbox'ı güncelle
        self.refresh_listbox()

    def update_preview(self, image_path):
        """Resim önizlemesini günceller"""
        self.preview_canvas.delete("all")
        
        if image_path and os.path.exists(image_path):
            try:
                img = Image.open(image_path)
                img.thumbnail((300, 300))  # Önizleme boyutunu ayarla
                self.tk_preview_img = ImageTk.PhotoImage(img)
                self.preview_canvas.create_image(
                    150, 150,  # Canvas'ın ortasına yerleştir
                    image=self.tk_preview_img
                )
            except Exception as e:
                self.preview_canvas.create_text(
                    150, 150,
                    text="Resim yüklenemedi",
                    fill="gray"
                )
        else:
            self.preview_canvas.create_text(
                150, 150,
                text="Resim seçilmedi",
                fill="gray"
            )

    # ---------- Ürün ekleme ----------
    def select_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if path:
            self.image_path = path
            self.update_preview(path)  # Önizlemeyi güncelle

    def add_product(self):
        name = self.entry_name.get().strip()
        desc = self.entry_desc.get().strip()
        
        if not name or not desc or not self.image_path:
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurun ve resim seçin!")
            return
            
        if not os.path.exists(ASSETS_DIR):
            os.makedirs(ASSETS_DIR)
            
        product_id = str(uuid.uuid4())
        ext = os.path.splitext(self.image_path)[1]
        new_image_path = os.path.join(ASSETS_DIR, f"{product_id}{ext}")
        
        try:
            # Resmi kopyala (orijinal dosyayı korumak için)
            img = Image.open(self.image_path)
            img.save(new_image_path)
            
            product = {
                "id": product_id,
                "name": name,
                "description": desc,
                "image": new_image_path
            }
            
            self.products.append(product)
            self.save_products()
            
            # Sadece silme sayfası aktifse listbox'ı güncelle
            if self.current_frame == "delete":
                self.refresh_listbox()
                
            self.entry_name.delete(0, tk.END)
            self.entry_desc.delete(0, tk.END)
            self.image_path = None
            self.update_preview(None)  # Önizlemeyi temizle
            messagebox.showinfo("Başarılı", "Ürün eklendi!")
            
        except Exception as e:
            messagebox.showerror("Hata", f"Resim kaydedilemedi: {str(e)}")

    # ---------- Ürün arama & silme ----------
    def search_products(self, event=None):
        query = self.entry_search.get().lower()
        self.listbox.delete(0, tk.END)
        for p in self.products:
            if query in p["name"].lower():
                self.listbox.insert(tk.END, p["name"])

    def refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for p in self.products:
            self.listbox.insert(tk.END, p["name"])

    def show_image(self, event=None):
        selection = self.listbox.curselection()
        if not selection:
            return
            
        index = selection[0]
        name = self.listbox.get(index)
        product = next((p for p in self.products if p["name"] == name), None)
        
        if product and os.path.exists(product["image"]):
            img = Image.open(product["image"])
            img.thumbnail((200, 200))
            self.tk_img = ImageTk.PhotoImage(img)
            self.canvas.delete("all")
            self.canvas.create_image(100, 100, image=self.tk_img)

    def delete_product(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Uyarı", "Silmek için ürün seçin!")
            return
            
        index = selection[0]
        name = self.listbox.get(index)
        
        # Resmi de sil
        product = next((p for p in self.products if p["name"] == name), None)
        if product and os.path.exists(product["image"]):
            try:
                os.remove(product["image"])
            except Exception as e:
                messagebox.showwarning("Uyarı", f"Resim dosyası silinemedi: {str(e)}")
        
        self.products = [p for p in self.products if p["name"] != name]
        self.save_products()
        self.refresh_listbox()
        self.canvas.delete("all")
        messagebox.showinfo("Başarılı", f"{name} silindi!")

    # ---------- JSON işlemleri ----------
    def load_products(self):
        if os.path.exists(PRODUCTS_FILE):
            with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_products(self):
        with open(PRODUCTS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.products, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    root = tk.Tk()
    app = ProductApp(root)
    root.mainloop()