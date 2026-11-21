from playwright.sync_api import Page, expect

URL = "https://portal.uat.gofive.co.th/Register/empeo"


def click_submit(page: Page):
    """กดปุ่มทดลองใช้ฟรีเพื่อ Trigger การตรวจสอบ Validation"""
    page.get_by_test_id(
        "button_submit_registration_try_for_free"
    ).click()


# ==================================================
# REQUIRED FIELD VALIDATION
# ==================================================

def test_empty_company(page: Page):
    """กรณีไม่กรอกข้อมูลบริษัท: ต้องแสดงข้อความแจ้งเตือน"""
    page.goto(URL)
    click_submit(page)

    expect(
        page.get_by_text("กรุณากรอกเลขประจำตัวผู้เสียภาษีหรือชื่อบริษัท")
    ).to_be_visible()


def test_empty_business_type(page: Page):
    """กรณีไม่เลือกประเภทธุรกิจ: ต้องแสดงข้อความแจ้งเตือน"""
    page.goto(URL)
    click_submit(page)

    expect(
        page.get_by_text("กรุณากรอกประเภทธุรกิจ")
    ).to_be_visible()


def test_empty_user_amount(page: Page):
    """กรณีไม่เลือกจำนวนผู้ใช้งาน: ต้องแสดงข้อความแจ้งเตือน"""
    page.goto(URL)
    click_submit(page)

    expect(
        page.get_by_text("กรุณากรอกผู้ใช้งาน")
    ).to_be_visible()


def test_empty_email(page: Page):
    """กรณีไม่กรอกอีเมล: ต้องแสดงข้อความแจ้งเตือน"""
    page.goto(URL)
    click_submit(page)

    expect(
        page.get_by_text("กรุณากรอกอีเมล")
    ).to_be_visible()


def test_empty_first_name(page: Page):
    """กรณีไม่กรอกชื่อ: ต้องแสดงข้อความแจ้งเตือน"""
    page.goto(URL)
    click_submit(page)

    expect(
        page.get_by_text("กรุณากรอกชื่อ")
    ).to_be_visible()


def test_empty_last_name(page: Page):
    """กรณีไม่กรอกนามสกุล: ต้องแสดงข้อความแจ้งเตือน"""
    page.goto(URL)
    click_submit(page)

    expect(
        page.get_by_text("กรุณากรอกนามสกุล")
    ).to_be_visible()


def test_empty_phone(page: Page):
    """กรณีไม่กรอกเบอร์มือถือ: ต้องแสดงข้อความแจ้งเตือน"""
    page.goto(URL)
    click_submit(page)

    expect(
        page.get_by_text("กรุณากรอกเบอร์โทรศัพท์มือถือ")
    ).to_be_visible()


# ==================================================
# EMAIL FORMAT VALIDATION
# ==================================================

def test_invalid_email(page: Page):
    """กรณีรูปแบบอีเมลไม่ถูกต้อง: ต้องแสดงข้อความแจ้งเตือนรูปแบบอีเมล"""
    page.goto(URL)

    page.get_by_test_id(
        "input_textfield_input_registration_email"
    ).fill("yeesibsonggmail.com")

    click_submit(page)

    expect(
        page.get_by_text("กรุณาใส่อีเมลที่ถูกต้อง")
    ).to_be_visible()


# ==================================================
# PHONE NUMBER VALIDATION
# ==================================================

def test_phone_too_short(page: Page):
    """กรณีเบอร์มือถือสั้นเกินไป: ต้องแสดงข้อความแจ้งเตือนรูปแบบเบอร์"""
    page.goto(URL)

    page.get_by_role(
        "textbox",
        name="เบอร์มือถือ*"
    ).fill("1234")

    click_submit(page)

    expect(
        page.get_by_text("รูปแบบเบอร์โทรศัพท์ไม่ถูกต้อง")
    ).to_be_visible()


def test_phone_too_long(page: Page):
    """กรณีเบอร์มือถือยาวเกินไป: ต้องแสดงข้อความแจ้งเตือนรูปแบบเบอร์"""
    page.goto(URL)

    page.get_by_role(
        "textbox",
        name="เบอร์มือถือ*"
    ).fill("0967690708123")

    click_submit(page)

    expect(
        page.get_by_text("รูปแบบเบอร์โทรศัพท์ไม่ถูกต้อง")
    ).to_be_visible()


# ==================================================
# TERMS & CONDITIONS VALIDATION
# ==================================================

def test_terms_not_accepted(page: Page):
    """กรณีไม่ได้ติ๊กยอมรับเงื่อนไข: Checkbox ต้องไม่ถูกเลือก"""
    page.goto(URL)
    click_submit(page)

    checkbox = page.get_by_test_id(
        "input_checkbox_registration_checkbox"
    )

    expect(checkbox).not_to_be_checked()
