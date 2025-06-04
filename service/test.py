
from ldap3 import Server, Connection, ALL, SUBTREE, NTLM


class settings:
    LDAP_SERVER = '10.229.253.34'
    LDAP_PORT = 636
    LDAP_BASE_DN = 'OU=YiHaiKerryGroup,dc=wilmar,dc=cn'
    LDAP_BASE_DOMAIN = 'wilmar' 



def ldap_verify(username: str, password: str) -> tuple:
    try:
        # 配置LDAP服务器
        ldap_server = Server(
            host=settings.LDAP_SERVER,
            port=settings.LDAP_PORT,  # LDAPS端口
            use_ssl=True,
            get_info=ALL
        )

        # 创建连接并尝试绑定
        conn = Connection(
            ldap_server,
            user=f'{settings.LDAP_BASE_DOMAIN}\\{username}',
            # user=username,
            password=password,
            authentication=NTLM,
            auto_bind=True,
            raise_exceptions=False
        )

        if not conn.bound:
            print(f"LDAP bind failed for user: {username}")
            return (False, None, None, None, "用户名或密码错误")

        print(f"LDAP connection established for user: {username}")

        # 搜索用户信息
        search_result = conn.search(
            search_base=settings.LDAP_BASE_DN,
            search_filter=f'(sAMAccountName={username})',
            search_scope=SUBTREE,
            attributes=['cn', 'givenName', 'mail', 'sAMAccountName']
        )

        if not search_result or len(conn.response) == 0:
            print(f"User not found in LDAP: {username}")
            return (False, None, None, None, "LDAP中未找到该用户")

        entry = conn.response[0]
        attr_dict = entry['attributes']

        print(f"Found user in LDAP: {entry['dn']}")

        # 返回成功结果
        return (True,
                attr_dict.get("mail", ""),
                attr_dict.get("sAMAccountName", ""),
                attr_dict.get("givenName", ""),
                "登录成功")

    except Exception as e:
        print(f"LDAP verification error: {str(e)}")
        return (False, None, None, None, f"LDAP连接失败: {str(e)}")
    

print(ldap_verify('dengjingren','djrenbb321!'))