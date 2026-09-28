"""Shared HTML shell (header, nav, footer) for every Chatudo page."""

from icons import icon

NAV_ITEMS = [
    ("home", "หน้าแรก", "/"),
    ("pricing", "ราคา", "/pricing/"),
]

FOOTER_LEGAL = [
    ("/privacy/", "นโยบายความเป็นส่วนตัว"),
    ("/terms/", "ข้อตกลงการใช้บริการ"),
    ("/data-deletion/", "วิธีขอลบข้อมูล"),
]


def nav_link(active_key, key, label, href):
    current = ' aria-current="page"' if key == active_key else ""
    return f'<a href="{href}"{current}>{label}</a>'


def render_header(active_key: str, contact_href: str) -> str:
    nav_html = "\n      ".join(
        nav_link(active_key, key, label, href) for key, label, href in NAV_ITEMS
    )
    return f"""
<a class="skip-link" href="#main">ข้ามไปเนื้อหาหลัก</a>
<header class="site-header">
  <div class="container">
    <a class="brand" href="/">
      <img src="/assets/img/logo-mark.png" alt="" width="30" height="30">
      <span class="brand-word">chatudo</span>
    </a>
    <input type="checkbox" id="nav-toggle" class="nav-toggle">
    <nav class="main-nav" aria-label="เมนูหลัก">
      {nav_html}
      <a href="{contact_href}" class="nav-contact-mobile">ติดต่อเรา</a>
    </nav>
    <div class="header-cta">
      <a href="{contact_href}" class="btn btn-primary btn-sm">
        <span class="btn-label-full">คุยกับทีมงาน</span><span class="btn-label-short">ติดต่อ</span>
      </a>
      <label for="nav-toggle" class="nav-toggle-label" aria-hidden="false" role="button" tabindex="0">
        <span class="visually-hidden">เปิดเมนู</span>
        <span class="icon-menu">{icon('menu')}</span>
        <span class="icon-close">{icon('close')}</span>
      </label>
    </div>
  </div>
</header>
"""


def render_footer(config: dict, ph) -> str:
    legal_html = "\n          ".join(
        f'<li><a href="{href}">{label}</a></li>' for href, label in FOOTER_LEGAL
    )
    contact_email = ph("contact_email", "อีเมลติดต่อ")
    contact_phone = ph("contact_phone", "เบอร์โทรติดต่อ")
    legal_name = ph("legal_name", "ชื่อนิติบุคคล")
    address = ph("registered_address", "ที่อยู่จดทะเบียน")
    return f"""
<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <a class="brand" href="/">
          <img src="/assets/img/logo-mark.png" alt="" width="26" height="26">
          <span class="brand-word">chatudo</span>
        </a>
        <p>ระบบผู้ช่วยแอดมินสำหรับร้านค้าที่ขายผ่านแชท AI ร่างคำตอบ แอดมินของร้านเป็นคนตรวจและกดส่งเองเสมอ</p>
      </div>
      <div class="footer-col">
        <h3>บริการ</h3>
        <ul>
          <li><a href="/">หน้าแรก</a></li>
          <li><a href="/pricing/">ราคา</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h3>ข้อกฎหมาย</h3>
        <ul>
          {legal_html}
        </ul>
      </div>
    </div>
    <div class="footer-grid" style="margin-top:-8px">
      <div class="footer-col" style="grid-column:1/-1">
        <h3>ติดต่อ</h3>
        <ul style="flex-direction:row;flex-wrap:wrap;gap:22px">
          <li>อีเมล {contact_email}</li>
          <li>โทร {contact_phone}</li>
          <li>{legal_name} &middot; {address}</li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; 2026 Chatudo. สงวนลิขสิทธิ์.</span>
      <span>chatudo.com &middot; เอกสารฉบับร่าง รอการยืนยันข้อมูลก่อนเผยแพร่จริง</span>
    </div>
  </div>
</footer>
"""


def base_page(*, lang="th", path, title, description, og_title, og_description,
              body_html, active_key, config, ph, extra_head="") -> str:
    header = render_header(active_key, "/#contact" if path != "/" else "#contact")
    footer = render_footer(config, ph)
    canonical = f"https://chatudo.com{path}"
    og_image = "https://chatudo.com/assets/img/cover-hero.png"
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Chatudo">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{og_description}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_image}">
<meta property="og:locale" content="th_TH">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#B5502E">
<link rel="icon" href="/assets/img/logo-mark-tile.png" type="image/png">
<link rel="apple-touch-icon" href="/assets/img/logo-mark-tile.png">
<link rel="stylesheet" href="/css/style.css">
{extra_head}</head>
<body>
{header}
<main id="main">
{body_html}
</main>
{footer}
</body>
</html>
"""
