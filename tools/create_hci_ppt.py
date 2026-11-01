from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile, ZIP_DEFLATED
from PIL import Image, ImageDraw, ImageFont
import html, re, shutil

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'Presentasi_HCI_Sabuh_Mas_Catering_Final.pptx'
ASSET = ROOT / 'js' / 'assets' / 'images' / 'produk'
WORK = ROOT / 'temp_ppt_hci'
WORK.mkdir(exist_ok=True)

W, H = 13.333, 7.5
EMU = 914400
NS = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main', 'p': 'http://schemas.openxmlformats.org/presentationml/2006/main', 'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
for k, v in NS.items():
    ET.register_namespace(k, v)

BG = 'F6F1E8'; INK = '33271F'; TERR = 'C96E54'; ORANGE = 'D8792B'; OLIVE = '75805A'; LINE = 'D8CABC'; WHITE = 'FFFDF9'; MUTED = '75675C'

def font(size, bold=False, color=INK, face='Aptos'):
    return {'size': size, 'bold': bold, 'color': color, 'face': face}

def load_font(size, bold=False):
    candidates = [
        Path('C:/Windows/Fonts/arialbd.ttf' if bold else 'C:/Windows/Fonts/arial.ttf'),
        Path('C:/Windows/Fonts/segoeuib.ttf' if bold else 'C:/Windows/Fonts/segoeui.ttf'),
    ]
    for p in candidates:
        if p.exists():
            return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()

