class LoginPageLocators:
    USERNAME_INPUT = "input[name='username']"
    PASSWORD_INPUT = "input[name='password']"
    LOGIN_BUTTON = "button[type='submit']"
    LOGIN_ERROR_MESSAGE = ".oxd-alert-content > p" # A more generic selector, to be refined if needed
    FORGOT_PASSWORD_LINK = "a[href='/web/index.php/auth/requestPasswordResetCode']"