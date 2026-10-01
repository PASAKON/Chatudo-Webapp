#!/usr/bin/env python3
"""Chatudo static site generator.

Stdlib only, runs fully offline. Reads site.config.json (the single
source of truth for facts the CEO has not confirmed yet) and writes
plain HTML into public/. Re-run after editing site.config.json or any
content in this file:

    python3 build/render.py
"""
import json
import pathlib
import shutil

from icons import icon
from layout import base_page

ROOT = pathlib.Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
CONFIG = json.loads((ROOT / "site.config.json").read_text(encoding="utf-8"))


def ph(key: str, label: str) -> str:
    """Return the confirmed value for `key`, or a visible placeholder.

    Every unconfirmed fact in site.config.json renders on the page as
    literal text `[รอยืนยัน: <label>]` wrapped in a `.ph` style so it is
    impossible to miss during review.
    """
    value = CONFIG.get(key)
    if value:
        return str(value)
    return f'<span class="ph">[รอยืนยัน: {label}]</span>'


def ph_en(key: str, label: str) -> str:
    """English-language counterpart to ph(): same config value, or a
    visible `[TBC: <label>]` placeholder for the /en/ legal pages."""
    value = CONFIG.get(key)
    if value:
        return str(value)
    return f'<span class="ph">[TBC: {label}]</span>'


# ---------------------------------------------------------------------------
# Shared fragments
# ---------------------------------------------------------------------------

def meta_note_html() -> str:
    return f"""
<div class="notice">
  <span class="icon">{icon('info')}</span>
  <span>การเชื่อมต่อ Facebook Messenger และ Instagram จะเปิดใช้งานได้หลังจาก Meta อนุมัติแอปของเราแล้ว
  ช่วงแรกเปิดให้ใช้เฉพาะ LINE OA และเฉพาะแพ็ก Founding กับ Starter ส่วน Messenger และ IG จะเปิดทันทีที่ Meta อนุมัติแอปของเรา ตอนนี้ยังบอกวันไม่ได้</span>
</div>
"""


CONTACT_SECTION = None  # set below after helper defs


def contact_section() -> str:
    line_url = CONFIG.get("line_oa_url")
    contact_email = CONFIG.get("contact_email")
    line_html = (
        f'<a class="btn btn-primary" href="{line_url}">คุยผ่าน LINE OA</a>'
        if line_url
        else f'<span class="btn btn-primary" aria-disabled="true">คุยผ่าน LINE OA {ph("line_oa_url", "ลิงก์ LINE OA")}</span>'
    )
    email_html = (
        f'<a class="btn btn-outline" href="mailto:{contact_email}">อีเมลหาเรา {contact_email}</a>'
        if contact_email
        else f'<span class="btn btn-outline" aria-disabled="true">อีเมลหาเรา {ph("contact_email", "อีเมลติดต่อ")}</span>'
    )
    return f"""
<section id="contact">
  <div class="container">
    <div class="cta-band">
      <h2>พร้อมให้ Chatudo ช่วยดูแลแชทร้านคุณหรือยัง</h2>
      <p>ทักมาเล่าให้ฟังว่าร้านคุณขายผ่านช่องทางไหน แชทเยอะช่วงไหน ทีมงานจะช่วยดูว่าแพ็กไหนเหมาะกับร้านคุณที่สุด</p>
      <div class="cta-actions">
        {line_html}
        {email_html}
      </div>
    </div>
  </div>
</section>
"""


# ---------------------------------------------------------------------------
# Home page
# ---------------------------------------------------------------------------

JOBS = [
    ("moon", "ร่างคำตอบรอไว้ตั้งแต่ลูกค้าทักตอนดึก", "ลูกค้าทักมาช่วง 22:00 ถึง 09:00 วันหยุด หรือช่วงแชทล้นมือ Chatudo ช่วยร่างคำตอบให้ทันที แอดมินเปิดมาเช็กแล้วกดส่งได้ทันที"),
    ("pencil", "ร่างคำตอบให้แอดมิน", "AI อ่านแชทแล้วร่างคำตอบให้พร้อมส่ง แอดมินเช็กแล้วกดส่งได้ในคลิกเดียว ไม่ต้องพิมพ์เองทุกข้อความ"),
    ("bell", "ตามลูกค้าที่เงียบไป", "ลูกค้าทักมาแล้วหาย Chatudo ช่วยส่งข้อความตามให้ ก่อนที่ออเดอร์นั้นจะหลุดมือไปเฉยๆ (ฟีเจอร์นี้อยู่ในแพ็ก Pro ที่กำลังพัฒนา ยังไม่เปิดรับสมัคร)"),
    ("book", "ความรู้ไม่หายไปกับแอดมิน", "คำตอบ โปรโมชัน และข้อมูลร้านถูกเก็บไว้ในระบบ แอดมินลาออกหรือเปลี่ยนคนก็ยังตอบลูกค้าได้ต่อเนื่อง"),
    ("chart", "เจ้าของร้านเห็นภาพรวม", "ดูได้ว่าแชทไหนปิดการขายแล้ว แชทไหนยังค้างอยู่ ไม่ต้องไล่เปิดทีละแชทเอง (ฟีเจอร์นี้อยู่ในแพ็ก Pro ที่กำลังพัฒนา ยังไม่เปิดรับสมัคร)"),
]

STEPS = [
    ("link", "เชื่อมต่อ LINE OA ของร้าน", "เชื่อมบัญชี LINE OA ที่ร้านใช้อยู่กับ Chatudo ใช้เวลาไม่นาน ไม่ต้องเปลี่ยนเบอร์หรือย้ายลูกค้าไปที่ใหม่"),
    ("book", "ตั้งค่าข้อมูลร้านให้", "ทีมงานตั้งค่าจากข้อมูลบนเพจและเว็บของร้าน รวมถึงรายการราคาที่ร้านส่งให้ ตอนติดตั้ง"),
    ("check", "แอดมินเช็กแล้วกดส่ง", "แอดมินของร้านเป็นคนตรวจและกดส่งคำตอบที่ AI ร่างไว้เองทุกข้อความ"),
]

