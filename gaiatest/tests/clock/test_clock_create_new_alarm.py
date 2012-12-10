# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
from gaiatest.tests.clock import clock_object
import time

class TestClockCreateNewAlarm(GaiaTestCase):
    
    def setUp(self):
        GaiaTestCase.setUp(self)

        # unlock the lockscreen if it's locked
        self.lockscreen.unlock()

        # launch the Clock app
        self.app = self.apps.launch('Clock')

    
    def test_clock_create_new_alarm(self):
        """ Add a alarm
        
        https://moztrap.mozilla.org/manage/case/1772/ 
        
        """
        self.wait_for_element_displayed(*clock_object._alarm_create_new_locator)

        # Get the number of alarms set, before adding the new alarm
        initial_alarms_count = len(self.marionette.find_elements(*clock_object._all_alarms))

        # create a new alarm with the default values that are available
        self.marionette.find_element(*clock_object._alarm_create_new_locator).click()
        self.marionette.find_element(*clock_object._alarm_save_locator).click()

        # verify the banner-countdown message appears
        self.wait_for_element_displayed(*clock_object._banner_countdown_notification_locator)
        alarm_msg = self.marionette.find_element(*clock_object._banner_countdown_notification_locator).text
        self.assertTrue('The alarm is set for' in alarm_msg, 'Actual banner message was: "' + alarm_msg + '"')

        # Get the number of alarms set after the new alarm was added
        new_alarms_count = len(self.marionette.find_elements(*clock_object._all_alarms))

        # Ensure the new alarm has been added and is displayed
        self.assertTrue(initial_alarms_count < new_alarms_count,
            'Alarms count did not increment')
        
        
    def tearDown(self):
        
        # delete the new alarm
        clock_object.delete_alarm(self)
        
        # close the app
        if hasattr(self, 'app'):
            self.apps.kill(self.app)

        GaiaTestCase.tearDown(self)
