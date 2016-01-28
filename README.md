#The reporter system for online report viewing and trigger the test from web.

##User manual
###Developement, Run, Deployment
1. System Dependencies
    - Python2.x, Pip.
    
2. How to install the project dependencies
    - Change directory to `reporter`
    - pip install -r requirements.txt
    
3. How to open project and develop in IDE
    - Use PyCharm to select the project root directory to open it
    - Run the `run.py` to start the web server on local machine
    
4. How to use the local configuration file
    - Copy `reporter/config/development.py` to `reporter/app/instance/config.py`
    - Modify the `PPE_REPORT_PATH` and `PPE_SCRIPT_PATH` and others based on the local development env
    
5. How to use the production configuration file
    - Open `reporter/config/default.py`
    - Modify the `PPE_REPORT_PATH` and `PPE_SCRIPT_PATH` and others based on the production env
    
6. How to deploy in production env
    - Open `reporter/supervisor/reporter.conf`
    - Modify `directory`, `command`, `stdout_logfile`, `stderr_logfile` based on the environment
    - Run `echo_supervisord_conf > /etc/supervisord.conf`
    - Add `reporter.conf` to the `/etc/supervisord.conf`
    - Run `sudo supervisord`
    - Run `sudo supervisorctl start reporter`
    
###If any issue, please contact braveheart2004@163.com