SEGMENTS = [
    ("cap", "คอร์สเรียนออนไลน์ / งานสัมมนา", "ร่างคำตอบเรื่องหลักสูตร ตารางเรียน และการชำระเงินให้แอดมินเช็กแล้วกดส่ง"),
    ("calendar", "ร้านที่ต้องจองคิว", "ร้านทำผม ทำเล็บ สปา ที่ลูกค้าทักมาถามคิวว่างตลอดวัน"),
    ("bag", "ร้านขายของผ่านแชท", "ร้านที่ปิดการขายในแชทเป็นหลัก ต้องตอบไว ไม่ปล่อยให้ลูกค้ารอ"),
    ("sparkle", "คลินิกความงาม", "ตอบคำถามเรื่องบริการและนัดหมาย พร้อมส่งต่อให้แอดมินดูแลเคสที่ต้องใช้ดุลยพินิจ"),
]


def render_home() -> str:
    jobs_html = "\n".join(
        f"""
    <div class="card">
      <div class="icon">{icon(ic)}</div>
      <h3>{title}</h3>
      <p>{body}</p>
    </div>""" for ic, title, body in JOBS
    )

    steps_html = "\n".join(
        f"""
    <div class="step">
      <span class="step-num">{i}</span>
      <h3>{title}</h3>
      <p>{body}</p>
    </div>""" for i, (ic, title, body) in enumerate(STEPS, start=1)
    )

    segments_html = "\n".join(
        f"""
        <li><span class="icon">{icon(ic)}</span> {title}</li>""" for ic, title, _ in SEGMENTS
    )

    pricing_teaser = """
<section class="alt">
  <div class="container">
    <div class="section-head">
      <h2>ราคาเรียบง่าย เลือกได้ตามขนาดร้าน</h2>
      <p>เริ่มจากแพ็กเดียวก็ใช้ได้ อยากได้ครบทุกช่องทางค่อยอัปเกรดทีหลัง</p>
    </div>
    <div class="hero-ctas">
      <a class="btn btn-primary" href="/pricing/">ดูราคาทั้งหมด <span class="icon" style="width:18px;height:18px;display:inline-flex">""" + icon('arrow-right') + """</span></a>
    </div>
  </div>
</section>
"""

    body = f"""
<section class="hero">
  <div class="container">
    <div class="hero-copy">
      <span class="eyebrow">{icon('sparkle')} ระบบผู้ช่วยแอดมิน</span>
      <h1>ผู้ช่วยแอดมินที่ร่างคำตอบแชทให้ทันที</h1>
      <p class="hero-lede">Chatudo คือระบบผู้ช่วยแอดมินสำหรับร้านที่ขายผ่านแชท AI ร่างคำตอบให้ แอดมินของร้านเช็กแล้วกดส่งเอง ลูกค้าได้รับคำตอบเร็วขึ้น แอดมินไม่ต้องตอบซ้ำๆ ทุกข้อความเอง</p>
      <div class="hero-ctas">
        <a class="btn btn-primary" href="/pricing/">ดูราคา</a>
        <a class="btn btn-outline" href="#contact">คุยกับทีมงาน</a>
      </div>
      <div class="hero-trust">{icon('users')} ออกแบบมาสำหรับร้านที่มีแอดมินตอบแชทอยู่แล้ว และอยากให้ทำงานได้เบาลง</div>
    </div>
    <div class="hero-art">
      <img src="/assets/img/logo-mark.png" alt="" width="100" height="100">
      <span class="hero-art-badge">{icon('check')} แอดมินอนุมัติก่อนส่งเป็นค่าเริ่มต้น</span>
      <p style="color:var(--warm-gray);font-size:0.95rem">AI ร่าง แอดมินของร้านตรวจและกดส่งเองทุกข้อความ</p>
    </div>
  </div>
</section>

<section class="alt" id="jobs">
  <div class="container">
    <div class="section-head">
      <h2>สิ่งที่ Chatudo ช่วยร้านคุณ</h2>
      <p>ช่วยแอดมินตรงจุดที่เหนื่อยที่สุด ไม่ใช่แทนแอดมิน</p>
    </div>
    <div class="grid">{jobs_html}
    </div>
  </div>
</section>

<section id="how">
  <div class="container">
    <div class="section-head">
      <h2>ทำงานยังไง</h2>
      <p>เริ่มใช้งานได้ใน 3 ขั้นตอน</p>
    </div>
    <div class="steps">{steps_html}
    </div>
  </div>
</section>

<section class="alt" id="segments">
  <div class="container">
    <div class="section-head">
      <h2>เหมาะกับร้านแบบไหน</h2>
      <p>ร้านที่มีแชทเข้าทุกวันและอยากให้ลูกค้ารอน้อยลง</p>
    </div>
    <ul class="segment-list">{segments_html}
    </ul>
  </div>
</section>

{pricing_teaser}
{contact_section()}
"""
    return base_page(
        path="/",
        title="Chatudo · ระบบผู้ช่วยแอดมินสำหรับร้านค้าที่ขายผ่านแชท",
        description="Chatudo คือระบบผู้ช่วยแอดมินสำหรับร้านค้าที่ขายผ่าน LINE OA, Facebook Messenger และ Instagram AI ร่างคำตอบ แอดมินของร้านตรวจและกดส่งเอง",
        og_title="Chatudo · ระบบผู้ช่วยแอดมิน",
        og_description="AI ร่างคำตอบ แอดมินของร้านตรวจก่อนส่งทุกข้อความ ผู้ช่วยแอดมินสำหรับร้านที่ขายผ่านแชท",
        body_html=body,
        active_key="home",
        config=CONFIG,
        ph=ph,
    )


# ---------------------------------------------------------------------------
# Pricing page
# ---------------------------------------------------------------------------

