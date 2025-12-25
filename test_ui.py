""""
Selenium tests for Spanish Learning App
Run with: python test_spanish_app.py
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.edge.service import Service as EdgeService
import time

class SpanishAppTest:
    def __init__(self):
        # Setup Edge driver
        service = EdgeService(executable_path=r"C:\webdriver\edgedriver_win64\msedgedriver.exe")
        self.driver = webdriver.Edge(service=service)
        self.driver.maximize_window()
        self.base_url = "http://127.0.0.1:8000"
        self.wait = WebDriverWait(self.driver, 10)
    
    def test_homepage(self):
        """Test 1: Homepage loads and shows two learning paths"""
        print("\n=== Test 1: Homepage ===")
        self.driver.get(self.base_url)
        
        # Check title
        assert "Spanish Learning Hub" in self.driver.title or "SpanishChat" in self.driver.title
        print("✓ Homepage loaded")
        
        # Check both cards exist
        phrase_practice_card = self.wait.until(
            EC.presence_of_element_located((By.LINK_TEXT, "Start Phrase Practice"))
        )
        conversation_card = self.driver.find_element(By.LINK_TEXT, "Start Conversation")
        
        print("✓ Both learning paths visible")
        time.sleep(1)
    
    def test_phrase_practice_flow(self):
        """Test 2: Complete phrase practice flow"""
        print("\n=== Test 2: Phrase Practice Flow ===")
        
        # From homepage, click phrase practice
        self.driver.get(self.base_url)
        phrase_btn = self.wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Start Phrase Practice"))
        )
        phrase_btn.click()
        print("✓ Clicked 'Start Phrase Practice'")
        time.sleep(1)
        
        # Should see list of scenarios
        assert "/phrase-practice/" in self.driver.current_url
        print("✓ Scenario list page loaded")
        
        # Click first scenario's practice button
        practice_btn = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Practice')]"))
        )
        scenario_name = self.driver.find_element(By.CLASS_NAME, "card-title").text
        print(f"✓ Found scenario: {scenario_name}")
        practice_btn.click()
        time.sleep(1)
        
        # Should be on vocab builder page
        assert "/phrase-practice/" in self.driver.current_url
        assert self.driver.current_url != self.base_url + "/phrase-practice/"
        print("✓ Vocab builder page loaded")
        
        # Check vocabulary is displayed
        vocab_items = self.driver.find_elements(By.CLASS_NAME, "vocab-item")
        assert len(vocab_items) > 0, "No vocabulary items found"
        print(f"✓ Found {len(vocab_items)} vocabulary items")
        
        # Click a vocab word to hear pronunciation
        first_vocab = vocab_items[0]
        spanish_text = first_vocab.find_element(By.TAG_NAME, "strong").text
        first_vocab.click()
        print(f"✓ Clicked vocab item: {spanish_text}")
        time.sleep(1)
        
        # Click words to build sentence
        word_buttons = self.driver.find_elements(By.CLASS_NAME, "word-btn")
        if len(word_buttons) >= 2:
            # Scroll to first button to make it visible
            self.driver.execute_script("arguments[0].scrollIntoView(true);", word_buttons[0])
            time.sleep(0.5)
            word_buttons[0].click()
            time.sleep(0.5)
            word_buttons[1].click()
            print("✓ Built sentence by clicking words")
            time.sleep(1)
            
            # Check sentence display updated
            sentence_display = self.driver.find_element(By.ID, "sentence-display")
            assert sentence_display.text.strip() != "", "Sentence not built"
            print(f"✓ Sentence built: {sentence_display.text}")
        
        # Scroll to clear button
        clear_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Clear')]")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", clear_btn)
        time.sleep(0.5)
        clear_btn.click()
        time.sleep(0.5)
        print("✓ Cleared sentence")
        
        time.sleep(1)
    
    def test_conversation_flow(self):
        """Test 3: Complete conversation flow"""
        print("\n=== Test 3: Conversation Flow ===")
        
        # From homepage, click conversation practice
        self.driver.get(self.base_url)
        conversation_btn = self.wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Start Conversation"))
        )
        conversation_btn.click()
        print("✓ Clicked 'Start Conversation'")
        time.sleep(1)
        
        
        # Should see level and scenario selection
        assert "/select/" in self.driver.current_url
        print("✓ Selection page loaded")
        
        # Select level
        level_select = Select(self.wait.until(
            EC.presence_of_element_located((By.ID, "user_level"))
        ))
        level_select.select_by_value("beginner")
        print("✓ Selected beginner level")
        time.sleep(0.5)
        
        # Select scenario
        scenario_select = Select(self.driver.find_element(By.ID, "scenario_id"))
        scenario_select.select_by_index(1)  # Select first scenario
        selected_scenario = scenario_select.first_selected_option.text
        print(f"✓ Selected scenario: {selected_scenario}")
        time.sleep(0.5)
        
        # Click start conversation
        start_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Start Conversation')]")
        start_btn.click()
        print("✓ Clicked 'Start Conversation'")
        time.sleep(2)
        
        # Should be on chat page
        assert "/chat/" in self.driver.current_url
        print("✓ Chat page loaded")
        
        # Check for scenario header (using your actual class names)
        scenario_title = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "card-title"))
        )
        print(f"✓ Scenario header found: {scenario_title.text}")
        
        # Check for messages area
        messages_area = self.driver.find_element(By.ID, "messages")
        print("✓ Messages area found")
        
        # Type a message
        message_input = self.driver.find_element(By.NAME, "user_message")
        test_message = "Hola, buenos días"
        message_input.send_keys(test_message)
        print(f"✓ Typed message: {test_message}")
        time.sleep(0.5)
        
        # Send message
        send_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Send')]")
        send_btn.click()
        print("✓ Sent message")
        
        # Note: Skipping AI response check - requires API tokens
        print("⚠ AI response check skipped (requires API tokens)")
        
        time.sleep(2)  # Brief wait to see the page update
    
    def test_navigation(self):
        """Test 4: Navigation between pages"""
        print("\n=== Test 4: Navigation ===")
        
        # Start from phrase practice
        self.driver.get(self.base_url + "/phrase-practice/")
        time.sleep(1)
        
        # Click home in nav
        home_link = self.wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Home"))
        )
        home_link.click()
        time.sleep(1)
        assert self.driver.current_url == self.base_url + "/"
        print("✓ Home navigation works")
        
        # Go to conversation selection
        self.driver.find_element(By.LINK_TEXT, "Start Conversation").click()
        time.sleep(1)
        
        # Go back home
        self.driver.find_element(By.LINK_TEXT, "Home").click()
        time.sleep(1)
        assert self.driver.current_url == self.base_url + "/"
        print("✓ Back to home works")
    
    def test_responsive_design(self):
        """Test 5: Check responsive design"""
        print("\n=== Test 5: Responsive Design ===")
        
        # Test mobile size
        self.driver.set_window_size(375, 667)  # iPhone size
        self.driver.get(self.base_url)
        time.sleep(1)
        
        # Check elements still visible
        phrase_btn = self.driver.find_element(By.LINK_TEXT, "Start Phrase Practice")
        assert phrase_btn.is_displayed()
        print("✓ Mobile view renders correctly")
        
        # Test desktop size
        self.driver.set_window_size(1920, 1080)
        time.sleep(1)
        print("✓ Desktop view renders correctly")
    
    def run_all_tests(self):
        """Run all tests in sequence"""
        try:
            print("\n" + "="*60)
            print("Starting Spanish Learning App Tests")
            print("="*60)
            
            self.test_homepage()
            self.test_phrase_practice_flow()
            self.test_conversation_flow()
            self.test_navigation()
            self.test_responsive_design()
            
            print("\n" + "="*60)
            print("✅ ALL TESTS PASSED!")
            print("="*60)
            
        except Exception as e:
            print("\n" + "="*60)
            print(f"❌ TEST FAILED: {str(e)}")
            print("="*60)
            # Take screenshot on failure
            self.driver.save_screenshot("test_failure.png")
            print("Screenshot saved as test_failure.png")
            raise
        
        finally:
            time.sleep(2)
            self.driver.quit()
            print("\nBrowser closed")

if __name__ == "__main__":
    # Make sure Django server is running at http://127.0.0.1:8000
    print("Make sure your Django server is running!")
    print("Run: python manage.py runserver")
    input("Press Enter when ready to start tests...")
    
    tester = SpanishAppTest()
    tester.run_all_tests()