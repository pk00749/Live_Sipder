import configparser, os

class USER_PROFILE:

    def __init__(self, name):
        print('getting USER_PROFILE %s' % name)
        self.cf = configparser.ConfigParser()
        self.user_name = name
        self.user_profile = os.path.dirname(
            os.path.realpath(__file__)) + os.sep + '..'\
                    + os.sep + "users" + os.sep + "%s.ini"% self.user_name

    def get_user_profile(self):
        if os.path.exists(self.user_profile):
            self.cf.read(self.user_profile)
        else:
            print('user profile %s does not exist...' % self.user_name)
            return

        user_info = self.cf.options('user_info')
        if 'user_name' not in user_info:
            print('Please input user name.')
            raise IOError
        elif 'user_pw' not in user_info:
            print('Please input user pw.')
            raise IOError
        elif 'topic' not in user_info:
            print('Please input topic.')
            raise IOError
        elif 'msg' not in user_info:
            print('Please input msg.')
            raise IOError

        user_name = self.cf.get('user_info', 'user_name')
        user_pw = self.cf.get('user_info', 'user_pw')
        topic = self.cf.get('user_info', 'topic')
        msg = self.cf.get('user_info', 'msg')

        return {'user_name' : user_name,
                'user_pw' : user_pw,
                'topic' : topic,
                'msg' : msg
                }

class HUYA_CONFIG:

    def __init__(self):
        self.cf = configparser.ConfigParser()
        self.huya_config = os.path.dirname(
            os.path.realpath(__file__)) + os.sep + '..'\
                    + os.sep + "config" + os.sep + "config.ini"

    def get_huya_config(self):
        if os.path.exists(self.huya_config):
            self.cf.read(self.huya_config)
        else:
            print('config does not exist...')

        huya_config = self.cf.options('huya_config')
        if 'phantomjs' not in huya_config:
            print('Please input phantomjs.')
            raise IOError
        elif 'phantomjs_timeout' not in huya_config:
            print('Please input phantomjs_timeout.')
            raise IOError
        elif 'interval_time' not in huya_config:
            print('Please input interval_time.')
            raise IOError

        phantomjs = self.cf.get('huya_config', 'phantomjs')
        phantomjs_timeout = self.cf.get('huya_config', 'phantomjs_timeout')
        interval_time = self.cf.get('huya_config', 'interval_time')

        return {'phantomjs' : phantomjs,
                'phantomjs_timeout' : phantomjs_timeout,
                'interval_time' : interval_time
                }

if __name__ == '__main__':
    test = USER_PROFILE('13250219510')
    huya_config = test.get_user_profile()
    print(huya_config['user_name'])


