## fba插件 ldap认证


```使用方法
backend/.env 配置:
LDAP_SERVER = '10.10.10.35:389'
LDAP_Bind_DN = 'CN=user,DC=domain,DC=cn'
LDAP_Bind_DN_PASSWORD = '123456'
LDAP_BASE_DOMAIN = 'domain' 
LDAP_Base_DN = 'OU=OU,dc=domain,dc=cn'

backend/core/conf.py 配置:
# LDAP
LDAP_SERVER: str
LDAP_Bind_DN: str
LDAP_Bind_DN_PASSWORD: str
LDAP_BASE_DOMAIN: str
LDAP_Base_DN: str

```
test_ldap.py为测试文件
TODO：根据部门分配权限