def make_site_images():
    home = WORK / 'site_home.png'
    catalog = WORK / 'site_catalog.png'
    mobile = WORK / 'site_mobile.png'
    f_title = load_font(38, True); f_nav = load_font(16); f_h1 = load_font(54, True); f_body = load_font(20); f_small = load_font(14); f_card = load_font(22, True)
    products = [ASSET / 'nasi kotak.jpeg', ASSET / 'prasmanan.jpeg', ASSET / 'pmt.jpeg', ASSET / 'snack box.jpeg']
    def base(size):
        im = Image.new('RGB', size, '#F6F1E8'); d = ImageDraw.Draw(im)
        d.rectangle((0,0,size[0],72), fill='#FFFDF9'); d.line((0,72,size[0],72), fill='#D8CABC', width=2)
        d.text((48,20), 'Sabuh Mas', font=f_title, fill='#33271F')
        d.text((240,31), 'CATERING · GIANYAR', font=f_small, fill='#C96E54')
        nav = ['Beranda','Profil Usaha','Katalog Layanan','Pemesanan']
        x = size[0] - 530
        for n in nav:
            d.text((x,29), n, font=f_nav, fill='#33271F'); x += 125 if n != 'Katalog Layanan' else 150
        return im, d
    im, d = base((1440, 820))
    d.text((70,145), '01 — PROFIL · JASA CATERING · GIANYAR, BALI', font=f_small, fill='#C96E54')
    d.text((70,195), 'Catering untuk Berbagai', font=f_h1, fill='#33271F')
    d.text((70,260), 'Kebutuhan Acara di Gianyar.', font=f_h1, fill='#33271F')
    d.text((70,350), 'Layanan konsumsi untuk kegiatan masyarakat,', font=f_body, fill='#75675C')
    d.text((70,382), 'acara keluarga, rapat, dan kegiatan instansi.', font=f_body, fill='#75675C')
    d.rounded_rectangle((70,470,275,525), radius=8, fill='#33271F'); d.text((98,487), 'Lihat Katalog', font=f_nav, fill='#FFFDF9')
    d.rounded_rectangle((870,145,1360,620), radius=16, fill='#E8DCCB', outline='#C96E54', width=3)
    d.text((920,190), 'Sabuh Mas Catering', font=f_title, fill='#33271F')
    d.text((920,258), 'Melayani kebutuhan konsumsi', font=f_body, fill='#75675C')
    d.text((920,290), 'untuk berbagai acara.', font=f_body, fill='#75675C')
    d.line((920,380,1310,380), fill='#C96E54', width=3)
    d.text((920,425), 'Gianyar, Bali', font=f_card, fill='#33271F')
    d.text((920,470), 'Nasi Kotak · Prasmanan', font=f_small, fill='#75675C')
    d.text((920,500), 'PMT Balita · Snack Box', font=f_small, fill='#75675C')
    d.rectangle((0,700,1440,820), fill='#33271F'); d.text((70,748), 'Sabuh Mas Catering', font=f_card, fill='#FFFDF9'); d.text((950,754), 'Profil  Katalog  Pemesanan', font=f_small, fill='#E8DCCB')
    im.save(home)

    im, d = base((1440, 820))
    d.text((70,120), 'KATALOG LAYANAN', font=f_small, fill='#C96E54'); d.text((70,160), 'Pilihan Layanan', font=f_h1, fill='#33271F')
    d.text((70,240), 'Menu dan kategori layanan disusun agar mudah dipindai.', font=f_body, fill='#75675C')
    names = ['Nasi Kotak','Prasmanan','PMT Balita','Snack Box']
    for i, (name, path) in enumerate(zip(names, products)):
        x = 70 + (i%2)*660; y = 320 + (i//2)*220
        d.rounded_rectangle((x,y,x+610,y+175), radius=12, fill='#FFFDF9', outline='#D8CABC', width=2)
        img = Image.open(path).convert('RGB'); img.thumbnail((220,145)); im.paste(img, (x+18,y+15))
        d.text((x+270,y+34), name, font=f_card, fill='#33271F')
        d.text((x+270,y+80), 'Layanan konsumsi', font=f_small, fill='#75675C')
        d.text((x+270,y+108), 'Detail dikonfirmasi saat pesan', font=f_small, fill='#75675C')
    d.rectangle((0,755,1440,820), fill='#33271F'); d.text((70,780), 'Galeri katalog · foto dokumentasi yang tersedia', font=f_small, fill='#FFFDF9')
    im.save(catalog)

    im = Image.new('RGB', (620, 1000), '#F6F1E8'); d = ImageDraw.Draw(im)
    d.rectangle((0,0,620,76), fill='#FFFDF9'); d.text((28,21), 'Sabuh Mas', font=load_font(28, True), fill='#33271F'); d.text((470,27), '☰', font=load_font(25), fill='#33271F')
    d.text((32,130), 'Catering untuk', font=load_font(34, True), fill='#33271F'); d.text((32,172), 'Berbagai Acara.', font=load_font(34, True), fill='#33271F')
    d.text((32,245), 'Informasi usaha dan katalog', font=load_font(17), fill='#75675C'); d.text((32,274), 'dalam satu antarmuka.', font=load_font(17), fill='#75675C')
    d.rounded_rectangle((32,340,240,390), radius=8, fill='#33271F'); d.text((63,355), 'Lihat Katalog', font=load_font(16), fill='#FFFDF9')
    d.rounded_rectangle((32,450,588,710), radius=16, fill='#E8DCCB', outline='#C96E54', width=3); d.text((70,510), 'Mudah dipindai', font=load_font(28, True), fill='#33271F'); d.text((70,562), 'Profil · Katalog · Pesan', font=load_font(18), fill='#75675C'); d.text((70,625), 'Responsif untuk smartphone', font=load_font(18), fill='#75675C')
    d.rectangle((0,900,620,1000), fill='#33271F'); d.text((32,935), 'Gianyar, Bali', font=load_font(17), fill='#FFFDF9')
    im.save(mobile)
    return home, catalog, mobile

def esc(s): return html.escape(str(s))
def tag(name, attrs=None, children=None, text=None):
    e = ET.Element('{%s}%s' % (NS['p'] if name.startswith('p:') else NS['a'], name.split(':')[-1]), attrs or {})
    if text is not None: e.text = text
    if children:
        for c in children: e.append(c)
    return e

def x(tagname, attrs=None, children=None, text=None):
    if ':' in tagname: prefix, local = tagname.split(':',1); ns=NS[prefix]
    else: ns=NS['a']; local=tagname
    e=ET.Element('{%s}%s'%(ns,local), attrs or {})
    if text is not None: e.text=text
    if children:
        for c in children: e.append(c)
    return e

def txbody(text, style, w, h, align='l'):
    body=x('a:txBody', children=[x('a:bodyPr', {'wrap':'square'}), x('a:lstStyle')])
    for idx, line in enumerate(str(text).split('\n')):
        p=x('a:p'); pPr=x('a:pPr', {'algn': {'l':'l','c':'ctr','r':'r'}.get(align,'l')}); p.append(pPr)
        r=x('a:r'); rPr=x('a:rPr', {'lang':'id-ID','sz':str(int(style['size']*100)), 'b':'1' if style.get('bold') else '0', 'typeface':style.get('face','Aptos')}); rPr.append(x('a:solidFill', children=[x('a:srgbClr', {'val':style.get('color',INK)})])); r.append(rPr); r.append(x('a:t', text=line)); p.append(r); p.append(x('a:endParaRPr', {'lang':'id-ID'})); body.append(p)
    return body

def shape(x0,y0,w,h, fill=None, line=None, radius=False, text=None, style=None, align='l'):
    attrs={'bwMode':'auto'}
    sp=x('p:sp', children=[x('p:nvSpPr', children=[x('p:cNvPr', {'id':'0','name':'shape'}), x('p:cNvSpPr', {'txBox':'1'}), x('p:nvPr')]), x('p:spPr')])
    spPr=sp.find('.//{%s}spPr'%NS['p'])
    spPr.append(x('a:xfrm', children=[x('a:off', {'x':str(int(x0*EMU)),'y':str(int(y0*EMU))}), x('a:ext', {'cx':str(int(w*EMU)),'cy':str(int(h*EMU))})]))
    spPr.append(x('a:prstGeom', {'prst':'roundRect' if radius else 'rect'}, children=[x('a:avLst')]))
    if fill: spPr.append(x('a:solidFill', children=[x('a:srgbClr', {'val':fill})]))
    else: spPr.append(x('a:noFill'))
    ln=x('a:ln', {'w':'12700'})
    if line: ln.append(x('a:solidFill', children=[x('a:srgbClr', {'val':line})]))
    else: ln.append(x('a:noFill'))
    spPr.append(ln)
    if text is not None:
        sp.append(txbody(text, style or font(16), w, h, align))
    return sp

def image_shape(x0,y0,w,h, rel_id):
    pic=x('p:pic', children=[x('p:nvPicPr', children=[x('p:cNvPr', {'id':'0','name':'image'}), x('p:cNvPicPr'), x('p:nvPr')]), x('p:blipFill', children=[x('a:blip', {'{%s}embed'%NS['r']:rel_id}), x('a:stretch', children=[x('a:fillRect')])]), x('p:spPr', children=[x('a:xfrm', children=[x('a:off', {'x':str(int(x0*EMU)),'y':str(int(y0*EMU))}), x('a:ext', {'cx':str(int(w*EMU)),'cy':str(int(h*EMU))})]), x('a:prstGeom', {'prst':'rect'}, children=[x('a:avLst')])])])
    return pic

def slide_xml(items):
    tree=x('p:spTree', children=[x('p:nvGrpSpPr', children=[x('p:cNvPr', {'id':'1','name':''}), x('p:cNvGrpSpPr'), x('p:nvPr')]), x('p:grpSpPr')])
    for it in items: tree.append(it)
    return x('p:sld', {'showMasterSp':'1'}, children=[x('p:cSld', children=[tree]), x('p:clrMapOvr', children=[x('a:masterClrMapping')])])

def build_deck():
    home, catalog, mobile = make_site_images()
    slides=[]; media=[]
    def add_slide(title, kicker, content, bg=BG):
        items=[shape(0,0,W,H,fill=bg), shape(.55,.35,12.25,.02,fill=LINE), shape(.6,.18,12,.18,text='HCI · SABUH MAS CATERING',style=font(8,True,TERR)), shape(.6,.65,12,0.6,text=title,style=font(27,True,INK))]
        if kicker: items.append(shape(.6,1.3,12,.25,text=kicker,style=font(10,False,MUTED)))
        items.extend(content); slides.append(items)
    # Cover
    slides.append([shape(0,0,W,H,fill=INK), shape(.65,.6,6.4,1.15,text='Human-Computer\nInteraction',style=font(34,True,WHITE)), shape(.7,2.15,5.8,.75,text='Perancangan UI/UX Website\nSabuh Mas Catering',style=font(22,False,'E8DCCB')), shape(.7,3.25,5.8,.3,text='Website High-Fidelity · HTML · CSS · JavaScript',style=font(11,True,TERR)), shape(.7,6.62,6.4,.3,text='Profil usaha · katalog layanan · navigasi · pemesanan',style=font(10,False,'E8DCCB')), shape(7.05,.72,5.65,5.9,fill='F6F1E8',line=TERR,radius=True), image_shape(7.15,.82,5.45,5.7,'rId1')]); media.append(home)
    add_slide('Latar Belakang','Mengapa antarmuka ini dirancang?', [shape(.7,1.8,4,.55,text='Konteks usaha',style=font(17,True,TERR)), shape(.7,2.45,4.2,2.2,fill=WHITE,line=LINE,radius=True,text='Sabuh Mas Catering melayani kebutuhan konsumsi di Gianyar, Bali. Website menjadi ruang informasi profil, katalog, dan jalur pemesanan yang lebih terstruktur.',style=font(15,False,INK)), shape(5.3,1.8,3.2,.55,text='Masalah informasi',style=font(17,True,TERR)), shape(5.3,2.45,3.2,2.2,fill=WHITE,line=LINE,radius=True,text='Menu, foto, legalitas, dan alur pesan sebelumnya berisiko tersebar di percakapan manual.',style=font(15,False,INK)), shape(9,1.8,3.5,.55,text='Peluang HCI',style=font(17,True,TERR)), shape(9,2.45,3.5,2.2,fill=WHITE,line=LINE,radius=True,text='Membuat informasi lebih mudah ditemukan, dipindai, dipahami, lalu ditindaklanjuti.',style=font(15,False,INK)), shape(.7,5.2,11.8,.7,fill='EFE4D3',line='D5BDA8',radius=True,text='Prinsip utama: informasi yang jelas → navigasi sederhana → keputusan pemesanan lebih percaya diri.',style=font(18,True,INK),align='c')])
    add_slide('Tujuan Perancangan','Tujuan UI/UX yang diterjemahkan ke dalam antarmuka', [shape(.7,1.8,3.7,3.9,fill=WHITE,line=LINE,radius=True,text='01\n\nMenyatukan profil dan katalog\n\nInformasi usaha, layanan, dan konteks pemesanan disusun dalam struktur yang mudah dipindai.',style=font(16,False,INK)), shape(4.8,1.8,3.7,3.9,fill=WHITE,line=LINE,radius=True,text='02\n\nMemudahkan orientasi pengguna\n\nNavbar konsisten dan tampilan dinamis membantu pengguna berpindah konteks tanpa halaman panjang.',style=font(16,False,INK)), shape(8.9,1.8,3.7,3.9,fill=WHITE,line=LINE,radius=True,text='03\n\nMendorong tindakan yang jelas\n\nCTA katalog dan pemesanan memberi jalur lanjutan tanpa mengarang kontak yang belum dikonfirmasi.',style=font(16,False,INK))])
    add_slide('Identifikasi Pengguna','Sumber: artefak persona dan laporan HCI yang tersedia di project', [shape(.7,1.8,5.3,4.4,fill=WHITE,line=LINE,radius=True,text='PENGGUNA UTAMA\n\nBu Agung — pemilik & admin\n\n• Mengelola katalog dan pesanan\n• Membutuhkan informasi yang praktis\n• Berinteraksi melalui smartphone dan laptop\n• Perlu menjaga kejelasan informasi untuk pelanggan',style=font(15,False,INK)), shape(6.35,1.8,5.9,2.05,fill='EFE4D3',line='D5BDA8',radius=True,text='PENGGUNA SEKUNDER\n\nPelanggan instansi (B2G) dan masyarakat umum (B2C) yang mencari katalog, profil usaha, dan jalur pemesanan.',style=font(15,False,INK)), shape(6.35,4.2,5.9,2.0,fill=WHITE,line=LINE,radius=True,text='CATATAN VALIDITAS\n\nPersona dan kebutuhan berasal dari satu narasumber; kebutuhan pelanggan B2G/B2C di laporan diberi label dugaan dan masih perlu validasi.',style=font(14,False,MUTED))])
    add_slide('Permasalahan UX','Tantangan yang menjadi dasar keputusan desain', [shape(.7,1.8,3.7,3.8,fill=WHITE,line=LINE,radius=True,text='DISCOVER\n\nInformasi usaha perlu ditemukan cepat dari smartphone.\n\n→ Solusi: hero ringkas, label bagian, dan CTA utama.',style=font(16,False,INK)), shape(4.8,1.8,3.7,3.8,fill=WHITE,line=LINE,radius=True,text='EVALUATE\n\nPengguna perlu memahami kategori layanan dan materi foto tanpa membaca blok panjang.\n\n→ Solusi: kartu katalog dan hierarki tipografi.',style=font(16,False,INK)), shape(8.9,1.8,3.7,3.8,fill=WHITE,line=LINE,radius=True,text='ACT\n\nJalur pemesanan harus terlihat, tetapi kontak resmi yang belum tersedia tidak boleh dikarang.\n\n→ Solusi: status konfirmasi dan CTA yang terarah.',style=font(16,False,INK))])
    add_slide('Konsep Desain','Warm editorial interface untuk bisnis catering lokal', [shape(.7,1.8,3.6,3.8,fill='F6F1E8',line=LINE,radius=True,text='PALET WARNA\n\nKrem hangat — ruang utama\nCokelat tua — teks & navigasi\nTerracotta — aksen & CTA\nOlive — aksen pendukung',style=font(17,False,INK)), shape(4.7,1.8,3.6,3.8,fill=WHITE,line=LINE,radius=True,text='TIPOGRAFI\n\nHeading serif/editorial untuk karakter\n\nBody sans-serif untuk keterbacaan, scanning, dan navigasi.',style=font(17,False,INK)), shape(8.7,1.8,3.9,3.8,fill=WHITE,line=LINE,radius=True,text='KOMPONEN\n\n• Navbar konsisten\n• CTA berbentuk tombol\n• Kartu katalog\n• Label bagian\n• Footer informatif\n• Lightbox galeri',style=font(17,False,INK))])
    add_slide('Struktur Navigasi','Sitemap single-page dinamis dengan satu index.html', [shape(4.7,1.8,3.9,.85,fill=INK,radius=True,text='BERANDA\nHero + pengenalan',style=font(17,True,WHITE),align='c'), shape(1.0,3.6,2.7,1.05,fill=WHITE,line=TERR,radius=True,text='PROFIL USAHA\nTentang & informasi',style=font(15,True,INK),align='c'), shape(4.0,3.6,2.7,1.05,fill=WHITE,line=TERR,radius=True,text='KATALOG\n4 kategori + galeri',style=font(15,True,INK),align='c'), shape(7.0,3.6,2.7,1.05,fill=WHITE,line=TERR,radius=True,text='PEMESANAN\nAlur & kontak',style=font(15,True,INK),align='c'), shape(10.0,3.6,2.3,1.05,fill=WHITE,line=TERR,radius=True,text='FOOTER\nAlamat & legal',style=font(15,True,INK),align='c'), shape(1.0,5.35,11.3,.7,fill='EFE4D3',line=LINE,radius=True,text='Klik navbar → JavaScript mengganti view aktif → URL hash tetap dapat dibagikan → tidak reload halaman.',style=font(15,True,INK),align='c')])
    add_slide('Wireframe / Low Fidelity','Status dokumentasi: tidak ditemukan file wireframe asli di workspace', [shape(.8,1.85,5.5,3.9,fill=WHITE,line=LINE,radius=True,text='TIDAK ADA ARTEFAK WIREFRAME TERSIMPAN\n\nTidak ada klaim bahwa wireframe ini pernah dibuat atau diuji.\n\nMateri yang tersedia berupa artefak UX (persona, empathy map, scenario, journey) dan implementasi HTML/CSS.',style=font(17,False,INK),align='c'), shape(7.0,1.85,5.3,3.9,fill='EFE4D3',line=LINE,radius=True,text='FUNGSI WIREFRAME YANG TETAP DITERAPKAN\n\n• Menetapkan urutan informasi\n• Menentukan prioritas CTA\n• Membagi konten ke empat view\n• Memastikan navbar dan footer konsisten\n\nDokumentasi visual wireframe dapat ditambahkan jika tersedia.',style=font(17,False,INK))])
    add_slide('Mid Fidelity','Struktur antarmuka sebelum visual final', [shape(.75,1.9,3.4,3.7,fill=WHITE,line=LINE,radius=True,text='STRUKTUR\n\nHeader\nHero\nSection content\nCards\nFooter',style=font(18,False,INK)), shape(4.95,1.9,3.4,3.7,fill=WHITE,line=LINE,radius=True,text='HIERARKI\n\nLabel → heading → deskripsi → CTA\n\nJarak, garis, dan blok warna membantu scanning.',style=font(18,False,INK)), shape(9.15,1.9,3.4,3.7,fill=WHITE,line=LINE,radius=True,text='KOMPONEN\n\nNavbar aktif\nKartu layanan\nGaleri\nLightbox\nAlur pemesanan',style=font(18,False,INK)), shape(.75,6.0,11.8,.55,fill=INK,radius=True,text='Tahap ini memvalidasi layout, hierarki, dan interaksi utama sebelum detail visual final.',style=font(15,True,WHITE),align='c')])
    add_slide('High Fidelity','Hasil akhir website dengan visual dan interaksi yang sudah diimplementasikan', [image_shape(.7,1.7,11.95,5.55,'rId1')]); media.append(home)
    add_slide('Implementasi UI High-Fidelity','Empat view utama dalam satu antarmuka dinamis', [image_shape(.7,1.75,7.7,4.4,'rId1'), image_shape(9.0,1.75,3.0,4.4,'rId2'), shape(.7,6.35,11.8,.4,text='Beranda: hero & CTA  ·  Profil: konteks usaha  ·  Katalog: kartu + foto  ·  Pemesanan: alur & kontak',style=font(13,True,INK),align='c')]); media.extend([catalog,mobile])
    add_slide('Penerapan Prinsip HCI','Hubungan prinsip dengan fitur nyata yang tersedia', [shape(.7,1.75,3.75,1.25,fill=WHITE,line=LINE,radius=True,text='KONSISTENSI\nNavbar, warna, dan footer dipakai lintas view.',style=font(15,False,INK)), shape(4.8,1.75,3.75,1.25,fill=WHITE,line=LINE,radius=True,text='VISIBILITY\nCTA, label section, dan status informasi terlihat jelas.',style=font(15,False,INK)), shape(8.9,1.75,3.75,1.25,fill=WHITE,line=LINE,radius=True,text='FEEDBACK\nActive nav, transisi view, dan lightbox memberi respons.',style=font(15,False,INK)), shape(.7,3.4,3.75,1.25,fill=WHITE,line=LINE,radius=True,text='READABILITY\nKontras warna dan hierarchy mendukung scanning.',style=font(15,False,INK)), shape(4.8,3.4,3.75,1.25,fill=WHITE,line=LINE,radius=True,text='USABILITY\nKatalog dikelompokkan menjadi empat layanan.',style=font(15,False,INK)), shape(8.9,3.4,3.75,1.25,fill=WHITE,line=LINE,radius=True,text='RESPONSIVE\nNavbar hamburger dan layout mobile disediakan.',style=font(15,False,INK)), shape(.7,5.4,11.8,.65,fill='EFE4D3',line=LINE,radius=True,text='Prinsip HCI diterapkan pada keputusan antarmuka, bukan sekadar dekorasi visual.',style=font(16,True,INK),align='c')])
    add_slide('Evaluasi Desain','Yang dapat diklaim dari artefak dan implementasi yang tersedia', [shape(.8,1.8,5.5,3.95,fill=WHITE,line=LINE,radius=True,text='SUDAH TERSEDIA\n\n✓ Review struktur navigasi dan konten\n✓ Implementasi HTML, CSS, JavaScript\n✓ Pemeriksaan responsive layout secara teknis\n✓ Galeri dan navigasi dinamis di source\n\nCatatan: ini bukan hasil usability testing formal.',style=font(16,False,INK)), shape(7.0,1.8,5.3,3.95,fill='EFE4D3',line=LINE,radius=True,text='BELUM TERSEDIA\n\n— Data usability testing pengguna\n— Skor SUS atau metrik task success\n— Feedback pelanggan terukur\n— Validasi langsung persona B2G/B2C\n\nTahap lanjutan: uji dengan 3–5 pengguna dan pemilik usaha.',style=font(16,False,INK))])
    add_slide('Kesimpulan','UI/UX Sabuh Mas Catering sebagai studi penerapan HCI', [shape(.8,1.8,3.55,3.8,fill=WHITE,line=LINE,radius=True,text='01\n\nInformasi usaha dipusatkan dalam struktur yang lebih mudah ditemukan.',style=font(18,False,INK)), shape(4.9,1.8,3.55,3.8,fill=WHITE,line=LINE,radius=True,text='02\n\nWarna, tipografi, kartu, dan navigasi membangun interface High Fidelity yang konsisten.',style=font(18,False,INK)), shape(9.0,1.8,3.55,3.8,fill=WHITE,line=LINE,radius=True,text='03\n\nPrinsip HCI sudah diterapkan pada layout dan interaksi; validasi pengguna formal masih menjadi pekerjaan berikutnya.',style=font(18,False,INK)), shape(.8,6.1,11.75,.6,fill=INK,radius=True,text='Website: sabuh-mas-catering.vercel.app',style=font(16,True,WHITE),align='c')])

    # add media relationship ids in order of slides; slides that use images reference rId1/rId2 locally
    media_by_slide = {1:[home], 10:[home], 11:[catalog,mobile]}
    root = WORK / 'pptx';
    if root.exists(): shutil.rmtree(root)
    (root/'ppt/slides/_rels').mkdir(parents=True, exist_ok=True); (root/'ppt/slides').mkdir(parents=True, exist_ok=True); (root/'ppt/media').mkdir(parents=True, exist_ok=True); (root/'ppt/_rels').mkdir(parents=True, exist_ok=True); (root/'_rels').mkdir(parents=True, exist_ok=True); (root/'ppt/slideLayouts/_rels').mkdir(parents=True, exist_ok=True); (root/'ppt/slideMasters/_rels').mkdir(parents=True, exist_ok=True); (root/'ppt/theme').mkdir(parents=True, exist_ok=True)
    for idx, items in enumerate(slides, 1):
        rels = media_by_slide.get(idx, [])
        out_items=[]; # rebuild images are already embedded through relationship ids
        ET.ElementTree(slide_xml(items)).write(root/f'ppt/slides/slide{idx}.xml', encoding='utf-8', xml_declaration=True)
        relxml=x('Relationships' if False else 'a:root')
        # use standalone relationships namespace
        R=ET.Element('{http://schemas.openxmlformats.org/package/2006/relationships}Relationships')
        if rels:
            for j,p in enumerate(rels,1):
                target=f'../media/{p.name}'; R.append(ET.Element('{http://schemas.openxmlformats.org/package/2006/relationships}Relationship', {'Id':f'rId{j}','Type':'http://schemas.openxmlformats.org/officeDocument/2006/relationships/image','Target':target})); shutil.copy2(p, root/'ppt/media'/p.name)
        ET.ElementTree(R).write(root/f'ppt/slides/_rels/slide{idx}.xml.rels', encoding='utf-8', xml_declaration=True)
    # common presentation package files
    types='''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Default Extension="png" ContentType="image/png"/><Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/><Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/><Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/><Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>''' + ''.join(f'<Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>' for i in range(1,len(slides)+1)) + '</Types>'
    (root/'[Content_Types].xml').write_text(types, encoding='utf-8')
    (root/'_rels/.rels').write_text('<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/></Relationships>', encoding='utf-8')
    slide_ids=''.join(f'<p:sldId id="{255+i}" r:id="rId{i}"/>' for i in range(1,len(slides)+1))
    (root/'ppt/presentation.xml').write_text(f'''<?xml version="1.0" encoding="UTF-8"?><p:presentation xmlns:a="{NS['a']}" xmlns:r="{NS['r']}" xmlns:p="{NS['p']}" ><p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst><p:sldIdLst>{slide_ids}</p:sldIdLst><p:sldSz cx="12192000" cy="6858000" type="screen16x9"/><p:notesSz cx="6858000" cy="9144000"/></p:presentation>''', encoding='utf-8')
    pres_rels=['<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>'] + [f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{i}.xml"/>' for i in range(1,len(slides)+1)]
    (root/'ppt/_rels/presentation.xml.rels').write_text('<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'+''.join(pres_rels)+'</Relationships>', encoding='utf-8')
    (root/'ppt/slideMasters/slideMaster1.xml').write_text(f'''<?xml version="1.0" encoding="UTF-8"?><p:sldMaster xmlns:a="{NS['a']}" xmlns:r="{NS['r']}" xmlns:p="{NS['p']}"><p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/></p:spTree></p:cSld><p:sldLayoutIdLst><p:sldLayoutId id="1" r:id="rId1"/></p:sldLayoutIdLst><p:txStyles><p:titleStyle/><p:bodyStyle/><p:otherStyle/></p:txStyles></p:sldMaster>''', encoding='utf-8')
    (root/'ppt/slideMasters/_rels/slideMaster1.xml.rels').write_text('<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/></Relationships>', encoding='utf-8')
    (root/'ppt/slideLayouts/slideLayout1.xml').write_text(f'''<?xml version="1.0" encoding="UTF-8"?><p:sldLayout xmlns:a="{NS['a']}" xmlns:r="{NS['r']}" xmlns:p="{NS['p']}" type="blank"><p:cSld name="Blank"><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/></p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sldLayout>''', encoding='utf-8')
    (root/'ppt/slideLayouts/_rels/slideLayout1.xml.rels').write_text('<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="../slideMasters/slideMaster1.xml"/></Relationships>', encoding='utf-8')
    (root/'ppt/theme/theme1.xml').write_text(f'''<?xml version="1.0" encoding="UTF-8"?><a:theme xmlns:a="{NS['a']}" name="Sabuh Mas"><a:themeElements><a:clrScheme name="Sabuh"><a:dk1><a:srgbClr val="{INK}"/></a:dk1><a:lt1><a:srgbClr val="{WHITE}"/></a:lt1><a:dk2><a:srgbClr val="{TERR}"/></a:dk2><a:lt2><a:srgbClr val="{BG}"/></a:lt2><a:accent1><a:srgbClr val="{ORANGE}"/></a:accent1><a:accent2><a:srgbClr val="{OLIVE}"/></a:accent2><a:accent3><a:srgbClr val="{LINE}"/></a:accent3><a:accent4><a:srgbClr val="{MUTED}"/></a:accent4><a:accent5><a:srgbClr val="{TERR}"/></a:accent5><a:accent6><a:srgbClr val="{INK}"/></a:accent6><a:hlink><a:srgbClr val="{TERR}"/></a:hlink><a:folHlink><a:srgbClr val="{ORANGE}"/></a:folHlink></a:clrScheme><a:fontScheme name="Sabuh"><a:majorFont><a:latin typeface="Aptos Display"/></a:majorFont><a:minorFont><a:latin typeface="Aptos"/></a:minorFont></a:fontScheme><a:fmtScheme name="Sabuh"><a:fillStyleLst/><a:lnStyleLst/><a:effectStyleLst/><a:bgFillStyleLst/></a:fmtScheme></a:themeElements></a:theme>''', encoding='utf-8')
    with ZipFile(OUT, 'w', ZIP_DEFLATED) as z:
        for p in root.rglob('*'):
            if p.is_file(): z.write(p, p.relative_to(root).as_posix())
    print(OUT)

if __name__ == '__main__': build_deck()
