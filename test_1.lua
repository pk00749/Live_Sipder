function main(splash)
    assert(splash:go("https://www.huya.com/"))
    --for var=0,50,1 do
	local get_dimensions = splash:jsfunc([[
	function () {
	var rect = document.getElementById('nav-login').getClientRects()[0];
	return {"x": rect.left, "y": rect.top}
	}
	]])
	--splash:set_viewport_full()
	splash:wait(0.1)
	--local dimensions = get_dimensions()         
	--splash:mouse_click(dimensions.x, dimensions.y)
	splash:mouse_click(get_dimensions().x, get_dimensions().y)
	-- Wait split second to allow event to propagate.
	splash:wait(0.5)
    --end
    return {
        html = splash:html(),
        png = splash:png(),
		get_dimensions().x
    }
end