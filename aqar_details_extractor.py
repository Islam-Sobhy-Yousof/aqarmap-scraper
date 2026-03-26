from playwright.sync_api import Page

def get_aqar_details(page: Page, url: str) -> dict:
    page.goto(url)
    page.wait_for_selector("div >data.text-title-2[value]")

    total_price = page.query_selector("div >data.text-title-2[value]")
    total_price = total_price.inner_text() if total_price else 'N/A'

    description = page.query_selector("div > h1.text-body-1")
    description = description.inner_text() if description else 'N/A'

    about = page.query_selector("section > div > span.text-caption-1")
    about = about.inner_text().strip().replace('\n', '').split('.') if about else []

    short_description = about[0] if len(about) > 0 else 'N/A'
    publish_time = about[-1] if len(about) > 1 else 'N/A'

    location = page.query_selector("section > div > a > div > p")
    location = location.inner_text() if location else 'N/A'

    area = page.query_selector("section > div > div > div > svg[aria-label='size'] + p")
    area = area.inner_text() if area else 'N/A'

    number_of_rooms = page.query_selector("section > div > div > div > svg[aria-label='bedroom'] + p")
    number_of_rooms = number_of_rooms.inner_text() if number_of_rooms else 'N/A'

    extra_super_lux = page.query_selector("section > div > div > div > svg[aria-label='finish'] + p")
    extra_super_lux = extra_super_lux.inner_text() if extra_super_lux else 'N/A'

    number_of_bath_rooms = page.query_selector("section > div > div > div > svg[aria-label='bathroom'] + p")
    number_of_bath_rooms = number_of_bath_rooms.inner_text() if number_of_bath_rooms else 'N/A'

    details = []
    for i in range(1, 7):
        detail = page.query_selector(f"section#details > div > div > div:nth-child({i})")
        detail = detail.inner_text().replace('\n', ' ') if detail else None
        if detail:
            details.append(detail)

    description_lines = []
    chevron_btn = page.query_selector(".chevron-down-blue-bold-icon")
    if chevron_btn:
        chevron_btn.click()
        for i in range(1, 11):
            line = page.query_selector(f"section > div > div > span:nth-child({i})")
            line = line.inner_text().replace('\n', ' ') if line else None
            if line:
                description_lines.append(line)

    adv_owner_rating = page.query_selector("section#location + section > div > div > div > div > div > p")
    adv_owner_rating = adv_owner_rating.inner_text() if adv_owner_rating else 'N/A'
    try:
        adv_owner_rating = round(float(adv_owner_rating),1)
    except:
        adv_owner_rating = 'N/A'
        

    adv_owner = page.query_selector("section#location + section a > p")
    adv_owner = adv_owner.inner_text() if adv_owner else 'N/A'

    return {
        "total_price": total_price,
        "description": description,
        "short_description": short_description,
        "publish_time": publish_time,
        "location": location,
        "area": area,
        "number_of_rooms": number_of_rooms,
        "extra_super_lux": extra_super_lux,
        "number_of_bath_rooms": number_of_bath_rooms,
        "details": details,
        "description_lines": description_lines,
        "adv_owner_rating": adv_owner_rating,
        "adv_owner": adv_owner
    }