PLANS = [
    {
        "name": "Founding",
        "badge": "ร้านนำร่องกลุ่มแรก จำนวนจำกัด",
        "price": "฿990",
        "period": "/เดือน",
        "note": "ใช้ฟรี 14 วัน หลังจากนั้น 990 บาทต่อเดือน 2 เดือนแรก แล้วเป็น 1,990 บาทต่อเดือน "
                "สำหรับร้านนำร่องกลุ่มแรก ถ้าผลออกมาดี ขอเขียนเป็นเคสสั้นๆ โดยร้านอ่านก่อนเผยแพร่ทุกครั้ง",
        "features": ["ฟีเจอร์เท่าแพ็ก Starter"],
        "featured": False,
    },
    {
        "name": "Starter",
        "badge": None,
        "price": "฿1,990",
        "period": "/เดือน",
        "note": "เริ่มต้นใช้งาน 1 ช่องทาง",
        "features": [
            "1 ช่องทาง (LINE OA)",
            "AI ร่างคำตอบ แอดมินตรวจแล้วกดส่งเองทุกข้อความ",
            "เรื่องที่บอทไม่แน่ใจ ส่งกลับให้แอดมิน พร้อมแจ้งเตือนทาง LINE",
            "ใช้ฟรี 14 วันแรก ไม่ตัดเงินอัตโนมัติ",
        ],
        "featured": False,
    },
    {
        "name": "Pro",
        "badge": "เร็วๆ นี้ ยังไม่เปิดรับสมัคร",
        "badge_muted": True,
        "price": "฿3,990",
        "period": "/เดือน",
        "note": "ครบทุกช่องทางแชทหลัก",
        "features": [
            "LINE OA + Facebook Messenger + Instagram (หลัง Meta อนุมัติ)",
            "ตามลูกค้าที่ทักมาแล้วเงียบไป (กำลังพัฒนา)",
            "รายงานสรุปให้เจ้าของร้าน (กำลังพัฒนา)",
        ],
        "featured": True,
    },
    {
        "name": "Business",
        "badge": "เร็วๆ นี้ ยังไม่เปิดรับสมัคร",
        "badge_muted": True,
        "price": "฿9,900",
        "period": "/เดือน",
        "note": "สำหรับร้านที่มีหลายเพจหรือหลายสาขา",
        "features": ["หลายเพจ / หลายสาขาในบัญชีเดียว", "ทีมงานติดตั้งให้ถึงพร้อมใช้งาน"],
        "featured": False,
    },
]


def render_price_card(plan: dict) -> str:
    badge_cls = "badge badge-muted" if plan.get("badge_muted") else "badge"
    badge_html = f'<span class="{badge_cls}">{plan["badge"]}</span>' if plan["badge"] else ""
    features_html = "\n".join(
        f'<li><span class="icon">{icon("check")}</span> {f}</li>' for f in plan["features"]
    )
    cls = "price-card featured" if plan["featured"] else "price-card"
    return f"""
    <div class="{cls}">
      {badge_html}
      <span class="plan-name">{plan['name']}</span>
      <span class="plan-price">{plan['price']} <small>{plan['period']}</small></span>
      <p class="plan-note">{plan['note']}</p>
      <ul>{features_html}
      </ul>
    </div>"""


def render_pricing() -> str:
    cards = "\n".join(render_price_card(p) for p in PLANS)
    body = f"""
<section>
  <div class="container">
    <div class="section-head">
      <h2>ราคา Chatudo</h2>
      <p>เลือกแพ็กตามช่องทางและขนาดร้าน</p>
    </div>
    <div class="pricing-grid">{cards}
    </div>
    {meta_note_html()}
    <div class="notice">
      <span class="icon">{icon('info')}</span>
      <span>{ph('vat_note', 'ราคารวม VAT หรือไม่')}</span>
    </div>
  </div>
</section>

<section class="alt">
  <div class="container">
    <div class="section-head">
      <h2>คำถามที่พบบ่อย</h2>
    </div>
    <div class="grid">
      <div class="card">
        <h3>Chatudo ตอบแทนแอดมินเลยไหม</h3>
        <p>ไม่ใช่ระบบตอบอัตโนมัติเต็มรูปแบบ AI ร่างคำตอบให้ แอดมินของร้านเป็นคนตรวจและกดส่งเองทุกข้อความ</p>
      </div>
      <div class="card">
        <h3>ใช้ Messenger กับ IG ได้เลยไหม</h3>
        <p>ยังใช้ไม่ได้ในตอนนี้ รอ Meta อนุมัติแอปของเราก่อน ตอนนี้ใช้งานผ่าน LINE OA</p>
      </div>
    </div>
  </div>
</section>

{contact_section()}
"""
    return base_page(
        path="/pricing/",
        title="ราคา Chatudo · Founding, Starter, Pro, Business",
        description="ราคา Chatudo แพ็ก Founding ฿990 สองเดือนแรก Starter ฿1,990 Pro ฿3,990 Business ฿9,900 ต่อเดือน เลือกได้ตามช่องทางและขนาดร้าน",
        og_title="ราคา Chatudo",
        og_description="แพ็กเรียบง่าย Starter ฿1,990 ต่อเดือน เลือกได้ตามช่องทางและขนาดร้าน",
        body_html=body,
        active_key="pricing",
        config=CONFIG,
        ph=ph,
    )


# ---------------------------------------------------------------------------
# Legal pages
# ---------------------------------------------------------------------------

def legal_meta(effective_label="วันที่มีผลบังคับใช้") -> str:
    return f'<p class="legal-meta">มีผลบังคับใช้ตั้งแต่วันที่ {ph("effective_date", effective_label)}</p>'


