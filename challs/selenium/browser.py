#!/usr/bin/python3

from mock import patch
from pyvirtualdisplay import Display
from selenium import webdriver


@patch('pyvirtualdisplay.abstractdisplay.AbstractDisplay.lock_files')
def selenium_init(mock_lock):
    """
        Init selenium instance
    """
    mock_lock.return_value = []
    display = Display(visible=0, size=(800, 1024))
    display.start()

    browser = webdriver.Firefox()
    return browser


Browser = selenium_init()
