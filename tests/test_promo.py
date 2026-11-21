from playwright.sync_api import Page, expect

URL = "https://portal.uat.gofive.co.th/Register/empeo"


def open_promo_section(page: Page):
    """เปิดหน้าเว็บและกดเปิดส่วนกรอกรหัสส่วนลด"""
    page.goto(URL)
    page.get_by_text("ใช้โค้ดส่วนลด", exact=True).click()


def test_valid_promo_code(page: Page):
    """
    กรณีใช้งานโค้ดส่วนลดที่ถูกต้อง (FREE15DAY):
    ระบบต้องยอมรับโค้ดและแสดงผลโค้ดในช่องกรอก
    """
    open_promo_section(page)

    promo_input = page.get_by_test_id(
        "input_text_registration_coupon_code"
    )
    promo_input.fill("FREE15DAY")

    page.get_by_test_id(
        "input_button_registration_btn_apply"
    ).click()

    # ตรวจสอบว่าโค้ดยังคงปรากฏอยู่ในช่องหลังกด Apply
    expect(promo_input).to_have_value("FREE15DAY")


def test_invalid_promo_code(page: Page):
    """
    กรณีใช้งานโค้ดส่วนลดที่ไม่ถูกต้อง/ไม่มีในระบบ (Banana):
    ตาม Test Case ที่ออกแบบไว้ ระบบควรปฏิเสธและแสดงข้อความแจ้งเตือน "ไม่พบรหัสส่วนลด"

    หมายเหตุ (Known Defect / UAT Behavior):
    การทดสอบนี้จงใจปล่อยให้ FAIL เพื่อสะท้อนพฤติกรรมจริงของระบบ UAT
    เนื่องจากระบบไม่ได้แสดง Validation Error ตามที่คาดหวัง และดูเหมือนจะยอมรับโค้ดที่ไม่ถูกต้อง
    """
    open_promo_section(page)

    promo_input = page.get_by_test_id(
        "input_text_registration_coupon_code"
    )
    promo_input.fill("Banana")

    page.get_by_test_id(
        "input_button_registration_btn_apply"
    ).click()

    # คาดหวัง: ระบบควรแสดงข้อความปฏิเสธโค้ดที่ไม่ถูกต้อง
    expect(
        page.get_by_text("ไม่พบรหัสส่วนลด")
    ).to_be_visible(timeout=5000)