def render_privacy() -> str:
    email = ph("contact_email", "อีเมลติดต่อ")
    phone = ph("contact_phone", "เบอร์โทรติดต่อ")
    legal_name = ph("legal_name", "ชื่อนิติบุคคล")
    address = ph("registered_address", "ที่อยู่จดทะเบียน")
    retention = ph("data_retention_period", "ระยะเวลาเก็บข้อมูล")
    body = f"""
<section>
  <div class="container legal-wrap">
    <h1>นโยบายความเป็นส่วนตัว</h1>
    {legal_meta()}
    <p class="legal-lang-link"><a href="/en/privacy/">English version</a></p>
    <div class="legal-toc">
      <p>สารบัญ</p>
      <ol>
        <li><a href="#collect">ข้อมูลที่เราเก็บ</a></li>
        <li><a href="#purpose">วัตถุประสงค์ในการใช้ข้อมูล</a></li>
        <li><a href="#basis">ฐานทางกฎหมาย</a></li>
        <li><a href="#processors">ผู้ประมวลผลข้อมูล</a></li>
        <li><a href="#transfer">การโอนข้อมูลข้ามประเทศ</a></li>
        <li><a href="#retention">ระยะเวลาการเก็บข้อมูล</a></li>
        <li><a href="#security">มาตรการความปลอดภัย</a></li>
        <li><a href="#rights">สิทธิของเจ้าของข้อมูล</a></li>
        <li><a href="#deletion">วิธีขอลบข้อมูล</a></li>
        <li><a href="#contact">ติดต่อเรา</a></li>
      </ol>
    </div>

    <p>Chatudo (&ldquo;เรา&rdquo;) ให้บริการระบบผู้ช่วยแอดมินสำหรับร้านค้าที่ขายผ่านแชท นโยบายนี้อธิบายว่าเราเก็บ ใช้
    และดูแลข้อมูลส่วนบุคคลของลูกค้าที่แชทกับร้านค้าที่ใช้บริการ Chatudo อย่างไร ตามพระราชบัญญัติคุ้มครองข้อมูลส่วนบุคคล พ.ศ. 2562 (PDPA)</p>

    <h2 id="collect">1. ข้อมูลที่เราเก็บ</h2>
    <ul>
      <li>ข้อความสนทนาระหว่างร้านค้ากับลูกค้าของร้าน ที่ส่งผ่านช่องทางที่เชื่อมต่อกับ Chatudo (เช่น LINE OA, Facebook Messenger, Instagram)</li>
      <li>รหัสประจำตัวผู้ใช้บนแพลตฟอร์มนั้นๆ (platform user ID)</li>
      <li>ชื่อที่แสดง (display name) และรูปโปรไฟล์ หากแพลตฟอร์มส่งข้อมูลนี้มาให้</li>
    </ul>

    <h2 id="purpose">2. วัตถุประสงค์ในการใช้ข้อมูล</h2>
    <ul>
      <li>ร่างและส่งคำตอบแทนร้านค้าที่ใช้บริการ Chatudo</li>
      <li>ส่งต่อบทสนทนาให้แอดมินของร้านตรวจสอบและดำเนินการต่อ (handoff)</li>
      <li>ปรับปรุงคุณภาพการให้บริการ เช่น ความแม่นยำของคำตอบที่ร่างให้</li>
    </ul>

    <h2 id="basis">3. ฐานทางกฎหมายในการประมวลผลข้อมูล</h2>
    <p>เราประมวลผลข้อมูลโดยอาศัยฐานความจำเป็นเพื่อปฏิบัติตามสัญญาระหว่างร้านค้ากับ Chatudo และฐานประโยชน์โดยชอบด้วยกฎหมายในการให้บริการตอบแชทแทนร้านค้า
    ในกรณีที่กฎหมายกำหนดให้ต้องขอความยินยอมเพิ่มเติม เราจะขอความยินยอมจากเจ้าของข้อมูลตามขั้นตอนที่กฎหมายกำหนด</p>

    <h2 id="processors">4. ผู้ประมวลผลข้อมูล</h2>
    <p>เราใช้บริการผู้ให้บริการภายนอกเพื่อประมวลผลข้อมูลในนามของเรา ได้แก่ ผู้ให้บริการฐานข้อมูลและโฮสติ้งบนคลาวด์
    และผู้ให้บริการโมเดล AI ที่ใช้ร่างคำตอบ ผู้ให้บริการเหล่านี้ประมวลผลข้อมูลตามคำสั่งของเราเท่านั้น</p>

    <h2 id="transfer">5. การโอนข้อมูลข้ามประเทศ</h2>
    <p>ผู้ประมวลผลข้อมูลบางรายที่ระบุในข้อ 4 อาจตั้งอยู่นอกประเทศไทย ในกรณีที่มีการโอนข้อมูลออกนอกประเทศ
    เราจะดำเนินการให้เป็นไปตามมาตรฐานการคุ้มครองข้อมูลที่ PDPA กำหนด</p>

    <h2 id="retention">6. ระยะเวลาการเก็บข้อมูล</h2>
    <p>{retention} เว้นแต่กฎหมายจะกำหนดให้เก็บนานกว่านั้น หรือเจ้าของข้อมูลร้องขอให้ลบก่อนกำหนด</p>
    <p>{ph("backup_retention_note", "ระยะเวลาเก็บสำเนาสำรอง")}</p>

    <h2 id="security">7. มาตรการความปลอดภัย</h2>
    <p>เรามีมาตรการทางเทคนิคและการบริหารจัดการเพื่อป้องกันการเข้าถึง เปิดเผย หรือใช้ข้อมูลโดยไม่ได้รับอนุญาต เช่น
    การเข้ารหัสข้อมูลระหว่างส่ง (TLS) และการจำกัดสิทธิ์การเข้าถึงเฉพาะผู้ที่เกี่ยวข้อง</p>

    <h2 id="rights">8. สิทธิของเจ้าของข้อมูล</h2>
    <p>ภายใต้ PDPA เจ้าของข้อมูลมีสิทธิขอเข้าถึง ขอสำเนา ขอแก้ไขให้ถูกต้อง ขอระงับการใช้ ขอลบข้อมูล ถอนความยินยอม
    และร้องเรียนต่อหน่วยงานที่กำกับดูแลได้ หากต้องการใช้สิทธิเหล่านี้ ติดต่อเราตามช่องทางในข้อ 10</p>

    <h2 id="deletion">9. วิธีขอลบข้อมูล</h2>
    <p>ดูขั้นตอนละเอียดได้ที่หน้า <a href="/data-deletion/">วิธีขอลบข้อมูล</a></p>
    <ul>
      <li>{ph("deletion_scope_note", "ขอบเขตของการลบข้อมูล")}</li>
      <li>{ph("line_oa_data_note", "ข้อมูลแชทใน LINE OA")}</li>
    </ul>

    <h2 id="contact">10. ติดต่อเรา</h2>
    <p>{legal_name}<br>{address}<br>อีเมล {email}<br>โทร {phone}</p>

    <p class="legal-meta" style="border-bottom:none;padding-bottom:0;margin-top:2em">มีผลบังคับใช้ตั้งแต่วันที่ {ph('effective_date', 'วันที่มีผลบังคับใช้')}</p>
  </div>
</section>
"""
    return base_page(
        path="/privacy/",
        title="นโยบายความเป็นส่วนตัว · Chatudo",
        description="นโยบายความเป็นส่วนตัวของ Chatudo ข้อมูลที่เราเก็บ วัตถุประสงค์ ฐานทางกฎหมาย ผู้ประมวลผลข้อมูล และสิทธิของเจ้าของข้อมูลตาม PDPA",
        og_title="นโยบายความเป็นส่วนตัว · Chatudo",
        og_description="ข้อมูลที่เราเก็บ วัตถุประสงค์ และสิทธิของเจ้าของข้อมูลตาม PDPA",
        body_html=body,
        active_key="privacy",
        config=CONFIG,
        ph=ph,
    )


