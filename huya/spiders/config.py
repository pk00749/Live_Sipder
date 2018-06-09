import configparser, os

class USER_PROFILE:

    def __init__(self, name):
        self.cf = configparser.ConfigParser()
        self.user_name = name
        self.user_profile = os.path.dirname(
            os.path.realpath(__file__)) + os.sep + '..'\
                    + os.sep + "users" + os.sep + "{user_name}.ini".format(user_name=name)

    def get_user_profile(self):
        if os.path.exists(self.user_profile):
            self.cf.read(self.user_profile)
        else:
            print('user profile %s does not exist...' % self.user_name)

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

if __name__ == '__main__':
    test = USER_PROFILE('13250219510')
    user_profile = test.get_user_profile()
    print(user_profile['user_pw'])


