from playwright.sync_api import sync_playwright
from aqar_details_extractor import get_aqar_details
import openpyxl
headers = [
    "السعر الكلي",
    "الوصف",
    "الوصف المختصر",
    "وقت النشر",
    "الموقع",
    "المساحة",
    "عدد الغرف",
    "تشطيب إضافي فاخر",
    "عدد الحمامات",
    "التفاصيل",
    "الوصف",
    "تقييم المعلن",
    "المعلن"
]
base = "https://aqarmap.com.eg"
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    url = "https://aqarmap.com.eg/ar/for-sale/property-type/cairo/?location=cairo"
    page.goto(url)

    card_cnt = 0
    mx_threashold = 200
    elements_lnks = []
    while True:
        page.wait_for_timeout(1000)
        page.evaluate("window.scrollTo(0,document.body.scrollHeight)")
        elements = page.query_selector_all("a.standard-card-image:nth-child(1)")
        elements = [lnk.get_attribute("href") for lnk in elements]
        elements_lnks.extend(elements)
        card_cnt += len(elements)
        nxt_btn = page.query_selector("a[title='Next Page']")
        print("elements count : ",card_cnt)
        if card_cnt >= mx_threashold:
            break
        if nxt_btn:
            nxt_btn.click()
        else:
            break
    
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(headers)
    for lnk in elements_lnks:
        aqr_details = get_aqar_details(page, base + lnk)

        main_row = [
            aqr_details.get("total_price"),
            aqr_details.get("description"),
            aqr_details.get("short_description"),
            aqr_details.get("publish_time"),
            aqr_details.get("location"),
            aqr_details.get("area"),
            aqr_details.get("number_of_rooms"),
            aqr_details.get("extra_super_lux"),
            aqr_details.get("number_of_bath_rooms"),
            " | ".join(aqr_details.get("description_lines", [])),
            aqr_details.get("adv_owner_rating"),
            aqr_details.get("adv_owner"),
        ]

        details = aqr_details.get("details", [])
        for detail in details:
            main_row.append(detail)

        ws.append(main_row)

        for i in range(len(details)):
            ws.cell(row=1, column=13 + i, value=f"تفصيل {i+1}")

        wb.save("aqarmap.xlsx")


        
    



        