def render_terms() -> str:
    email = ph("contact_email", "อีเมลติดต่อ")
    legal_name = ph("legal_name", "ชื่อนิติบุคคล")
    address = ph("registered_address", "ที่อยู่จดทะเบียน")
    body = f"""
<section>
  <div class="container legal-wrap">
    <h1>ข้อตกลงการใช้บริการ</h1>
    {legal_meta()}
    <p class="legal-lang-link"><a href="/en/terms/">English version</a></p>

    <h2>1. การยอมรับข้อตกลง</h2>
    <p>การสมัครใช้บริการ Chatudo ถือว่าร้านค้าผู้ใช้บริการยอมรับข้อตกลงฉบับนี้ทั้งหมด หากไม่ยอมรับ กรุณาไม่ใช้บริการ</p>

    <h2>2. คำนิยาม</h2>
    <ul>
      <li>&ldquo;บริการ&rdquo; หมายถึง ระบบผู้ช่วยแอดมินของ Chatudo ที่ร่างและช่วยส่งคำตอบในแชท</li>
      <li>&ldquo;ร้านค้า&rdquo; หมายถึง ผู้สมัครใช้บริการ Chatudo</li>
      <li>&ldquo;ลูกค้าของร้าน&rdquo; หมายถึง ผู้ที่ทักแชทเข้ามาหาร้านค้าผ่านช่องทางที่เชื่อมต่อกับ Chatudo</li>
    </ul>

    <h2>3. ลักษณะของบริการ</h2>
    <p>Chatudo ใช้ AI ร่างคำตอบจากข้อมูลของร้านค้า แอดมินของร้านเป็นผู้ตรวจสอบและกดส่งคำตอบด้วยตนเองทุกข้อความ
    บริการนี้เป็นผู้ช่วยแอดมิน ไม่ใช่การแทนที่แอดมินทั้งหมด</p>

    <h2>4. การสมัครและการชำระค่าบริการ</h2>
    <p>ร้านค้าเลือกแพ็กและชำระค่าบริการตามราคาที่ระบุในหน้า <a href="/pricing/">ราคา</a> เป็นรายเดือน
    การเปลี่ยนแพ็กหรือยกเลิกบริการมีผลตั้งแต่รอบบิลถัดไป {ph('vat_note', 'ราคารวม VAT หรือไม่')}</p>

    <h2>5. หน้าที่ของร้านค้า</h2>
    <ul>
      <li>ให้ข้อมูลร้านค้าที่ถูกต้องและเป็นปัจจุบันสำหรับใช้ร่างคำตอบ</li>
      <li>ดูแลบัญชีผู้ใช้และสิทธิ์การเข้าถึงของทีมงานร้านให้ปลอดภัย</li>
      <li>ตรวจสอบคำตอบที่ระบบร่างให้ก่อนส่งจริงทุกข้อความ</li>
    </ul>

    <h2>6. ข้อมูลและความเป็นส่วนตัว</h2>
    <p>การเก็บและใช้ข้อมูลเป็นไปตาม <a href="/privacy/">นโยบายความเป็นส่วนตัว</a> ของเรา</p>

    <h2>7. ทรัพย์สินทางปัญญา</h2>
    <p>ซอฟต์แวร์ เครื่องหมายการค้า และเนื้อหาของ Chatudo เป็นทรัพย์สินของเรา ร้านค้าได้รับสิทธิใช้งานบริการตามข้อตกลงนี้เท่านั้น
    ไม่ใช่การโอนกรรมสิทธิ์</p>

    <h2>8. ข้อจำกัดความรับผิด</h2>
    <p>เราพยายามให้บริการอย่างเต็มความสามารถ แต่ไม่รับประกันว่าคำตอบที่ AI ร่างให้จะถูกต้องสมบูรณ์ทุกกรณี
    ร้านค้ามีหน้าที่ตรวจสอบคำตอบก่อนส่งตามข้อ 5 เราไม่รับผิดต่อความเสียหายที่เกิดจากการที่ร้านค้าไม่ตรวจสอบคำตอบก่อนส่ง</p>

    <h2>9. การยกเลิกบริการ</h2>
    <p>ร้านค้าสามารถยกเลิกบริการได้ทุกเมื่อ มีผลตั้งแต่รอบบิลถัดไป เราอาจระงับหรือยกเลิกบริการหากร้านค้าใช้งานผิดวัตถุประสงค์
    หรือไม่ชำระค่าบริการตามกำหนด</p>

    <h2>10. การเปลี่ยนแปลงข้อตกลง</h2>
    <p>เราอาจปรับปรุงข้อตกลงนี้เป็นครั้งคราว และจะแจ้งให้ร้านค้าทราบล่วงหน้าตามช่องทางที่เหมาะสมก่อนมีผลบังคับใช้</p>

    <h2>11. กฎหมายที่ใช้บังคับ</h2>
    <p>ข้อตกลงนี้อยู่ภายใต้บังคับกฎหมายไทย</p>

    <h2>12. ติดต่อเรา</h2>
    <p>{legal_name}<br>{address}<br>อีเมล {email}</p>

    <p class="legal-meta" style="border-bottom:none;padding-bottom:0;margin-top:2em">มีผลบังคับใช้ตั้งแต่วันที่ {ph('effective_date', 'วันที่มีผลบังคับใช้')}</p>
  </div>
</section>
"""
    return base_page(
        path="/terms/",
        title="ข้อตกลงการใช้บริการ · Chatudo",
        description="ข้อตกลงการใช้บริการ Chatudo ลักษณะบริการ การชำระเงิน หน้าที่ของร้านค้า และข้อจำกัดความรับผิด",
        og_title="ข้อตกลงการใช้บริการ · Chatudo",
        og_description="เงื่อนไขการใช้บริการระบบผู้ช่วยแอดมิน Chatudo",
        body_html=body,
        active_key="terms",
        config=CONFIG,
        ph=ph,
    )


