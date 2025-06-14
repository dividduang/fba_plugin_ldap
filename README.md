## fba插件 ldap认证


```使用方法
backend/.env 配置:
LDAP_SERVER = '10.10.10.10:389'
LDAP_BASE_DN = 'OU=OU,dc=domain,dc=cn'
LDAP_BASE_DOMAIN = 'domain' 

backend/core/conf.py 配置:
# LDAP
LDAP_SERVER: str
LDAP_BASE_DN: str
LDAP_BASE_DOMAIN: str

```
test_ldap.py为测试文件
TODO：根据部门分配权限
