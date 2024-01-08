from datetime import datetime
import pyautogui
from time import *
import pytesseract
from PIL import Image, ImageGrab
import random
import string
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
import pyperclip
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
divide_by_screen_width = 1 / SCREEN_WIDTH
divide_by_screen_height = 1 / SCREEN_HEIGHT
rational_locations = {'travel_img_location': (0.14081632653061224, 0.19351464435146443),
                      'go_to_terravilla_button_location': (0.4802721088435374, 0.33682008368200833),
                      'infiniportal_location': (0.710204081632653, 0.5512552301255229),
                      'infiniportal_input_box': (0.5299319727891156, 0.4623430962343096),
                      'store_search_box': (0.4020408163265306, 0.41841004184100417),
                      'store_sell_tab_location': (0.7047619047619047, 0.3598326359832636),
                      'buysell_max_button_location': (0.6210884353741496, 0.6903765690376569),
                      'input_quantity_location': (0.5285714285714286, 0.7018828451882845),
                      'confirm_buysell_location': (0.5061224489795918, 0.811715481171548),
                      'log_out_button_location': (0.9775510204081632, 0.37656903765690375),
                      'profile_clicked_by_mistake': (0.38095238095238093, 0.27928870292887026),
                      'large_map_button': (0.02040816326530612, 0.37656903765690375),
                      'input_highlight_with_mouse': (0.5272108843537414, 0.700836820083682)}

scaled_locations = {key: (value[0] * SCREEN_WIDTH, value[1] * SCREEN_HEIGHT) for key, value in
                    rational_locations.items()}


# Colors
fountain_color = (207, 138, 205)
bucks_store_color = (60, 82, 139)
energy_yellow_color = (227, 255, 55)
ranger_farms_shop_color = (71, 65, 148)
red_elephant = (255, 83, 193)
sell_desk_color = (240, 235, 198)

# meaning the chrom message takes 70 on the y-axis
all_accounts_usernames = [
    'bdzzzks',
    'q3dylz8', 'brqjbvt', 'uk029z1', 'ozsnf4p', 'adfwyt6', 'er1xaha', '1rrl8cc', 'or0iqvz',
    'q6fimvz', 'ghv029t', 'hmdmrfn', 'rfjz9zh', 'rvdhf7y', 'xjgk3hz', 'ocwu8jg', '8mdvnds',
    'lw1hv4n', 'zyovetr', 'vmpmpzo', 'rayehq3', 'z3l6oqk', 'excai3x', 'xkzibwm', 'snlbv8m',
    'etave6v', 'akbr4tr', 'swl4k98', 'emyv8bs', 'wus6xsq', 'kdsfvgu', '6zkyjwm', 'cc0pcu9',
    'sct9irs', '796pnn7', '4oet7xv', 'scdxrdx', 'lvpk5kk', 'smemhms', '7dnxg7g', 'taembyf',
    'u2tjmkg', 'bzjbxpf', 'xwwjrly', 'hj3etfj', 'wkhogza', 'u3wy1lm', '9ndpjcj', 'syvqwpe',
    'tf35mk', 'kw5gh0', 'j5tqfq', 'zbq22f', 'r1z2ei', 'fgbi5m', 'wnzqoe', 'decatd', 'hxgogz',
    'viclqb', 'pvwyem', 'i4izfv', 'emwe2r', 'qlqgwq', 'jhy2xj', 'rlp1nx', '19ctfr', 'x9f1ni',
    'anjve6', 'rycfio', 'myllve', '30ubau', 'suc2gs', '6vaxmv', 'payten', '7tpxxs', 'h8frlx',
    'qsqtxo', 'pgpazw', 'qikpto', 'qjp507', 'ppje8u', 'xb2q31', '3awsep', 'iscdn4', 'edr2kk', 'fdrcza', 'ryvtan',
    'ksxxzz8', 'kiaibdd', 'fojoahl', 'rj2n50b', 'dpfoogf', 'qfickwu', '2hop9fc', 'ytenr1e',
    'zfllar', 'v8t1kb', 'w4klhh',
    'iow44i', 'aysxns', '6iqkg9', 'wnze0g', '06upxd', 'h9govt', 'sfmhyp', 'trsht4', 'zqa57l', 'kbmi5d', 'xbb5e3',
    'zlvxxj', 'ylmyyp',
    'plmfecp', 'qmglxkl', 'a81hzpf', 'e9hb4by', 'svisudy', '71kwstw', 'ozhxtku', 'k5w6030', 'dwhpdui', 'rfyq3fk',
    'blhwqzn', 'czgw5pq', '9crrnvj', 'vtfz9jh', 'llhe2nk', 'ksyw2ja',
    'z1dgnno', 'nenfedo', 'wb6tnej', 'odf1pff', 'j6rbiwc', 'vysswns', 'fejygpl', 'doptz9k',
    'nyatznk', 'k41iwpr', 't5oqjxu', 'lbegaml', 'i9knljk', 'iqepkq0', 'quagik5', ]