def render_data_deletion() -> str:
    email = ph("contact_email", "อีเมลติดต่อ")
    sla = ph("deletion_request_sla", "ระยะเวลาดำเนินการลบข้อมูล")
    steps = [
        ("mail", "ส่งคำขอมาให้เรา", f"ส่งอีเมลมาที่ {email} พร้อมระบุชื่อร้านค้า ช่องทางที่ใช้งาน (LINE OA / Messenger / Instagram) "
         "และบัญชีที่ต้องการให้ลบข้อมูล (ช่องทางหลักที่แนะนำ) หรือพิมพ์คำขอในแชทที่คุยกับร้านค้าที่ใช้ Chatudo อยู่ "
         "เช่น พิมพ์ว่า “ขอลบข้อมูล” แล้วร้านค้าจะส่งคำขอต่อมาให้เรา"),
        ("shield", "เราตรวจสอบคำขอ", "ทีมงานยืนยันตัวตนผู้ขอและตรวจสอบว่าข้อมูลที่จะลบตรงกับบัญชีที่ระบุ เพื่อป้องกันการลบข้อมูลผิดบัญชี"),
        ("clock", "ดำเนินการลบ", sla),
        ("check", "ยืนยันผลให้ทราบ", "เราจะส่งอีเมลหรือข้อความยืนยันกลับไปเมื่อการลบข้อมูลเสร็จสมบูรณ์"),
    ]
    steps_html = "\n".join(
        f"""
      <li>
        <span class="step-num">{icon(ic)}</span>
        <div><h3>{title}</h3><p>{body}</p></div>
      </li>""" for ic, title, body in steps
    )
    body = f"""
<section>
  <div class="container legal-wrap">
    <h1>วิธีขอลบข้อมูล</h1>
    {legal_meta()}
    <p class="legal-lang-link"><a href="/en/data-deletion/">English version</a></p>
    <p>หากลูกค้าของร้านค้าที่ใช้ Chatudo ต้องการให้ลบข้อมูลส่วนบุคคลที่เกี่ยวข้องกับการสนทนาผ่าน Chatudo
    ทำตามขั้นตอนด้านล่าง</p>

    <ol class="steps-ol">{steps_html}
    </ol>

    <h2>ข้อมูลที่จะถูกลบ</h2>
    <ul>
      <li>ข้อความสนทนาที่เก็บไว้ในระบบซึ่งเกี่ยวข้องกับบัญชีที่ขอ</li>
      <li>ชื่อที่แสดงและรูปโปรไฟล์ที่จัดเก็บไว้สำหรับบัญชีนั้น</li>
      <li>รหัสประจำตัวผู้ใช้บนแพลตฟอร์ม (platform user ID) ที่ผูกกับบัญชีนั้น</li>
    </ul>
    <p>ข้อมูลบางส่วนที่กฎหมายกำหนดให้ต้องเก็บไว้ (เช่น เพื่อการตรวจสอบทางบัญชีหรือข้อพิพาท) อาจเก็บต่อไปตามระยะเวลาที่กฎหมายกำหนด
    แม้จะได้รับคำขอลบข้อมูลแล้ว</p>
    <p>{ph("deletion_scope_note", "ขอบเขตของการลบข้อมูล")} {ph("line_oa_data_note", "ข้อมูลแชทใน LINE OA")}</p>
    <p>{ph("backup_retention_note", "ระยะเวลาเก็บสำเนาสำรอง")}</p>

    <h2>ติดต่อเรา</h2>
    <p>มีคำถามเกี่ยวกับการขอลบข้อมูล ติดต่อได้ที่อีเมล {email}</p>
  </div>
</section>
"""
    return base_page(
        path="/data-deletion/",
        title="วิธีขอลบข้อมูล · Chatudo",
        description="วิธีขอลบข้อมูลส่วนบุคคลจากระบบ Chatudo ขั้นตอน ระยะเวลาดำเนินการ และการยืนยันผล",
        og_title="วิธีขอลบข้อมูล · Chatudo",
        og_description="ขั้นตอนการขอลบข้อมูลส่วนบุคคลจาก Chatudo",
        body_html=body,
        active_key="data-deletion",
        config=CONFIG,
        ph=ph,
    )


# ---------------------------------------------------------------------------
# English legal pages (Meta App Review reads English) — same content and
# same placeholders as the Thai pages above, kept in sync by hand.
# ---------------------------------------------------------------------------

def legal_meta_en(effective_label="effective date") -> str:
    return f'<p class="legal-meta">Effective from {ph_en("effective_date", effective_label)}</p>'


