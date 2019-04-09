import multiprocessing, time, sys, psutil, os, signal, logging, uuid
# ANL:waggle-license
#  This file is part of the Waggle Platform.  Please see the file
#  LICENSE.waggle.txt for the legal details of the copyright and software
#  license.  For more details on the Waggle project, visit:
#           http://www.wa8.gl
# ANL:waggle-license
from multiprocessing import Manager, Queue

"""
    A simple multiprocessing plugin architecture. 
    Kyle Lueptow 2015
    
"""

import plugins 


logger = logging.getLogger(__name__)



def check_pid(pid):        
    """ Check For the existence of a unix pid. """
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True



class plugin_runner(object):
    def __init__(self):
        self.jobs = []
        self.manager = Manager()
        self.man = self.manager.dict()
        
        
        self.mailbox_outgoing = Queue()
        self.system_send_queue = self.manager.Queue()
        self.system_receive_queue = self.manager.Queue()
        self.listeners = {} 
    
    
    #def listener_consolidate(self, name):
    #    if not name in self.listeners:
    #        return
    #        
    #    pid = self.listeners[name]['pid']
    #    
    #    if not pid:
    #        return
    #        
    #    if not check_pid(pid):
    #        del self.listeners[name]    
    
    #def listener_exists(self, name):
    #    #self.listener_consolidate(name)
    #    
    #   if name in self.listeners:
    #        return [1, '']
    #    return [0, '']
        
    # def add_listener(self, name, in_queue, out_queue, pid):
    #     #self.listener_consolidate(name)
        
    #     listener_uuid = str(uuid.uuid4())
        
    #     if listener_uuid in self.listeners:
    #         return [0, 'listener with that uuid already exists']
            
    #     if not pid:
    #         return [0, 'pid is not defined']
            
    #     if not type(pid) is int:
    #         return [0, 'pid is not int']
        
            
    #     self.listeners[listener_uuid] = {'name': name, 'incoming_queue': in_queue, 'outgoing_queue': out_queue, 'pid': pid}
        
    #     return [1, listener_uuid]
        
    def add_listener(self, name, queue, pid):
        #self.listener_consolidate(name)
        
        listener_uuid = str(uuid.uuid4())
        
        if listener_uuid in self.listeners:
            return [0, 'listener with that uuid already exists']
            
        if not pid:
            return [0, 'pid is not defined']
            
        if not type(pid) is int:
            return [0, 'pid is not int']
        
            
        self.listeners[listener_uuid] = {'name': name, 'queue': queue, 'pid': pid} 
        
        return [1, listener_uuid]

    #Lists all available plugins and their status
    def list_plugins(self):
        print('Plugins List:')
        for name in plugins.__all__:
            plugin = getattr(plugins, name)
            #checks if listed plugin is in list of active processes
            j = self.get_plugin_by_name(name)
            if j:
                print('Plugin', name, 'is active.')
                continue
            
            print('Plugin', name, 'is inactive.')

    #Tries to start a plugin with the name given by argument. Returns 1 for successful start, 0 for failure
    def start_plugin(self, plugin_name):
        #checks if plugin is in list of plugins
        if (plugin_name in plugins.__all__):
            #checks if plugin is already active
            j = self.get_plugin_by_name(plugin_name)
            if j:
                return [0, 'Plugin %s is already active.' % (plugin_name) ]

            #checks for register attribute in plugin
            plugin = getattr(plugins, plugin_name)
            try:
                register_plugin = plugin.register
            except AttributeError:
                return [0, 'Plugin %s has no register attribute' % (plugin_name) ]
            
            
            logger.debug('Calling plugin %s ...' % (plugin_name))
            #Starts plugin as a process named the same as plugin name
            #sys.stdout = open('/dev/null', 'w')
            if plugin_name == 'system_router':
                j = multiprocessing.Process(name=plugin_name, target=register_plugin, args=(plugin_name,self.man, self.mailbox_outgoing, self.listeners ))
                self.jobs.append(j)
                j.start()
                
            elif  plugin_name == 'system_send':
                
                try:
                    j = multiprocessing.Process(name=plugin_name, target=register_plugin, args=(plugin_name,self.man, self.system_send_queue))
                except Exception as e:
                    logger.error("Starting process failed: %s" % (str(e)))
                
                self.jobs.append(j)
                j.start()
                
                self.add_listener('system_send', self.system_send_queue, int(j.pid))
                
                
            else:
                j = multiprocessing.Process(name=plugin_name, target=register_plugin, args=(plugin_name,self.man, self.mailbox_outgoing))
                self.jobs.append(j)
                j.start()
            # if plugin_name == 'system_router':
            #     j = multiprocessing.Process(name=plugin_name, target=register_plugin, args=(plugin_name,self.man, self.system_send_queue, self.system_receive_queue, self.listeners ))
            #     self.jobs.append(j)
            #     j.start()
                
            # elif  plugin_name == 'system_send':
                
            #     try:
            #         j = multiprocessing.Process(name=plugin_name, target=register_plugin, args=(plugin_name,self.man, self.system_send_queue))
            #     except Exception as e:
            #         logger.error("Starting process failed: %s" % (str(e)))
                
            #     self.jobs.append(j)
            #     j.start()
                
            #     self.add_listener('system_send', self.system_send_queue, int(j.pid))
            # elif  plugin_name == 'system_receive':
            #     try:
            #         j = multiprocessing.Process(name=plugin_name, target=register_plugin, args=(plugin_name,self.man, self.system_receive_queue))
            #     except Exception as e:
            #         logger.error("Starting process failed: %s" % (str(e)))
            #     self.jobs.append(j)
            #     j.start()
            # else:
            #     j = multiprocessing.Process(name=plugin_name, target=register_plugin, args=(plugin_name,self.man, self.mailbox_outgoing))
            #     self.jobs.append(j)
            #     j.start()
                #self.add_listener(plugin_name, Queue(), Queue(), int(j.pid))
            #sys.stdout = sys.__stdout__
            # TODO proper check is missing !
            return [1 , 'Plugin %s started.' %(j.name)]
        
        
        return [0, 'Plugin %s not found - cannot start.' % (plugin_name) ]
            
    def get_plugin_by_name(self, plugin_name):
        for j in self.jobs:
            if (j.name == plugin_name):
                return j
        return None
    
    def update_job_list(self):
        self.jobs[:] = [x for x in self.jobs if x.is_alive()]
        
        
    #Tries to stop a plugin with the name given by argument. Returns 1 for successful stop, 0 for failure
    #If the terminate() call times out (SIGTERM fails to stop the process), it sends a SIGKILL to the process
    def kill_plugin(self, plugin_name):
        killed = 0
        #Tries to find plugin in list of active processes
        
        j = self.get_plugin_by_name(plugin_name)
        
        if not j:
            return [0, 'plugin %s not found' % (plugin_name)]
       
        j.terminate()
        j.join(5)
        if (j.is_alive()):
            os.kill(self.plugin_pid(j.name), signal.SIGKILL)
            j.join(5)
            if (j.is_alive()):
                return [0, 'plugin %s not killed, it is still alive' % (plugin_name)]
                
            logger.debug( 'Plugin' + j.name + 'ended with kill signal.')
        else: 
            logger.debug( 'Plugin' + j.name + 'terminated.')
        killed = 1
        #removes plugin from list of active plugins
        self.update_job_list()
        return [killed, '']
        
    #sends plugin a stop signal
    def stop_plugin(self, plugin_name):
        stopped = 0
        
        j = self.get_plugin_by_name(plugin_name)
        
        if not j:
            return [0, 'plugin %s not found' % (plugin_name)]
            
        # send nice termination signal
        self.man[plugin_name] = 0
        j.join(10)
        if (j.is_alive()):
            
            return [0, '%s has failed to stop.' % (plugin_name) ]
        
            
        stopped = 1
        self.update_job_list()
        return [stopped, 'Plugin %s stopped.' % (j.name)]
    
        
    def plugin_exists(self, plugin_name):
        stopped = 0
        j = self.get_plugin_by_name(plugin_name)
        
        if j:
            return [1, '']
        return [0,'']

    #sends plugin a pause signal
    def pause_plugin(self, plugin_name):
        j = self.get_plugin_by_name(plugin_name)
        
        if not k:
            return [ 0, 'Plugin %s not found.' % (plugin_name)]
        
        self.man[plugin_name] = -1
        return [1, 'Pause signal sent.']
       
        

    #sends plugin a run/resume signal
    def unpause_plugin(self, plugin_name):
        unpaused = 0
        for j in self.jobs:
            if (j.name == plugin_name):
                if (self.man[plugin_name] != -1):
                    return [unpaused, 'Plugin %s not paused - cannot unpause.' % (plugin_name)]
                self.man[plugin_name] = 1
                unpaused = 1
                
                return [unpaused, "Plugin %s unpaused." % (plugin_name)]
        
        return [ unpaused, 'Plugin %s not active - cannot unpause.' % (plugin_name) ]

    #Sends a SIGSTOP signal to process attached to plugin_name to suspend operations (unused)
    def suspend_plugin(self, plugin_name):
        pid = self.plugin_pid(plugin_name)
        if (pid == 0):
            return 0
      
        p = psutil.Process(pid)
        p.suspend()
        return 1

    #Sends a SIGCONT signal to process attached to plugin_name to resume operations (unused)
    def resume_plugin(self, plugin_name):
        pid = self.plugin_pid(plugin_name)
        if (pid == 0):
            return [0, '']
        
        p = psutil.Process(pid)
        p.resume()
        return [1 , '']

    #runs kill_plugin, then start_plugin if the first is successful
    def restart_plugin(self, plugin_name, force=False):
        logger.debug('Restarting plugin '+ plugin_name)
        
        
        exists = self.plugin_exists(plugin_name)
        if exists[0]:
            if force:
                stopped = self.kill_plugin(plugin_name)
            else:
                stopped = self.stop_plugin(plugin_name)
        else:
            stopped = [1,'']
        
        if stopped[0]:
            #If stopping plugin worked, try to start it again
            if(self.start_plugin(plugin_name)):
                return [1, 'Plugin %s restarted.' % (plugin_name)]
            else:
                return [0, 'Plugin %s stopped, but not restarted. Did you alter the plugin?' % (plugin_name)]
        
        return [0,  'Plugin %s did not terminate - cannot restart.' % (plugin_name)]



    #terminates all active processes
    def kill_all(self):
        logger.debug('Terminating all processes...')
        kill = 1
        fail = 0
        #Must be range(len()) instead of self.jobs because kill_plugin() removes plugin from beginning of list, confusing loop.
        #If self.jobs is used, only half the processes are stopped.
        for count in range(len(self.jobs)):
            j = self.jobs[0]
            kill = self.kill_plugin(j.name)
            if not kill:
                fail = fail + 1
        if (fail == 0):
            return [1, 'All active processes killed.']
        else:
            print([0, 'Attempted to kill all active processes with %d failures.' % (fail)])

    #sends all active plugins a stop signal
    def stop_all(self):
        logger.debug('Stopping all processes...')
        stop = 1
        fail = 0
        for count in range(len(self.jobs)):
            j = self.jobs[0]
            stop, msg = self.stop_plugin(j.name)
            if not stop:
                fail = fail + 1
                
        if (fail == 0):
            return [1, 'All active processes stopped.']
        
        return [0, 'Attempted to stop all active processes with %d failures.' % (fail)]
        

    #sends all active, unpaused plugins a pause signal
    def pause_all(self):
        logger.debug('Pausing all processes...')
        pause = 1
        fail = 0
        for j in self.jobs:
            if (self.man[j.name] == 1):
                pause = self.pause_plugin(j.name)
            if not pause:
                fail = fail + 1
        if (fail == 0):
            return [1, 'All active processes sent pause signal.']
        
        
        time.sleep(2)
        return [0, 'Attempted to pause all active processes with %d failures.' % (fail)]
        
    #Sends all paused plugins a run/resume signal.
    def unpause_all(self):
        logger.debug('Unpausing all processes...')
        unpause = 1
        fail = 0
        for j in self.jobs:
            if (self.man[j.name] == -1):
                unpause = self.unpause_plugin(j.name)
            if not unpause:
                fail = fail + 1
                
        if (fail == 0):
            return [1, 'All paused processes unpaused.']
        
        return [0, 'Attmepted to unpause all paused processes with',fail,'failures.']
        
    #Starts all processes (ignores if the process is already active)
    def start_all(self):
        print('Starting all processes...')
        start = 1
        fail = 0
        for plugin_name in plugins.__all__:
            start = self.start_plugin(plugin_name)
            if not start:
                fail = fail + 1
        if (fail == 0):
            return [1, 'All processes started.']
        
        return [0, 'Attempted to start all processes with %d failures.']

    #Retrieves the PID of plugin_name and returns it, or 0 if that plugin is not running.
    def plugin_pid(self, plugin_name):
        for j in self.jobs:
            if (j.name == plugin_name):
                return j.pid
        return 0
        

    #Using PID of plugin, returns memory% and CPU% of that process.
    def plugin_info(self, plugin_name):
        pid = self.plugin_pid(plugin_name)
        if (pid == 0):
            return [0 , '']
       
           
        p = psutil.Process(pid)
        message = "Memory Percent: %s\tCPU Percent: %s\tPID: %s"  % (str(p.memory_percent()), str(p.cpu_percent(interval=1.0)), str(pid) )
        logger.debug(message)
        return [1, message]
        

    #Calls plugin_info on all active plugins.
    def info_all(self):
        fail = 0
        for j in self.jobs:
            if (self.plugin_info(j.name) == 0):
                fail = fail + 1
        if (fail == 0):
            return [1, '']
    
        return [0 , "Attempted to get info on all active plugins, but",fail,"failures occurred."]
            
