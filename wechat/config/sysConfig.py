# 标签数据
TAGDATA = {
    'V1001_TAG_LEARN': 'learn',
    'V1001_TAG_COUPLES': 'couples',
    'V1001_TAG_SHOP': 'shop',
}


# 基础配置
TOKEN = 'zxc123zxc'


# APPID = 'wxdf64934e0ba38dab'
APPID = 'wx7415247a51d1158c'


# APPSECRET = '81ed798a5afe0afc0d2b36c098d9a2d4'
APPSECRET = '8f046fa3cee6a666d889a2d6975ea8d3'


# 微信api接口
# access_token api
ACCESSTOKENAPI = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s'


# 获取所有标签
ALLTAGAPI = 'https://api.weixin.qq.com/cgi-bin/tags/get?access_token=%s'
# 创建标签
ADDTAGAPI = 'https://api.weixin.qq.com/cgi-bin/tags/create?access_token=%s'
# 修改标签
CHANGETAGAPI = 'https://api.weixin.qq.com/cgi-bin/tags/update?access_token=%s'
# 删除标签
DELETETAGAPI = 'https://api.weixin.qq.com/cgi-bin/tags/delete?access_token=%s'
# 获取标签粉丝
USERTAGAPI = 'https://api.weixin.qq.com/cgi-bin/user/tag/get?access_token=%s'
# 为用户添加标签
ADDTAGTOUSERAPI = 'https://api.weixin.qq.com/cgi-bin/tags/members/batchtagging?access_token=%s'
# 取消用户标签
DELETETAGTOUSERAPI ='https://api.weixin.qq.com/cgi-bin/tags/members/batchuntagging?access_token=%s'
# 获取用户标签
GETUSERTAGAPI = 'https://api.weixin.qq.com/cgi-bin/tags/getidlist?access_token=%s'


# 创建菜单
CREATEMENUAPI = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s'


# 消息发送
CONTENTSENDAPI = 'https://api.weixin.qq.com/cgi-bin/message/mass/sendall?access_token=%s'


# 模板
# 获取所有模板
GETALLTEMPLATEAPI = 'https://api.weixin.qq.com/cgi-bin/template/get_all_private_template?access_token=%s'
# 使用幂伴发送消息
SENDMESSAGEWITHTEMPLATEAPI = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s'