def render_privacy_en() -> str:
    email = ph_en("contact_email", "contact email")
    phone = ph_en("contact_phone", "contact phone")
    legal_name = ph_en("legal_name", "legal entity name")
    address = ph_en("registered_address", "registered address")
    retention = ph_en("data_retention_period_en", "data retention period")
    body = f"""
<section>
  <div class="container legal-wrap">
    <h1>Privacy Policy</h1>
    {legal_meta_en()}
    <p class="legal-lang-link"><a href="/privacy/">Thai version (ภาษาไทย)</a></p>
    <div class="legal-toc">
      <p>Contents</p>
      <ol>
        <li><a href="#collect">Information We Collect</a></li>
        <li><a href="#purpose">Purpose of Use</a></li>
        <li><a href="#basis">Legal Basis</a></li>
        <li><a href="#processors">Data Processors</a></li>
        <li><a href="#transfer">Cross-Border Data Transfer</a></li>
        <li><a href="#retention">Data Retention Period</a></li>
        <li><a href="#security">Security Measures</a></li>
        <li><a href="#rights">Your Rights</a></li>
        <li><a href="#deletion">How to Request Deletion</a></li>
        <li><a href="#contact">Contact Us</a></li>
      </ol>
    </div>

    <p>Chatudo (&ldquo;we&rdquo;) provides an admin-assistant system for shops that sell through chat. This policy
    explains how we collect, use and protect the personal data of customers who chat with shops using Chatudo,
    under Thailand&rsquo;s Personal Data Protection Act B.E. 2562 (PDPA).</p>

    <h2 id="collect">1. Information We Collect</h2>
    <ul>
      <li>Chat messages between a shop and its customers, sent through channels connected to Chatudo (e.g. LINE OA, Facebook Messenger, Instagram)</li>
      <li>The platform user ID on that platform</li>
      <li>Display name and profile picture, if the platform provides them</li>
    </ul>

    <h2 id="purpose">2. Purpose of Use</h2>
    <ul>
      <li>Draft and send replies on behalf of the shop using Chatudo</li>
      <li>Hand off the conversation to the shop&rsquo;s admin for review and follow-up</li>
      <li>Improve service quality, such as the accuracy of drafted replies</li>
    </ul>

    <h2 id="basis">3. Legal Basis</h2>
    <p>We process data on the basis of necessity to perform the contract between the shop and Chatudo, and on the
    basis of legitimate interest in providing chat-reply assistance for the shop. Where the law requires additional
    consent, we will request it from the data subject following the process the law requires.</p>

    <h2 id="processors">4. Data Processors</h2>
    <p>We use third-party service providers to process data on our behalf, including database and cloud hosting
    providers, and the AI model provider used to draft replies. These providers process data only on our instructions.</p>

    <h2 id="transfer">5. Cross-Border Data Transfer</h2>
    <p>Some data processors listed in section 4 may be located outside Thailand. Where data is transferred outside
    the country, we will do so in accordance with the data-protection standards the PDPA requires.</p>

    <h2 id="retention">6. Data Retention Period</h2>
    <p>{retention} This period may be extended where the law requires it, or shortened if the data subject
    requests earlier deletion.</p>
    <p>{ph_en("backup_retention_note_en", "backup retention period")}</p>

    <h2 id="security">7. Security Measures</h2>
    <p>We maintain technical and administrative measures to prevent unauthorized access, disclosure or use of data,
    such as encryption in transit (TLS) and restricting access to authorized personnel only.</p>

    <h2 id="rights">8. Your Rights</h2>
    <p>Under the PDPA, data subjects have the right to access, request a copy, request correction, request
    restriction of use, request deletion, withdraw consent, and file a complaint with the supervisory authority.
    To exercise these rights, contact us using the details in section 10.</p>

    <h2 id="deletion">9. How to Request Deletion</h2>
    <p>See the detailed steps on our <a href="/en/data-deletion/">Data Deletion</a> page.</p>
    <ul>
      <li>{ph_en("deletion_scope_note_en", "scope of deletion")}</li>
      <li>{ph_en("line_oa_data_note_en", "LINE OA chat data")}</li>
    </ul>

    <h2 id="contact">10. Contact Us</h2>
    <p>{legal_name}<br>{address}<br>Email {email}<br>Phone {phone}</p>

    <p class="legal-meta" style="border-bottom:none;padding-bottom:0;margin-top:2em">Effective from {ph_en('effective_date', 'effective date')}</p>
  </div>
</section>
"""
    return base_page(
        lang="en",
        path="/en/privacy/",
        title="Privacy Policy · Chatudo",
        description="Chatudo's privacy policy: what data we collect, why, our legal basis, data processors, and your rights under Thailand's PDPA.",
        og_title="Privacy Policy · Chatudo",
        og_description="What data we collect, why, and your rights under Thailand's PDPA.",
        body_html=body,
        active_key="privacy",
        config=CONFIG,
        ph=ph,
    )


def render_terms_en() -> str:
    email = ph_en("contact_email", "contact email")
    legal_name = ph_en("legal_name", "legal entity name")
    address = ph_en("registered_address", "registered address")
    body = f"""
<section>
  <div class="container legal-wrap">
    <h1>Terms of Service</h1>
    {legal_meta_en()}
    <p class="legal-lang-link"><a href="/terms/">Thai version (ภาษาไทย)</a></p>

    <h2>1. Acceptance of Terms</h2>
    <p>By signing up for Chatudo, the shop agrees to these terms in full. If you do not agree, please do not use the service.</p>

    <h2>2. Definitions</h2>
    <ul>
      <li>&ldquo;Service&rdquo; means Chatudo&rsquo;s admin-assistant system, which drafts and helps send chat replies</li>
      <li>&ldquo;Shop&rdquo; means the business that signs up for Chatudo</li>
      <li>&ldquo;Shop&rsquo;s customer&rdquo; means anyone who messages the shop through a channel connected to Chatudo</li>
    </ul>

    <h2>3. Nature of the Service</h2>
    <p>Chatudo uses AI to draft replies from the shop&rsquo;s information. The shop&rsquo;s admin reviews and sends
    every reply themselves. This service is an admin assistant, not a full replacement for the admin.</p>

    <h2>4. Sign-up and Payment</h2>
    <p>The shop selects a plan and pays the price listed on the <a href="/pricing/">Pricing</a> page monthly.
    Changing plans or cancelling takes effect from the next billing cycle. {ph_en('vat_note', 'whether prices include VAT')}</p>

    <h2>5. Shop Responsibilities</h2>
    <ul>
      <li>Provide accurate, up-to-date shop information for drafting replies</li>
      <li>Keep the shop&rsquo;s team accounts and access secure</li>
      <li>Review every AI-drafted reply before sending</li>
    </ul>

    <h2>6. Data and Privacy</h2>
    <p>Data collection and use follow our <a href="/en/privacy/">Privacy Policy</a>.</p>

    <h2>7. Intellectual Property</h2>
    <p>The software, trademarks and content of Chatudo are our property. The shop is granted a right to use the
    service under these terms only, not a transfer of ownership.</p>

    <h2>8. Limitation of Liability</h2>
    <p>We make every effort to provide the service fully, but we do not guarantee that AI-drafted replies will be
    accurate in every case. The shop is responsible for reviewing replies before sending, per section 5. We are not
    liable for damages arising from the shop&rsquo;s failure to review replies before sending.</p>

    <h2>9. Cancellation</h2>
    <p>The shop may cancel the service at any time, effective from the next billing cycle. We may suspend or
    terminate the service if the shop misuses it or fails to pay on time.</p>

    <h2>10. Changes to These Terms</h2>
    <p>We may update these terms from time to time and will notify the shop in advance through an appropriate
    channel before changes take effect.</p>

    <h2>11. Governing Law</h2>
    <p>These terms are governed by the laws of Thailand.</p>

    <h2>12. Contact Us</h2>
    <p>{legal_name}<br>{address}<br>Email {email}</p>

    <p class="legal-meta" style="border-bottom:none;padding-bottom:0;margin-top:2em">Effective from {ph_en('effective_date', 'effective date')}</p>
  </div>
</section>
"""
    return base_page(
        lang="en",
        path="/en/terms/",
        title="Terms of Service · Chatudo",
        description="Chatudo's terms of service: the nature of the service, payment, shop responsibilities, and limitation of liability.",
        og_title="Terms of Service · Chatudo",
        og_description="Terms of service for Chatudo's admin-assistant system.",
        body_html=body,
        active_key="terms",
        config=CONFIG,
        ph=ph,
    )


