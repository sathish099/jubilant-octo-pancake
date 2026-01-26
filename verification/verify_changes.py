from playwright.sync_api import sync_playwright

def verify_changes():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate to the local server
        page.goto("http://localhost:8000")

        # 1. Verify .attribution class
        attribution = page.locator(".attribution")
        if attribution.count() == 0:
            print("Error: Attribution element not found")
            exit(1)

        # Verify styles of attribution
        computed_style = attribution.evaluate("""element => {
            const style = window.getComputedStyle(element);
            return {
                fontSize: style.fontSize,
                marginTop: style.marginTop
            }
        }""")

        print(f"Attribution styles: {computed_style}")
        # Allow small tolerance
        if computed_style['fontSize'] not in ['14.4px', '0.9rem']:
             print(f"Warning: Expected fontSize 14.4px, got {computed_style['fontSize']}")

        if computed_style['marginTop'] not in ['8px', '0.5rem']:
             print(f"Warning: Expected marginTop 8px, got {computed_style['marginTop']}")

        # 2. Verify animations are renamed
        trend_h2 = page.locator(".trend-overlay h2")
        trend_p = page.locator(".trend-overlay p")

        h2_anim = trend_h2.evaluate("element => window.getComputedStyle(element).animationName")
        p_anim = trend_p.evaluate("element => window.getComputedStyle(element).animationName")

        print(f"H2 Animation: {h2_anim}")
        print(f"P Animation: {p_anim}")

        if h2_anim != "slide-up":
            print(f"Error: Expected animation 'slide-up', got '{h2_anim}'")
            exit(1)
        if p_anim != "fade-in":
             print(f"Error: Expected animation 'fade-in', got '{p_anim}'")
             exit(1)

        # 3. Verify Skip Link
        skip_link = page.locator(".skip-link")
        if skip_link.count() == 0:
            print("Error: Skip link not found")
            exit(1)

        # Check initial state (should be off-screen)
        top_pos = skip_link.evaluate("element => window.getComputedStyle(element).top")
        print(f"Skip link top: {top_pos}")
        if top_pos != "-40px":
             print(f"Error: Expected skip link top to be -40px, got {top_pos}")
             exit(1)

        # Check focus state
        skip_link.focus()
        page.wait_for_timeout(500)

        top_pos_focus = skip_link.evaluate("element => window.getComputedStyle(element).top")
        print(f"Skip link top after focus: {top_pos_focus}")
        if top_pos_focus != "0px":
             print(f"Error: Expected skip link top to be 0px after focus, got {top_pos_focus}")
             exit(1)

        # Take screenshot
        page.screenshot(path="/home/jules/verification/verification_v2.png", full_page=True)

        browser.close()
        print("Verification successful!")

if __name__ == "__main__":
    verify_changes()
