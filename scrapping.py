from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time

def scrape_amazon(selected_option,user_input='keyboard', path = 'scrapped/',
                  url='https://www.amazon.com/Manhattan-104-key-Keyboard-Built-Indicator/product-reviews/B07RQVB3HQ'
                      '/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews', direct_url=False):
    review_dict = {'comment': {}, 'time': {}}
    comment_count = 0
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)

    if not direct_url:
        search_bar = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "twotabsearchtextbox")))
        search_bar.click()
        search_bar.send_keys(user_input)
        search_btn = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "nav-search-submit-button")))
        search_btn.click()

        first_result = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[class= 'a-link-normal "
                                                         "s-underline-text "
                                                         "s-underline-link-text "
                                                         "s-link-style "
                                                         "a-text-normal']")))
        first_result.click()

    all_country_review = WebDriverWait(driver, 50).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[class='a-link-emphasis a-text-bold']")))

    if len(all_country_review) == 1:  # in case if there is no native country review option.
        all_country_review[0].click()
    else:
        all_country_review[1].click()  # going to all review section for all countries of the site.

    most_recent_dropdown = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "a-autoid-3-announce")))
    most_recent_dropdown.click()
    most_recent_option = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "sort-order-dropdown_1")))
    most_recent_option.click()
    try:
        verified_user_dropdown = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='a-autoid-4-announce']")))
        verified_user_dropdown.click()
        verified_user_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='reviewer-type-dropdown_1']")))
        verified_user_option.click()
    except:
        pass
    for page_number in range(10):  # for getting all the reviews by clicking next page.
        try:
            comments = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, 'div[class="a-row a-spacing-small review-data"]')))
            time_info = WebDriverWait(driver, 30).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, 'span[class="a-size-base a-color-secondary review-date"]')))
            if len(comments) < 10:  # end of line.
                print('yes')
                break
            for comment_index in range(len(comments)):
                # review_dict[f'{comment_index}'] = {'1': comments[comment_index].text,
                #                                    '2': time_info[comment_index].text}
                review_dict['comment'][comment_count] = comments[comment_index].text
                review_dict['time'][comment_count] = time_info[comment_index].text
                comment_count += 1
            print(f'done {page_number}')
            # clicking next page of review.
            time.sleep(0.3)

            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="cm_cr-pagination_bar"]/ul/li[2]/a'))).click()
        except:
            print('Time-out exception')
            time.sleep(0.5)
            continue
    print('done_web')
    df = pd.DataFrame(review_dict)
    if selected_option == '1':
        path_final =f'{path}/url_{int(time.time())}.csv'
        df.to_csv(path_final)
    else:
        path_final = f'{path}/{user_input}_{int(time.time())}.csv'
        df.to_csv(path_final)
    return path_final

# in the connector provide options to the user to avoid many of the exceptions.
# make the function more eficent.