def render_data_deletion_en() -> str:
    email = ph_en("contact_email", "contact email")
    sla = ph_en("deletion_request_sla_en", "deletion turnaround time")
    steps = [
        ("mail", "Send us your request", f"Email {email} with the shop&rsquo;s name, the channel used "
         "(LINE OA / Messenger / Instagram), and the account you want deleted (recommended primary route), or type "
         "the request in the chat with the shop that uses Chatudo, e.g. type &ldquo;delete my data&rdquo;, and the "
         "shop will forward the request to us."),
        ("shield", "We verify the request", "Our team verifies the requester&rsquo;s identity and checks that the "
         "data to be deleted matches the account specified, to prevent deleting the wrong account."),
        ("clock", "We carry out the deletion", sla),
        ("check", "We confirm the result", "We will send an email or message confirming once the deletion is complete."),
    ]
    steps_html = "\n".join(
        f"""
      <li>
        <span class="step-num">{icon(ic)}</span>
        <div><h3>{title}</h3><p>{body}</p></div>
      </li>""" for ic, title, body in steps
    )
    body = f"""
<section>
  <div class="container legal-wrap">
    <h1>How to Request Data Deletion</h1>
    {legal_meta_en()}
    <p class="legal-lang-link"><a href="/data-deletion/">Thai version (ภาษาไทย)</a></p>
    <p>If a shop&rsquo;s customer using Chatudo wants their personal data related to conversations through Chatudo
    deleted, follow the steps below.</p>

    <ol class="steps-ol">{steps_html}
    </ol>

    <h2>Data That Gets Deleted</h2>
    <ul>
      <li>Conversation data stored in the system related to the requested account</li>
      <li>Display name and profile picture stored for that account</li>
      <li>The platform user ID linked to that account</li>
    </ul>
    <p>Some data the law requires us to keep (e.g. for accounting or dispute records) may be retained for the period
    the law requires, even after a deletion request.</p>
    <p>{ph_en("deletion_scope_note_en", "scope of deletion")} {ph_en("line_oa_data_note_en", "LINE OA chat data")}</p>
    <p>{ph_en("backup_retention_note_en", "backup retention period")}</p>

    <h2>Contact Us</h2>
    <p>Questions about requesting deletion? Contact us at {email}</p>
  </div>
</section>
"""
    return base_page(
        lang="en",
        path="/en/data-deletion/",
        title="How to Request Data Deletion · Chatudo",
        description="How to request deletion of personal data from Chatudo: steps, turnaround time, and confirmation.",
        og_title="How to Request Data Deletion · Chatudo",
        og_description="Steps to request deletion of personal data from Chatudo.",
        body_html=body,
        active_key="data-deletion",
        config=CONFIG,
        ph=ph,
    )


def render_404() -> str:
    body = f"""
<section class="error-page">
  <img src="/assets/img/logo-mark.png" alt="">
  <h1>ไม่พบหน้านี้</h1>
  <p style="color:var(--warm-gray);max-width:40ch;margin:0 auto 1.6em">หน้าที่คุณตามหาอาจถูกย้ายหรือไม่มีอยู่ ลองกลับไปหน้าแรกอีกครั้ง</p>
  <a class="btn btn-primary" href="/">กลับหน้าแรก</a>
</section>
"""
    return base_page(
        path="/404.html",
        title="ไม่พบหน้านี้ · Chatudo",
        description="ไม่พบหน้าที่คุณตามหาบนเว็บไซต์ Chatudo",
        og_title="ไม่พบหน้านี้ · Chatudo",
        og_description="ไม่พบหน้าที่คุณตามหาบนเว็บไซต์ Chatudo",
        body_html=body,
        active_key="",
        config=CONFIG,
        ph=ph,
    )


# ---------------------------------------------------------------------------
# Build driver
# ---------------------------------------------------------------------------

PAGES = {
    "index.html": render_home,
    "pricing/index.html": render_pricing,
    "privacy/index.html": render_privacy,
    "terms/index.html": render_terms,
    "data-deletion/index.html": render_data_deletion,
    "en/privacy/index.html": render_privacy_en,
    "en/terms/index.html": render_terms_en,
    "en/data-deletion/index.html": render_data_deletion_en,
    "404.html": render_404,
}

ROBOTS_TXT = """User-agent: *
Allow: /

Sitemap: https://chatudo.com/sitemap.xml
"""

SITEMAP_URLS = [
    "/", "/pricing/", "/privacy/", "/terms/", "/data-deletion/",
    "/en/privacy/", "/en/terms/", "/en/data-deletion/",
]


def render_sitemap() -> str:
    urls = "\n".join(
        f"  <url><loc>https://chatudo.com{u}</loc></url>" for u in SITEMAP_URLS
    )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}
</urlset>
"""


def main():
    if PUBLIC.exists():
        shutil.rmtree(PUBLIC)
    PUBLIC.mkdir(parents=True)

    for rel_path, fn in PAGES.items():
        out = PUBLIC / rel_path
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(fn(), encoding="utf-8")
        print(f"wrote {out.relative_to(ROOT)}")

    (PUBLIC / "robots.txt").write_text(ROBOTS_TXT, encoding="utf-8")
    (PUBLIC / "sitemap.xml").write_text(render_sitemap(), encoding="utf-8")

    # static passthrough dirs
    for name in ("assets", "css"):
        src = ROOT / name
        dst = PUBLIC / name
        shutil.copytree(src, dst)

    print("build complete ->", PUBLIC)


if __name__ == "__main__":
    main()
