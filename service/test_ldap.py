
from ldap3 import Server, Connection, ALL, SUBTREE
import asyncio
from concurrent.futures import ThreadPoolExecutor


class settings :
    LDAP_SERVER = '10.229.253.35:389'
    LDAP_BindDN = 'CN=dengjingren,OU=Finance,OU=Users,OU=SZH-WH,OU=YiHaiKerryGroup,DC=wilmar,DC=cn'
    LDAP_BASEDN_PASSWORD = 'djrenbb321!'
    LDAP_BASE_DOMAIN = 'wilmar' 
    LDAP_BaseDN = 'DC=wilmar,DC=cn'


ad_settings = {
    'Domain': 'wilmar.cn',
    'Server': '10.229.253.35:389',
    'BaseDN': 'DC=wilmar,DC=cn',
    # 'BindDN': 'CN=renjianghai,OU=Infra,OU=Users,OU=SHH-IT,OU=YiHaiKerryGroup,DC=wilmar,DC=cn',
    'BindDN': 'CN=dengjingren,OU=Finance,OU=Users,OU=SZH-WH,OU=YiHaiKerryGroup,DC=wilmar,DC=cn',
    'BindPass': 'djrenbb321!'
}



async def ldap_verify(username: str, password: str) -> tuple:
    try:
        # 1. 先用管理账号查找用户信息
        user_info = await get_ad_account_info_by_samaccountname(username)
        if not user_info or not user_info.get('distinguishedName'):
            print(f"User not found in LDAP: {username}")
            return (False, None, None, None, "LDAP中未找到该用户")
        user_dn = user_info['distinguishedName']

        # 2. 用用户DN和密码bind验证密码
        server = Server(settings.LDAP_SERVER, get_info=ALL)
        try:
            user_conn = Connection(
                server,
                user=user_dn,
                password=password,
                auto_bind=True
            )
            if not user_conn.bound:
                print(f"LDAP bind failed for user: {username}")
                return (False, None, None, None, "用户名或密码错误")
        except Exception as e:
            print(f"LDAP bind failed for user: {username}, error: {e}")
            return (False, None, None, None, "用户名或密码错误")

        # 3. 返回用户信息
        return (
            True,
            user_info.get("mail", ""),
            user_info.get("sAMAccountName", ""),
            user_info.get("displayName", ""),
            "登录成功"
        )
    except Exception as e:
        print(f"LDAP verification error: {str(e)}")
        return (False, None, None, None, f"LDAP连接失败: {str(e)}")

async def get_ad_account_info_by_samaccountname(sam_account_name: str) -> dict | None:
    """
    先用管理账号连接LDAP，查找用户信息（如DN、displayName、mail等），返回属性字典。
    :param sam_account_name: sAMAccountName
    :return: 用户属性字典或None
    """
    def _ldap_query():
        from ldap3 import Server, Connection, SUBTREE, ALL
        from backend.core.conf import settings
        att_list = [
            'distinguishedName',  # 用户唯一标识
            'displayName',        # 用户名中文名
            'telephoneNumber',   # 手机号
            'sAMAccountName',    # 用户名
            'mail',
            'company',
            'department',
        ]
        try:
            server = Server(settings.LDAP_SERVER, get_info=ALL)
            conn = Connection(
                server,
                user=settings.LDAP_BIND_DN,
                password=settings.LDAP_BIND_PASSWORD,
                auto_bind=True
            )
            search_filter = f'(sAMAccountName={sam_account_name})'
            conn.search(
                search_base=settings.LDAP_BASE_DN,
                search_filter=search_filter,
                attributes=att_list,
                paged_size=10,
                search_scope=SUBTREE
            )
            for entry in conn.response:
                if entry.get('dn'):
                    return entry.get('attributes')
            return None
        except Exception as e:
            from backend.common.log import log
            print(f'LDAP管理账号查找用户失败: {e}')
            return None

    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        return await loop.run_in_executor(pool, _ldap_query)
    
ldap_verify('dengjingren','djrenbb321!')