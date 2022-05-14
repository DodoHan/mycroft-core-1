# Copyright 2016 Mycroft AI, Inc.
#
# This file is part of Mycroft Core.
#
# Mycroft Core is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Mycroft Core is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mycroft Core.  If not, see <http://www.gnu.org/licenses/>.

from mycroft_bus_client.message import Message
from mycroft.util.log import LOG
from urllib.request import urlopen
from urllib.request import Request
from urllib.error import URLError
from urllib.parse import urlencode
from mycroft import MycroftSkill
import json
import time

from robot_communication import BluetoothClient, Movement, MovementSpeed

timer = time.perf_counter


class RasaSkill(MycroftSkill):

    def __init__(self):
        """ The __init__ method is called when the Skill is first constructed.
        It is often used to declare variables or perform setup actions, however
        it cannot utilise MycroftSkill methods as the class does not yet exist.
        """
        super().__init__()
        self.log.info('[Flow Learning] in RasaSkill.__init__')
        LOG.info('in __init__, self.config_core = ' + str(self.config_core))
        self.url = "http://localhost:5005/webhooks/rest/webhook"
        mac_address = "88:25:83:f3:e9:f4"
        UUID_service = "0000ffe0-0000-1000-8000-00805f9b34fb"
        self.bluetoothClient = BluetoothClient(mac_address, UUID_service)

    def initialize(self):
        """ Perform any final setup needed for the skill here.
        This function is invoked after the skill is fully constructed and
        registered with the system. Intents will be registered and Skill
        settings will be available."""
        # my_setting = self.settings.get('my_setting')
        self.log.info(
            '[Flow Learning] in mycroft.skills.builtinskills.skill-rasa.__init__.py.RasaSkill.initialize, settings = ' + str(self.settings))

    '''
    Shore: no need
    @intent_handler('rasa')
    def handle_rasa_intent(self, message):
    '''

    def stop(self):
        pass

    def converse(self, message):
        LOG.info('[Flow Learning] in RasaSkill.converse ')
        utterances = message.data['utterances']
        utterance = utterances[0]
        LOG.info('[Flow Learning] in RasaSkill.converse, utterance =' +
                 str(utterance))

        # Shore: get utterance from Rasa
        params = {'sender': "0001", 'message': utterance}
        LOG.info('params are sent to rasa api:')
        # print(str(params))
        post_data = json.dumps(params, sort_keys=False)
        # print post_data
        req = Request(self.url, post_data.encode('utf-8'))
        req.add_header('Content-Type', 'application/json')
        try:
            begin = timer()
            f = urlopen(req)
            result_str = f.read()
            LOG.info("Request time cost %f" % (timer() - begin))
        except URLError as err:
            LOG.error('asr http response http code : ' + str(err.code))
            result_str = err.read()

        result_str = str(result_str, 'utf-8')
        LOG.info(result_str)

        recognized = json.loads(result_str)
        utteranceFromRasa = recognized[0]['custom']['option'][0]['utter']
        LOG.info(utteranceFromRasa)

        # Shore: action
        action = recognized[0]['custom']['action4VoiceAssistant']
        LOG.info('action:' + action)
        '''
        action.robot.stop
        action.robot.dance
        '''
        if (action == 'action.robot.dance'):
            self.bluetoothClient.executeMovement(Movement.DANCE,
                                                 MovementSpeed.MEDIUM)
        elif (action == 'action.robot.walk'):
            self.bluetoothClient.executeMovement(Movement.WALK,
                                                 MovementSpeed.MEDIUM)
        elif (action == 'action.robot.move_forward'):
            self.bluetoothClient.executeMovement(Movement.MOVE_FORWARD,
                                                 MovementSpeed.MEDIUM)
        elif (action == 'action.robot.move_backward'):
            self.bluetoothClient.executeMovement(Movement.MOVE_BACKWARD,
                                                 MovementSpeed.MEDIUM)
        elif (action == 'action.robot.move_right'):
            self.bluetoothClient.executeMovement(Movement.MOVE_RIGHT,
                                                 MovementSpeed.MEDIUM)
        elif (action == 'action.robot.move_left'):
            self.bluetoothClient.executeMovement(Movement.MOVE_LEFT,
                                                 MovementSpeed.MEDIUM)
        elif (action == 'action.robot.smile'):
            self.bluetoothClient.executeMovement(Movement.HAPPY,
                                                 MovementSpeed.MEDIUM)
        elif (action == 'action.robot.stop'):
            self.bluetoothClient.executeMovement(Movement.STOP,
                                                 MovementSpeed.MEDIUM)

        '''
        - custom:
            option:
                - utter: "Sure, let me dance."
                - utter: "Yes, let me dance."
            action4VoiceAssistant: "action.robot.dance"
        '''
        self.speak(str(utteranceFromRasa), expect_response=True)
        return True

    # Shore: never used, do we need to implement it here?
    def deactive(self):
        LOG.info('[Flow Learning] skill_id =' + str(self.skill_id))
        self.bus.emit(
            Message('deactive_skill_request', {'skill_id': self.skill_id}))


def create_skill():
    return RasaSkill()
