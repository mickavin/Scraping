function use_crawlera(splash)
    local user = splash.args.crawlera_user
    local password = ''

    local host = 'proxy.zyte.com'
    local port = 8010
    local session_header = 'X-Crawlera-Session'
    local session_id = 'create'

    splash:on_request(function (request)
        -- The commented code below can be used to speed up the crawling
        -- process. They filter requests to undesired domains and useless
        -- resources. Uncomment the ones that make sense to your use case
        -- and add your own rules.

        -- Discard requests to advertising and tracking domains.
        if string.find(request.url, 'doubleclick%.net') or
            string.find(request.url, 'analytics%.google%.com') then
            request.abort()
            return
        end

        -- Avoid using Smart Proxy Manager for subresources fetching to increase crawling
        -- speed. The example below avoids using Smart Proxy Manager for URLS starting
        -- with 'static.' and the ones ending with '.png'.
        if string.find(request.url, '://static%.') ~= nil or
           string.find(request.url, '%.png$') ~= nil then
            return
        end
        request:set_proxy(host, port, user, password)
        request:set_header('X-Crawlera-Profile', 'desktop')
        request:set_header('X-Crawlera-Cookies', 'disable')
        request:set_header(session_header, session_id)
    end)

    splash:on_response_headers(function (response)
        if type(response.headers[session_header]) ~= nil then
            session_id = response.headers[session_header]
        end
    end)
end

function main(splash, args)
    use_crawlera(splash)
    assert(splash:go(args.url))
    assert(splash:wait(3))
    splash:set_viewport_full()
    next = assert(splash:select("a[title='Page suivante'][onmousedown]"))
    assert(next:mouse_click())
    assert(splash:wait(1))
    return splash:html()
end