def highlight_with_mouse():
    # Set the duration for mouse actions (adjust as needed)
    duration = 0.5

    # Get the current mouse position
    # start_x, start_y = pyautogui.position()
    start_x, start_y = scaled_locations['input_highlight_with_mouse']

    # Press the mouse down
    pyautogui.mouseDown()

    # Move the mouse to the left (you can adjust the distance)
    pyautogui.move(-50, 0, duration=duration)

    # Release the mouse
    pyautogui.mouseUp()

    # Wait for a moment (optional)
    sleep(1)

    # If you want to return the mouse to the original position (optional)
    pyautogui.moveTo(start_x, start_y, duration=duration)


def find_pixels_with_color(image_path, target_color):
    # Open the image
    img = Image.open(image_path)

    # Get the width and height of the image
    width, height = img.size

    # Create a list to store the coordinates of pixels with the target color
    matching_pixels = []

    # Iterate through each pixel in the image
    for x in range(width):
        for y in range(height):
            # Get the RGB values of the current pixel
            pixel_color = img.getpixel((x, y))

            # Check if the pixel color matches the target color
            if pixel_color == target_color:
                matching_pixels.append((x, y))

    return matching_pixels


def generate_random_username():
    # Combine digits and letters
    characters = string.digits + string.ascii_letters

    # Generate a random string of length 6
    random_string = ''.join(random.choice(characters) for _ in range(7)).lower()

    return random_string


def send_image_email(body_text):
    my_email = "roied032@gmail.com"
    receive_mail = "roiefiz@icloud.com"
    gmail_app_python_password = "jbvlmgjssnkqipqq"

    subject = "Message with Image"
    body = f"Error at M's bot {body_text}"

    # Create the MIMEMultipart object
    em = MIMEMultipart()
    em['From'] = my_email
    em['To'] = receive_mail
    em['Subject'] = subject

    # Attach the body as text
    em.attach(MIMEText(body, 'plain'))

    # Attach the image
    image_path = "problems.png"
    with open(image_path, 'rb') as img_file:
        img = MIMEImage(img_file.read(), name="image.png")
        em.attach(img)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host='smtp.gmail.com', port=465, context=context) as connection:
        connection.login(user=my_email, password=gmail_app_python_password)
        connection.sendmail(from_addr=my_email, to_addrs=receive_mail, msg=em.as_string())


def record_error(*args):
    with open(file='errors.text', mode='a') as errors_file:

        capture_error = ImageGrab.grab()
        capture_error.save('problems.png')
        errors_file.write(f'Problem screenshot at problems.png file \n {datetime.now()} {args}')
    send_image_email(body_text=args)


def keyboard_move_figure(direction: str, duration: float):
    pyautogui.keyDown(direction)
    sleep(duration)
    pyautogui.keyUp(direction)


def find_first_pixel(target_color, image=None):
    if image is None:
        image = ImageGrab.grab()
    width, height = image.size
    pixels = list(image.getdata())

    for y in range(height):
        for x in range(width):
            pixel_value = pixels[y * width + x]
            if pixel_value == target_color:
                return x, y

    # If the target color is not found, return None
    return None


def press_on_color(target_color: tuple = (181, 211, 239)):
    screenshot = ImageGrab.grab()
    screenshot.save("screenshot.png")
    # Open an image
    image_path = "screenshot.png"  # Replace with the path to your image
    img = Image.open(image_path)
    # Find the location of the first pixel with the target color
    result = find_first_pixel(target_color, img)
    if result:
        print(f"Location of the first pixel with color {target_color}: {result}")
        # Specify the coordinates (x, y) where you want to click and hold
        x, y = result

        # Set the duration to click and hold (in seconds)
        hold_duration = 0.3

        # Click and hold at the specified location
        pyautogui.mouseDown(x, y)

        # Sleep for the specified duration
        sleep(hold_duration)

        # Release the mouse click
        pyautogui.mouseUp(x, y)
        pos = (x, y)
        return pos
    else:
        print(f"No pixel found with color {target_color}")
        return False


