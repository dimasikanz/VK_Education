from selenium.webdriver.common.by import By


class BasePage:
    AUTHORIZED_USERNAME_LOCATOR = (
        By.CSS_SELECTOR,
        "[class*=right-module-userNameWrap]"
    )
    AUTHORIZED_USER_INFO_BUTTON_LOCATOR = (
        By.CSS_SELECTOR,
        "[class*=right-module-rightButton]"
    )


class LoginPageLocators:
    SIGN_IN_FIRST_LOCATOR = (By.CSS_SELECTOR, "[class*=responseHead-module-button]")
    SIGN_IN_SECOND_LOCATOR = (By.CSS_SELECTOR, "[class*=authForm-module-button]")
    EMAIL_FORM_LOCATOR = (By.NAME, "email")
    PASSWORD_FORM_LOCATOR = (By.NAME, "password")


class MainPageLocators(BasePage):
    SEGMENTS_BUTTON_LOCATOR = (By.CSS_SELECTOR, "[class*=center-module-segments]")
    CAMPAIGNS_BUTTON_LOCATOR = (By.CSS_SELECTOR, "[class*=center-module-campaigns]")

    CREATE_CAMPAIGN_BUTTON_LOCATOR = (
        By.CSS_SELECTOR,
        "[class*=dashboard-module-createButtonWrap] [class*=button-module-button]"
    )
    CREATE_CAMPAIGN_BUTTON_LOCATOR_IF_ZERO = (
        By.CSS_SELECTOR,
        "[href = '/campaign/new']"
    )
    VIDEO_VIEWS_PURPOSE_BUTTON_LOCATOR = (
        By.CSS_SELECTOR,
        ".column-list-item._videoviews"
    )
    URL_FIELD_LOCATOR = (By.CSS_SELECTOR, "[data-gtm-id=ad_url_text]")
    CAMPAIGN_NAME_FIELD_LOCATOR = (By.CSS_SELECTOR, ".input_campaign-name input")
    BUMPER_ADS_FORMAT_BUTTON_LOCATOR = (By.CSS_SELECTOR, "[id*=patterns_BumperAds]")
    PIN_LOCATOR = (By.CSS_SELECTOR, "[class*=layout-float__bottom-pin]")
    VIDEO_UPLOAD_BUTTON_LOCATOR = (
        By.XPATH,
        "//div[contains(text(), '16:9 (6 секунд)') or contains(text(), '16:9 (6 seconds)')]/../../../div/input"
    )
    UPLOAD_GREEN_CHECK_MARK_LOCATOR = (
        By.CSS_SELECTOR,
        "[class*=patternTabs-module-green]"
    )
    CREATE_CAMPAIGN_SUBMIT_BUTTON_LOCATOR = (
        By.CSS_SELECTOR,
        ".footer__button [data-class-name=Submit]"
    )
    NEW_CAMPAIGN_NAME_LOCATOR = (
        By.CSS_SELECTOR,
        "[data-row-id='central-1'] [class*=nameCell-module-campaignNameLink]"
    )
    CAMPAIGNS_LIST_SEARCH_FIELD_LOCATOR = (
        By.CSS_SELECTOR,
        "[class*=multiSelectSuggester-module-searchInput]"
    )
    CAMPAIGNS_TEXT_IN_SEARCH_LOCATOR = (
        By.CSS_SELECTOR,
        "[class*=optionsList-module-item] [class*=suggesterOptionsList-module-text]"
    )


class SegmentsPageLocators(BasePage):
    APPLICATIONS_AND_GAMES_ADD_SEGMENT_BUTTON_LOCATOR = (
        By.XPATH,
        "//div[contains(text(), 'Приложения и игры в соцсетях') or contains(text(), 'Applications and games in social networks')]"
    )

    CREATE_SEGMENT_BUTTON_LOCATOR = (
        By.CSS_SELECTOR,
        "[data-class-name=Submit] .button__text"
    )
    CREATE_SEGMENT_BUTTON_IF_ZERO_SEGMENTS_LOCATOR = (
        By.CSS_SELECTOR,
        "[href='/segments/segments_list/new/']"
    )
    ADD_SEGMENT_BUTTON_LOCATOR = (
        By.CSS_SELECTOR,
        "[class*=adding-segments-modal] [data-class-name=Submit]"
    )
    SEGMENT_NAME_FIELD_LOCATOR = (By.CSS_SELECTOR, ".input_create-segment-form input")
    FINAL_CREATE_SEGMENT_BUTTON_LOCATOR = (By.CLASS_NAME, "button_submit")
    NEW_SEGMENT_NAME_LOCATOR = (
        By.CSS_SELECTOR,
        "[data-row-id=central-0] [class*=cells-module-nameCell] a"
    )
    CHECKBOX_DURING_ADD_SEGMENT_LOCATOR = (
        By.CSS_SELECTOR,
        ".adding-segments-source__header [type=checkbox]"
    )

    VK_AND_OK_GROUPS_SOURCE_BUTTON_LOCATOR = (
        By.XPATH,
        "//span[contains(text(), 'OK AND VK GROUPS') or contains(text(),'Группы ОК и VK')]"
    )
    GROUP_URL_FIELD_LOCATOR = (By.CSS_SELECTOR, "[class*=input-module-input]")
    SELECT_ALL_LOCATOR = (By.CSS_SELECTOR, "[data-test=select_all]")
    ADD_SELECTED_ITEMS_BUTTON_LOCATOR = (
        By.CSS_SELECTOR,
        "[data-test=add_selected_items_button]",
    )
    NEW_SOURCE_VK_EDUCATION = (By.XPATH, "//span[@title='VK Образование']")
    SEGMENTS_LIST_BUTTON_LOCATOR = (
        By.XPATH,
        "//span[contains(text(), 'Segments list') or contains(text(),'Список сегментов')]"
    )
    VK_AND_OK_GROUPS_ADD_SEGMENT_BUTTON_LOCATOR = (
        By.XPATH,
        "//div[contains(text(), 'OK AND VK GROUPS') or contains(text(), 'Группы ОК и VK')]"
    )
    NEW_SEGMENT_CHECKBOX_LOCATOR = (By.CSS_SELECTOR, "[data-row-id=central-0] input")
    SELECT_ACTION_WITH_SEGMENT_BUTTON_LOCATOR = (
        By.CSS_SELECTOR,
        "[class*=segmentsTable-module-selectItem]"
    )
    DELETE_SEGMENT_BUTTON = (By.CSS_SELECTOR, "[data-id=remove]")
    DELETE_SOURCE_VK_EDUCATION = (
        By.XPATH,
        "//span[@title='VK Образование']/../../td/div/div/span"
    )
    CONFIRM_REMOVE_BUTTON_LOCATOR = (By.CLASS_NAME, "button_confirm-remove")
    SEGMENTS_LIST_SEARCH_FIELD_LOCATOR = (
        By.CSS_SELECTOR,
        "[class*=suggester-module-searchInput]"
    )
    SEGMENTS_IN_SEARCH_LOCATOR = (
        By.CSS_SELECTOR,
        "[class*=optionsList-module-option][title]"
    )
