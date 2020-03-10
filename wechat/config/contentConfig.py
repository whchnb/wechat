BASECONTENT = """
                <xml>
                    <ToUserName><![CDATA[{}]]></ToUserName>
                    <FromUserName><![CDATA[{}]]></FromUserName>
                    <CreateTime>{}</CreateTime>
                    %s
                </xml>
              """


PICTURECONTENT = """
                <item>
                    <Title><![CDATA[{}]]></Title>
                    <Description><![CDATA[{}]]></Description>
                    <PicUrl><![CDATA[{}]]></PicUrl>
                    <Url><![CDATA[{}]]></Url>
                </item>
                """
MSGCONTENT = """
                <MsgType><![CDATA[text]]></MsgType>
                    <Content><![CDATA[{}]]></Content>
             """
ARTICLECONTENT = """
                <xml>
                    <ToUserName><![CDATA[{}]]></ToUserName>
                    <FromUserName><![CDATA[{}]]></FromUserName>
                    <CreateTime>{}</CreateTime>
                    <MsgType><![CDATA[news]]></MsgType>
                    <ArticleCount>{}</ArticleCount>
                    <Articles>
                        %s
                    </Articles>
                </xml>
                 """
COUPLESTEMPLATECONTENT = """{"touser": "%s","template_id": "%s","data": {"mine": {"value": "%s","color": "#173177"},"couple": {"value": "%s","color": "#173177"},"time": {"value": "%s","color": "#173177"}}}"""
COUPLESTOSAYMSGTEMPLATECONTENT = """{"touser": "%s","template_id": "%s","data": {"mine": {"value": "%s","color": "#173177"},"say": {"value": "%s","color": "#173177"},"time": {"value": "%s","color": "#173177"}}}"""