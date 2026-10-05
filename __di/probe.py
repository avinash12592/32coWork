from dotenv import load_dotenv; load_dotenv("D:/32co_work/automation-ui/.env")
import os, re
from playwright.sync_api import sync_playwright
from sleep.pages.dentist.sleep_login_page import SleepLoginPage
from sleep.pages.dentist.sleep_patient_list_page import SleepPatientListPage
ORIGIN=os.environ["BASE_URL"].split("/signin")[0]
def first_patient_id(ctx, user, pw):
    pg=ctx.new_page(); lp=SleepLoginPage(pg); lp.navigate(os.environ["BASE_URL"])
    lp.login(username=user, password=pw); lp.switch_to_sleep()
    pl=SleepPatientListPage(pg); pl.open_from_nav(); pl.wait_for_list_settled(); pl.open_first_patient()
    pg.wait_for_url(re.compile(r"/patients/[0-9a-fA-F]{8,}"), timeout=30000)
    return re.search(r"/patients/([0-9a-fA-F]{8,})", pg.url).group(1)
with sync_playwright() as p:
    b=p.chromium.launch(headless=True)
    c1=b.new_context(viewport={"width":1600,"height":1000})
    pid=first_patient_id(c1,"avinash.kumar+betaprac3@32co.com","123qwe!@#QWE")
    print("betaprac3 first patient id:", pid); c1.close()
    c2=b.new_context(viewport={"width":1600,"height":1000}); pg=c2.new_page()
    lp=SleepLoginPage(pg); lp.navigate(os.environ["BASE_URL"])
    lp.login(username=os.environ["SLEEP_PRACTICE_USERNAME"], password=os.environ["SLEEP_PRACTICE_PASSWORD"]); lp.switch_to_sleep()
    pg.goto(f"{ORIGIN}/sleep/practice/patients/{pid}", wait_until="domcontentloaded"); pg.wait_for_timeout(6000)
    print("Avinash url:", pg.url)
    print("NotFound 'Sorry, nothing to see here.' visible:", pg.get_by_text("Sorry, nothing to see here.", exact=False).is_visible())
    print("details container visible:", pg.locator(".sleep-patients-details-dentist").is_visible())
    c2.close(); b.close()
