from selenium.webdriver.common.by import By


class LogInLocators:
    SIGN_IN_FIRST_LOCATOR = (By.CSS_SELECTOR, "[class*=responseHead-module-button]")
    SIGN_IN_SECOND_LOCATOR = (By.CSS_SELECTOR, "[class*=authForm-module-button]")
    EMAIL_FORM_LOCATOR = (By.NAME, "email")
    PASSWORD_FORM_LOCATOR = (By.NAME, "password")
    AUTHORIZATION_ERROR_LOCATOR = (By.CLASS_NAME, "formMsg_text")


class AuthorizedUsernameButtonLocators:
    AUTHORIZED_USERNAME_LOCATOR = (
        By.CSS_SELECTOR,
        "[class*=right-module-userNameWrap]"
    )
    AUTHORIZED_USER_INFO_BUTTON_LOCATOR = (
        By.CSS_SELECTOR,
        "[class*=right-module-rightButton]"
    )
    LOGOUT_LOCATOR = (
        By.CSS_SELECTOR,
        '[class*=rightMenu-module-shownRightMenu] [href="/logout"]'
    )


class ElseButtonsLocators:
    ELSE_BUTTON_LOCATOR = (
        By.CSS_SELECTOR,
        "[class*=center-module-button][class*=center-module-more]"
    )
    ELSE_PROFILE_BUTTON_LOCATOR = (By.CSS_SELECTOR, '[data-gtm-id="pageview_profile"]')
    ELSE_BALANCE_BUTTON_LOCATOR = (By.CSS_SELECTOR, '[data-gtm-id="pageview_billing"]')
    ELSE_TOOLS_BUTTON_LOCATOR = (
        By.CSS_SELECTOR,
        '[class*=center-module-moreMenuButton][href="/tools"]'
    )


class ProfileLocators:
    PROFILE_BUTTON_LOCATOR = (By.CSS_SELECTOR, "[class*=center-module-profile]")
    FIO_FORM_LOCATOR = (By.CSS_SELECTOR, '[data-name="fio"] input')
    INN_FORM_LOCATOR = (By.CSS_SELECTOR, '[data-name="ordInn"] input')
    PHONE_FORM_LOCATOR = (By.CSS_SELECTOR, '[data-name="phone"] input')
    SAVE_BUTTON_LOCATOR = (By.CLASS_NAME, "button__text")
    SUCCESS_NOTIFICATION_LOCATOR = (
        By.CSS_SELECTOR,
        '[data-class-name="SuccessView"] ._notification__content'
    )
    CONTACT_INFORMATION_TITLE_LOCATOR = (By.CLASS_NAME, "profile__title")


class BalanceLocators:
    BALANCE_BUTTON_LOCATOR = (By.CSS_SELECTOR, "[class*=center-module-billing]")
    PAYER_LOCATOR = (By.CLASS_NAME, "deposit__payment-form__title")


class ToolsLocators:
    TOOLS_BUTTON_LOCATOR = (By.CSS_SELECTOR, "[class*=center-module-tools]")
    FEED_LIST_LOCATOR = (By.CSS_SELECTOR, "[class*=feeds-module-title]")


class OtherLocators:
    PAGE_BACKGROUND_LOCATOR = (By.CSS_SELECTOR, "[style='height: 100%;']")
