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
        self.root.title("ÜRÜN YÖNETİM SİSTEMİ")
        self.root.geometry("900x600")
        self.root.configure(bg="#f0f0f0")
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Stil ayarları
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabel", background="#f0f0f0", font=("Arial", 10))
        self.style.configure("TButton", font=("Arial", 10), padding=6)
        self.style.configure(
            "Header.TLabel", font=("Arial", 14, "bold"), foreground="#2c3e50"
        )

        # Dizin yollarını ayarla (2 üst dizine çık)
        base_dir = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        self.assets_dir = os.path.join(base_dir, "meserweb", "src", "assets")
        self.data_dir = os.path.join(base_dir, "meserweb", "src", "data")

        # Gerekli klasörleri oluştur
        os.makedirs(self.assets_dir, exist_ok=True)
        os.makedirs(self.data_dir, exist_ok=True)

        # JSON dosya yolu
        self.json_file = os.path.join(self.data_dir, "products.json")
        if not os.path.exists(self.json_file):
            with open(self.json_file, "w", encoding="utf-8-sig") as f:
                json.dump([], f, ensure_ascii=False, indent=4)

        # Var olan JSON'daki muhtemel mojibake karakterlerini otomatik düzelt
        self.repair_json_encoding()

        # Değişkenler (ekleme için)
        self.product_name = tk.StringVar()
        self.product_description = tk.StringVar()
        # self.image_path = None
        # self.image_preview = None
        self.image_paths = []   # çoklu resim listesi

        # Sol panelde arama/silme için değişkenler
        self.delete_search_var = tk.StringVar()
        self.left_list_items = []  # sol panel listbox için (id, name)

        # Arayüzü oluştur
        self.create_widgets()

    # --- Türkçe karakter onarım yardımcıları ---
    @staticmethod
    def normalize_turkish(text: str) -> str:
        if not isinstance(text, str):
            return text
        replacements = {
            "ð": "ğ",
            "Ð": "Ğ",
            "þ": "ş",
            "Þ": "Ş",
            "ý": "ı",
            "Ý": "İ",
        }
        for bad, good in replacements.items():
            text = text.replace(bad, good)
        combos = {
            "Ã¶": "ö",
            "Ã–": "Ö",
            "Ã¼": "ü",
            "Ãœ": "Ü",
            "Ã§": "ç",
            "Ã‡": "Ç",
            "Ã±": "ñ",
            "Ã¡": "á",
            "ÄŸ": "ğ",
            "Äž": "Ğ",
            "ÅŸ": "ş",
            "Åž": "Ş",
            "Ä±": "ı",
            "Ä°": "İ",
        }
        for bad, good in combos.items():
            text = text.replace(bad, good)
        text = text.replace("Â", "")
        return text

    def repair_json_encoding(self):
        try:
            with open(self.json_file, "r", encoding="utf-8-sig") as f:
                data = json.load(f)
            changed = False
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        for key in ("name", "description"):
                            if key in item and isinstance(item[key], str):
                                fixed = self.normalize_turkish(item[key])
                                if fixed != item[key]:
                                    item[key] = fixed
                                    changed = True
            if changed:
                with open(self.json_file, "w", encoding="utf-8-sig") as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception:
            pass

    # --- UI ---
    def create_widgets(self):
        # Header
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill=tk.X, padx=20, pady=10)
        ttk.Label(header_frame, text="ÜRÜN YÖNETİM SİSTEMİ", style="Header.TLabel").pack()

        # Ana çerçeve: SOL (sabit genişlik, içeriği değişir) | SAĞ (sabit içerik: Ürün Ekleme)
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Sol panel
        self.left_panel = ttk.Frame(main_frame, width=320)
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        self.left_panel.pack_propagate(False)  # sabit genişlik koru

        # Sağ panel
        self.right_panel = ttk.Frame(main_frame)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Sol panel: butonlar + değişen içerik alanı
        nav_frame = ttk.Frame(self.left_panel)
        nav_frame.pack(fill=tk.X, pady=5, padx=5)

        ttk.Button(nav_frame, text="Ürün Ekle (Sağda)", command=self.show_left_add_placeholder).pack(
            side=tk.LEFT, expand=True, padx=3
        )
        ttk.Button(nav_frame, text="Ürün Sil", command=self.show_delete_screen).pack(
            side=tk.LEFT, expand=True, padx=3
        )

        # Left content area (kanvas gibi) - burada içerik değişecek
        self.left_content = ttk.Frame(self.left_panel)
        self.left_content.pack(fill=tk.BOTH, expand=True, padx=5, pady=(10, 5))

        # Sağ panela mevcut Ürün Ekleme formunu yerleştir
        self.create_add_form(self.right_panel)

        # Sol panel varsayılan gösterimi: doğrudan ürün silme ekranı
        self.show_delete_screen()

        # Durum çubuğu
        self.status_bar = ttk.Label(
            self.root, text="Hazır", relief=tk.SUNKEN, anchor=tk.W
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    # --- Sol panel içerikleri ---
    def clear_left_content(self):
        for w in self.left_content.winfo_children():
            w.destroy()

    def show_left_welcome(self):
        self.clear_left_content()
        ttk.Label(
            self.left_content,
            text="Sol panel: burada ekran değişir.\n\n- 'Ürün Ekle (Sağda)' butonuna basınca\n  sağ paneldeki ekleme formunu kullanın.\n- 'Ürün Sil' ile ürün silme ekranı açılır.",
            wraplength=280,
            justify=tk.LEFT,
        ).pack(padx=10, pady=10)

    def show_left_add_placeholder(self):
        # Kullanıcı Ürün Ekle'yi sol panelde görmek isterse kısa bir rehber gösterebiliriz
        self.clear_left_content()
        ttk.Label(self.left_content, text="Ürün Ekleme (Sağ Panelde) 🡒", style="Header.TLabel").pack(
            anchor=tk.W, pady=(5, 10), padx=5
        )
        ttk.Label(
            self.left_content,
            text="Ürün eklemek için sağ paneldeki formu kullanın.\nSağ panel otomatik olarak açılır ve hazırdır.",
            wraplength=280,
            justify=tk.LEFT,
        ).pack(padx=5, pady=5)

    def show_delete_screen(self):
        self.clear_left_content()
        ttk.Label(self.left_content, text="Ürün Sil", style="Header.TLabel").pack(
            anchor=tk.W, pady=(5, 10), padx=5
        )

        # Arama satırı
        search_frame = ttk.Frame(self.left_content)
        search_frame.pack(fill=tk.X, padx=5, pady=(0, 8))
        ttk.Label(search_frame, text="Ürün Adı ile Ara:", width=14).pack(side=tk.LEFT)
        search_entry = ttk.Entry(search_frame, textvariable=self.delete_search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))
        ttk.Button(search_frame, text="Ara", command=self.left_search_products).pack(side=tk.LEFT)

        # Bulunan ürünleri listele
        list_frame = ttk.Frame(self.left_content)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.left_listbox = tk.Listbox(list_frame, height=12)
        self.left_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.left_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.left_listbox.config(yscrollcommand=scrollbar.set)

        # Silme butonları
        action_frame = ttk.Frame(self.left_content)
        action_frame.pack(fill=tk.X, padx=5, pady=8)
        ttk.Button(action_frame, text="Seçiliyi Sil", command=self.left_delete_selected).pack(side=tk.LEFT)
        ttk.Button(action_frame, text="Tümünü Yenile", command=self.left_search_products).pack(side=tk.LEFT, padx=(8, 0))

        # 👇 Bu satır değişti: koşul olmadan listeyi getir
        self.left_search_products()

    def left_search_products(self):
        query = self.delete_search_var.get().strip()
        normalized_query = self.normalize_turkish(query).lower()

        matches = []
        try:
            with open(self.json_file, "r", encoding="utf-8-sig") as f:
                data = json.load(f)
            for item in data:
                name_norm = self.normalize_turkish(item.get("name", "")).lower()
                if normalized_query in name_norm:
                    matches.append(item)
        except Exception as e:
            messagebox.showerror("Hata", f"JSON okunurken hata: {e}")
            return

        # Liste kutusunu güncelle
        self.left_list_items = [(itm.get("id"), itm.get("name")) for itm in matches]
        self.left_listbox.delete(0, tk.END)
        for itm in matches:
            display = f"{itm.get('id')} — {itm.get('name')}"
            self.left_listbox.insert(tk.END, display)

        if not matches:
            self.left_listbox.insert(tk.END, "Eşleşme bulunamadı.")

    def left_delete_selected(self):
        sel = self.left_listbox.curselection()
        if not sel:
            messagebox.showinfo("Bilgi", "Lütfen silmek istediğiniz ürünü seçin.")
            return

        index = sel[0]
        if index >= len(self.left_list_items):
            messagebox.showinfo("Bilgi", "Geçerli bir ürün seçin.")
            return

        prod_id, prod_name = self.left_list_items[index]
        confirm = messagebox.askyesno(
            "Onay", 
            f"'{prod_name}' (ID: {prod_id}) kaydını JSON'dan ve resmini assets klasöründen silmek istediğinize emin misiniz?"
        )
        if not confirm:
            return

        # Silme işlemi
        try:
            with open(self.json_file, "r", encoding="utf-8-sig") as f:
                data = json.load(f)
        except Exception as e:
            messagebox.showerror("Hata", f"JSON okunurken hata: {e}")
            return

        new_data = []
        removed_item = None
        for item in data:
            if item.get("id") == prod_id:
                removed_item = item
                # Resim dosyasını silme
                img_rel = item.get("image", "")
                if img_rel:
                    img_path1 = os.path.join(os.path.dirname(self.json_file), img_rel)
                    img_path2 = os.path.join(self.assets_dir, os.path.basename(img_rel))
                    for img_path in [img_path1, img_path2]:
                        try:
                            if os.path.exists(img_path):
                                os.remove(img_path)
                                self.status_bar.config(text=f"Silindi: {img_path}")
                        except Exception:
                            # sessizce devam et
                            pass
                continue
            new_data.append(item)

        if removed_item is None:
            messagebox.showinfo("Bilgi", "Seçili ürün JSON içinde bulunamadı (muhtemelen zaten silinmiş).")
            self.left_search_products()
            return

        try:
            with open(self.json_file, "w", encoding="utf-8-sig") as f:
                json.dump(new_data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Hata", f"JSON yazılırken hata: {e}")
            return

        # GitHub commit (mevcut fonksiyonu kullan)
        commit_msg = f"Ürün silindi: {removed_item.get('name')} (ID: {removed_item.get('id')})"
        self.github_commit(commit_message=commit_msg)

        messagebox.showinfo("Başarılı", f"'{removed_item.get('name')}' silindi ve değişiklik GitHub'a gönderildi.")
        self.status_bar.config(text=f"Silindi: {removed_item.get('name')}")
        # Listeyi yenile
        self.left_search_products()

    # --- Sağ panel: Ürün ekleme formu (mevcut fonksiyonu biraz bölerek taşıdım) ---
    def create_add_form(self, parent):
        # input_frame yerleştiriliyor parent içinde (sağ panel)
        input_frame = ttk.LabelFrame(parent, text="Ürün Bilgileri", padding=15)
        input_frame.pack(fill=tk.BOTH, pady=(0, 15), padx=5, expand=True)

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
        ttk.Button(image_frame, text="Resim(ler) Seç", command=self.select_images, width=15).pack(
            side=tk.LEFT, padx=(5, 10)
        )
        self.image_status = ttk.Label(image_frame, text="Resim seçilmedi", foreground="#e74c3c")
        self.image_status.pack(side=tk.LEFT)

        # Çoklu Resim önizleme alanı
        preview_frame = ttk.Frame(input_frame)
        preview_frame.pack(fill=tk.X, pady=10)
        ttk.Label(preview_frame, text="Önizleme:", width=12).pack(side=tk.LEFT)
        self.preview_area = tk.Frame(preview_frame, bg="#ecf0f1")
        self.preview_area.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.preview_images = []  # referansları saklamak için

        # Butonlar
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=5, padx=5)
        ttk.Button(button_frame, text="Ürünü Kaydet", command=self.save_product, style="TButton").pack(
            side=tk.LEFT, padx=(0, 10)
        )
        ttk.Button(button_frame, text="Temizle", command=self.clear_form).pack(side=tk.LEFT)

    def select_images(self):
        file_paths = filedialog.askopenfilenames(
            title="Ürün Resimleri Seçin",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
        )

        if file_paths:
            # Öncekileri silme, yeni seçimleri ekle
            self.image_paths.extend(file_paths)

            self.image_status.config(
                text=f"{len(self.image_paths)} resim seçildi",
                foreground="#27ae60"
            )

            # Önizleme alanını temizle
            for widget in self.preview_area.winfo_children():
                widget.destroy()
            self.preview_images.clear()

            # Tüm seçilen resimleri thumbnail olarak göster
            for img_path in self.image_paths:
                try:
                    image = Image.open(img_path)
                    image.thumbnail((80, 80))
                    photo = ImageTk.PhotoImage(image)
                    self.preview_images.append(photo)  # referansları sakla

                    lbl = tk.Label(self.preview_area, image=photo, bg="#ecf0f1")
                    lbl.pack(side=tk.LEFT, padx=5, pady=5)
                except Exception as e:
                    print(f"Önizleme hatası: {e}")

    def generate_unique_id(self):
        return str(uuid.uuid4().int)[:8]

    def github_commit(self, commit_message: str = None):
        """Değişiklikleri GitHub'a gönder. commit_message verilmezse eski davranışla ürün eklendi mesajı kullanılır."""
        original_cwd = os.getcwd()
        try:
            # repo klasörünü bir üst dizine ayarlıyoruz (eski davranış korunuyor)
            os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            subprocess.run(["git", "add", "--all"], check=True)

            status_result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                check=True,
            )

            if not status_result.stdout.strip():
                self.status_bar.config(text="GitHub: Değişiklik yok")
                return

            if commit_message is None:
                commit_message = f"Ürün eklendi: {self.product_name.get()}"

            subprocess.run(["git", "commit", "-m", commit_message], check=True)
            push_result = subprocess.run(["git", "push"], capture_output=True, text=True)

            if push_result.returncode == 0:
                self.status_bar.config(text="Değişiklikler GitHub'a başarıyla gönderildi!")
            else:
                error_msg = push_result.stderr if push_result.stderr else push_result.stdout
                self.status_bar.config(text=f"GitHub Hatası: {error_msg[:150]}...")

        except subprocess.CalledProcessError as e:
            error_msg = e.stderr if hasattr(e, "stderr") and e.stderr else str(e)
            self.status_bar.config(text=f"GitHub Hatası: {error_msg}")
        except Exception as e:
            self.status_bar.config(text=f"Hata: {str(e)}")
        finally:
            os.chdir(original_cwd)

    def save_product(self):
        if not self.product_name.get():
            messagebox.showerror("Hata", "Ürün adı boş olamaz!")
            return

        if not self.image_paths:
            messagebox.showerror("Hata", "Lütfen en az bir resim seçin!")
            return

        try:
            name_fixed = self.normalize_turkish(self.product_name.get())
            desc_fixed = self.normalize_turkish(self.desc_entry.get("1.0", tk.END).strip())
            product_id = self.generate_unique_id()

            saved_images = []
            for idx, img_path in enumerate(self.image_paths):
                ext = os.path.splitext(img_path)[1].lower()
                if ext not in [".jpg", ".jpeg", ".png"]:
                    continue

                new_image_name = f"{product_id}-{idx}{ext}"
                target_path = os.path.join(self.assets_dir, new_image_name)
                shutil.copy2(img_path, target_path)
                saved_images.append(f"assets/{new_image_name}")

            product_data = {
                "id": product_id,
                "name": name_fixed,
                "description": desc_fixed,
                "images": saved_images
            }

            if os.path.exists(self.json_file):
                with open(self.json_file, "r", encoding="utf-8-sig") as f:
                    data = json.load(f)
            else:
                data = []

            data.append(product_data)

            with open(self.json_file, "w", encoding="utf-8-sig") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            self.github_commit()

            messagebox.showinfo(
                "Başarılı",
                f"Ürün kaydedildi! {len(saved_images)} resim eklendi."
            )

            self.clear_form()

        except Exception as e:
            messagebox.showerror("Hata", f"Bir hata oluştu: {str(e)}")
            self.status_bar.config(text=f"Hata: {str(e)}")

    def clear_form(self):
        self.product_name.set("")
        self.desc_entry.delete("1.0", tk.END)
        self.image_paths = []
        self.image_status.config(text="Resim seçilmedi", foreground="#e74c3c")
        # Çoklu önizleme alanını temizle
        if hasattr(self, "preview_area"):
            for widget in self.preview_area.winfo_children():
                widget.destroy()
        if hasattr(self, "preview_images"):
            self.preview_images.clear()
        self.status_bar.config(text="Hazır")


if __name__ == "__main__":
    root = tk.Tk()
    app = ProductApp(root)
    root.mainloop()