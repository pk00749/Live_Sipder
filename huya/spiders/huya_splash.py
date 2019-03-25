import requests
from urllib.parse import quote

# lua = '''
# function main(splash)
#     return 'hello'
# end
# '''

# lua = '''
# function main(splash)
#   splash:go("https://www.baidu.com/")
#   input = splash:select("#kw")
#   input:send_text('Splash')
#   submit = splash:select('#su')
#   submit:mouse_click()
#   splash:wait(3)
#   return splash:png()
# end
# '''

# submit = splash:select("#nav-login")
# submit: mouse_click()
huya = '''
function main(splash)
    assert(splash:go("https://www.huya.com/"))
    splash.images_enabled=false
    splash.plugins_enabled=false
    splash.html5_media_enabled=false
	local login = splash:jsfunc([[
	function () {
		document.getElementById('nav-login').click()
	}
	]])
	local switch = splash:jsfunc([[
	function () {
		document.getElementsByClassName('UDBSdkLgn-switch UDBSdkLgn-webQuick')
	}
	]])
	login()
	switch()
    splash:wait(1)
    return splash:png()
end
'''

# url='http://192.168.150.134:8050//'
# response=requests.get(url+'render.html?url=https://www.baidu.com&wait=3&images=0')
url='http://192.168.150.134:8050/execute?lua_source='+quote(huya)
response = requests.get(url)
print(response.text) #返回网页源代码