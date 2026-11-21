import re
from playwright.sync_api import Page, expect

URL = "https://portal.uat.gofive.co.th/Register/empeo"


def go_to_otp_step(page: Page):
    """ฟังก์ชันช่วยเหลือ: กรอกข้อมูลลงทะเบียนที่ถูกต้องเพื่อเข้าสู่หน้ายืนยัน OTP"""
    page.goto(URL, wait_until="domcontentloaded")

    # ค้นหาและเลือกบริษัท
    page.get_by_test_id(
        "input_textfield_input_registration_tax_id"
    ).fill("ยี่สิบสอง")

    page.locator("div").filter(
        has_text=re.compile(r"^- ยี่สิบสองอินเตอร์ฟู้ด จำกัด0115557006957$")
    ).nth(1).click()

    # เลือกประเภทธุรกิจ
    business_type = page.get_by_text(
        "ประเภทธุรกิจ*",
        exact=True
    )
    business_type.locator("..").click()
    page.wait_for_timeout(500)
    page.locator("div").filter(
        has_text=re.compile(r"^นำเข้าและส่งออก$")
    ).last.click()

    # เลือกจำนวนผู้ใช้งาน
    page.get_by_text(
        "ผู้ใช้งาน*",
        exact=True
    ).click()
    page.get_by_text(
        "101-200",
        exact=True
    ).last.click()

    # กรอกอีเมล ชื่อ นามสกุล เบอร์มือถือ
    page.get_by_test_id(
        "input_textfield_input_registration_email"
    ).fill("otp_test@gmail.com")

    page.get_by_test_id(
        "input_textfield_input_register_first_name"
    ).fill("สมชาย")

    page.get_by_test_id(
        "input_textfield_input_register_last_name"
    ).fill("ใจดี")

    page.get_by_role(
        "textbox",
        name="เบอร์มือถือ*"
    ).fill("0967690708")

    # ยอมรับเงื่อนไขและกดยืนยันเพื่อเปิดหน้าต่าง OTP
    page.get_by_test_id(
        "input_checkbox_registration_checkbox"
    ).check()

    page.get_by_test_id(
        "button_submit_registration_try_for_free"
    ).click()

    # ตรวจสอบว่าหน้าต่างยืนยัน OTP แสดงผลสำเร็จ
    expect(
        page.get_by_text("กรุณาตรวจสอบข้อความ")
    ).to_be_visible(timeout=10000)


# ==================================================
# OTP NEGATIVE TESTS
# ==================================================

def test_empty_otp(page: Page):
    """
    กรณีไม่ได้กรอกรหัส OTP เลย:
    ปุ่มยืนยัน ('ยืนยัน') จะต้องอยู่ในสถานะ Disabled (กดไม่ได้)
    """
    go_to_otp_step(page)

    verify_button = page.get_by_test_id(
        "button_button_registration_verify"
    )

    expect(verify_button).to_be_disabled()


def test_incomplete_otp(page: Page):
    """
    กรณีกรอกรหัส OTP ไม่ครบ 6 หลัก (เช่น กรอกแค่ 3 หลัก):
    ปุ่มยืนยัน ('ยืนยัน') จะต้องยังคง Disabled (กดไม่ได้)
    """
    go_to_otp_step(page)

    otp_first = page.locator('[id^="otp_0_"]')
    otp_first.click()

    # พิมพ์เพียง 3 หลัก
    page.keyboard.type("123", delay=100)

    verify_button = page.get_by_test_id(
        "button_button_registration_verify"
    )

    expect(verify_button).to_be_disabled()


def test_invalid_otp(page: Page):
    """
    กรณีกรอกรหัส OTP ที่ไม่ถูกต้อง (เช่น 654123):
    ปุ่มยืนยันจะกดได้ แต่ระบบต้องไม่อนุญาตให้ผ่านและยังคงอยู่ที่หน้ายืนยัน OTP
    """
    go_to_otp_step(page)

    otp_first = page.locator('[id^="otp_0_"]')
    otp_first.click()

    # พิมพ์ OTP ที่ไม่ถูกต้อง 6 หลัก
    page.keyboard.type("654123", delay=100)

    verify_button = page.get_by_test_id(
        "button_button_registration_verify"
    )

    expect(verify_button).to_be_enabled()
    verify_button.click()

    # รอผลตอบกลับจากระบบ
    page.wait_for_timeout(1000)

    # ตรวจสอบว่ายังคงอยู่ที่หน้ายืนยัน OTP
    expect(
        page.get_by_text("กรุณาตรวจสอบข้อความ")
    ).to_be_visible()
