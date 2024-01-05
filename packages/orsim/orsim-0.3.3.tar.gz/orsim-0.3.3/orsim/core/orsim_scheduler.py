from abc import ABC, abstractclassmethod, abstractmethod
import asyncio, json, logging, time, os, pprint

from datetime import datetime
# from apps import orsim
from orsim.messenger import Messenger

from random import random
from .orsim_env import ORSimEnv

from orsim.tasks import start_agent


class ORSimScheduler(ABC):

    def __init__(self, run_id, scheduler_id, orsim_settings, init_failure_handler='soft'):

        if ORSimEnv.messenger_settings is None:
            raise Exception("Please Initialize ORSimEnv.set_backend()")

        self.orsim_settings = ORSimEnv.validate_orsim_settings(orsim_settings)

        self.run_id = run_id
        self.scheduler_id = scheduler_id
        self.time = 0

        self.init_failure_handler = init_failure_handler

        self.agent_collection = {}
        self.agent_stat = {}

        self.agent_credentials = {
            'email': f"{self.run_id}_{self.scheduler_id}_ORSimScheduler",
            'password': "secret_password",
        }

        self.agent_messenger = Messenger(ORSimEnv.messenger_settings, self.agent_credentials, f"{self.run_id}/{self.scheduler_id}/ORSimScheduler", self.on_receive_message)

        self.pp = pprint.PrettyPrinter(indent=2)
        logging.info(f'Starting new {scheduler_id= } for {run_id= }')


    # def add_agent(self, unique_id, method, spec):
    def add_agent(self, spec, #unique_id,
                  project_path, agent_class):
        ''' '''
        self.agent_collection[spec['unique_id']] = {
            # 'method': method,
            'spec': spec,
            # 'step_response': 'waiting'
            'step_response': {
                self.time: {
                    'reaction': 'waiting',
                    'did_step': False,
                    'run_time': 0,
                }
            }
        }

        # import sys
        # if not project_path in sys.path:
        #     sys.path.append(project_path)
        # print(sys.path)

        module_comp = agent_class.split('.')
        module_name, agent_class_name = str.join('.', module_comp[:-1]), module_comp[-1]

        kwargs = spec.copy()
        # kwargs['scheduler_id'] = self.scheduler_id
        kwargs['scheduler'] = {
            'id': self.scheduler_id,
            'orsim_settings': self.orsim_settings
        }
        # method.delay(**kwargs) # NOTE This starts the Celery Task in a new worker thread
        start_agent.delay(project_path, module_name, agent_class_name, ORSimEnv.messenger_settings, **kwargs) # NOTE This starts the Celery Task in a new worker thread

        logging.info(f"agent {spec['unique_id']} entering market")
        print(f"agent {spec['unique_id']} entering market")

        # launch_start = time.time()
        # while True:
        #     # if self.agent_collection[unique_id]['step_response'] == 'ready':
        #     if self.agent_collection[unique_id]['step_response'][self.time]['reaction'] == 'ready':
        #         logging.info(f'agent {unique_id} is ready')
        #         print(f'agent {unique_id} is ready')
        #         break
        #     elif (self.agent_collection[unique_id]['step_response'][self.time]['reaction'] == 'init_error') or \
        #                         ((time.time() - launch_start) > self.orsim_settings['AGENT_LAUNCH_TIMEOUT']):
        #         logging.exception(f'Failed to Launch agent {unique_id}')
        #         print(f'Failed to Launch agent {unique_id}')
        #         self.remove_agent(unique_id)
        #         if self.init_failure_handler == 'soft':
        #             break
        #         else:
        #             raise Exception(f"Shutdown {self.scheduler_id} due to {self.init_failure_handler=}. Agent {unique_id} failed to launch.")
        #     else:
        #         time.sleep(0.1)


    def remove_agent(self, unique_id):
        try:
            logging.info(f"agent {unique_id} has left")
            print(f"agent {unique_id} has left")
            self.agent_collection.pop(unique_id)
        except Exception as e:
            logging.exception(str(e))
            # print(e)

    def on_receive_message(self, client, userdata, message):
        if message.topic == f"{self.run_id}/{self.scheduler_id}/ORSimScheduler":
            payload = json.loads(message.payload.decode('utf-8'))

            response_time_step = payload.get('time_step') if payload.get('time_step') != -1 else self.time

            try:
                self.agent_collection[payload.get('agent_id')]['step_response'][response_time_step] = {
                    'reaction': payload.get('action'),
                    'did_step': payload.get('did_step'),
                    'run_time': payload.get('run_time')
                }
            except: pass
            # except Exception as e:
            #     logging.exception(str(e))

            if (payload.get('action') == 'error') or (response_time_step is None):
                logging.warning(f'{self.__class__.__name__} received {message.payload = }')

    async def confirm_responses(self):
        ''' '''
        start_time = time.time()
        base = 0
        completed = 0
        ready = 0
        shutdown = 0
        error = 0
        waiting = len(self.agent_collection)

        while waiting > 0:
            completed = 0
            ready = 0
            shutdown = 0
            error = 0
            waiting = 0
            num_did_step = 0
            for agent_id, _ in self.agent_collection.items():
                response = self.agent_collection[agent_id]['step_response'][self.time]
                if (response['reaction'] == 'completed'):
                    completed += 1
                elif (response['reaction'] == 'ready'):
                    ready += 1
                elif (response['reaction'] == 'error'):
                    error += 1
                elif (response['reaction'] == 'shutdown'):
                    shutdown += 1
                elif (response['reaction'] == 'waiting'):
                    waiting += 1

                if response['did_step']:
                    num_did_step += 1

            self.agent_stat[self.time] = {
                'completed': completed,
                'ready': ready,
                'error': error,
                'shutdown': shutdown,
                'waiting': waiting,
                'stepping_agents': num_did_step,
                'total_agents': len(self.agent_collection),
                # 'run_time_dist': []
            }
            current_time = time.time()
            if current_time - start_time >= 5:
                # logging.info(f"Waiting for Agent Response... {completed=}, {error=}, {shutdown=}, {waiting=} of {len(self.agent_collection)}: {base + (current_time - start_time):0.0f} sec")
                logging.info(f"Waiting for Agent Response... {self.agent_stat[self.time]}: {base + (current_time - start_time):0.0f} sec")
                base = base + (current_time - start_time)
                start_time = current_time

            await asyncio.sleep(0.1)

    async def step(self):

        logging.info(f"{self.scheduler_id} Step: {self.time}")
        start_time = time.time()

        if self.time == self.orsim_settings['SIMULATION_LENGTH_IN_STEPS']-1:
            message = {'action': 'shutdown', 'time_step': self.time}
        else:
            message = {'action': 'step', 'time_step': self.time}

        for agent_id, _ in self.agent_collection.items():
            self.agent_collection[agent_id]['step_response'][self.time] = {
                'reaction': 'waiting',
                'did_step': False,
                'run_time': 0
            }

        self.agent_messenger.client.publish(f'{self.run_id}/{self.scheduler_id}/ORSimAgent', json.dumps(message))

        try:
            # start_time = time.time()
            await asyncio.wait_for(self.confirm_responses(), timeout=self.orsim_settings['STEP_TIMEOUT'])
            # end_time = time.time()
            logging.info(f'{self.agent_stat[self.time] = }')
            # logging.info(f'{self.scheduler_id} Runtime: {(time.time()-start_time):0.2f} sec')

        except asyncio.TimeoutError as e:
            logging.exception(f'Scheduler {self.scheduler_id} timeout beyond {self.orsim_settings["STEP_TIMEOUT"] = } while waiting for confirm_responses.')
            self.step_timeout_handler(e)

        # Handle shutdown agents once successfully exiting the loop
        agents_shutdown = []
        for agent_id, agent_item in self.agent_collection.items():
            if agent_item['step_response'][self.time]['reaction'] in ['shutdown', 'waiting']:
                agents_shutdown.append(agent_id)

        for agent_id in agents_shutdown:
            self.remove_agent(agent_id)


        self.time += 1

        sim_stat = {
            'status': 'success',
            'end_sim': False,
        }

        if self.time == self.orsim_settings['SIMULATION_LENGTH_IN_STEPS']-1:
            sim_stat['end_sim'] = True


        logging.info(f'{self.scheduler_id} Runtime: {(time.time()-start_time):0.2f} sec')
        return sim_stat


    def step_timeout_handler(self, e):
        ''' '''
        tolerance = self.orsim_settings['STEP_TIMEOUT_TOLERANCE'] # Max % or agents having network issues


        if (self.agent_stat[self.time]['waiting'] / len(self.agent_collection)) <= tolerance:
            logging.warning(f"agent_stat = {self.pp.pformat(self.agent_stat[self.time])}")
            logging.warning(f"Unable to receive response from {self.agent_stat[self.time]['waiting']} Agents at {self.time=}. % Error ({(self.agent_stat[self.time]['waiting'] / len(self.agent_collection)):0.3f}) is within {tolerance=}. Continue processing...")
            # logging.warning(f'{self.pp.pformat(self.agent_collection)}')
        else:
            logging.error(f"Too many missing messages. % Error ({self.agent_stat[self.time]['waiting'] *100 / len(self.agent_collection)}) exceeded {tolerance=}. Abort...")
            logging.error(f'{self.pp.pformat(self.agent_collection)}')
            raise e