def make_sure_game_is_on():
    counter = 0
    print('Making Sure The game is on')
    while not bool(find_first_pixel(energy_yellow_color)):
        print('Game is still not on')
        sleep(2)
        counter += 1


class PixelsUser:
    def __init__(self, my_driver=None, operation_system='windows'):
        self.username = generate_random_username()
        self.email = self.username + '@mail7.io'
        self.software = 'windows'
        self.website = 'https://play.pixels.xyz'
        if operation_system == 'macOS':
            self.ctrl_keyboard = 'command'
        else:
            self.ctrl_keyboard = 'ctrl'
        self.inventory_dic = {
            1: '1',
            2: '2',
            3: '3',
            4: '4',
            5: '5',
            6: '6'
        }
        if my_driver is None:
            self.driver = webdriver.Chrome()
        else:
            self.driver = my_driver

        self.account_errors = 0

    def look_for_profile_mistake(self):
        try:
            exit_profile_button = self.driver.find_element(By.CLASS_NAME, 'Profile_closeButton__1n0Um')
        except NoSuchElementException:
            pass
        else:
            exit_profile_button.click()
            sleep(1)

    def get_energy_amount(self):
        return float(self.driver.find_element(By.CLASS_NAME, 'Hud_energytext__3PQZQ').text)

    def skip_dialog(self):
        sleep(3)
        skip_button_class = 'GameDialog_skip__Y5RGE'
        while True:
            try:
                skip_button = self.driver.find_element(By.CLASS_NAME, skip_button_class)
            except NoSuchElementException:
                print('Dialog probably over')
                break
            else:
                skip_button.click()
                print('skip button clicked ')
                continue
            finally:
                sleep(0.5)

    def get_berry_amount(self):
        wallet = self.driver.find_element(By.CLASS_NAME, 'commons_coinBalance__d9sah').text
        if ',' in wallet:
            wallet = float(wallet.replace(',', ''))
        else:
            wallet = float(wallet)
        if wallet:
            return wallet

    def center_pointer(self):
        full_x, full_y = pyautogui.size()
        center_x = full_x / 2
        center_y = full_y / 2
        pyautogui.moveTo(center_x, center_y)

    def click_on_four_directions(self, offset=70):
        self.center_pointer()
        # Move right
        current_x, current_y = pyautogui.position()
        pyautogui.moveTo(current_x + offset, current_y)
        pyautogui.click()
        self.look_for_profile_mistake()

        self.center_pointer()
        # Move up
        pyautogui.moveTo(current_x, current_y - offset)
        pyautogui.click()
        self.look_for_profile_mistake()

        self.center_pointer()
        # Move down
        pyautogui.moveTo(current_x, current_y + offset)
        pyautogui.click()
        self.look_for_profile_mistake()

        self.center_pointer()
        # Move left
        pyautogui.moveTo(current_x - offset, current_y)
        pyautogui.click()
        self.look_for_profile_mistake()

    def start_game_with_existing_account(self):
        self.driver.get(self.website)
        self.driver.maximize_window()
        sleep(10)
        log_in = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[3]/div[2]/div[1]/button[1]')
        log_in.click(), sleep(2)
        email_radio = self.driver.find_element(By.XPATH,
                                               '//*[@id="__next"]/div/div[3]/div[2]/div[1]/div[2]/div[1]/label[3]/input')
        email_radio.click(), sleep(2)
        email_input = self.driver.find_element(By.XPATH,
                                               '/html/body/div[1]/div/div[3]/div[2]/div[1]/div[2]/div[2]/input')
        email_input.send_keys(f'{self.email}'), sleep(1)
        pyautogui.press('enter'), sleep(2)
        pyautogui.hotkey(self.ctrl_keyboard, 't')
        sleep(2)
        self.driver.switch_to.window(self.driver.window_handles[1]), sleep(1)
        self.driver.get('https://www.mail7.io/'), sleep(3)
        input_mail7_mail = self.driver.find_element(By.XPATH, '/html/body/main/section[2]/div/form/div[1]/input[1]')
        input_mail7_mail.send_keys(self.email)
        sleep(1)
        self.driver.find_element(By.XPATH, '/html/body/main/section[2]/div/form/div[1]/input[2]').click()
        sleep(13)
        email_with_the_code = self.driver.find_elements(By.CLASS_NAME, 'mail-col')[2]
        email_with_the_code.click(), sleep(6)
        # Capture the content of the window
        screenshot = pyautogui.screenshot()
        # Use Tesseract to perform OCR on the captured image
        try:
            text = pytesseract.image_to_string(screenshot)
        except Exception as pytercreept_error:
            record_error(f'pytercreept_error {pytercreept_error} username: {self.username}')
            mail_7_x = 0.75 * SCREEN_WIDTH
            mail_7_y = 0.75 * SCREEN_HEIGHT
            pyautogui.click(mail_7_x, mail_7_y)
            sleep(1.5)
            pyautogui.hotkey(self.ctrl_keyboard, "A")
            sleep(1.2)
            pyautogui.hotkey(self.ctrl_keyboard, "C")
            sleep(1)
            text = pyperclip.paste()
        finally:
            code_end_location = str(text).find('is your one-time code')
            end = int(code_end_location) - 1
            start = end - 7
            code = str(text)[start:end]
            print(code)
            pyautogui.hotkey(self.ctrl_keyboard, 'w')
            self.driver.switch_to.window(self.driver.window_handles[0]), sleep(1)
            pyautogui.typewrite(f'{code}')
            sleep(3)
            pyautogui.hotkey('enter')
            sleep(3)
            pyautogui.hotkey('enter')
            sleep(3)
            start_game_button = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[3]/div[2]/button[1]')
            start_game_button.click()
            sleep(6)

    def center_terravilla(self):
        sleep(10)
        pyautogui.doubleClick(scaled_locations['travel_img_location'])
        sleep(3)
        pyautogui.doubleClick(scaled_locations['go_to_terravilla_button_location'])
        sleep(4)
        for num in range(18):
            press_on_color(fountain_color)
        keyboard_move_figure('down', 1)
        keyboard_move_figure('right', 1)
        keyboard_move_figure('up', 1)
        keyboard_move_figure('left', 1)
        keyboard_move_figure('down', 1)
        for num in range(18):
            press_on_color(fountain_color)

    def go_to_farm(self, farm_number=2498):
        sleep(5)
        pyautogui.keyDown('left')
        sleep(5.7)
        pyautogui.keyUp('left')
        make_sure_game_is_on()
        pyautogui.keyDown('up')
        sleep(6)
        pyautogui.keyUp('up')
        for improve in range(8):
            press_on_color(target_color=ranger_farms_shop_color)
        sleep(8)
        make_sure_game_is_on()
        pyautogui.keyDown('right')
        sleep(1.6)
        pyautogui.keyUp('right')
        pyautogui.keyDown('up')
        sleep(4)
        pyautogui.keyUp('up')
        sleep(2)
        pyautogui.doubleClick(scaled_locations['infiniportal_location'], duration=0.3)
        sleep(1)
        pyautogui.click(x=scaled_locations['infiniportal_location'][0], y=scaled_locations['infiniportal_location'][1],
                        duration=0.3)
        sleep(2.5)
        try:
            farm_search = self.driver.find_element(By.TAG_NAME, 'input')
        except NoSuchElementException as ranger_error:
            record_error(f'ranger error {ranger_error} username: {self.username}')
            self.account_errors += 1
            self.center_terravilla()
            self.go_to_farm()
        else:
            counter = 0
            while f'{farm_number}' not in str(farm_search.get_attribute('value')):
                print(str(farm_search.get_attribute('value')))
                farm_search.clear()
                sleep(1)
                farm_search.send_keys(f'{farm_number}')
                sleep(2)
                farm_search = self.driver.find_element(By.TAG_NAME, 'input')
                counter += 1
                if counter >= 3:
                    break
            pyautogui.hotkey('enter')
            sleep(10)

    def click_on_all_the_field(self, rows=7, go_down=1.2, distance_field=0.2):
        sleep(7)
        seeds_amount = self.discover_seeds_amount()
        keyboard_move_figure('up', 2)
        if seeds_amount < 30:
            rows = 3
            go_down = 0.25
        else:
            rows = 7  # consider to add elif for the second phase with 26 seeds
            go_down = 1.4
        for i in range(3, 0, -1):
            pyautogui.hotkey(self.inventory_dic[i], duration=0.25)
            for number in range(18):
                press_on_color(red_elephant)
            keyboard_move_figure('right', 0.5)
            keyboard_move_figure('down', 0.5)
            keyboard_move_figure('right', 3)
            for _ in range(1, rows):
                if _ % 2 == 0:
                    for field in range(10):
                        self.click_on_four_directions()
                        self.look_for_profile_mistake()
                        keyboard_move_figure('right', distance_field)
                        if field == 9:
                            self.click_on_four_directions()
                else:
                    for field in range(10):
                        self.click_on_four_directions()
                        self.look_for_profile_mistake()
                        keyboard_move_figure('left', distance_field)
                        if field == 9:
                            self.click_on_four_directions()
                keyboard_move_figure('up', distance_field)
            pyautogui.hotkey(self.inventory_dic[i], duration=0.25)
            keyboard_move_figure('left', 0.5)
            keyboard_move_figure('down', go_down)

    def go_to_bucks_store(self):
        keyboard_move_figure('right', 5.17)
        for pp in range(6):
            press_on_color(bucks_store_color)
        sleep(9)
        make_sure_game_is_on()
        keyboard_move_figure('right', 3.3)
        keyboard_move_figure('up', 2)

    def sell_goods(self, items_to_sell='Popberry'):
        x_desk, y_desk = press_on_color(target_color=sell_desk_color)
        x_desk -= 20
        y_desk -= 20
        pyautogui.doubleClick(x=x_desk, y=y_desk)
        sleep(2)
        store_sell_class = 'Store_sellButton__F9vtc'
        try:
            self.driver.find_element(By.CLASS_NAME, store_sell_class).click()
        except NoSuchElementException as sell_error:
            record_error(f'Store sell error {sell_error} username: {self.username}')
            self.account_errors += 1
            sleep(1)
            pyautogui.hotkey('esc')
            self.center_terravilla()
            self.go_to_bucks_store()
            self.sell_goods()
        sleep(1)
        all_items_for_sale_class = 'Store_card-title__InPpB'
        all_items_for_sale = self.driver.find_elements(By.CLASS_NAME, f'{all_items_for_sale_class}')
        for item in all_items_for_sale:
            if f'{items_to_sell}' in item.text and 'Seeds' not in item.text:
                item.click()
                sleep(1)
        # Sell Max button
        sleep(1)
        pyautogui.doubleClick(1318, 700)
        sleep(2)
        # confirm sell
        sleep(1.5)
        pyautogui.click(scaled_locations['confirm_buysell_location'], duration=0.35)
        sleep(1)
        pyautogui.hotkey('esc')

    def buy_goods(self, items_to_buy='Popberry Seeds'):
        pyautogui.hotkey('esc')
        sleep(1)
        berries_wallet = self.get_berry_amount()
        sleep(2)
        x_desk, y_desk = press_on_color(target_color=sell_desk_color)
        x_desk += 20
        y_desk += 30
        pyautogui.doubleClick(x=x_desk, y=y_desk)
        sleep(5)
        try:
            self.driver.find_element(By.CLASS_NAME, 'Store_filter__qtqd7').send_keys(items_to_buy)
        except NoSuchElementException as store_buy_error:
            record_error(f'Store Buy Error {store_buy_error} username: {self.username}')
            self.account_errors += 1
            pyautogui.hotkey('esc')
            self.center_terravilla()
            sleep(2)
            self.go_to_bucks_store()
            sleep(2)
            self.buy_goods()
        else:
            cards_founded_titles = 'Store_card-title__InPpB'
            sleep(3)
            self.driver.find_element(By.CLASS_NAME, cards_founded_titles).click()
            sleep(3)
            pyautogui.moveTo(1066, 718)
            sleep(2)
            highlight_with_mouse()
            sleep(2)
            if berries_wallet >= 65:
                pyautogui.typewrite('65')
            else:
                pyautogui.typewrite(f'{berries_wallet}')
            sleep(1.5)
            # confirm Buy
            pyautogui.moveTo(1000, 910)
            pyautogui.doubleClick(scaled_locations['confirm_buysell_location'], duration=0.3)
            sleep(1)
            pyautogui.hotkey('esc')
            sleep(1)
            seeds_amount = self.discover_seeds_amount()
            while seeds_amount is None:
                self.buy_goods()
                seeds_amount = self.discover_seeds_amount()

    def discover_seeds_amount(self):
        all_inventory_quantities = self.driver.find_elements(By.CLASS_NAME, 'Hud_quantity__V_YWQ')
        for item_quantity in all_inventory_quantities:
            if 'x' in item_quantity.text:
                print(f'Current seeds {item_quantity}, {item_quantity.text[1]}')
                number_of_seeds = item_quantity.text[1:]
                if ',' in number_of_seeds:
                    number_of_seeds = float(number_of_seeds.replace(',', ''))
                else:
                    number_of_seeds = float(number_of_seeds)
                return number_of_seeds


