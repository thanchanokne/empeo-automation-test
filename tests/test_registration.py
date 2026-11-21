import re
from playwright.sync_api import Page, expect

URL = "https://portal.uat.gofive.co.th/Register/empeo"


def test_registration_happy_path(page: Page):
    """
    Happy Path: ทดสอบการกรอกข้อมูลลงทะเบียนที่ถูกต้องครบถ้วน
    และตรวจสอบว่าระบบสามารถส่งฟอร์มและเปิดหน้าต่างยืนยัน OTP ได้สำเร็จ
    """
    page.goto(URL, wait_until="domcontentloaded")

    # ==========================================
    # 1. ค้นหาและเลือกบริษัท (Search & Select Company)
    # ==========================================
    page.get_by_test_id(
        "input_textfield_input_registration_tax_id"
    ).fill("ยี่สิบสอง")

    company = page.locator("div").filter(
        has_text=re.compile(r"^- ยี่สิบสองอินเตอร์ฟู้ด จำกัด0115557006957$")
    ).nth(1)

    company.wait_for(state="visible")
    company.click()

    # ==========================================
    # 2. เลือกประเภทธุรกิจ (Select Business Type)
    # ==========================================
    business_type = page.get_by_text(
        "ประเภทธุรกิจ*",
        exact=True
    )
    business_type.locator("..").click()

    page.wait_for_timeout(500)

    page.locator("div").filter(
        has_text=re.compile(r"^นำเข้าและส่งออก$")
    ).last.click()

    # ==========================================
    # 3. เลือกจำนวนผู้ใช้งาน (Select Number of Users)
    # ==========================================
    page.get_by_text(
        "ผู้ใช้งาน*",
        exact=True
    ).click()

    page.get_by_text(
        "101-200",
        exact=True
    ).last.click()

    # ==========================================
    # 4. อีเมล (Valid Email)
    # ==========================================
    page.get_by_test_id(
        "input_textfield_input_registration_email"
    ).fill("Somchai99@gmail.com")

    # ==========================================
    # 5. ชื่อ (First Name)
    # ==========================================
    page.get_by_test_id(
        "input_textfield_input_register_first_name"
    ).fill("สมชาย")

    # ==========================================
    # 6. นามสกุล (Last Name)
    # ==========================================
    page.get_by_test_id(
        "input_textfield_input_register_last_name"
    ).fill("ใจดี")

    # ==========================================
    # 7. เบอร์มือถือ (Phone Number)
    # ==========================================
    page.get_by_role(
        "textbox",
        name="เบอร์มือถือ*"
    ).fill("0967690708")

    # ==========================================
    # 8. ยอมรับข้อกำหนดและเงื่อนไข (Accept Terms)
    # ==========================================
    page.get_by_test_id(
        "input_checkbox_registration_checkbox"
    ).check()

    # ==========================================
    # 9. ส่งข้อมูลลงทะเบียน (Submit Registration)
    # ==========================================
    page.get_by_test_id(
        "button_submit_registration_try_for_free"
    ).click()

    # ==========================================
    # 10. ตรวจสอบว่าหน้ายืนยัน OTP แสดงผล
    # ==========================================
    otp_first = page.locator('[id^="otp_0_"]')
    expect(otp_first).to_be_visible(timeout=10000)
    expect(
        page.get_by_text("กรุณาตรวจสอบข้อความ")
    ).to_be_visible(timeout=10000)
