import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="module")
def browser():
    # Použití Playwright a Chromium
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, slow_mo=0)
        yield browser
        browser.close()

@pytest.fixture(scope="function")
def page(browser):
    # Vytvoření nové stránky pro každý test
    context = browser.new_context()
    page = context.new_page()
    yield page
    page.close()
    context.close()

def test_title(page):
    #Otestování, že title je Reflex.cz - ...atd
    url = "https://www.reflex.cz"
    page.goto(url)
    assert page.title() == "Reflex.cz - Komentáře, zprávy, výrazné autorské fotografie"

def test_reflex_search(page):
    # Otestování, že pokud otevřu URL, potvrdím reklamu a do vyhledávání napíšu rozhovory, stránka bude mít URL se slovem rozhovory
    # Otevření Reflexu
    print("Navigating to Reflex")
    page.goto("https://www.reflex.cz")

    # Souhlas s reklamou
    page.click('#cpexSubs_consentButton')

    # Rozbalení menu
    page.click("//div[@class='header-menu-hamburger__icon']")
    
    # Zadání textu do vyhledávacího pole a spuštění vyhledávání
    page.fill('#searchInput', 'Rozhovory')
    page.click('button[title="Vyhledat"]')
    
    # Ověření, že URL stránky obsahuje vyhledávaný text
    page.wait_for_load_state("networkidle")  
    assert 'rozhovory' in page.url.lower(), "URL neobsahuje slovo 'rozhovory'"

def test_open_X_after_click(page):
    # Otestování, že kliknutí na ikonu X otevře v nové záložce X.com Reflexu
    # Otevření Reflexu
    print("Navigating to Reflex")
    page.goto("https://www.reflex.cz")

    # Souhlas s reklamou
    page.click('#cpexSubs_consentButton')

    # Kliknutí na ikonu X
    page.click("path[fill='#191919']")

    # Definice toho, že click otevře nové okno nebo záložku v prohlížeči
    new_page = None
    for context in page.context.browser.contexts:
        if len(context.pages) > 1:  
            new_page = context.pages[-1]
            break

    # Ověření, že se otevřela stránka, která obsahuje požadovanou URL
    assert new_page.url and "x.com/Reflex_cz" in new_page.url, f"Nové okno neobsahuje správnou URL, nalezena: {new_page.url}"
