from telegram.ext import BaseFilter


#custom filters
class MyFilters(BaseFilter):
    # def Ann(self, message):
    #     return 'Ann' in message.text
    # def Antoine(self, message):
    #     return 'Antoine' in message.text
    # def together(self, message):
    #     return 'together' in message.text
    # def friends(self, message):
    #     return 'friends' in message.text
    # def djSych(self, message):
    #     return 'dj Sych 🎵' in message.text
    # def djAnn(self, message):
    #     return 'dj Аnn 🎵' in message.text
    def testmp3(self, message):
        return 'Тестовый вызов' in message.text
    

# filter_anna_photo = MyFilters().Ann
# filter_anton_photo = MyFilters().Antoine
# filter_together_photo = MyFilters().together
# filter_friends_photo = MyFilters().friends
# filter_dj_Sych = MyFilters().djSych
# filter_dj_Ann = MyFilters().djAnn
filter_testmp3 = MyFilters().testmp3
